# Bug in Cash App Withdraw Process
__Could Cause You to Send Wrong Amount or Wrong Address__

This is a brief description of two bugs previously reported to Cash App Support in early August 2020 which have not yet been addressed.  Multiple application updates have transpired since then, and the bugs are still present.  A follow up to Cash App Support was initiated to redescribe the bug, and make them aware that this would be disclosed to the public after 30 days.

For what its worth, the title is intentionally “click-baity” to get your attention. A key word here is “could”.  There are no known instances where people have inadvertently sent the wrong amount, or sent to an unintended address as doing so requires identifying the issue during a verification check, and then outright ignoring the same verification check.

Here’s the basics of the bug:

1. From within Cash App, navigate to the Bitcoin screen and initiate a withdraw by choosing the Airplane icon to Send Bitcoin.
2. Specify an amount to be sent. Any amount will suffice.
3. Specify an address to send it to. Again, any address will suffice.
4. On the confirmation screen, make note that the amount and address are as you entered on steps 2 and 3.
5. Now, lets assume that you entered either the address or the amount incorrectly.  Press the back button to return to the input screen.
6. Specify a new amount to be sent.  This should be different then that in step 2.
7. Specify a new address to send it to. Again this should be different then that in step 3.
8. Continue to the confirmation screen.  Note that both the amount and the address have not been updated and continue to reflect the values from steps 2 and 3.

If a user on step 5 notices an incorrect input (transposed amounts, missing digit, too many digits whatever), and wants to correct, they need to be certain they actually check again on step 8.  Continuing on step 8 and putting in pin or biometrics will send the amount to address originally entered, not that which may be intended by steps 6 and 7.

This was tested and verified on the Android version of the application.

Cash App support was notified on August 11, 2020, and again two weeks later on August 25, 2020. During this same period of time the Cash App application was updated to 1) Add the Coindesk News section 2) Remove the Coindesk News section 3) Change the Send process 4) Add the Coindesk News section again.
