# Review of eSignus Hardware Wallet Offering
_HASHWallet “features” that raise concerns_

by @vicariousdrama
654886–654896

![image](https://user-images.githubusercontent.com/88121568/221383401-cd13b641-4a7c-4486-b9e9-475c5678e687.png)

## Introduction

I want to be clear upfront that I don’t have this hardware wallet and have not physically examined it. All statements within are based purely upon the information that eSignus makes available on their website(s). As a result, some of the statements may be based on a misunderstanding. The device is yet to release so some aspects may change after the time of publication.

If you are a backer of the device, I implore you to do your own research (DYOR) and not to blindly trust either myself or the maker. For the eSignus and CardLab teams, it’s clear that some decisions were intentional at the outset. I wish you the best of luck in your endeavor and strongly encourage you to adopt standards to avoid abuse of users through vendor lock-in.

As usual, I won't be reviewing all features of the device, but rather selecting a few characteristics to draw attention to.

## Change History

| Date | Description |
| --- | --- |
| 2020-10-31 | Initial Document |
| 2023-02-25 | Conversion to Markdown |

## Things I Like

I’d be remiss if I didn’t at least acknowledge some of the features that I do like about this device offering. I want to make sure that manufacturers know what I (and possibly others) are wanting so that they have insight on ways forward to bring new devices to market

### Credit Card Form Factor

This size (85.6mm x 54mm) is perfect for fitting in existing traditional physical wallets. At only 1.5mm thick it won't be overly bulky.

Why this is important: As digital currencies gain greater adoption, hardware wallets that share a similar form factor as traditional debit, credit, and proximity access cards are more apt to be carried with a user for their daily spend wallet.

### Large e-Ink Screen

Larger screens are good. One of Ledger Nano’s largest failings is its tiny screen requiring massive amounts of scrolling. Trezor and ColdCard wallets have a small screen but still require paging transaction information.

Why this is important: The more information that can be assessed on the device at a time the better. Furthermore, it opens up to improved accessibility with larger font sizes.

### Water and Dust Resistance

It claims IP-67. This means it offers protection from contact with harmful dust and is protected from immersion in water with a depth up to 1 meter for up to 30 minutes.

Why this is important: A wallet with a credit card form factor is inevitably going to end up in locations like a wallet, your pocket, and may be exposed to rain, an accidental brief dip in the pool, etc.

### Secure Element

The site doesn’t clarify this exactly, but it seems that the secure element, in this case, is the Ambiq Apollo 3 microprocessor running the main software as it has secure key storage on the chip (section 4.4 page 174 of [datasheet](https://cdn.sparkfun.com/assets/learn_tutorials/9/0/9/Apollo3_Blue_MCU_Data_Sheet_v0_9_1.pdf)). The way this is applied in this case is questionable, but all hardware wallets should leverage secure elements

Why this is important: Secure keys should be kept in dedicated chips resistant to tampering. One of the failings of Trezor and Keepkey is their lack of securely storing the private keys.

### The Indiegogo Storefront

This project began in late 2018 and launched on Indiegogo as a store in the Spring of 2020. At the time of writing it has 206 backers with an average backing of $293. The perks available on Indiegogo were purely based on the quantity of wallets and an effective discount with pricing ranging from $161 to $234 per unit. Retail set for $261 per unit with an initial pre-order pricing of $235. The advantage of the Indiegogo campaign is that it yields eSignus Vault service free of charge to those users forever

## Security “Features”

A few of the stated advantages, and their failings

    “Its a non-programmable device. This feature creates a really secure environment for signing transactions and the safeguard of the keys”
    
This is bad for users because any vulnerability identified is only mitigated by the acquisition of a new HASHWallet with updated firmware flashed at the factory. Apart from an additional cost to the user (which eSignus may give discounts on), there’s no indication of how a user would ensure they have the latest version of what the version of firmware is.

    “Public/Private keys are generated inside the card through a random process, which cannot be replicated. No external seeds are used to generate keys.”
    
This is bad for users as they can’t verify that the resulting addresses are in their possession independent of the wallet.

    “Your fingerprint has patterns that are unique to you. As they are impossible to replicate, security is guaranteed with your touch only”

This may be bad for users as an attacker can cut off their thumb or fingers to use in perpetuity. Or bound the user and force them to physically sign. Passcodes are much better controlling for unlocking devices.

![image](https://user-images.githubusercontent.com/88121568/221383538-3002b1ce-6158-4a5f-acc1-8ff5c60ffcc5.png)

Regardless, the use of biometric capabilities like this eliminates the potential for duress pin access or password/code/phrase level protection. For further information, the device uses the FPC1321 chip for fingerprint reading. It’s the first generation release from Fingerprint Cards AB.

## Failings in the Recovery Process

The recovery process is based on two secure elements, plus optional fingerprint integration. When initialized, there is a recovery key component which consists of a one time pad used as an encryption key, and the recovery seed, which is randomized. The recovery key may be kept in the secure vault service or under your control.

It’s important to note that the recovery seed doesn’t follow the long-established [BIP-39 standard of mnemonics](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki) that you may be familiar with for other wallets. __Personally, this alone makes it dead on arrival__ as it doesn’t fit well in existing standards and creates unnecessary risk but it gets worse. I can only assume that this was bypassed in part due to the desire to support other digital assets in addition to Bitcoin.

According to their documentation the card “stores the private key without anyone knowing it, not even the user. This key cannot be accessed from the outside in any way. Therefore, the card is invulnerable and cannot suffer external attacks.”. On the contrary, this makes it vulnerable to grief attacks

![image](https://user-images.githubusercontent.com/88121568/221383574-f8400af6-5a6b-495f-b84d-61a812396c9b.png)

Water and Fire represent the most common environmental risks to your backup. What if an arsonist burns your house down? If a fire occurs, you could lose your device and the backup recovery cards through melt from high heat, or water from subsequent fire suppression. Make sure your backup solution can survive the fire. I recommend reviewing the results of [Jameson Lopp’s Metal Bitcoin Seed Storage Stress Tests](https://jlopp.github.io/metal-bitcoin-storage-reviews/).

Another issue is the need to plan your recovery up front, whether you are using the fingerprint option or not. The contents out of the box don’t permit the fingerprint recovery, as that necessitates a separate Fingerprint Recovery Card to support it. Pricing on that, nor additional basic Recovery Cards isn’t currently available on the website at the time of writing, but users should bear this in mind for the total cost of operations.

## The eSignus Vault Service

This feature is described in detail [here](https://gethashwallet.com/features/vault-service), and makes the claim “You’re in control with our recovery system”. Take a moment to re-read that and grasp what that means.

![image](https://user-images.githubusercontent.com/88121568/221383587-f8142197-265a-45fe-93f2-e39e3f82a86d.png)

The page describes different models of control which are referenced herein

__Not distributed__. The recovery seed and recovery key are stored on a single recovery card. Effectively, this is a 2-of-2 recovery process melded into 1, on par with writing down seed words or engraving into a metal plate for safekeeping. They don’t recommend this. If I was forced to use this wallet, this, or Distributed is the only way I’d use it.

__Distributed__. Saving the seed and key in two separate recovery cards and in different places. This is a 2-of-2 recovery process, that results from cutting in half.

__eSignus Vault__, The User saves the recovery seed, delegating custody of the recovery key to the eSignus Vault. Effectively, this makes recovery 2-of-2 where you only have absolute control over 1 piece, trusting eSignus with the other. This is really a bad idea.

This service requires an annual subscription, but is free for Indiegogo backers/buyers. Well, at least as long as eSignus is in operation I suppose. What’s the guarantee there?

__eSignus Trust__. Doesn’t exist yet, but intent is to establish an insurance contract with eSignus, and transfer the recovery seed. eSignus would reimburse the user for the full amount of funds in the event of theft or loss of access to accounts. This model implies that you get to pay for a service where you also trust the provider that can act as a man-in-the-middle on your funds.

Note that if you start with eSignus Vault, you’ve already delegated custody of the recovery key. Moving to eSignus Trust hands over the seed. This is absurdity.

Any time recovery is split into multiple components, risk of loss is dramatically increased. Conversely if it were actual seed words split, that reduces security (see [https://youtu.be/p5nSibpfHYE](https://youtu.be/p5nSibpfHYE) for a refresher)

## End User Verification

At the time of writing, eSignus has [clearly indicated](https://support.esignus.com/hc/en-us/articles/360007230778-Is-HASHWallet-an-Open-Source-Project-) that they have no intention of making the firmware or the application software open source.

This means that user’s will put full faith into eSignus that they aren’t performing a Man-In-The-Middle Attack on the transactions. To clarify, the user “signs what they see”, on both the device in conjunction with the application. If the user wants to send funds to address `36rQ1G4HFvWn5ug5msjmQ4TfMHhkVSEHdr`, both the application and the HASHWallet can display `36rQ1G4HFvWn5ug5msjmQ4TfMHhkVSEHdr`, but in turn prepare the transaction as sending to `33jUhZ9QM5yseMgKvvn7tfL8nLxXuPkiJh`. The user then thinks they are signing one transaction, but actually another, and is none the wiser until they find out there funds went elsewhere. This isn’t limited to just addresses, but also amounts and change addresses. The user has no recourse to verify that what they are seeing is actually what is being signed.

Related to this, since the recovery seed and key are proprietary, there is no way to configure watch wallets in external wallet facilitators such as [Electrum](https://electrum.org/), [Sparrow Wallet](https://www.sparrowwallet.com/), or [Specter Desktop](https://github.com/cryptoadvance/specter-desktop/releases). This also means there’s no ready independent verification of how addresses are derived for receiving.

Since the applications on mobile and desktop facilitate sending the transaction, the user has limited control over independent verification. This unfortunately leads to weak privacy as IP Addresses, and other identifiers will be associated with the transaction. Even if the hardware wallet itself is fully secure, the same cannot be claimed about the desktop or mobile software which introduces new attack vectors.

## Summary

Use of this hardware wallet as it stands today offers some convenience in physical dimensions and has some features that I appreciate.

But security and privacy are quite weak. This is marginally a step up from custodial bitcoin on an exchange, and should indeed be thought of as custodial as there is no independent verification. All transactions are through software that a third party controls. Without capacity to verify that its real coin, users might as well be using PayPal. I don’t think the intent is to use this wallet to store large amounts of funds.

For eSignus, what is really concerning is that surely there must be at least one security-conscious member of the team that has thought of at least some of the concerns expressed within. Perhaps they were under the impression that they were improving security and would have a unique offering. But creating proprietary solutions in a silo is a good way to fail on delivery.

With HASHWallet, you are not in control. eSignus is. You just pay for it, perpetually.
