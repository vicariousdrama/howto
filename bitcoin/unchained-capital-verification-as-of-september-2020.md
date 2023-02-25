# Unchained Capital Verification as of September 2020
_Don’t Trust. Verify. What’s in your vault?_

by @vicariousdrama
644428 - 648834

![image](https://user-images.githubusercontent.com/88121568/221368410-44392dcd-3296-436e-bff7-43f53e0a29d0.png)

## Introduction

Unchained Capital describes itself as a bitcoin native financial services company offering collaborative custody multisignature vaults and loans for bitcoin holders.

Unchained Capital has a [YouTube channel](https://www.youtube.com/channel/UCTkCLH1VSjWakXyF6z-mjtA) where they cover some of the capabilities of their service from a marketing and user perspective. This article enumerates features I tested in September 2020.  A lengthier 50+ page version of these results exists which I may post as a separate article.  At the very least, reading through the bullet points may give you an idea of what to look into when verifying these features for your own needs.

Within, you’ll see ✔️ indicators for a feature that was verified, and ⬜ which indicates a feature that should be available, but I did not verify as I lack sufficient testing hardware to do so.  There were no failures.

The presence of ⚠️ is used to alert you to aspects you should be aware of should you choose to use Unchained Capital that may represent privacy concerns, bugs or possibly confusing aspects.

## Change History

| Date | Description |
| --- | --- | 
| 2020-09-28 | Initial Document |
| 2023-02-25 | Conversion to Markdown |

## The Test Bed

For this testing, I’ve used only Trezor One and Ledger Nano S.  According to the website, they do not support Coldcard at this time.  Most testing is done through the web browser using Chrome or a Chrome derivative (e.g. Brave).  In some instances I used Electrum and Caravan.  All testing is done on mainnet/production.

## Website Signup and Privacy Concerns

✔️ I was able to [create an account](https://my.unchained-capital.com/sign_up) with username, password, email, and phone<br />
⚠️ To create a vault (or a loan), more KYC information is needed (first and last name, date of birth, photo identification, address information)<br />
⚠️ Website calls are made to the following fully qualified domain names<br />
  - my.unchained-capital.com
  - www.google-analytics.com
  - fonts.googleapis.com
  - Pi.typekit.net
  - fonts.gstatic.com

⚠️ Common to all multisig providers, Since Unchained Capital needs the xpubs for devices to facilitate creation of transactions and derivation keys, they can see all transactions associated with the wallet(s). <br />

## Vault Creation

✔️ The derivation path used for all keys by default is m/45'/0'/0'.<br />
✔️ You can specify a custom derivation path. For example m/45'/0'/1'.<br />
✔️ Setup Key with Ledger Nano S.<br />
✔️ Setup Second Key with same hardware wallet (Unchained Capital does not recommend)<br />
✔️ Setup Key with Trezor One<br />
✔️ Setup Multisig Wallet (Vault #1) using 2 devices<br />
✔️ Setup Multisig Wallet (Vault #2) using 1 device but 2 different derivation paths (Unchained Capital does not recommend doing this)<br />
⬜ Setup Key with Ledger Nano X<br />
⬜ Setup Key with Trezor Model T<br />
⚠️ Dependence on third party website without dead link or content verification<br />
⚠️ Keys that you create don’t “remember” what type of device they are associated with.<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This is left up to the user for all future transactions and may result in confusion.  <br />

## Verifying Receive Addresses

✔️ Can verify Ledger Nano S has ownership to address<br />
✔️ Can verify Trezor One has ownership to address<br />
✔️ Premade Backup File with important details to recover wallet<br />
⚠️ Full Derivation path has a depth of 6 which is nonstandard.  <br />
⚠️ Unchained Capital doesn’t automatically see transactions it didn’t broadcast <br />
⚠️ Unchained Capital will recommend reuse of the same address for deposits<br />
⚠️ Unchained Capital effectively has a gap limit of 0 and only appears to monitor the current deposit address, while skipping already used addresses<br />

## Caravan

✔️ Wallet file is compatible with Unchained Capital’s Caravan product<br />
⚠️ Default BIP32 path in Caravan doesn’t match Unchained Capital default scheme<br />

## Electrum

✔️ Can setup, sign, and send transactions using Electrum<br />
⚠️ Wallet file can not be directly imported into Electrum (but easy to convert)<br />

## Signing Transactions

✔️ Able to prepare transaction, sign, and send funds to another address<br />
✔️ Send dialog permits nearly full control over the fee rate<br />
⚠️ Fee rate must be greater than 0 and less than 1000 sats per byte.<br />
⚠️ Send dialog link for Fee Estimator goes to [bitcoinfees.earn.com](https://bitcoinfees.earn.com),<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; an external website, that does not consider recent blocks, but days as a whole. <br />
⚠️ Send dialog has no way to specify amount in satoshis.<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Recall sats are at 8th decimal place<br />
⚠️ Send dialog permits an amount with more than 8 decimal places but does validate before<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; allowing you to move next<br />
⚠️ Unchained Capital doesn’t monitor more than the current address<br />
⚠️ Wallet will only reflect balance based on the current address<br />
⚠️ No UTXO management when there are multiple addresses with a balance<br />
⚠️ Links for reviewing transactions are all external to [blockstream.info](https://blockstream.info)<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; with no ability to define your own node<br />
⚠️ All transactions prepared through the web interface are broadcast through Unchained Capital servers, with no ability to define your own node<br />
⚠️ Transaction ID is not revealed until after broadcast<br />
⚠️ Vault will skip addresses that have a transaction associated but wont include in overall balance<br />
⚠️ Must wait until a transaction is confirmed before beginning another transaction in a vault.<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This can be problematic if a low fee transaction is never included in a block. To resolve, do RBF using external wallet software.<br />
⚠️ Vaults with pending deposit transactions cannot send (withdraw or transfer) funds until the<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; pending deposit is completed.<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This is a possible denial of service attack vector.<br />

## Key Replacement

✔️ Able to create a new replacement key<br />
✔️ Able to mark a key as lost or compromised needing replaced<br />
✔️ Steps to walk through transaction work to reuse remaining key parts.  <br />
✔️ Able to replace a key with a new key on a vault.<br />
✔️ Unchained Capital facilitates the key rotation incrementing the “account” or 4th of 6 position in the derivation path automatically<br />
✔️ Prevented from re-creating the same key for a key actively in use<br />
✔️ Prevented from re-creating the same key for a key marked as compromised<br />
⚠️ Fees for moving funds to new key set cant be set<br />
⚠️ No clear way to verify address that funds will be sent to<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_I wrote about how to do this in the article here: [address-verification-changing-keys-for-unchainedcapital-vaults.md](./address-verification-changing-keys-for-unchainedcapital-vaults.md)_<br />
⚠️ List of replacement keys includes keys that cannot be used for replacement.<br />
⚠️ List of replacement keys is not sorted by name or creation date.<br />
⚠️ Unable to replace a key while the vault has an unconfirmed transaction.<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This is a mixed result, but could result in denial of service on pending inbound transactions<br />
⚠️ Unable to spend funds while the vault is being swept from key replacement.<br />

## Performing Health checks

✔️ Able to perform a Key Health Check<br />
✔️ Verified website shows when a health check was last performed<br />
✔️ Verified that health check on incorrect device does not trigger success.<br />

## Signing Transactions with Unchained Key

✔️ Able to setup a transaction that requests signing by Unchained<br />
✔️ Able to control amount and fees of transaction being setup<br />
✔️ Verified that Unchained signed the transaction<br />
✔️ Able to control broadcast of signed transaction<br />
⚠️ Not certain whether I owe Unchained $20 for signing the transaction and how that would be paid.<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Not integrated in web application.<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_-- As a follow up, Phil indicated that they were not yet charging for this service._<br />

## Managing Vaults

✔️ Able to create multiple vaults.<br />
✔️ Able to mark a vault as closed.<br />
✔️ A closed vault cannot be reopened.<br />
✔️ Verified that Unchained doesn’t permit initiating new transactions from a closed vault.<br />
✔️ A closed vault can be renamed<br />
✔️ According to Unchained Capital, you can have an unlimited number of vaults<br />
⚠️ Closed vaults remain in the list of vaults.<br />
⚠️ By default, vaults may be sorted by the generated ID instead of name<br />

## Trust Minimized External Recovery

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

✔️ Verified ability to change my account password<br />
✔️ Verified ability to logout/login on website and app with new credentials<br />

## Conclusion

Unchained Capital provides a useful collaborative multisig service that is driven from their website and can dovetail into their loan product.  While KYC is unnecessarily high, privacy is generally not at top of mind for any collaborative multisig product.  

The greatest strengths of Unchained Capital are that they put excellent effort into the Trust Minimized External Recovery through their Caravan project.  In addition, its easy to adapt for use with Electrum wallet.

There are several points within the application that I hope get improved, most notably guidance on verifying addresses, UTXO management, and ability to have more then one address being monitored at a time.  Given the dearth of emails received, I wish there was a way I could toggle those off in account settings.

I recommend anyone considering Unchained Capital to do their own due diligence in testing the setup, and periodically reverifying as the service may be updated over time.  It is critical that users always capture the external spend info anytime they create a new vault or replace a key.  The derivation paths along with their device seeds, and the unchained capital xpub on the vault is essential to recover.

To reiterate -- __Do Not Trust what I have written in this article.__

__Verify it for yourself!__

Use the information as you see fit as a jumping off point to run through your own scenarios based on your personal threat model.
