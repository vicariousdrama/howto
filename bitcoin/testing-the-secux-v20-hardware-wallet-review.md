# Testing the SecuX V20 Hardware Wallet | Review
_Hidden Accounts, Exposed XPubs, Leaked Keys, and Other Shenanigans_

by @vicariousdrama
653892–654043

![image](https://user-images.githubusercontent.com/88121568/221381510-c61fe70d-a896-4334-8957-400eba358d0f.png)

## Summary

The SecuX V20 is the flagship hardware wallet offering from [SecuX](https://secuxtech.com/), which is a relative newcomer having been established in 2018. The device has a large touch screen color display, a battery to operate offline/disconnected, and interfaces with host over USB or Bluetooth. It touts an [Infineon](https://www.infineon.com/) secure element chip that has been CC EAL5+ certified. While on the bulky side as far as wallets go, it looks pleasant, yet dated and resembles an oversized coaster or flattened hockey puck.

This article isn’t an unboxing or a walkthrough of user features. For that, I direct your attention to the user manual or assorted videos on your favorite video streaming site. What I will cover however are some security and privacy concerns I ran into while testing out this wallet. For anyone using a hardware wallet, security is a significant concern, and is often tempered with usability depending on needs of the individual. It is my hope that you learn something here for not only the SecuX wallets, but also the things look for while choosing the best hardware wallet for you.

## Change History

| Date | Description |
| --- | --- |
| 2020-10-24 | Initial Document |
| 2023-02-25 | Conversion to Markdown |

## The Testbed

Let me start off by stating that I usually do all my testing in production. This is more of a personal choice due to limited resources, and it forces me to pay extra special attention to what I’m doing. In this case, there isn’t a way to run testnet if I wanted to as the device doesn’t support it.

While this device supports Bluetooth, I don’t make use of it in testing. It’s probably super handy for pairing with mobile devices but considering the bulkiness of the SecuX, I found that I’d likely be sitting at my desk anytime I wanted to operate it.

![image](https://user-images.githubusercontent.com/88121568/221381576-0ff65c5d-79f0-4cd9-9294-8dcfecd54823.png)

USB was the sole means of interfacing that I chose, and only with browser based capabilities as that offers the full feature set and is cross platform.

## Hidden Accounts and Plausible Deniability

For initializing the device, I use pins `1234` and `0000` (Pins and Passwords expressed herein are for simplicity in explanation. Use something stronger!). I allow the device to generate seed words, as well as verified it could restore seed recovery words. For the security conscious, you should generate your own seed words following protocol, and can use the [Estudio Bitcoin guide](https://estudiobitcoin.com/do-you-trust-your-seed-dont-generate-it-yourself/).

Regardless of whether you allow the device to randomly pick a set of seed words or you generate it on your own, it will only support without a passphrase. The “25th” word is actually part of the Hidden Wallet feature. So if you have a passphrase, you initialize with the base 24 words, and then create a Hidden Wallet specifying your password at the time of configuration.

Also important to note that the wallet ONLY works with nested segwit.

Page 4 of the [manual](https://secuxtech.com/secuxtech-download/User-Manual/SecuX-User-Manual-2019.pdf) states this for the Hidden wallet feature.

![image](https://user-images.githubusercontent.com/88121568/221381657-4d59c03a-d915-4f5b-a577-57a9c1eae56e.png)


So in my case, I protect the base 24 words with the pin `1234`. I’ll refer to this as the “`Main Key`”. When logged into the device with the pin for the `Main Key`, the Settings menu has a choice for `Hidden`. Click on that, and I choose and confirm pin `0000`. For Passphrase, on pin `0000`, I use `AAAA`. This I refer to as “`Hidden Key`”. At this point, the device restarts, and when logged in with the `Hidden Key`, the Settings menu no longer shows `Hidden` as an option.

Now let’s review how this is applied if under duress. In a wrench attack situation, if you log in with the `Main Key`, then an attacker familiar with this device can verify that you are on the `Main Key` because Hidden is available in the settings. Likewise, if you login with the `Hidden Key`, they know that as well.

So to use this wallet with a Duress type setup, you need to do the following

1. Login with pin for the `Main Key` (`1234`)
2. From the Settings menu, verify `Hidden` is a displayed option
3. Click the `Hidden` option
4. Enter and confirm a pin (`0000`)
5. Enter a password

Now I don’t use `AAAA`. Instead, I’m going to use `ZZZZ`. The device restarts and I log in with the ping for the `hidden key`.

Since the passphrase acts as the 25th word, the `Hidden Key` is now setup with a completely different private key then it was when I first used `AAAA`. I can log in to the web console, and manage accounts. While the label on the `hidden` account remains the same with different pass phrases, under the hood it is a different private and public key.

So to protect funds, you want to remember not only 2 different pins, but also your passphrases. With the aforementioned info..
- `Main Key` — Treat as fake with a small amount of funds
- `Hidden Key` passphrase `AAAA` — Treat as fake with small amount of funds
- `Hidden Key` passphrase `ZZZZ` — Real “stash” with most of the funds
 
To recap: Anytime I need to spend/review my stash, I login to `Main`, and configure `Hidden` with passphrase `ZZZZ` for my stash. I then login to the `Hidden key`, perform transactions, and then restart again. Log back into main and configure `Hidden` with passphrase `AAAA` for the fake stash. This allows for showing both the `Main` and `Hidden` accounts without exposing your secret stash.

A bit of work, and not really a good way to protect funds but it is passable for plausible deniability.

## Exposed XPubs

One of the major caveats to the SecuX wallet is that all interfacing has to be done with servers that SecuX themself controls, or third parties they interface with. There is no HWI interface, or plugin to use the wallet with common software interfaces like [Electrum](http://electrum.org/), [Sparrow](https://sparrowwallet.com/), or [Specter](https://github.com/cryptoadvance/specter-desktop).

Perhaps it's intended to shield the user from technicals, but neither the device, nor the web interface, (and likely the iOS and Android mobile apps) provide any information regarding the XPubs or Derivation Paths. Such would be handy for setting up a watch wallet in Electrum for example. There are two ways to mitigate this however

### Option 1. Use Electrum offline

With a fully offline computer not connected to the network, bootup with [Tails](https://tails.boum.org/), open Electrum, and recover the wallet with the seed words established when initializing the device. Choose options to denote that it is [BIP 39](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki), and optionally enter your passphrase (`AAAA` and `ZZZZ` above) for the key you want. For the type of wallet, you should choose `P2WPKH-P2SH`, with the derivation path `m/49’/0’/0’`. You can then view the Wallet information which will display the `ypub`. From the console, you can get more details, including both the `xpub` and `ypub` by entering the following

```c
k.dump() for k in wallet.get_keystores()
```

## Option 2. Use the website

At some point you have to use the website anyways. Even to just create an account for a coin to appear in the list on your device.

When you goto the [wallet website](https://wallet.secuxtech.com/SecuXcess/#/wallet/account) and connect your device, there is an abundance of activity to assorted domains and API calls.

While viewing the Bitcoin account information, two calls are made with both the XPub and the YPub for the current account being viewed. You can see these requests in the developer tools and retain for future reference. In brief, the web interface is communicating with the hardware wallet, extracting the public keys, and sending them to api.blockchair.com to get the list of addresses.

From a privacy standpoint, your xpub information, or at least traffic regarding cryptocurrency is being shared with the following and maybe more

- maxst.icons8.com
- fonts.gstatic.com
- wallet.secuxtech.com
- www.google-analytics.com
- cdnjs.cloudflare.com
- o414050.ingest.sentry.io
- api.blockchair.com
- bitcoinfees.earn.com
- report-uri.cloudflare.com


One aspect that should be crystal clear is that the use of this device affords zero privacy. While it is a stretch, it is conceivable that some of the above entities could perform pattern recognition on the requests to ascertain the sets of public keys over time and determine the state of whether your hidden wallet is in “stash mode” or not.

## Address Verification and Coin Control

Regardless of which option you use to derive your XPubs from the prior section, you can then load them up in Electrum to have another means to verify the addresses being displayed on the device are under your control.

Within the web interface, I found that when clicked the Receive button for an account, the address presented seemed to be randomly chosen from the next 5 addresses available. This initially raised concerns when it didn’t match the first address and is all the more reason to have another means to verify addresses in Electrum or other wallet setups for watching the XPub.

There is no coin control available for choosing addresses to spend from.

All signing of transactions is done integrating the device with the web application and confirmation actions on the device through the touch pad. There is no support for offline transactions, PSBTs, or control of broadcast to your own or preferred server.

## Leaked Keys

This brings me to my next major concern. Leaked keys on the website itself. Not your private keys (which hopefully are kept in the secure element of the device), but keys used by the web site to call different web services.

Based upon the information collected, this could be easily exploited to bring down the service and prevent people from viewing their accounts. Since the device is dependent upon this interaction with the website to prepare transactions, the user is left in the unfortunate position of not only not being able to see their accounts, but also not being able to spend from them. The FAQ on the SecuX website addresses this

![image](https://user-images.githubusercontent.com/88121568/221382024-8d53c65d-8bd1-4883-95a4-933e47e6cf76.png)

This coincides with my recommendation. Generate your seed words you use to initialize the device and have a backup of them so that you can recover your account and funds.

## Recommendations for SecuX

For SecuX, I recommend the following

Website

- Close the security holes that could lead to denial of service. Contact me if you need more details here.
- Reduce excess data sharing
- Make it clear to the user the data being collected and how it is used
- Add coin control and thorough labeling
- Add support for native segwit retrieval
- Consider adding multi-signature support
- Use a more accurate fee estimator service

Device firmware

- Add support for native segwit
- Add support for user choosing account number
- Add support to github.com/bitcoin-core/HWI for hardware interface
- Add support for displaying the public key, derivation path, and type

Documentation

- Improve/expand upon the hidden wallet feature taking into account the section enclosed above
- Definitely denote what the type of wallet (P2WPKH-P2SH)
- Consider explaining the derivation path to users

Conclusion

With so many security and privacy concerns, I can’t recommend this wallet at this time.

![image](https://user-images.githubusercontent.com/88121568/221382072-0c87c482-e200-4684-9a06-685758654669.png)

It’s important to note though that many of these concerns can be addressed with appropriate focus.

For Users, if you own this wallet, be mindful of the caveats above and make sure you can recover your funds.
