# It’s Time to Run the Numbers
_Periodic autorun of Bitcoin’s gettxoutsetinfo_

by @vicariousdrama
655466–655718

![image](https://user-images.githubusercontent.com/88121568/221383781-6c174cb9-8d20-4930-9345-6cc1eb9bfe7e.png)

## Introduction

In early August 2020, there was some serious questions raised about the ability to independently audit the supply of Ethereum. Comparatively, Bitcoin supply can be audited by anyone running a node by calling a one line command 

```shell
bitcoin-cli gettxoutsetinfo
```

After a lively exchange on Twitter, [Nunya Bidness](https://twitter.com/bennd77) proposed that Bitcoin node operators and Ethereum node operators pick a block in the future, and run the numbers and compare their respective supply amongst their base to ensure consistency. In support of this effort, [BashCo](https://twitter.com/bashco_) created a [simple script](https://github.com/BashCo/RunTheNumbers) that runs, waits for a target block height, and reports the output. At block 650,000 this was done for Bitcoin and dozens (hundreds?) of node operators posted their results to twitter with the hashtag [#RunTheNumbers](https://twitter.com/search?q=%23RunTheNumbers&src=typed_query).

![image](https://user-images.githubusercontent.com/88121568/221383820-111c9e3a-0d7c-4fa6-8e38-c8e1ef27787b.png)

## Enhancing the Script

An [alternative version](https://github.com/vicariousdrama/runthenumbers) of this capability is now available that keeps running and will audit the supply, reporting results, every so many blocks.

At a high level, the data flow can be depicted as follows

![image](https://user-images.githubusercontent.com/88121568/221383844-0ac9b582-d88c-44a4-9dc3-c42688ca32db.png)

(1) Bitcoin runs as it always has, processing blocks, transactions, the mempool.

(2) As with the original script, runthenumbers will call out to Bitcoin requesting the gettxoutsetinfo. It does this by leveraging bitcoin-cli and running as the bitcoin user.
There are configuration options at the top of the script that allow for setting how often the call should be made, and the time to sleep for. An aggressive setting that I used for testing is to run the numbers every 5 blocks. This should result in an update every 45 minutes to an hour.

(3) With the results captured from bitcoin, the runthenumbers service then saves these to the designated folder. On each run, three files are created

- the_numbers_latest.txt
- The_numbers_latest.htm
- The_numbers_{block-number}.txt (e.g. the_numbers_655690.txt)
 
(4) You, the user, accesses a page in your web browser to get the latest results

(5) Nginx retrieves the file from the folder and returns it to you for rendering

## Run the Numbers as a Service

The script for running the numbers, as well as a systemd service configuration are [available here](https://github.com/vicariousdrama/runthenumbers).

![image](https://user-images.githubusercontent.com/88121568/221383868-4e7c0ac6-8c4d-4902-82d1-a29e8d003dd1.png)

Following the guidance allows for quickly getting this operational in nodes like Stadicus [Raspibolt](https://raspibolt.org).

I’m able to see the results of the most recent run at https://raspberrypi.local:1839/

![image](https://user-images.githubusercontent.com/88121568/221383881-5796ac7a-f3c4-4f77-a744-6b847f56c8d7.png)

I can also selectively retrieve the JSON of previous runs by formulating the request to retrieve a specific file. For example

https://raspberrypi.local:1839/the_numbers_655405.txt

![image](https://user-images.githubusercontent.com/88121568/221383891-a16da688-6d07-4e17-9836-a02f7def21b7.png)

## Next Steps

__UI Cleanup__ — As you can see in the previous section, the font referenced by the HTML rendered output isn’t installed on my computer. This can be resolved by either installing the font, or modifying the runthenumbers script in the locations below to be augmented with other fonts

![image](https://user-images.githubusercontent.com/88121568/221383899-debaa966-b0c7-41d3-b750-13014f02a020.png)

__Links for Previous Runs__ — It would be more convenient to the user if there was an easy way to click previous/next for available results, or for soliciting a specific block height from the user to be retrieved.

Overall though, I’m pleased with how it turned out so far.
