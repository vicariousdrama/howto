# Address Verification when Changing Keys for Unchained Capital Vaults
_Don’t Trust. Verify. _

by @vicariousdrama
649093 - 649108

![image](https://user-images.githubusercontent.com/88121568/221362120-5fe183af-a672-45c6-bd32-90dc5673bab2.png)

## Summary

Unchained Capital describes itself as a bitcoin native financial services company offering collaborative custody multisignature vaults and loans for bitcoin holders.

The vaults, which are free to setup with a KYC profile, allow the client to control 2 keys while they control a backup key.  Periodically, a user may mark a key as lost or stolen or otherwise need or desire to replace it.  Within the web application for managing Vaults, addresses are displayed that the user should verify independently to ensure that their signing devices will have the ability to spend.  This steps for address verification are not covered in detail within the application so I’ve prepared this article to give some guidance in that regard.

If you follow along and have a vault to try this with, I hope this will improve your understanding of how to verify addresses in general.

## Change History

| Date | Description |
| --- | --- |
| 2020-09-19 | Initial Document |
| 2023-02-19 | Add footers for page numbers, adjust table of contents |
| 2023-02-25 | Conversion to Markdown |

## Initial Vault & Key Configuration

For the purposes of this article, I have a vault that uses 2 keys that are derived from a single hardware device.  The names and BIP32 paths are as follows
- hollywood: `m/45'/0'/0'`
- balboa:	`m/45'/0'/1'`

When the vault was created with these keys, the “account number” for each was 0, making the full base derived path as follows
- hollywood: `m/45'/0'/0'/0`
- balboa: `m/45'/0'/1'/0`

The xpubs for each, along with the unchained key can be seen on the `External Spend Information` dialog accessible from the menu of the vault’s `Transact` section.  Anytime a vault is created, or a key is changed, the information from this screen should be retained. I recommend printing it and keeping with your records. The `Download` button produces a JSON file that can be used directly with Caravan, converted for use with Electrum and other wallets and is also suitable for printing.

![image](https://user-images.githubusercontent.com/88121568/221362206-86055c05-a5a2-465d-b58e-babdaf6c029a.png)

In this case, the unchained key has the following xpub

  `xpub6EDykLBC5ERX7WREobYaca2ALTFZKLku9RDuPCi2MKf4YbnA4pGF7zVzRqGjrdJK33aeJ2K6qr2qfrz64EikAyEkpbdkmoedFC16smSacJB`

## Key Replacement Process

When a key is replaced on a vault, a new “wallet” is formulated with new addresses.  A transaction to sweep funds from the old “wallet” to the new one in the vault is established, signed with remaining keys, and broadcast.  The web application does a good job of explaining this and walking through the process.

![image](https://user-images.githubusercontent.com/88121568/221362257-018d75d8-c1e1-4bf5-99a7-00c1bc701e5d.png)

For purposes of this example, I create a new key which has the following base BIP32 path
- crater: `m/45'/0'/2'`

I plan to replace balboa and specify crater as the Replacement Key. Since I still have access to balboa to be able to sign, I toggle that option on and continue clicking `Replace Key`.

The vault screen depicts the new key and that a Sweep transaction is in progress.

![image](https://user-images.githubusercontent.com/88121568/221362328-e0061f11-b809-4dc1-b637-b1c06baaa452.png)

Transaction details show the keys that can sign for this transaction. Note that balboa is present, but crater is not.  The address funds are to be sent to is `31w1VhPmSvoCqQJ227aG83prWyQcDKbjiC` and is what I want to verify.

![image](https://user-images.githubusercontent.com/88121568/221362340-49e0a45f-4833-4441-a469-95c8e99e88c6.png)

The External Spend Information for the vault still reflects the existing key setup with unchained, balboa, and hollywood, and cannot be used to verify the address in external tools.

## Determining the New External Spend Information

To verify the address for the new wallet within the vault, its important to understand how the multi-signature wallet is setup.

The full derivation path for keys used by Unchained Capital vaults and addresses is segmented as follows

| Depth | Path Value | Description |
| --- | --- | --- |
| Depth 1 | 45' | Hardened. Indicates it is for multisig |
| Depth 2 |  0' | Hardened. Indicates it is for mainnet |
| Depth 3 |  0' | Hardened. The account number |
| Depth 4 |  0  | Product key for an account, incremented as used in a vault or a loan |
| Depth 5 |  0  | 0 for a deposit address, 1 for a change address. Unchained Capital doesn’t support change addresses yet so this is always 0. |
| Depth 6 |  0  | he address depth which increments as addresses are used. |

Depth 4 is what we need to track to for the new key.  Recall that when the replacement key crater was made, it had a BIP 32 path of `m/45'/0'/2'`.

Each time a key is used in a different vault, it’s product key number is incremented.  The very first time it is used on a vault, it starts at 0.

The xpubs that comprise the new wallet are as follows
- xpub for hollywood key with derived path `m/45'/0'/0'/1`
- xpub for new crater key with derived path `m/45'/0'/2'/0`
- xpub for unchained key `xpub6EDykLBC5ERX7WREobYaca2ALTFZKLku9RDuPCi2MKf4YbnA4pGF7zVzRqGjrdJK33aeJ2K6qr2qfrz64EikAyEkpbdkmoedFC16smSacJB`

If I had not created crater, and instead replaced with another key in my account, then the 4th depth would have incremented.  For example, A key associated with 3 other vaults (active or closed) with a base path of `m/45'/0'/99'/` would have derived paths of `m/45'/0'/99'/0`, `m/45'/0'/99'/1`, and `m/45'/0'/99'/2`. The next derived path would be incremented to `m/45'/0'/99'/3`.

Most of the remaining aspects of External Spend Information remain the same.  The Address Type is P2SH, and the Quorum is 2 of 3.  The starting address index will differ and likely directly associated to the total number of addresses already used in the vault.

## Verification with Caravan

With the newly derived External Spend Information, we can load this up in the Caravan which is accessible here: [https://unchained-capital.github.io/caravan/#/wallet](https://unchained-capital.github.io/caravan/#/wallet)

For `Extended Public Key 1`, connect the hardware device for the remaining key, choose the type and specify the BIP32 Path down to the product key taking care to set the apostrophes where required for hardening.  In my example, I enter `m/45'/0'/0'/1` for my hollywood key. Click `Import Extended Public Key` and follow on screen instructions.

Similarly for `Extended Public Key 2`, repeat the process, but for the new key.  In my example, I enter `m/45'/0'/2'/0` for my crater key and click `Import Extended Public Key`.

Finally for `Extended Public Key 3`, I choose `Enter as text`, and specify the xpub for the Unchained key.  Upon doing so, a summary is displayed

![image](https://user-images.githubusercontent.com/88121568/221362671-cfc17639-ad19-4291-b022-53d9393df029.png)

When clicking confirm, you will likely see that there is 0 BTC in the multisig wallet, and no records to display for addresses.  At the bottom of the screen, check the boxes for Spent Addresses and Zero Balances.

![image](https://user-images.githubusercontent.com/88121568/221362680-24d3f5db-822c-4c41-97cd-83ccd3e625ca.png)

The addresses are displayed, starting with the first 10.  

I can verify address `31w1VhPmSvoCqQJ227aG83prWyQcDKbjiC` is at index 2.

## Verification with Electrum

This process can also be done with Electrum. 

Create new multi-signature wallet

![image](https://user-images.githubusercontent.com/88121568/221362737-d328cc1c-6789-4e43-a7dd-364fee205c8d.png)

Specify 2 signatures required, of 3 cosigners

![image](https://user-images.githubusercontent.com/88121568/221362743-c21f4651-f136-4df1-a030-4da1944732fe.png)

### Import the public key for cosigner 1

![image](https://user-images.githubusercontent.com/88121568/221362754-1d472018-a435-42e6-8ab2-ff49f51c59b6.png)

Scan devices

![image](https://user-images.githubusercontent.com/88121568/221362763-80232a82-1870-4c47-a559-31bbf4f7f9f5.png)

Specify script type and derivation path

![image](https://user-images.githubusercontent.com/88121568/221362767-ab671886-149b-42df-89f3-7b48a9af081c.png)

![image](https://user-images.githubusercontent.com/88121568/221362774-3832c7e5-d29d-4f58-afdf-d02dab57ee35.png)

### For device 2, I repeat the process

![image](https://user-images.githubusercontent.com/88121568/221362791-56a5cba7-db5e-4986-a4fe-d75380575ff1.png)

And use it’s device and derivation path

![image](https://user-images.githubusercontent.com/88121568/221362799-35c657ee-ab70-42d6-8c1a-bad7892784b1.png)

### And lastly, cosigner 3 for the unchained key

![image](https://user-images.githubusercontent.com/88121568/221362842-1ce0c5aa-30da-4ab3-ac32-1c28be5f4239.png)

![image](https://user-images.githubusercontent.com/88121568/221362846-a8b85be3-1cc5-4594-a114-c0c12a7d2857.png)

### Optionally specify a password

![image](https://user-images.githubusercontent.com/88121568/221362852-fc7975f1-8ba9-4e99-bea6-a146c5edfcd6.png)

### Wallet Created

The History is displayed

![image](https://user-images.githubusercontent.com/88121568/221362857-3d168668-3bcf-4769-8049-3cb4b2eb5e52.png)

And the addresses

![image](https://user-images.githubusercontent.com/88121568/221362888-656d21fb-7775-4541-8bd7-f1804657ac77.png)

From this I can verify that the address `31w1VhPmSvoCqQJ227aG83prWyQcDKbjiC`  intended for Key Replacement is present in index 2.  Funds swept to the address would be spendable by me.  Two transactions are shown here as I’ve since swept funds out of this wallet when my testing was concluded.

## Verification with Electrum Watch Wallet

A watch wallet is convenient to have for verifying addresses on a wallet, as well as reviewing transactions over time.  For the aforementioned example, the following public keys are used for this wallet which you can use to test this on your own. 

These public keys were derived by using both Caravan and Electrum in prior sections

`xpub6FBFAVmiF1pgCYanH9GdbgHbiLkHSUq9c5KkY6c7mEk4o8757p8JsrdXo3zsy3uifqGEsBkp45C4jFYPM1X7k3bgsRmijrjz5edaFsxdodA`

`xpub6EkQHCE3w9F6qyCAZxW5vh87b969wiKUaB6NnYcjcsuLzPeEckNSffjHPFhP2hKM6jeAtRdoRiPGBJ3F72t6n4psx4gvEyhPsRitDo7yKkj`

`xpub6EDykLBC5ERX7WREobYaca2ALTFZKLku9RDuPCi2MKf4YbnA4pGF7zVzRqGjrdJK33aeJ2K6qr2qfrz64EikAyEkpbdkmoedFC16smSacJB`

Create new multi-signature wallet

![image](https://user-images.githubusercontent.com/88121568/221362977-f17dd560-cb25-4220-aa65-79f76a0dea73.png)

Specify 2 signatures required, of 3 cosigners

![image](https://user-images.githubusercontent.com/88121568/221362995-0faf3000-5bed-4f7f-875f-b5fc778b24de.png)

Specify the master key for cosigner 1

![image](https://user-images.githubusercontent.com/88121568/221363006-1163532d-3218-42b9-b95b-04cd085d74f5.png)

![image](https://user-images.githubusercontent.com/88121568/221363011-2333dc0a-41f3-4730-888f-26af5db31189.png)

It will display it back to you

![image](https://user-images.githubusercontent.com/88121568/221363027-902bbdf1-90ef-4b2f-8214-8221932df7b5.png)

For cosigner 2 and 3, repeat the process with those keys

![image](https://user-images.githubusercontent.com/88121568/221363051-4e5aab71-8e86-433d-b282-3a9b34ff3d30.png)

Optionally specify a password

![image](https://user-images.githubusercontent.com/88121568/221363062-41e2b35c-7e78-4a8f-9aec-148ca0c9447d.png)

When this wallet loads, it will display its history as follows

![image](https://user-images.githubusercontent.com/88121568/221363069-83454b09-b561-4d16-8187-403d540faf4e.png)

If the Addresses tab is not displayed, from the menubar, select View, and then Show Addresses.  Switch to the Addresses tab. The address in index 2 is the one used for the Key Replacement process previously

![image](https://user-images.githubusercontent.com/88121568/221363090-241728c9-5b74-40ed-85ef-43e01eeca17c.png)

## Conclusion

Determining the intended key information for a wallet is essential to ascertaining whether you have access to an address when sweeping funds during a key replacement process in Unchained Capital.

Both Caravan and Electrum are useful wallet facilitators to be able to see addresses associated with a Multi-signature wallet.

When sending funds between wallets, Don’t Trust. Verify.
