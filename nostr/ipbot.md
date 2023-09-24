# IPBot

A simple bot written in python that will DM a specified account whenever
its externally reachable IP address changes.  For me this can be helpful
to make network changes in lieu of a dynamic DNS setup, and for capturing
how often such change from the provider occurs.

You can repurpose this script using the pattern to periodically send you 
some other relevant data that you want remotely.

## Preparation

To use this script, you'll need to run it with python 3.9 or higher
and with the nostr and requests packages installed.

```sh
python3 -m venv ~/.pyenv/ipbot
source ~/.pyenv/ipbot/bin/activate
python3 -m pip install nostr@git+https://github.com/callebtc/python-nostr.git
python3 -m pip install requests
```

## Download ipbot.py

Create a folder for the script

```sh
mkdir -p ~/nostripbot
cd ~/nostripbot
```

And download the file

```sh
wget https://raw.githubusercontent.com/vicariousdrama/howto/main/nostr/ipbot.py
```

## Configuration

Configure a file in the same folder named config.json

```sh
nano config.json
```

And structure its contents as follows.

```json
{
  "ourPrivateKey": "hexadecimal-representation-of-private-key-for-signing",
  "sendToPubKey": "hexadecimal-representation-of-public-key-to-direct-message",
  "relays": [
    "nostr.pleb.network",
    "nostr-pub.wellorder.net",
    "nostr.mom",
    "relay.nostr.bg"
  ]
}
```

The value of `ourPrivateKey` is the private key for your bot. Don't use
your normal user key. Create a new one.  You can do this at the command
line using the same package via

```python
from nostr.key import PrivateKey
print(PrivateKey().hex())
quit()
```

Or generate one with like this

```sh
hexdump -vn32 -e '8/4 "%08x" 1 "\n"' /dev/random
```

The value of `sendToPubKey` should be the hexadecimal representation
of your account for which the direct encrypted message of the status
should be sent.

If you only have your npub, you can convert it to hexadecimal like
this

```python
from nostr.key import PublicKey
npub = "npub1yx6pjypd4r7qh2gysjhvjd9l2km6hnm4amdnjyjw3467fy05rf0qfp7kza"
pubkey = PublicKey().from_npub(npub)
print(pubkey.hex())
quit()
```

Make sure you put in YOUR value for the npub! Otherwise you will end
up sending direct messages to me :)

The `relays`` should be ones that your bot, can actually write to.

## Run it

To run the bot, simply start the script

```python
~/.pyenv/ipbot/bin/python ipbot.py
```

press CTRL+C to stop it.
