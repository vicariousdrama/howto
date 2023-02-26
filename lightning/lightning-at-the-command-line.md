# Lightning at the Command Line
_An Intro to Creating Reports for Invoices and Payments for the LND tool_

by @vicariousdrama
714130–714326

![image](https://user-images.githubusercontent.com/88121568/221387335-eeab6967-659f-4eba-ad17-56b7f9e10b0a.png)

## Summary

The purpose of this article is to guide users through use of some of the command line operations to query their lightning node, and produce summary reports using basic formatting and JSON processing tools. This article assumes that you already have a lightning node running LND, and access to the command prompt. If you don’t yet have a lightning node, consider checking out [assorted node projects](https://bitcoiner.guide/node/), or even setting up a node using [voltage.cloud](https://voltage.cloud/). Commands are presented in a way that builds up the overall result gradually so that we can better understand each part that goes into the result. You can jump to the end of major sections if you just want to copy-pasta the end result.

## Change History

| Date | Description |
| --- | --- |
| 2022-03-11 | Initial Document |
| 2023-02-26 | Conversion to Markdown |

## Invoices

Invoices are payment requests that have been initiated from a lightning node for which another should pay. The creation of requests is out of scope of this article and is often created using applications or interfaces like ThunderHub, Ride The Lightning, or a Lightning capable wallet.

### Listing Invoices

From the command line, we can use the `lncli` tool, the control plane for your lightning network daemon (lnd) with the listinvoices command.

![image](https://user-images.githubusercontent.com/88121568/221387857-39143ea1-8555-4595-b52f-16a98588ecc7.png)

This will output some invoices in JSON format. We can use the `jq` command to easily apply some formatting and color syntax coloring to improve readability. Later we will use this tool for filtering as well.

![image](https://user-images.githubusercontent.com/88121568/221387861-ed5f04b9-da3b-4a4f-863b-ee8bd3fdf646.png)

If there are invoices, they will be listed in JSON format with several fields for each. While all these fields have their purpose, the ones we are most concerned about for reporting are the ones for `memo`, `value`, `settled`, `creation_date`, `settle_date`, `amt_paid_sat`, and `state`. 

In follow up sections, the highlighted colors depicted here will be included in commands to draw attention to where they are used.

![image](https://user-images.githubusercontent.com/88121568/221387597-18c899aa-a85a-490e-b6fa-8e3435cc28a1.png)

### Only List Paid Invoices

This is the command to filter the results to only show those which were paid

```shell
lncli listinvoices | jq '.invoices[] | select(.state=="SETTLED")'
```
![image](https://user-images.githubusercontent.com/88121568/221387619-da68af88-4d44-4546-8a8f-280e0c8a1eab.png)

### Only List Failed Invoices

This command alters the filter to show those which were eventually cancelled due to timeout before being paid.

```shell
lncli listinvoices | jq '.invoices[] | select(.state=="CANCELLED")'
```
![image](https://user-images.githubusercontent.com/88121568/221387664-c9f52d39-268b-4650-88f2-8df7b02f31c2.png)

### List Invoices Paid for a Period of Time

To limit the invoices to a period of time, we will establish some variables and update the filter of those invoices that are being selected. The date command will return the seconds since epoch, and start on the first second of that day. Each day is comprised of 86400 seconds. For the end date, we will want to advance the result by one day, minus one second to ensure the entire day is included in the period.

![image](https://user-images.githubusercontent.com/88121568/221387672-5c0e9138-fcdf-46d4-b6a4-04229526051c.png)

Similarly, we can limit the invoices selected to a single month

![image](https://user-images.githubusercontent.com/88121568/221387677-a02897c6-e8c3-4d40-900a-0828fab9bf47.png)

### Controlling the Output for Invoices

Up until now, our output has just been JSON. For reporting purposes, we will begin cleaning up the output to report information on a line by line basis. With the selected objects, we can further use the jq command line JSON processor to direct output concatenating values for a string.

![image](https://user-images.githubusercontent.com/88121568/221387680-f56bfada-ac8f-4285-9460-938324a2bd50.png)

Here is a sample result formatted from the string

![image](https://user-images.githubusercontent.com/88121568/221387684-5d317c8c-80b2-4bbb-b68b-48103dd3ef8c.png)

Let’s use some trivial formatting to right align the value field by creating spaces padded on the left side. This makes it easier to read numbers when there are multiple rows. In this example, we take the value field, convert to a string using a builtin tostring function. This will then be written out with spaces before it up to 8 minus the length of the value using the built in length function. For example, if the value is 123, it has a length of 3, and to give it a total overall length of 8, 5 spaces will be written in front.

![image](https://user-images.githubusercontent.com/88121568/221387687-73e7403e-132e-474e-a1bf-e49a95e2dc27.png)

Here is the revised sample result showing the additional padding of spaces on the left side of the value.

![image](https://user-images.githubusercontent.com/88121568/221387690-ac6dba28-2870-4631-bc0c-48d98ca5d810.png)

To show our values lined up, let’s run the same report with all invoices. To do this, we’ll change the begin date to an earlier time. Your results will vary depending on how many invoices you’ve had in the past.

![image](https://user-images.githubusercontent.com/88121568/221387692-3afd5eb1-dee3-4469-bdad-2706d9b67b6f.png)

And here are some sample results showing alignment of the values.

![image](https://user-images.githubusercontent.com/88121568/221387694-6af87515-889e-465a-b0fc-e9d3d86d8383.png)

### Capturing Filtered Results for Invoices

Going forward, we’ll be performing multiple queries against the dataset. To avoid putting unnecessary load on the service itself, and ensure that we are always working with the same data between queries, we can capture the results to a variable and use that in our formatting.

Here, we capture the data to a variable named `REPORT_DATA`

![image](https://user-images.githubusercontent.com/88121568/221387707-f1ddca89-512a-4f88-91c5-26c9ebfb43d4.png)

Now lets use that, and change our output to display the date in a readable format, followed by the memo field, and finally the amount right aligned.

To convert the date, we take the string, convert to a number using the builtin `tonumber` function, and then pass that through `todateiso8601` another builtin function before parsing the Year, Month, and Day portions from it.

The memo field will be left aligned, whereas right aligned fields create spaces before it, we want to write out extra spaces after its value.

Finally, for the value field, lets extend the length which will better account for a header later on.

![image](https://user-images.githubusercontent.com/88121568/221387712-bba7e452-df8d-4175-9eb6-dbd65d42030c.png)

And here is our revised sample results with the new formatting.

![image](https://user-images.githubusercontent.com/88121568/221387717-a1f3426b-22b4-41e4-98d6-3fc43cefd844.png)

### Creating a Header for Invoices

We can add a header to the report to put context to the data presented. Lets add both a report header for the period of time, as well as column names.

For the period of time, we’ll convert the numeric start and end date in seconds back to a readable time stamp. The column headers will be spaced out to match that of the data, and finally, we’ll create a line between the header and the data.

![image](https://user-images.githubusercontent.com/88121568/221387722-70a3a85f-3262-4970-81d2-fe5b1f1774c9.png)

Our sample results

![image](https://user-images.githubusercontent.com/88121568/221387728-74f502a7-1834-4e6b-bc03-a70870fc798a.png)

Let’s combine them so the command output runs together without interspersing the command line prompt.

![image](https://user-images.githubusercontent.com/88121568/221387740-b0ee31d4-d834-45e0-a9c6-f7b79c4153cc.png)

The header looks much cleaner now.

![image](https://user-images.githubusercontent.com/88121568/221387745-4b633e99-21ba-47ec-bea2-3c60a80d1baa.png)

### Calculating the Total for a Footer for Invoices

It would be helpful if we summarized the total sats recieved for the period. We can do this by taking the inputs, converting the value to a number, reducing the array, initializing a temporary variable, and adding the value to it for each item in the array. That may sound more complicated then it is but don’t worry, it’ll become clear with the command and results. The results we will store in another variable.

![image](https://user-images.githubusercontent.com/88121568/221387752-88802ace-d827-4046-b5fc-167b5ec89569.png)

To see the value, we can echo it out

![image](https://user-images.githubusercontent.com/88121568/221387761-30181152-a0f1-48be-a99c-4fe3a51f3b08.png)

Sample result

![image](https://user-images.githubusercontent.com/88121568/221387767-e14db8ea-dd93-4d84-be13-2a6a9446e8a7.png)

With the total, we can now put it into a footer. We’ll draw another line closing out the data and report the total

![image](https://user-images.githubusercontent.com/88121568/221387770-38847fde-946e-4163-9361-69ce0b9a2de7.png)

The sample footer

![image](https://user-images.githubusercontent.com/88121568/221387773-f2fbce2e-a2bf-47c5-bf4f-155985fafbc7.png)

### Overall Report of Invoices

Now lets combine all the portions of the above into one simple set of commands. We can take this and save it to a file for reuse later.

![image](https://user-images.githubusercontent.com/88121568/221387778-78c6c439-f231-42d4-8754-62051f3d854b.png)

And here is the sample report of invoices

![image](https://user-images.githubusercontent.com/88121568/221387782-ed692ff2-e6c7-4a52-b9d3-ed130168f24a.png)

## Payments

For reporting with payments, we’ll assume some of the same concepts that were outlined in the invoices section.

### Listing Payments

To list successful payments, we can use the `lncli` command with the `listpayments` operation, and then follow up with filtering with the `jq` JSON processor.

![image](https://user-images.githubusercontent.com/88121568/221387795-2293f2a2-c2a4-42a2-b7de-923a28d32167.png)

If there are payments, they will be listed in JSON format with several fields for each. While all of these fields have their purpose, the ones we are most concerned about for reporting are `value`, `creation_date`, `fee`, and `status`. In follow up sections, the highlighted colors depicted here will be included in commands to draw attention to where they are used.

![image](https://user-images.githubusercontent.com/88121568/221387810-2458e758-d07e-45ce-b92a-ccfcd0fc8dd0.png)

Within the `htlcs` field (hashed timelock contracts), there are more details about the routing path the payment took, and fees down to the millisat that were paid for each hop. For this basic report, we’ll stick to the basic rollup of fees rounded to the next sat.

### Capture the Filtered Payment Results

Let’s setup our reporting begin and end dates, and capture the matched payments to a variable.

![image](https://user-images.githubusercontent.com/88121568/221387818-7b81029c-95a4-4981-99b9-a1e4ed6d8347.png)

### Capture the Totals for Payments

Next, for reporting purposes, lets sum the total of invoices paid, the fees, and the overall total.

![image](https://user-images.githubusercontent.com/88121568/221387820-c6c9d0a2-a91b-4292-b848-fe6d3c436249.png)

### Overall Report of Payments

Similar to the invoices report, we prepare a payments report with a header block followed by data lines, and then a footer with the calculated sums.

![image](https://user-images.githubusercontent.com/88121568/221387824-be9d7e08-c083-4ab0-93cf-2d98f8988c1d.png)

Here’s a sample report output

![image](https://user-images.githubusercontent.com/88121568/221387828-be309a1a-6cf0-4e37-bc31-e5a65d44eaa3.png)

## Conclusion

Using the command line, we built up a report for invoices created with a lightning service. Basic filtering by date periods allows for flexibility in our reports. Textual alignment of data, formatting dates, and creation of headers and footers help make for a useful summary report. We then applied the same concepts to creation of a report for payments made. You may consider using this as a stepping stone to more reports and automation. If you think I should create more guides like this, or expand on it, please leave a comment on the article.
