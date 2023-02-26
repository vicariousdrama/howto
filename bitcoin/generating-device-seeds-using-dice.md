# Generating Device Seeds Using Dice

_Cross Referencing Coldcard, Cobo Vault, and Rolls.Py for Seed Generation_

by @vicariousdrama
662650–662806

![image](https://user-images.githubusercontent.com/88121568/221386999-b022de49-00c4-41bf-8ae4-e3f3b54cf872.png)

## Summary

In the past, it was common practice to allow a software or hardware wallet to generate a new wallet for you based on its random number generator. A set of seed words would be produced that you in turn wrote down. These words, along with the wallet type and derivation path serve as a backup and can be restored in any wallet supporting the BIP39 standard. But relying on the software or hardware wallet to generate randomness carries some risk as there is no good way to ascertain whether its truly random, or subject to supply chain attacks. An alternative approach is to use your own source of randomness and generate seed words from that. This article covers the use of dice as entropy, deriving seed words from the result, and use of assorted tools freely available to come up with the same result.

## Change History

| Date | Description |
| --- | --- |
| 2020-12-24 | Initial Document |
| 2023-02-26 | Conversion to Markdown |

## Gather Your Dice Supplies

Let’s start with what you’ll need

- Good Quality 6 Sided Dice (preferably more than one)
- A paper and writing instrument to record your rolls
- An optional Dice Tray
- An optional Dice Tower
- 
Do you need casino quality dice with exacting specifications? I’m gonna say “no”. But if you really want them, you can get a set [from Jeff Bezos here](https://www.amazon.com/Trademark-Poker-Grade-Serialized-Casino/dp/B00157YFJE)

Personally I use a set of [Chessex Dice that are 16mm in size and come in a pack of 12](https://www.amazon.com/Chessex-Dice-d6-Sets-Nebula/dp/B0011WKL3M). I like these because they are translucent, performed well when checking for bias, and 12 is a good number to roll many at a time without being overwhelmed.

You can also gather up assorted six sided dice from any board games you may have lying around.

If you want to roll your dice one time and have enough entropy, consider the [100 pack of very tiny dice that Coinkite makes available](https://store.coinkite.com/store/dice-100). If you want something a bit bigger and translucent, there’s a set on [Amazon](https://www.amazon.com/butterfunny-Translucen-6-Sided-Teaching-Colors/dp/B087Q6WPHW).

In addition to the dice themselves, I like to use a dice tray to constrain the rolling (and dampen the sound). The tray I most often use is this one by [Metallic Dice Games](https://www.amazon.com/Metallic-Dice-Games-Tray-Black/dp/B07MKLPSPN).

![image](https://user-images.githubusercontent.com/88121568/221387053-5bd9cbd7-2fa4-4c09-81c6-f5b307fd187f.png)

It’s convenient to be able to stow away when not in use. You may also consider [making a Dice Tray](https://www.youtube.com/watch?v=M4tywHNeK0A).

Dice Towers are optional as a form of entertainment, but don’t really add to randomness. But if you don’t yet have one and are considering it, I’d recommend one with transparent sides so that you can verify that the dice being dropped in are getting a good bounce, and not simply sliding down. [This one has 5 paddle ramps each velvet lined](https://www.amazon.com/C4Labs-Tall-Velvet-Lined-Tower/dp/B08L8BJWDQ) to help dampen the sound

If you want a more modular system, and don’t mind or actually prefer the noise, consider getting a [few of these](https://www.amazon.com/Broken-Token-Modular-Dice-Tumbler/dp/B07B8TF4C3).

## Rolling the Dice

Rolling dice is going to be part tedious, part fun, and part geeky. While it takes some time it’s easy to understand why this works for randomness.

Most Importantly, your dice, and your method of recording should exist in the physical world without digital attachments. Don’t use Dice Apps on your phone or computer. Likewise, don’t use your phone or computer to record results. Stick to a paper and pen, something you can burn afterwards.

Take your dice, and roll. Record the result. Repeat until you’ve gotten at least 100 dice rolls. If you have a printer, you can print out this page and use the grid to record your results with die roll in each square

![image](https://user-images.githubusercontent.com/88121568/221387083-356afd28-732a-4a97-a63c-7020df3c0ffd.png)

If you are rolling multiple dice at a time, then you’ll want an objective way to “order” the results of those rolled. Absolutely do not order from smallest to largest number. Instead, take your spatial representation and use a straight edge to get them all in a line. Then read from left to right.

If using a Dice Tower, drop one in at a time, and record in the order they come out. For Dice Trays, you may be able to tilt the tray, relying on gravity to line up the dice at the bottom.

![image](https://user-images.githubusercontent.com/88121568/221387090-238140d8-fca7-48dc-91d7-c30c3262797c.png)

I didn’t have the grid when doing a sample for this article, but just recorded on a post it note. Here’s an example.

![image](https://user-images.githubusercontent.com/88121568/221387093-7e496975-a7e2-4ccc-931c-5714ec960b2c.png)

There’s 120 numbers here instead of 100. That’s fine. The more the better, though 99 is sufficient for 256 bits of entropy.


Don’t use this example as your source of entropy for a real wallet. This is only provided here so you can test this with expected outputs below

For copy paste convenience for testing, the order is

`661146665536425463244263515545445463645132435343342264543356444314263566145335642355541211533234355663444433431454644613`

## Preparing Your Hardware Wallet

Now that you have your dice rolls, you can use them to create your wallet. At the time of this writing, hardware wallets such as the Coldcard, and Cobo Vault have support for inputting dice rolls when Importing a wallet. The steps to do this are outlined below, but this approach still trusts the code in the firmware of these wallets to do the conversion.

__If using a new Coldcard__, you do this when first setting up the device.

1. Perform the normal quick start guidance to verify device packaging, power up, accept terms of service and establish your pin. https://coldcardwallet.com/docs/quick
2. Download the latest release firmware for your device and upgrade per the instructions here https://coldcardwallet.com/docs/upgrade. At time of writing its 2020–08–06T1722-v3.1.9-coldcard.dfu. Unzip and verify the SHA-256 Checksum of the DFU file and store on MicroSD card. `ac756e8f90d7cdc706fb24a1358585780c0105329e95d0095d91d48579caa5a1`
3. Upgrade the firmware from Advanced, Upgrade menu and follow instructions. The device will reboot at the end of this process.
4. On the main menu, choose Import Existing and scroll down the menu to Dice Rolls. Then input the numbers as you rolled them. Be careful as there is no “backspace” for errant entries.
5. Press the checkmark button when completed.
6. Once done, the 24 mnemonic seed words will be presented to you. Write these down, proceed and verify on the next step by choosing the matching word from the set provided for each slot.
7. Your wallet has now been initialized with entropy that you created.

A video demonstrating the input process is [available on YouTube](https://www.youtube.com/watch?v=Rc29d9m92xg)

__On a new Cobo Vault__, you need to do these steps to go through the firmware versions to get to the latest version. It’s a bit more involved as you need to update the firmware three times to get most up to date. The downloads page is here https://cobo.com/hardware-wallet/downloads

1. Download 1.0.5 Firmware from the website, unzip, verify the SHA-256 Checksum of the update.zip, and store the update.zip on a MicroSD card. Insert that into the Cobo Vault device and power up. `71e5b1e04ec88d89c90c300b4c14abbc71e0cc55ec737e1565a7279def1b8393`
2. Upgrade Firmware to 1.0.5 when prompted
3. Restart, and initialize the device creating a wallet. This will be a temporary wallet but you must fully setup before proceeding. For convenience, you can Import an existing 12 word seed (abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about)
4. Power off, remove battery pack, and the MicroSD card
5. Download 1.2.1 BTC Only Firmware from the website, unzip, verify the SHA-256 Checksum of the update.zip, and store the update.zip on the MicroSD card. Insert into Cobo Vault and power up. `afb82abe013373c262cbd518ebd9bbcf7156b713270b776a4c3d3a15d69bb0f0`
6. Do your normal login password and upgrade the firmware when prompted.
7. After restart, power off again, remove battery pack and MicroSD card.
8. Download 2.3.1 BTC Only Firmware from the website, unzip, verify the SHA-256 Checksum of the update.zip, and store the update.zip on the MicroSD card. Insert into Cobo Vault and power up. `1210f73d012226f69579339cfec7911e7eafb8395e252e8f4ed5e16b91531210`
9. Do your normal login password and upgrade the firmware when prompted.
10. From the Menu, choose Settings, then Create/Import Vault, and supply your password
11. Click the I’ve read and agree to the Terms of Service radio button, and click Create Vault
12. On the explanation screen for Generate Recovery Phrase, tap the image of the cobo-tablet three times. This will access the hidden Dice Rolls process
13. Click the Start button, and tap the numbers corresponding to the dice roll results on your sheet in the same order you rolled them. Once complete, press Done.
14. The 24 mnemonic seed words will be presented to you. Write these down, proceed and verify on the next step by re-entering.
15. Your wallet has now been initialized with entropy that you created.

If you have both a Coldcard and a Cobo Vault to try out the above, you’ll soon realize that they produce a different set of seed words. Let’s look into why this is.

## Verifying Mnemonic Generation

What you will need

- A laptop not connected to the internet. Preferably, an older one that allows switching off wifi, bluetooth, removing the hard drive and battery.
- An Up to Date Tails OS Bootable USB Stick
- Another USB stick to store the rolls.py script

If you don’t already have the latest version of a Tails Bootable USB stick, go ahead and create that now. While setup is outside the scope of this article, you should start here [https://tails.boum.org/](https://tails.boum.org/) and have an available USB stick at least 8GB in size to write the image to.

![image](https://user-images.githubusercontent.com/88121568/221387172-55f94705-f42a-4fb6-9c8b-087695ed22c6.png)

Coldcard provides a useful guide for verifying the dice rolls and the mnemonic that is generated here.

https://coldcardwallet.com/docs/verifying-dice-roll-math .

You’ll need a copy of the most recent rolls.py script available here https://github.com/Coldcard/firmware/blob/master/docs/rolls.py

Copy that file to your second USB stick

Boot up your disconnected laptop using your Tails OS USB stick.

Open a Terminal Window

Insert your USB stick with rolls.py

Navigate to the directory containing that script. In general this should be a subfolder underneath /media/amnesia

Now run your dice rolls as input as follows

```shell
echo “661146665536425463244263515545445463645132435343342264543356444314263566145335642355541211533234355663444433431454644613” | python3 rolls.py
```

The output is as follows.

![image](https://user-images.githubusercontent.com/88121568/221387203-c25cc3d3-53dd-40aa-9e68-165ff8ca9295.png)

This matches the seed words if using the same dice rolls as input into the Coldcard with Importing Wallet.

Does this mean that the Cobo Vault is wrong? No. Cobo Vault follows the Ian Coleman BIP39 Mnemonic approach, and takes the dice rolls and converts to Base6. We can do the same using the rolls.py script by using sed to substitute values as follows

```shell
echo “661146665536425463244263515545445463645132435343342264543356444314263566145335642355541211533234355663444433431454644613” | sed s/6/0/g | python3 rolls.py
```

Now the result, having changed each 6 to 0 is as follows


This matches what a Cobo Vault would produce from the dice rolls entered.
You can cross check this with the sample rolls above using the Ian Coleman BIP39 tool available here https://iancoleman.io/bip39/ . On that page, check the box for Show Entropy Details, and then paste in the sequence from our sample

```
661146665536425463244263515545445463645132435343342264543356444314263566145335642355541211533234355663444433431454644613
```

Note that the Entropy Type automatically detects and selects Base 6 (dice).

For Mnemonic Length, choose 24 words. The words shown will reflect that of the Cobo Vault. The Filtered Entropy shows every 6 changed to a 0.

![image](https://user-images.githubusercontent.com/88121568/221387233-a600cb04-2c42-4782-ae24-b50779daddf1.png)

On the right hand side, choose Base 10. Now the words will change to the same set as the Coldcard, and the Filtered Entropy shows the same value as the entropy we provided.

![image](https://user-images.githubusercontent.com/88121568/221387241-1ab5d3e8-a86c-47d6-af15-aab889a0d8c9.png)

I’ve personally verified and am quite content with the use of the rolls.py implementation for its simplicity and elegance. The word list within that single download file matches the same word list as the bip39 english word list here https://github.com/bitcoin/bips/blob/master/bip-0039/english.txt.

I strongly encourage use of the rolls.py script for generating your seed words from dice. It’s the easiest to use off line with Tails in a secure way.

It’s important to note that whether you take your dice rolls and convert to Base6 or leave as Base10 is inconsequential as either approach still yields the same amount of entropy adequate for seed generation.

- Use your own dice rolls and generate your seed words using the script.
- Then record those seed words.
- Next, in your hardware wallet of choice, import your seed words.

## Backup Your Seed Words

Take the seed words, and record them permanently into metal for durability and resilience against fire and floods. Personally, I like the metal plates available from

- Coinkite Seedplate : http://bitcoinseedbackup.com/
- Blockplate : https://www.blockplate.com/collections/frontpage
- Cobo Tablet Punch : https://shop.cobo.com/products/cobo-tablet-punch

There are plenty of good options for backing up to metal in various forms at different price points. I strongly encourage you to read through Jameson Lopp’s testing here https://blog.lopp.net/metal-bitcoin-seed-storage-stress-test-iv/

## Getting Rid of the Evidence

Gather up all those pieces of paper you used when writing down dice rolls and seed words.

If you have a wood burning stove, feel free to chuck it in to your fire. An outdoor fire pit is also useful. Just make sure all the paper burns. If you have neither, burn in a location outside that is away from structures and other flammables. A cement patio works well for small amounts. Once burned, douse the ashes in water and smear. Let dry, sweep up the ashes, and dispose.

In general, burn in accordance with your local laws and regulations.

![image](https://user-images.githubusercontent.com/88121568/221387281-aa2d5502-714b-4c2b-9a81-9b8d5c0bf75e.png)

