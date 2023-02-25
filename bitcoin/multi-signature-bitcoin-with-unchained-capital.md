# Multi-signature Bitcoin with Unchained Capital
_Don’t Trust. Verify. Service Capabilities and Caveats._

by @vicariousdrama
644428 - 648834

## Introduction

Unchained Capital describes itself as a bitcoin native financial services company offering collaborative custody multisignature vaults and loans for bitcoin holders.

I wanted to take a look at the vault offerings by Unchained Capital for their multisig 2-of-3 options and compare to that of Casa which I reviewed previously.

Unchained Capital has a [YouTube channel](https://www.youtube.com/channel/UCTkCLH1VSjWakXyF6z-mjtA) where they cover some of the capabilities of their service from a marketing and user perspective. This article covers how I verify capabilities from user land as any third party custodial offer implies a certain degree of trust. 

Within, you’ll see ✔️ indicators for a feature that was verified, and ⚠️ to alert you to aspects you should be aware of should you choose to use Unchained Capital.  Occasionally you may see the ⬜ indicator which indicates a feature that should be available, but I did not verify as I lack sufficient testing hardware to do so.

## Change History

| Date | Description |
| --- | --- |
| 2020-09-19 | Initial Document |
| 2023-02-19 | Reformatted, updated toc, added footer |
| 2023-02-25 | Conversion to Markdown |

## The Test Bed

For this testing, I’ve used only Trezor One and Ledger Nano S.  According to the website, they do not support Coldcard at this time.  Most testing is done through the web browser using Chrome or a Chrome derivative (e.g. Brave).  In some instances I used Electrum and Caravan.  All testing is done on mainnet/production.

## Website Signup and Privacy Concerns

The first thing you’ll be asked to do if you want to sign up for a vault is to create an account whereby you’ll provide 
- A username and a password
- Email address 
- Phone number

The email address should be real as you’ll need it to confirm creation of the account.  Pretty much all actions involving creation or signing a transaction, creating keys or vaults will generate copious amounts of emails for each major event.  Bear this in mind if you don’t want free email providers to be aware of this kind of activity.

✔️ I was able to create an account.

![image](https://user-images.githubusercontent.com/88121568/221363590-293de07e-b4d4-47d4-b385-f0a2825491d2.png)

⚠️ After login, you are presented with the dashboard, where you can choose to Create a new vault.  Upon doing so, you’ll be prompted to complete a basic KYC profile
  - First and Last Name
  - Date of Birth
  - Photo Identification (Drivers License or Passport)
  - Address Information

This is in stark contrast to Casa which does not require KYC and may be a dealbreaker for some users.  Unchained Capital is primarily in the business of making loans and vaults can be thought of as a loss leader side product.

Once you’ve completed your basic profile submission, it will need to be approved.  This process takes time as it is a manual process, and presumably only happens during normal business hours (9am - 5pm US Central Time, Monday - Friday). In my case, this occurred on the same day, about 3 hours after submission.

⚠️ Website calls are made to the following fully qualified domain names
  - my.unchained-capital.com
  - www.google-analytics.com
  - fonts.googleapis.com
  - pi.typekit.net
  - fonts.gstatic.com

⚠️ Common to all multisig providers, Since Unchained Capital needs the xpubs for devices to facilitate creation of transactions and derivation keys, they can see all transactions associated with the wallet(s). 

## Vault Creation

Once logged in and approved, the dashboard gives you options for managing your keys, creating vaults, or loans.  

When you create a vault you first choose the custody model. The website does a good job explaining the two different types available. Client Controlled, which this review focuses on, entails 2 keys held by the user, and the emergency/backup key for cosigning created and held by Unchained Capital.

![image](https://user-images.githubusercontent.com/88121568/221363621-48ceb2d7-9bd9-437c-8277-208daaa4c6a2.png)

The next screen lets you choose default signers, and again, we’ll focus on the Signers being the user, and Backup being Unchained Capital.

An interesting feature of is the ability to establish many vaults, and give them unique names.  Think of this as multiple accounts at traditional financial institutions.  Accept the default name `Vault #1` or specify a custom one and continue

The next step is selection of Keys.  If you previously established keys you can pick them here.  If you don’t yet have one, click the + Pick A Key anyways, and it’ll walk you through the process. 

![image](https://user-images.githubusercontent.com/88121568/221363632-0596deb1-3261-4b39-ab0b-a5d47af0bc51.png)

I added keys for a Trezor One and a Ledger Nano S by connecting them to the computer and walking through the on screen prompts.  Each key can be given a unique name.  In this instance, the Ledger Nano S I named “hollywood”, and the Trezor One I went with “neptune”.  As part of this process you’ll be presented with the xpub key for the device, along with the derivation path.  

Once you choose the keys for the vault you’ll also specify a name for the vault or use the default.  I continued with the default, and my vault was named “Vault #1”.

On the vault screen you’ll see your current balance, the keys used in the multisignature wallet, and have actions for deposit and withdraw, synonymous with receive and send.  Clicking the Deposit button explains that the address will be the same until used, and stored in a 2-of-3 multisignature P2SH address.

### Section Test Results

✔️ The derivation path used for all keys by default is m/45'/0'/0'.<br />
✔️ You can specify a custom derivation path. For example m/45'/0'/1'.<br />
✔️ Setup Key with Ledger Nano S (I used m/45'/0'/0', named hollywood)<br />
✔️ Setup Second Key with same Ledger Nano S (I used m/45'/0'/1', named neptune)<br />
⬜ Setup Key with Ledger Nano X<br />
✔️ Setup Key with Trezor One (I used m/45'/0'/0', named balboa)<br />
⬜ Setup Key with Trezor Model T<br />
✔️ Setup Multisig Wallet (Vault #1) using 2 devices (hollywood and neptune)<br />
✔️ Setup Multisig Wallet (Vault #2) using 1 device but 2 different derivation paths (neptune and balboa)<br />
⚠️ Dependence on third party without dead link or content verification<br />
⚠️ Keys that you create don’t “remember” what type of device they are associated with. This is left up to the user for all future transactions and may result in confusion.<br />

## Verifying Receive Addresses

If continuing from the deposit button in the previous section, you can then show the address and have the option to confirm on a Trezor. 

![image](https://user-images.githubusercontent.com/88121568/221363735-62f1e5a7-500e-4c97-8ba3-d5b0e5a37216.png)

This dialog indicates that you may receive a warning about the selected BIP32 path.  I followed the instructions and the error on my Trezor was as follows:

```
   Wrong address path for selected coin.
       Continue at your own risk!
```

Continuing showed the same address and path with depth of 6.


Another way to view addresses is by choosing Address History from the menu for the Vault. This option lets you see the redeemscript for the address and can use Caravan for verifying ownership of the address.  Caravan is a multisig coordinator.

![image](https://user-images.githubusercontent.com/88121568/221363754-5b6cc2fd-390a-4176-b852-8a3f4beb5db5.png)

From Address History, choose External Spend Info from the actions.  

On the new External Spending Information dialog, click show information to reveal the redeem script and Key BIP32 paths.  Note that the paths are `m/45’/0’/0’/0/0/0`.

![image](https://user-images.githubusercontent.com/88121568/221363758-a78c012c-f0ae-4c60-96bf-d56c7b91c81b.png)

Click the Copy button on the Redeem Script value, and then click Caravan.  Paste the Redeem Script value into the input field.  Immediately it will reveal the same address (`3DyRHVUfCx5v8syqePCT2iwtebVUfgJ11c`), coin (BTC), network (Mainnet), multisig m-of-n (2-of-3), and type (P2SH).

Click the Confirm Ownership button and specify the parameters of the device to check.  For both my Trezor One, and my Ledger Nano S, they are on the same BIP32 Key Path `m/45’/0’/0’/0/0/0`.  I start with the Trezor, and it defaults to a BIP32 Path of `m/45’/0’/0’/0` and the Model T (the second option).  I correct the BIP32 path and choose the ONE.

A successful verification appears as follows

![image](https://user-images.githubusercontent.com/88121568/221363807-179e7fd1-c8c0-4701-b03a-fccecda66f64.png)

A failure to verify will look like this

![image](https://user-images.githubusercontent.com/88121568/221363816-0eda8a82-2289-49ff-8873-b140df04c1c5.png)

The full derivation path for addresses is a depth of 6. According to representatives of Unchained Capital this is segmented as follows:
- Depth 1: 45' - For multisig
- Depth 2: 0' - For mainnet
- Depth 3: 0' - For account 0
- Depth 4: 0 - Product key for a given account key, increments up as it is used in a vault or a loan
- Depth 5: 0 - 0 for deposit address, 1 for change address, which they don’t use yet.  It will always be 0
- Depth 6: 0 - The address which increments up as they use addresses

Another option is to see the external spend info from the menu for Transact.  This option lets you download wallet file for recovery.  Theres a warning about spending funds outside of unchained capital and it not updating automatically.

![image](https://user-images.githubusercontent.com/88121568/221363851-f6127f28-7ef9-4afb-a2b3-5bb993090be1.png)

The exported file is a JSON file and contains the public keys associated with the value, the name associated with each key, and the BIP 32 path for the keys under control of the client.  Of note is that the base bip32Path value isn’t just the derivation path but includes a depth of 4 to include Unchained Capital’s concept of a product key.  This file can be directly imported into Caravan and is easier then copying/pasting and setting the key path.  It’s also what I’d consider a functional backup file that includes everything critical for recovery outside of the private keys.

![image](https://user-images.githubusercontent.com/88121568/221363870-0c034353-b7c6-41df-baba-56b0a7cdd957.png)

The exported file is specific to Caravan and will not work with Electrum.  From the above, the equivalent file structure for Electrum as a watch wallet is as follows

![image](https://user-images.githubusercontent.com/88121568/221363884-c95b82cd-7871-4cf4-b7ad-de96ca6af27a.png)

It is advisable to have multiple methods by which you can verify the receive addresses are calculated.  Hardware wallets are just now adding the ability to do this on the device itself, and until that is the standard procedure, you should compare across multiple sources.

## Sidequest: Quick Overview of Caravan

It’s worth pointing out that Unchained Capital builds their own tool to help with sovereign recovery and understanding multisig wallets in general.  This tool can be used even if you aren’t making use of Unchained Capital’s vaults.

From the caravan tool, you import the file, and specify whether using the public Bitcoin Client or one of your own.  Since I’m testing with a disposable wallet, I chose Public, but I strongly encourage use of this tool both downloaded, and set to communicate with your own private full node.  Once loaded, the wallet will display the addresses as described below.

I sent some funds to the wallet for demonstration purposes.   I am able to see the address that I sent the funds to with a balance along with the date funds were sent.   

![image](https://user-images.githubusercontent.com/88121568/221363921-db08e717-97da-4a34-8342-dcd4107654bc.png)

The Receive tab sets up to advance to the next unused address with a QR code matching the address depicted. 

![image](https://user-images.githubusercontent.com/88121568/221363924-024656a8-8355-4626-bd1c-6c2be9bef8ea.png)

A full review of Caravan is outside the scope of this article but in general, it is a suitable tool for recovery discussed in a later section.

## Setting up a Watch Wallet with Electrum

I currently prefer Electrum, but have been looking into Sparrow. In any event, I want to ensure that I can setup transactions using my external software of choice rather then being constrained to Unchained Capital’s interface as implied by the website.

I took the existing exported file from Unchained Capital for the vault and manually converted to Electrum format.  This will let me sign with my hardware devices.  If I just specified the xpub keys during wallet creation, it would be a typical watch wallet without the ability to spend.

![image](https://user-images.githubusercontent.com/88121568/221364187-9878b578-2e5a-4af9-bf6f-db6c9252bf23.png)

After setting up a wallet in Electrum, I tested sweeping funds from address 1 to address 2, with no change output.  Based upon the website and staff of Unchained Capital, I’m of the impression that they don’t currently support change addresses.  As a result, I’ve restricted all tests from moving from one address, to the next address available.

Prepared and signed a transaction using the Ledger Nano S and Trezor One.

![image](https://user-images.githubusercontent.com/88121568/221364200-bf4426cb-b361-45c4-9623-c3004677bd90.png)

My address list, after the transaction to move from address 0 to address 1

![image](https://user-images.githubusercontent.com/88121568/221364203-d914bbf0-d4ed-4012-a6fc-a0ebfc208157.png)

There is a caveat to using external software however. The transaction is confirmed as shown here:

![image](https://user-images.githubusercontent.com/88121568/221364216-c3a3433e-f945-472b-953c-bc9e9a744c99.png)

The Vault in Unchained Capital doesn’t see this change, and instead reflects that address 0 has a 0 balance, and will want you to use that for Deposits and disallow withdraws or transfers.  

![image](https://user-images.githubusercontent.com/88121568/221364223-2e9b1614-9404-490c-bf88-f4d8bd3d1542.png)

To mitigate this without involving Unchained Capital, I’ll sweep all the funds back to address 0.

![image](https://user-images.githubusercontent.com/88121568/221364226-7c933c8c-5420-4b06-8ade-9d363343f155.png)

### Section Test Results

✔️ Can verify Ledger Nano S (hollywood) has ownership to address<br />
✔️ Can verify Trezor One (neptune) has ownership to address<br />
⚠️ Default BIP32 path in Caravan doesn’t match Unchained Capital default scheme<br />
⚠️ Full Derivation path has a depth of 6 which is nonstandard.<br />
✔️ Premade Backup File with important details to recover wallet<br />
✔️ Wallet file is compatible with Unchained Capital’s Caravan product<br />
⚠️ Wallet file can not be directly imported into Electrum (but easy to convert)<br />
✔️ Can setup, sign, and send transactions using Electrum<br />
⚠️ Unchained Capital doesn’t automatically see transactions it didn’t broadcast <br />
⚠️ Unchained Capital will recommend reuse of the same address in this scenario for deposits<br />
⚠️ Unchained Capital effectively has a gap limit of 0 and only appears to monitor the current deposit address, while skipping already used addresses<br />

Primarily, the benefit of Electrum is to support sweeping funds for sovereign recovery, and as another method of verifying receive addresses that should belong to the multisig wallet.

## Signing Transactions

Using the web interface for Unchained Capital, I want to verify that I can prepare transactions, sign them using the keys associated with the vault, and send them.  I will test sending transactions that are both to the same vault, and to an external wallet.  In addition, I will check for UTXO management

### 0. External Spends

As indicated in the section for Watch Wallet with Electrum, address 0 was funded with a deposit, and then Electrum was used to spend those funds to address 1.  Once it was discovered that the Vault shows a zero balance because it didn’t initiate the transfer, the funds were swept from address 1 back to address 0 using Electrum.

### 1. From Vault 1 - Transaction 1

__Send funds to an address in wallet, skipping to address 2__

For the first transaction, I’ll send to an address within the wallet at `*/0/2`.  This is `322Md2zMv1sUbXJEesznKVVTb8fFWGtC6q`.  I’ll send 500,000 sats (.005 BTC) with a fee rate of 5 sat/byte.  This should result in two UTXOs.

![image](https://user-images.githubusercontent.com/88121568/221364384-57794430-0ed0-4d75-adca-61280c8cd41a.png)

On the next screen you can decide which keys will be used for signing.  This defaults to that which you chose during vault setup. In my case, this is my 2 hardware keys.

![image](https://user-images.githubusercontent.com/88121568/221364392-eb7fcff6-1ba0-45c2-8802-d38e78d73e1e.png)

A summary is depicted when going to the next screen.  And this is the last point where you can go back and change parameters of the transaction.  As with all multisig setups, the fees can change from start to finish of signing and this can influence when the final signed transaction will be accepted into a block

![image](https://user-images.githubusercontent.com/88121568/221364400-3d12516b-1912-4282-bc0f-c7486736ad74.png)

It’s here that I found an interesting bug. Because I had previously used Electrum to try sending funds from address 0 to address 1, and back to address 0, the Withdrawal screen below shows the wrong amounts for the Change Address (0.01219746), and the Total Outputs (0.01720871).  This should be sending 0.00358463 to the change address, which is really address 1 under the account.

![image](https://user-images.githubusercontent.com/88121568/221364408-86060a5f-1597-4592-b444-c6fb35c940f1.png)

The Ledger Nano S (hollywood) was able to sign the transaction, and displayed the correct amounts (not those depicted above).  However, it wasn’t able to display the fees, instead displaying UNKNOWN

The Trezor One (neptune) through use of connect.trezor.io facilitating, was able to show the recipient address and amount, change address and amount, and the fees.

After both keys sign, the withdraw screen looks like the following and is ready for broadcast.

![image](https://user-images.githubusercontent.com/88121568/221364415-596a4402-a51e-4947-9e40-8c1e9e7edfc6.png)

After clicking Broadcast, the transaction id is rendered.

![image](https://user-images.githubusercontent.com/88121568/221364425-0d062e1c-ef4f-4a4e-89da-1b73f9d946c2.png)

While the transaction is pending, the main screen of the vault reflects the withdrawal

![image](https://user-images.githubusercontent.com/88121568/221364433-2b62a878-fdd4-4fa2-815c-c8084e8ef4d1.png)

A watch wallet in Electrum (discussed in a later section) shows the following for the addresses involved. The amounts are depicted in sats.

![image](https://user-images.githubusercontent.com/88121568/221364485-d8303677-87b8-4375-8b2a-e4e3d41600ce.png)

Once the confirmation occurs, Unchained Capital updates the vault balance as shown here.  Note that it is only showing the balance of address 1 (the second for the wallet) even though there is funds in the address following it.

![image](https://user-images.githubusercontent.com/88121568/221364491-eec7f160-a875-488e-84ca-748929cf356c.png)

### 2. From Vault 1 - Transaction 2
__Send funds to an address in another vault__

For the next transaction, .003 BTC (300000 sats) will be transferred to Vault 2.  The first address there is 3Nz4o8Cmb8myiozigGotWN8roacu8X9EiJ.  This can be done from Vault #1 by either choosing Withdraw and specifying the address manually, or by choosing the Transfer option, of which the web interface will automatically determine it.

![image](https://user-images.githubusercontent.com/88121568/221364505-23f1b4f5-6454-4724-81da-539e011debe8.png)

![image](https://user-images.githubusercontent.com/88121568/221364516-82c93df0-4a0a-4d06-9d53-8fcc3fd321b0.png)

Something important to note here is that the change address for this transaction from Vault #1 will result in the remainder being put into address position 3 `3DANQTmvr82LbtJMypJh7MMPY5LhUuhEXV` which skips the address position 2 which currently has funds that Unchained Capital doesn’t show.  This implies that Unchained Capital sees the address as already being used, and is skipping over it.  The total balance should be 57338 sats + 500000 sats for .00557338 BTC total.

![image](https://user-images.githubusercontent.com/88121568/221364541-93794f86-9171-4289-a03a-6c9a734e070c.png)

If you leave a transaction screen, the transaction is still pending and you can get back to it.  Here is what the vault screen looks like with no signatures yet. The Transact block shows Waiting for Signatures and I can view the transaction.  I cannot initiate further transactions at the same time.

![image](https://user-images.githubusercontent.com/88121568/221364544-df55ad82-aaac-4a06-8e6f-adeae9ce8975.png)

Viewing the transaction and starting the signing process. I’ve signed with the Trezor (neptune) and now need to sign with my Ledger Nano (hollywood).
 
![image](https://user-images.githubusercontent.com/88121568/221364565-8e77ee90-5381-4dd0-9c71-6a67930392d8.png)

Back on the main vault screen, the transact section updates to denote that it is waiting for second signature.

![image](https://user-images.githubusercontent.com/88121568/221364578-97ea7351-77d4-4c16-8980-1bae0d39c4dc.png)

I go through the steps with the Ledger Nano, and sure enough, it still shows fees as UNKNOWN.  

I finish signing and broadcast the transaction. The transaction ID given is `a8a4eb8ec426eb7d34a245067fd77bbc1b5cd3117319abf45609d5a74f1d2898`

![image](https://user-images.githubusercontent.com/88121568/221364583-32215f70-81e4-4b43-88d8-93a8b3994efb.png)

And the main screen for the vault now reflects the updated transaction history, pending the transfer

![image](https://user-images.githubusercontent.com/88121568/221364593-a3d52c66-eeb0-48cb-b7e5-0e89e041efb7.png)

Overall current balance showed as a mere .00057338 BTC, as it skipped over the 500000 sats previously sent.

![image](https://user-images.githubusercontent.com/88121568/221364595-c417ffe2-a9e4-4aea-a5ec-a00e96f216a9.png)

### 3. From Vault 1 - Transaction 3

__Reorganize account funds in the Vault using Electrum to Fix Vault Balance__

Due to previous transactions, address 2 containing funds previously sent during Transaction 1 was skipped when funds were sent with Transaction 2. To clean this up, I used external wallet software, Electrum, to spend from `322Md2zMv1sUbXJEesznKVVTb8fFWGtC6q` and send to address `3DANQTmvr82LbtJMypJh7MMPY5LhUuhEXV` currently recognized for deposit.   Paying fees of 3 sats per byte (1017), this should result in a new balance of .00556321

### 4. From Vault 2 - Transaction 1

__Spend some funds to an external address__

From Vault #2 I initiated a withdraw in the amount of .002 BTC to address `bc1qfqjlxwug25kdkylx5ehrq87rzm0jarwqzfs08n` with Fee Rate of 3 sat/byte.  Signed with the Ledger for Keys balboa and hollywood.  Transaction ID `5684178fc2ce7a115eb6ebb0dd4b743096188a20cc28bdbbcdb5dd5c6394c9b8`.  I was able to confirm that the funds were sent to the external address.

### Section Test Results

✔️ Send dialog permits nearly full control over the fee rate<br />
✔️ Able to prepare transaction, sign, and send funds to another address<br />
⚠️ Fee rate must be greater than 0 and less than 1000 sats per byte.<br />
⚠️ Send dialog link for Fee Estimator goes to [bitcoinfees.earn.com](https://bitcoinfees.earn.com), an external website, that does not consider recent blocks, but days as a whole.<br /> 
⚠️ Send dialog has no way to specify amount in satoshis.  Recall sats are at 8th decimal place<br />
⚠️ Send dialog permits an amount with more than 8 decimal places but does validate before allowing you to move next<br />
⚠️ Unchained Capital doesn’t monitor more than the current address<br />
⚠️ Wallet will only reflect balance based on the current address<br />
⚠️ No UTXO management when there are multiple addresses with a balance<br />
⚠️ Links for reviewing transactions are all external to [blockstream.info](https://blockstream.info) with no ability to define your own node<br />
⚠️ All transactions prepared through the web interface are broadcast through Unchained Capital servers, with no ability to define your own node<br />
⚠️ Transaction ID is not revealed until after broadcast<br />
⚠️ Vault will skip addresses that have a transaction associated but wont include in overall balance<br />
⚠️ Must wait until a transaction is confirmed before beginning another transaction in a vault.  This can be problematic if a low fee transaction is never included in a block. To resolve, do RBF using external wallet software.<br />
⚠️ Vaults with pending deposit transactions cannot send (withdraw or transfer) funds until the pending deposit is completed. This is a possible denial of service attack vector.<br />

## Key Replacement

This is being verified without Unchained Capital intervention. I will mark one of the keys as compromised. For simplicity, Vault #2 currently uses `balboa` and `hollywood`, and I will mark `balboa` as compromised, or to be replaced.  

The list of replacement keys available to me are the other keys.  The default appears to be alphabetically sorted, showing `hollywood` as the selected choice.  I will toggle the selector to indicate that I am still able to sign transactions using this key.

![image](https://user-images.githubusercontent.com/88121568/221364719-cf375a4c-5568-4b24-ad35-de1dc158d335.png)

When clicking Replace Key, I confirm the action and then am met with a warning that the `hollywood` key already protects the vault.  Ideally this key would not be listed in the drop down. 

As such, I decide to once again upload a new replacement key. The name is `crater`, and I set it to the BIP32 Path `m/45'/0'/2'`.  Upon doing so I start the process to replace the `balboa` key all over again.  This time, the list of keys is `hollywood`, `crater`, `neptune`.  Clearly it’s not alphabetical order, and it turns out that keys are sorted by the option value as the key identifier.  For someone that maintains a very large quantity of keys, this could be a nuisance to locate within the list.

I choose `crater`, and click Replace Key. I confirm the action and am met with a new error as shown below.

![image](https://user-images.githubusercontent.com/88121568/221364772-1df0bbba-c450-41df-9583-7a8f2bf85b93.png)

Apparently, I must wait for the current transaction to be confirmed, to settle the vault state, before I can replace a key on it.  I allowed that transaction to settle and repeated the process to get to this landing screen

![image](https://user-images.githubusercontent.com/88121568/221364780-25a2e6d2-2ca6-4ec8-83a5-73b3adc56ac7.png)

There isn’t explicit guidance on what the next step is, but the transaction is started and can be seen back on the main screen for the vault

![image](https://user-images.githubusercontent.com/88121568/221364787-63ee5c02-ce89-4bc0-a7ab-eaf6696ea9a0.png)

For the sweep transaction, it sets up the order of key signing as the remaining key `hollywood`, then unchained, with `balboa` still selectable.  

![image](https://user-images.githubusercontent.com/88121568/221364795-fc2b1e57-008c-4a72-9d4f-81e0d70bc42c.png)

The external address `31w1VhPmSvoCqQJ227aG83prWyQcDKbjiC` is not able to be verified directly in the Unchained Capital interface. This is because external spending information on the Vault page still reflects the current keys where one (`balboa`) is being replaced.  

While its not documented, it is possible to confirm the addresses by
- Manually retrieve the xpub for the remaining key (`hollywood`) with its derived path `m/45'/0'/0'/1`
- Manually retrieve the xpub for the new key (`crater`) with the derived path `m/45'/0'/2'/0`
- Use the same xpub that unchained associated with the vault previously: `xpub6EDykLBC5ERX7WREobYaca2ALTFZKLku9RDuPCi2MKf4YbnA4pGF7zVzRqGjrdJK33aeJ2K6qr2qfrz64EikAyEkpbdkmoedFC16smSacJB`
Setup as a legacy P2SH 2of3 multisig wallet in Electrum. For Caravan, be certain that the unchained xpub is entered as text and remains the same on confirmation screen. I was able to confirm that the address is at index 2.

The fees of 20801 sats were set by Unchained Capital during this process and I had no control over it.  Given that its about 20x what I’ve been paying in fees for most other transactions, I can estimate that its around 60 sats/byte, with an intent to settle quickly.  A quick glance at [Mempool.space](https://mempool.space) shows that I’m drastically overpaying:

![image](https://user-images.githubusercontent.com/88121568/221364875-bee45603-49e9-4942-8df4-11fcdf452c8e.png)

After signing with `hollywood` and `balboa`, I broadcast the transaction.

![image](https://user-images.githubusercontent.com/88121568/221364907-df067d87-7ccc-4acf-bf9b-7357e58a6c4e.png)

While waiting for the transaction to confirm

![image](https://user-images.githubusercontent.com/88121568/221364916-efe5e8cb-a623-45b4-bead-511fddfe12e8.png)

Once confirmed, the xpubs visible, and starting address indicated.

![image](https://user-images.githubusercontent.com/88121568/221364925-d14748f1-53b9-4f31-9624-0b18f7dc20ca.png)

### Section Test Results
✔️ Able to create a new replacement key<br />
✔️ Able to mark a key as lost or compromised needing replaced<br />
✔️ Steps to walk through transaction work to reuse remaining key parts.<br />
⚠️ Fees for moving funds to new key set cant be set<br />
⚠️ No clear way to verify address that funds will be sent to<br />
✔️ Able to replace a key with a new key on a vault.<br />
✔️ Unchained Capital facilitates the key rotation incrementing the “account” or 4th of 6 position in the derivation path automatically<br />
⚠️ List of replacement keys includes keys that cannot be used for replacement.<br />
⚠️ List of replacement keys is not sorted by name or creation date.<br />
⚠️ Unable to replace a key while the vault has an unconfirmed transaction.  This is a mixed result, but could result in denial of service on pending inbound transactions<br />
⚠️ Unable to spend funds while the vault is being swept from key replacement.<br />
⚠️ Unable to control fees when replacing a key.<br />
⚠️ Unable to easily verify ownership of address that funds are being swept to but have derived it for how to do with Electrum and Caravan<br />

## Creating Keys on Existing Paths

To summarize, at this point I have created the following keys

![image](https://user-images.githubusercontent.com/88121568/221364971-a3657e2f-2ab6-4b30-adc1-385ffcccd583.png)

Attempting to create a new key on a currently active derivation path for a device initially appears to succeed.  I created a key named `wooster` on the `m/45'/0'/0'` path alongside `hollywood`.  At the final Review Key stage, it denotes the key is already in use

![image](https://user-images.githubusercontent.com/88121568/221364987-eddb9cfe-e150-4aa2-82f1-a195996d3d10.png)

The same occurs when I use `m/45'/0'/1'` for the replaced `balboa` key.

### Section Test Results

✔️ Prevented from re-creating the same key for a key actively in use<br />
✔️ Prevented from re-creating the same key for a key marked as compromised<br />


## Performing Health checks

Periodic health checks are a good way to verify everything is good. Just like regular dental, medical and vision checks, you should check that your hardware wallets are functioning as intended.  

Health checks on keys is super easy. Simply navigate to the Key to be checked, and click Check Now

![image](https://user-images.githubusercontent.com/88121568/221365019-f5fb6625-2679-4dae-afde-32e97a1e0572.png)

Follow the on screen prompts.  Assuming all checks out, it’ll show as follows

![image](https://user-images.githubusercontent.com/88121568/221365022-15d9e9bb-f6da-4805-a7b0-f95a2882ef18.png)

Here’s an example if the key check fails.  I tried the neptune key with my Ledger Nano S instead of the Trezor One it belonged to.

![image](https://user-images.githubusercontent.com/88121568/221365037-e92a08c4-a18b-4a10-8546-7108ad3b1637.png)

### Section Test Results

✔️ Able to perform a Key Health Check<br />
✔️ Verified website shows when a health check was last performed<br />
✔️ Verified that health check on incorrect device does not trigger success.<br />

## Signing Transactions with Unchained Key

Unchained Capital performs key signing once a day, around 11 AM Monday-Friday during normal business operating days.

Prior to continuing, I perform a transaction to sweep all remaining funds back from Vault #2 to Vault #1. Details of the transaction are shown here, but note that the referenced Change Address (which is valid) has 0 sent to it.

![image](https://user-images.githubusercontent.com/88121568/221365071-16b92bd9-2c21-4273-8f9a-054ab4b0c49c.png)

While waiting for this transfer from Vault #2, Vault #1 is also effectively frozen, disallowing any transactions other than deposits.

Once complete, Vault #2 has a 0 balance, and Vault #1 has a balance of .00633372. 

I will now initiate a transaction to send part of the funds to an external address with intent to use unchained as a signer. 

![image](https://user-images.githubusercontent.com/88121568/221365087-0d0e3fd9-8f10-4388-9bd9-e5d4e7b0e9e8.png)

On the next screen I deselect `hollywood` key as a signer, and choose `Unchained` in its place to sign along with `neptune`.

![image](https://user-images.githubusercontent.com/88121568/221365094-2b9009c3-d4c8-4cc1-91fb-54caee764f21.png)

I choose to Create withdrawal and am then redirected to the Withdrawal transaction signing. After signing with my Trezor for the `neptune key`, the status is Waiting for Signature for Unchained.  I don’t have a video verification on file.

![image](https://user-images.githubusercontent.com/88121568/221365097-d0dc8b9a-68ff-4a7e-b112-59e65044249c.png)

![image](https://user-images.githubusercontent.com/88121568/221365124-61ace00a-bedf-49e4-9462-b1ef864ad564.png)

It’s my understanding that anytime Unchained acts as a signer, that they charge a fee for the service in the amount of $20 for individuals.  This was denoted on their primary webpage for vaults but isn’t relayed in the transaction screens.

![image](https://user-images.githubusercontent.com/88121568/221365131-231737d8-aac6-4965-a000-6a25e446749f.png)

I will need to check back in a few hours to see if the transaction was signed or if its awaiting payment.

I received an email at 16:50 UTC that the Spend was fully signed and that I can now broadcast the spend.  Logging in and checking on the Vault I see the status waiting for the transaction to be broadcast. Nothing on this screen or those following infer that I owe a payment to Unchained for their performing the signing.

![image](https://user-images.githubusercontent.com/88121568/221365133-f3710351-3733-4583-830a-919abd02284f.png)

And details for the transaction show that it’s been signed by Unchained

![image](https://user-images.githubusercontent.com/88121568/221365142-a48644b1-f950-4a5a-b05d-5eded89cd037.png)

I continue with the Broadcast of the message and get the success screen.  Now the transaction is pending confirmation.

![image](https://user-images.githubusercontent.com/88121568/221365147-02b51491-fb7c-40c6-ad1c-71aa846779d5.png)

After some time, the transaction gets confirmed in a block. 

### Section Test Results

✔️ Able to setup a transaction that requests signing by Unchained<br />
✔️ Able to control amount and fees of transaction being setup<br />
✔️ Verified that Unchained signed the transaction<br />
✔️ Able to control broadcast of signed transaction<br />
⚠️ Not certain whether I owe Unchained $20 for signing the transaction and how that would be paid. Not integrated in web application.<br />

## Managing Vaults

Unchained Capital lets you have as many vaults as you want. Over time you may no longer have need of a vault.  There is an action on the Vault screen that allows you to close it when you no longer need it.

At this point in testing, Vault #2 has a zero balance, no pending transactions, and I don’t have any further need for it.

![image](https://user-images.githubusercontent.com/88121568/221365178-ee3f7bd6-b0d3-466a-bdd6-c658ab2619f8.png)

Upon clicking the Close menu option, you’ll be prompted to confirm this action

![image](https://user-images.githubusercontent.com/88121568/221365183-070e5c54-ba9c-41c8-8bc6-3500254bb71e.png)

If the vault has a balance, you’ll be prompted to withdraw or transfer that balance

![image](https://user-images.githubusercontent.com/88121568/221365187-e74f8cb9-21af-43f8-8a6d-92e6f4fde5ee.png)

After proceeding with closing the vault, a success dialog is temporarily displayed before returning to the vault list and revealing the vault as closed.  Apparently it stays in the list indefinitely? 

![image](https://user-images.githubusercontent.com/88121568/221365193-e9c4558d-48fe-494e-97ca-f9264cd7e487.png)

The details of the vault can be seen. While it indicates that the vault is closed and all funds withdrawn, you can view details about transactions, address history and a new feature `Monthly Statements`.

![image](https://user-images.githubusercontent.com/88121568/221365203-3290a52d-6429-40ea-87a3-d5977e3b5cff.png)

If you choose `Monthly Statements` you’ll be prompted to select the month, and from there a PDF is generated enumerating the transactions for deposits and withdraws and summarizing the beginning and ending balance along with miner fees.  I checked with Unchained Capital on this and Phil Geiger indicated that they are generated at the end of the month.

The vault can still be renamed, however I couldn’t use this to influence its position in the list of vaults. Whether prefixed with ZZZ or AAA, the vault shows in the second position, either due to when it was created, or possibly from sorting by the Vault identity or the keys used.  I created two more vaults to show this influences the list. 

![image](https://user-images.githubusercontent.com/88121568/221365212-6fabe2c6-713d-41c8-88e0-ed6c22488054.png)

The column headers can be used to sort the vaults, which by default seem to possibly be by creation date, then generated vault identity.  

### Section Test Results

✔️ Able to mark a vault as closed.<br />
✔️ A closed vault cannot be reopened.<br />
✔️ Verified that Unchained doesn’t permit initiating new transactions from a closed vault.<br />
✔️ A closed vault can be renamed<br />
✔️ According to Unchained Capital, you can have an unlimited number of vaults<br />
⚠️ Closed vaults remain in the list of vaults.<br />

## Trust Minimized External Recovery

For any managed or collaborative custody multisignature solution, the ability to spend funds without needing the service provider to exist is paramount.  In the event that Unchained Capital went out of business and no longer operated for any reason, you want to ensure that you still have access to your funds.  Here is the relevant section from the [FAQ page](https://unchained-capital.com/faq/) 

![image](https://user-images.githubusercontent.com/88121568/221365228-67204cdb-bdb6-44d6-b08b-6a557b51c016.png)

I actually tested this at the outset when setting up a watch wallet in Electrum, but I’ll recover the important bits in this section using Caravan.

From within any Vault you have setup, in the `Transact` section, click the three dots to bring up the context menu.  Choose `External Spend Info`.

![image](https://user-images.githubusercontent.com/88121568/221365242-05b30006-91a3-41e0-ab63-d0c6b58bc1e0.png)

On the dialog that appears titled `External Spending Information`, a brief synopsis of Caravan is given along with options to `Download` the configuration file or to `Show Information`

![image](https://user-images.githubusercontent.com/88121568/221365276-420efbec-7634-42c8-b21d-5c54cfc1df48.png)

If you click Show Information, then the details about each key name, derivation path, and associated xpub value are displayed along with the address type,  multisig quorum, and starting address.

It’s important to note that whether using this information in another wallet such as Electrum or Sparrow, or if using Caravan, you always need to keep track of which hardware device and type is associated with a key by name.  This isn’t maintained by Unchained Capital, which is why you are always prompted for it when signing transactions.

I choose to download the file as I will use it with Caravan.  I save the file and then click the link for Caravan.  This is running directly off of github at [https://unchained-capital.github.io/caravan/#/wallet](https://unchained-capital.github.io/caravan/#/wallet) 

![image](https://user-images.githubusercontent.com/88121568/221365297-0438ae7f-0485-46a2-987d-d914560f0a0b.png)

After importing my wallet configuration file, I see the details for each key name, path and extended public key.

![image](https://user-images.githubusercontent.com/88121568/221365302-6aba1042-b214-44df-86e4-a1adb5769763.png)

For Bitcoin Client, choosing Public will cause the tool to send requests to blockstream.info.  You should choose Public with a proxied bitcoin node you control if you want to improve privacy.

After continuing, I’m able to see my balance in the vault, and the addresses.  Toggling to show `Spent Addresses` reveals the previously used addresses. 

![image](https://user-images.githubusercontent.com/88121568/221365312-f0612729-3665-4c3d-8ee0-7b38108f15e6.png)

For this trust minimized external recovery, I will want to ensure that I am able to send funds using this tool just as I’ve done with Electrum.  

On the `Send` tab, I specify an address, set fee rate to 3 sats/byte, and then click MAX for the amount.

![image](https://user-images.githubusercontent.com/88121568/221365324-db8d8f42-d5a7-4371-b97a-22efb11b2414.png)

The transaction preview screen shows the details and allows me to go back to edit or begin the signing process

![image](https://user-images.githubusercontent.com/88121568/221365337-2af7c1cf-2436-4885-b60a-97224a11bd5e.png)

On the Sign Transaction screen, you choose which keys to sign with and have the option to see the raw transaction by clicking `Show Unsigned Transaction`.  This can easily be copy and pasted and checked against a bitcoin node at the command line

![image](https://user-images.githubusercontent.com/88121568/221365342-de34d34f-efcd-4f39-a150-a730c52bfd29.png)

Taking that hexadecimal format of the transaction, I can check it against a bitcoin node as another means to verify the tool isn’t using different addresses while managing the transaction.

```shell
bitcoin-cli decoderawtransaction "0100000001ec95c88d41e5dc6fa891ed1a292c1b41dc069588636e5d46279d5e050c29cfe00100000000ffffffff0169810400000000001600145487d30833cd52e19cb15e6a4c8ac373a815b2b900000000"
{
  "txid": "79d0a8bb038e690ed49662f94dc4d8917aae6481468d8c9521ecd40a2cb31d61",
  "hash": "79d0a8bb038e690ed49662f94dc4d8917aae6481468d8c9521ecd40a2cb31d61",
  "version": 1,
  "size": 82,
  "vsize": 82,
  "weight": 328,
  "locktime": 0,
  "vin": [
    {
      "txid": "e0cf290c055e9d27465d6e63889506dc411b2c291aed91a86fdce5418dc895ec",
      "vout": 1,
      "scriptSig": {
        "asm": "",
        "hex": ""
      },
      "sequence": 4294967295
    }
  ],
  "vout": [
    {
      "value": 0.00295273,
      "n": 0,
      "scriptPubKey": {
        "asm": "0 5487d30833cd52e19cb15e6a4c8ac373a815b2b9",
        "hex": "00145487d30833cd52e19cb15e6a4c8ac373a815b2b9",
        "reqSigs": 1,
        "type": "witness_v0_keyhash",
        "addresses": [
          "bc1q2jraxzpne4fwr893te4yezkrww5ptv4erhp7e8"
        ]
      }
    }
  ]
}
```

To proceed with signing, the first key I sign is with `neptune`, which is a Trezor Model One.  Upon clicking the `Sign` button, I get redirected as usual to the connect.trezor.io website which facilitates the signing

![image](https://user-images.githubusercontent.com/88121568/221365375-dd3813aa-1e07-4559-9df8-6c2dea754c3b.png)

Once signed, the signature block is replaced with the signature that was imported

![image](https://user-images.githubusercontent.com/88121568/221365387-c9ab90d4-55d8-4813-b6f2-0b63734ad076.png)

I repeat the process for Signature 2 using my `hollywood` key on a Ledger Nano and click `Sign`

![image](https://user-images.githubusercontent.com/88121568/221365397-ab6f3983-ffd9-4628-abd8-764498627ba6.png)

The Caravan application provides additional guidance for the Ledger

![image](https://user-images.githubusercontent.com/88121568/221365401-8d8ac663-eebd-4605-8fcf-321196fd57f8.png)

After confirming on my Ledger, with 2 signatures of the 3 required meeting quorum, the Signed Transaction is shown on Caravan ready to broadcast

![image](https://user-images.githubusercontent.com/88121568/221365410-20b55128-a823-4a5d-827c-4cd0c251031b.png)

Once again, I copy the signed transaction hex and verify it with a bitcoin node

```shell
bitcoin-cli decoderawtransaction '0100000001ec95c88d41e5dc6fa891ed1a292c1b41dc069588636e5d46279d5e050c29cfe001000000fdfd00004730440220310cb2980c64b7a7d02d0a416bcda74b1c9e55401908ac67cd9066ab2e0b15b4022036b9ce12a2efe441d0af7873813a34badec430293329640ce359eac4303d233d01483045022100e21797339488e924d03fd2999bed5c3e31ec6f418a14859f5105a57289ae448102205d6cc82821c278fd058ceaa9c8123464d7de2a0d317462df475796a2077f17c8014c69522102863f8bc6dfb0ba57d0c756c61bfae5a6f919d2c1439b161e0614340253f545d32102a7e26aba061d0e186a560429833ce88c18b1951cbc02f2fb0cde669959fb7f8f2102fda5d852af846bfe82994d60e4ef9c2bc72fc79bcd9e4d050e9fb2d443bd484653aeffffffff0169810400000000001600145487d30833cd52e19cb15e6a4c8ac373a815b2b900000000'

{
  "txid": "fad600626522554640e57d00ab212f3666fd657aa945a2297fa5219eacb1bc5f",
  "hash": "fad600626522554640e57d00ab212f3666fd657aa945a2297fa5219eacb1bc5f",
  "version": 1,
  "size": 337,
  "vsize": 337,
  "weight": 1348,
  "locktime": 0,
  "vin": [
    {
      "txid": "e0cf290c055e9d27465d6e63889506dc411b2c291aed91a86fdce5418dc895ec",
      "vout": 1,
      "scriptSig": {
        "asm": "0 30440220310cb2980c64b7a7d02d0a416bcda74b1c9e55401908ac67cd9066ab2e0b15b4022036b9ce12a2efe441d0af7873813a34badec430293329640ce359eac4303d233d[ALL] 3045022100e21797339488e924d03fd2999bed5c3e31ec6f418a14859f5105a57289ae448102205d6cc82821c278fd058ceaa9c8123464d7de2a0d317462df475796a2077f17c8[ALL] 522102863f8bc6dfb0ba57d0c756c61bfae5a6f919d2c1439b161e0614340253f545d32102a7e26aba061d0e186a560429833ce88c18b1951cbc02f2fb0cde669959fb7f8f2102fda5d852af846bfe82994d60e4ef9c2bc72fc79bcd9e4d050e9fb2d443bd484653ae",
        "hex": "004730440220310cb2980c64b7a7d02d0a416bcda74b1c9e55401908ac67cd9066ab2e0b15b4022036b9ce12a2efe441d0af7873813a34badec430293329640ce359eac4303d233d01483045022100e21797339488e924d03fd2999bed5c3e31ec6f418a14859f5105a57289ae448102205d6cc82821c278fd058ceaa9c8123464d7de2a0d317462df475796a2077f17c8014c69522102863f8bc6dfb0ba57d0c756c61bfae5a6f919d2c1439b161e0614340253f545d32102a7e26aba061d0e186a560429833ce88c18b1951cbc02f2fb0cde669959fb7f8f2102fda5d852af846bfe82994d60e4ef9c2bc72fc79bcd9e4d050e9fb2d443bd484653ae"
      },
      "sequence": 4294967295
    }
  ],
  "vout": [
    {
      "value": 0.00295273,
      "n": 0,
      "scriptPubKey": {
        "asm": "0 5487d30833cd52e19cb15e6a4c8ac373a815b2b9",
        "hex": "00145487d30833cd52e19cb15e6a4c8ac373a815b2b9",
        "reqSigs": 1,
        "type": "witness_v0_keyhash",
        "addresses": [
          "bc1q2jraxzpne4fwr893te4yezkrww5ptv4erhp7e8"
        ]
      }
    }
  ]
}
```

The amounts and addresses shown match expected values. The vin is now populated with the signature information.  Using the same bitcoin node, I could simply call the following

![image](https://user-images.githubusercontent.com/88121568/221365459-265751fd-5a81-4662-a268-fc79fa13d85b.png)

However, for testing purposes, I’m going to broadcast with Caravan itself.  It’s important to note that the ability to verify the addresses and amounts on my hardware devices is the only certainty I have that the transaction hasn’t been altered under the hood by Caravan or Unchained Capital as a whole.  I have not yet reviewed the underlying code for Caravan and cannot attest to its safety. If you do make use of this tool, you should download a copy to run locally.

After clicking the `Broadcast Transaction` button, it is replaced with the transaction id, which matches what I could see with the bitcoin node.

![image](https://user-images.githubusercontent.com/88121568/221365473-bb121c3e-88b2-48e5-80c9-df579fca9cb8.png)

### Section Test Results

✔️ Able to import the generated wallet into Caravan<br />
✔️ Able to see address history on the wallet with UTXOs<br />
✔️ Able to create new transaction for sending<br />
✔️ Send transaction gives full control over address, fees, amounts<br />
✔️ Send transaction supports manual control of individual UTXOs to spend from<br />
✔️ Each step of the transaction gives raw hexadecimal which can be verified externally<br />
✔️ Signing with hardware devices supports the Trezor and Ledger devices I used previously.<br />
✔️ The transaction can be fully signed and prepared for broadcast<br />
✔️ The tool is capable of broadcasting the transaction<br />

## Website Account Management

If you forget your password to Unchained Recovery, the login screen provides a convenient `Forgot your password?` [link](https://my.unchained-capital.com/credentials/password/reset/request) to get you back on track.  You’ll be prompted to enter your email address, and upon doing so, an email will be sent to you with instructions to reset the account.

### Section Test Results

✔️ Verified ability to change my account password<br />
✔️ Verified ability to logout/login on website and app with new credentials<br />

## Conclusion

Unchained Capital provides a useful collaborative multisig service that is driven from their website and can dovetail into their loan product.  While KYC is unnecessarily high, privacy is generally not at top of mind for any collaborative multisig product.  

The greatest strengths of Unchained Capital are that they put excellent effort into the Trust Minimized External Recovery through their Caravan project.  In addition, its easy to adapt for use with Electrum wallet.

There are several points within the application that I hope get improved, most notably guidance on verifying addresses, UTXO management, and ability to have more then one address being monitored at a time.  Given the dearth of emails received, I wish there was a way I could toggle those off in account settings.

I recommend anyone considering Unchained Capital to do their own due diligence in testing the setup, and periodically reverifying as the service may be updated over time.  It is critical that users always capture the external spend info anytime they create a new vault or replace a key.  The derivation paths along with their device seeds, and the unchained capital xpub on the vault is essential to recover.

To reiterate --__Do Not Trust what I have written in this article. 
Verify it for yourself!__

Use the information as you see fit as a jumping off point to run through your own scenarios based on your personal threat model.
