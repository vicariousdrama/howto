#!/usr/bin/env python3

from os.path import exists
import json
import logging
import random
import ssl
import sys
import time
from requests import get
from nostr.key import PrivateKey
from nostr.relay_manager import RelayManager
from nostr.event import EncryptedDirectMessage

def getConfig(filename):
    logger.debug(f"Loading config from {filename}")
    if not exists(filename):
        logger.warn(f"Config file does not exist at {filename}")
        return {}
    with open(filename) as f:
        return(json.load(f))

def getNostrRelays():
    if "relays" in config:
        return config["relays"]
    else:
        logger.warn("Using default relays as none were defined in config")
        return ["nostr.pleb.network",
                "nostr-pub.wellorder.net",
                "nostr.mom",
                "relay.nostr.bg"
                ]

def sendNostrDM(senderPrivateKey, recipientPubKey, message):
    logger.info(f"Sending message: {message}")
    # Pad message
    paddedMessage = "{:<512}".format(message)
    # Setup relays
    relay_manager = RelayManager()
    nostrRelays = getNostrRelays()
    for nostrRelay in nostrRelays:
        relay_manager.add_relay(f"wss://{nostrRelay}")
    # Connect
    relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE}) # disables ssl certificate verification
    time.sleep(1.25) # allow connections
    # Prepare the event message, sign it
    dm = EncryptedDirectMessage(
      recipient_pubkey=recipientPubKey,
      cleartext_content=paddedMessage
    )
    senderPrivateKey.sign_event(dm)
    # Send it
    relay_manager.publish_event(dm)
    time.sleep(1) # allow messages to send
    # Close
    relay_manager.close_connections()

def getExternalIP():
    serviceURLs = ["https://ifconfig.me/ip", 
                   "https://api.ipify.org"]
    serviceURL = random.choice(serviceURLs)
    logger.debug(f"Getting external IP address from {serviceURL}")
    return get(serviceURL).text

# Logging to systemd
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(fmt="%(asctime)s %(name)s.%(levelname)s: %(message)s", datefmt="%Y.%m.%d %H:%M:%S")
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Global config
config = getConfig("config.json")

if __name__ == '__main__':

    # Read in key config info
    if "sendToPubKey" in config:
        sendToPubKey = config["sendToPubKey"]
    else:
        logger.warn("Config file is missing sendToPubKey value")
        quit()
    if "ourPrivateKey" not in config:
        logger.warn("Config file does not have ourPrivateKey defined. A new one will be created")
        botKey = PrivateKey() # generate new each time script run
    elif len(config["ourPrivateKey"]) != 64:
        logger.warn("Config file has improperly formed value for ourPrivateKey. A new one will be created")
        botKey = PrivateKey() # generate new each time script run
    else:
        # Use existing
        raw_secret=bytes.fromhex(config["ourPrivateKey"])
        botKey = PrivateKey(raw_secret=raw_secret)
    sleepInterval = 1800
    if "sleepInterval" in config:
        sleepInterval = config["sleepInterval"]
    reportInterval = 86400
    if "reportInterval" in config:
        reportInterval = config["reportInterval"]

    oldip = ""
    lastMessageSent = 0
    statusJustChanged = "🔴"
    statusOK = "🟢"
    statusRecentlyChanged = "🟡"
    changeCountReportMax = 5
    changeCount = 0

    # Main Loop
    logger.info("Beginning loop")
    while True:
        # Fetch data
        ip = getExternalIP()

        # Do stuff with it
        currenttime = int(time.time())
        # Report if changed
        if len(oldip) > 0 and oldip != ip:
            nostrMessage = f"{statusJustChanged} IP changed to {ip} as of {currenttime}\n\n(it used to be {oldip})"
            sendNostrDM(senderPrivateKey=botKey, recipientPubKey=sendToPubKey, message=nostrMessage)
            lastMessageSent = currenttime
            changeCount = changeCountReportMax
        # Additional DMs when counter above 0 to draw attention to issue
        if changeCount > 0:
            nostrMessage = f"{statusRecentlyChanged} IP recently changed to {ip}"
            sendNostrDM(senderPrivateKey=botKey, recipientPubKey=sendToPubKey, message=nostrMessage)
            changeCount = changeCount - 1
        # Report at least as often as reportInterval (default 1 day)
        if currenttime > lastMessageSent + reportInterval:
            nostrMessage = f"{statusOK} IP is {ip} as of {currenttime}"
            sendNostrDM(senderPrivateKey=botKey, recipientPubKey=sendToPubKey, message=nostrMessage)
            lastMessageSent = currenttime
        oldip = ip

        # Rest for a bit (default 30 minutes)
        logger.info(f"sleeping for {sleepInterval} seconds")
        time.sleep(sleepInterval)
