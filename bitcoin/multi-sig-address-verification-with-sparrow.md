# Multi-Sig Address Verification with Sparrow
_XPubs, Watch Wallets, and Derivation Paths, Oh My!_

by @vicariousdrama
649169 - 649173

![image](https://user-images.githubusercontent.com/88121568/221367962-a0df58de-fa5f-4f23-bc05-2e832ebd4e07.png)

## Summary

Sparrow Wallet is a Bitcoin wallet facilitator that is gaining in popularity. According to the website, it is a wallet for those who value financial self sovereignty with an emphasis on transparency and usability.  This wallet is available on Mac, Windows, and Linux from the [download](https://www.sparrowwallet.com/download/) page.

This article is a follow up to a previous one I wrote titled ‘Address Verification when Changing Keys for Unchained Capital Vaults’.  The intent is to provide similar steps for setting up a watch wallet to give another option for verifying addresses.

## Change History

| Date | Description |
| --- | --- |
| 2020-09-20 | Initial Docuemnt |
| 2023-02-25 | Conversion to Markdown |

## Creating a Watch Wallet with XPubs

Similar to Electrum, you can create a Watch Wallet in Sparrow for purposes of monitoring a wallet if you have the xpubs of the cosigners.

For consistency, this sample will use the same xpub values that I referenced previously

`xpub6FBFAVmiF1pgCYanH9GdbgHbiLkHSUq9c5KkY6c7mEk4o8757p8JsrdXo3zsy3uifqGEsBkp45C4jFYPM1X7k3bgsRmijrjz5edaFsxdodA`

`xpub6EkQHCE3w9F6qyCAZxW5vh87b969wiKUaB6NnYcjcsuLzPeEckNSffjHPFhP2hKM6jeAtRdoRiPGBJ3F72t6n4psx4gvEyhPsRitDo7yKkj`

`xpub6EDykLBC5ERX7WREobYaca2ALTFZKLku9RDuPCi2MKf4YbnA4pGF7zVzRqGjrdJK33aeJ2K6qr2qfrz64EikAyEkpbdkmoedFC16smSacJB`

Once you’ve opened Sparrow, from the menu bar, choose `File`, then `New Wallet`.  Give the wallet a name.  In my setup, I chose `Sparrow Sample XPub Watch`.  Initially, the view will default to a single signature wallet and pay to witness private key hash.  

![image](https://user-images.githubusercontent.com/88121568/221368036-2c9f073c-c01e-44ef-852b-33ffbfa19a8b.png)

Change it to Multi Signature, with a script type of P2SH, with M of N cosigners set to 2 / 3.  For different wallets, you may use a different script type.  I chose P2SH as I’m modeling this after a wallet setup in an Unchained Capital vault.

![image](https://user-images.githubusercontent.com/88121568/221368047-57fab427-513c-49c6-bff7-e81f7d7253e5.png)

Next, the three Keystores representing the Cosigners need to be setup.  Note that each of the captions for the Keystore tabs appears with red hue indicating they need more information.

![image](https://user-images.githubusercontent.com/88121568/221368055-e2ed6450-9722-49af-8a3c-a487e38c7f87.png)

Choose the XPUB / Watch Only Wallet option.

![image](https://user-images.githubusercontent.com/88121568/221368107-08d35e6f-e294-4c6a-82d1-44205ceb0463.png)

In the xPub field, copy and paste one of the xPub values.

![image](https://user-images.githubusercontent.com/88121568/221368114-d4173396-4fee-4689-8746-29a221f49f31.png)

Upon doing so, the `Master fingerprint` and `Derivation` fields will be color coded with a reddish outline indicating they need a value.  For the master fingerprint, just enter 8 zeros.  And for Derivation, provide the value `m/`

Repeat this process for the other two tabs and xpubs

![image](https://user-images.githubusercontent.com/88121568/221368139-19d932ea-f96e-48c5-a7d8-99361041d5e7.png)

![image](https://user-images.githubusercontent.com/88121568/221368144-527f7e5b-c86d-4c6d-b17f-79821435f374.png)

Finally, click the `Apply` button.  A dialog will appear prompting you if you want to add a password to the wallet. I left this empty and clicked the button `No Password` to continue.

Now navigate to the Addresses view to see all available receiving addresses. The addresses depicted are under the control of the private keys associated with the xpubs.  I had setup this wallet previously inside of an Unchained Capital vault and needed a way to verify that I controlled a specific address.  

![image](https://user-images.githubusercontent.com/88121568/221368175-087910b6-84f9-43ee-9d62-80f14d4ff1f3.png)

## Creating a Regular Wallet with Devices

In this example, I will setup a multi-sig wallet where two cosigners are from hardware devices I control, and the third cosigner is the xpub. This mimics typical setups for both Unchained Capital and Casa where the collaborative custody provider holds one of the keys.

- Device 1 has a derivation path of m/45'/0'/0'/1
- Device 2 has a derivation path of m/45'/0'/2'/0

The xpub from the provider is 
`xpub6EDykLBC5ERX7WREobYaca2ALTFZKLku9RDuPCi2MKf4YbnA4pGF7zVzRqGjrdJK33aeJ2K6qr2qfrz64EikAyEkpbdkmoedFC16smSacJB`

From the menu bar of Sparrow, choose `File`, then `New Wallet`.  Give the wallet a name.  In my setup, I chose `Sparrow Sample HW Device`.  Initially, the view will default to a single signature wallet and pay to witness private key hash.  

![image](https://user-images.githubusercontent.com/88121568/221368238-6b7e21a6-c11a-4fe5-9a7c-995c13f95145.png)

Change it to Multi Signature, with a script type of P2SH, with M of N cosigners set to 2 / 3.  For different wallets, you may use a different script type.  I chose P2SH as I’m modeling this after a wallet setup in an Unchained Capital vault.

![image](https://user-images.githubusercontent.com/88121568/221368239-9e62e856-7e79-4780-9b3c-a1e6d470c50a.png)

Next, the three Keystores representing the Cosigners need to be setup.  Note that each of the captions for the Keystore tabs appears with red hue indicating they need more information.

![image](https://user-images.githubusercontent.com/88121568/221368244-6250e2a2-d8f5-4562-bcf6-758f8e5a1701.png)

Click the `Connected Hardware Wallet` button. A new dialog opens for Connecting the Hardware Wallet. Click the `Scan` button.  

For Ledger Nano, I click the Show Derivation… link to expand.

![image](https://user-images.githubusercontent.com/88121568/221368268-1b703325-b831-43b5-bef7-f5690623318f.png)

Change the value to my derivation path `m/45'/0'/0'/1` and click `Import`.  The xpub is determined from the master key and populated in the entry fields. As a convenience, the Label is also updated to reflect that this was a Ledger Nano S

![image](https://user-images.githubusercontent.com/88121568/221368286-80a260cd-b57f-4b14-b198-3993b7a77a88.png)

For the second Keystore, I repeat the process, but for that device I use derivation path `m/45'/0'/2'/0`

![image](https://user-images.githubusercontent.com/88121568/221368297-91b01c64-a0e5-4e04-8784-57a519522ca8.png)

And for the third keystore, specify the XPUB, with a derivation path of m/ and master fingerprint as any value

![image](https://user-images.githubusercontent.com/88121568/221368302-83f1218e-4a19-47e9-a29e-b32b517f63a6.png)

Finally, click the `Apply` button.  A dialog will appear prompting you if you want to add a password to the wallet. I left this empty and clicked the button `No Password` to continue.

Now navigate to the Addresses view to see all available receiving addresses.  With this wallet, I can use my hardware devices to sign any transactions I create, as well as verify the receiving addresses

![image](https://user-images.githubusercontent.com/88121568/221368319-c534cc34-1090-4e45-bae4-9b7717e4e2ef.png)

## Conclusion

Sparrow Wallet is an easy to setup and transparent bitcoin wallet for multi-signature.  The addresses displayed for my multi-signature wallet are the same as those I had previously seen in both Caravan and Electrum.  

I hope you are able to verify this for yourself.  Give Sparrow Wallet a try if you haven’t already, and try setting up the same watch wallet with provided xpubs. You should see the same addresses and transactions.

Don’t Trust. Verify.
