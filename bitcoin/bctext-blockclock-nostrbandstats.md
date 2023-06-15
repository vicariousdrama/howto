# Nostr Band Stats on a BlockClock

## Summary 

If you have a Blockclock Mini, you can use it to display stats from nostr.band by making some API calls to retrieve the data, formatting it, and additional API calls to your blockclock to display it.

The goal is to look something like this, which is the total number of zaps as of this writing on 2023-06-15 16:39

![image](https://github.com/vicariousdrama/howto/assets/88121568/49b74962-5d9c-4cae-9fcd-d3cb9b691503)

## Preparation

You will need to acquire the following

1. The IP address of your Blockclock.  As you'll need to reference it when calling the script
2. A Linux environment to run the bctext utility and the script
3. The [bctext](https://github.com/vicariousdrama/bctext) (That's BlockClock Text) utility
4. The script denoted below

## Installing BCText

BCTEXT is a utility I wrote for formatting text strings and interfacing with the Blockclock to write it as over/under text.

It is available here: https://github.com/vicariousdrama/bctext

You can either follow the steps to clone and build bctext as depicted in the README of that project, or you can download a prebuilt binary from the [releases page](https://github.com/vicariousdrama/bctext/releases)

For example, on a Raspberry Pi, you can issue the following commands to download, extract and install the utility

```shell
wget https://github.com/vicariousdrama/bctext/releases/download/v1.0.0/bctext-1.0.0-arm64-linux.tar.gz
tar -xvf bctext-1.0.0-arm64-linux.tar.gz
sudo install -m 0755 -o root -g root -t /usr/local/bin bctext
```

## Creating the script

Find a place where you want to store the script where its convenient to run it.

Then create or edit the file for the script

```shell
nano nostrbandstats.sh
```

Copy and paste the contents as follows

```shell
#!/bin/bash

# Variable for Blockclock IP address (pass this as an argument when calling this script)
blockclockip=$1

# Variable for stat to report (pass this as an argument when calling this script)
# valid values are: relays, pubkeys, users, trusted_users, events, posts, zaps, zap_amount
# default: zaps
nostrstat=$2
case $nostrstat in
  "events") ;;
  "posts") ;;
  "pubkeys") ;;
  "relays") ;;
  "trusted_users") ;;
  "users") ;;
  "zap_amount") ;;
  "zaps") ;;
  *) nostrstat="zaps"
esac

# Variable for our text output. Will get populated
textoutput=""

# Get nostr stats from nostr.band
nostrstats=`curl -s -X 'GET' 'https://stats.nostr.band/stats_api?method=stats'`

# Parse the field we want
nostrvalue=`echo ${nostrstats} | jq ."${nostrstat}"`

# Assemble text
textoutput="nostr stats from nostr.band ${nostrstat}=${nostrvalue}"

# Send to the blockclock
bctext -wordalign -texttoshow "${textoutput}" -blockclockip "${1}"
```

Save (press CTRL+O) and Exit (press CTRL+X) the file

Mark the file as executable

```shell
chmod +x nostrbandstats.sh
```

## Running the Script

Now you can try running the script.  You'll need to provide the IP address of your blockclock as the first argument.

For example, if your Blockclock is on IP address 192.168.1.121, then you would run the script as follows

```shell
./7dayclosing.sh 192.168.1.121
```

If you don't provide the IP address, then the BCTEXT utility will display the Debug output of the parsed values

```
Debug results for this text string
---------------------------------------------------------------------------------------
 slot      over            under       url
    0  NOSTR           ZAPS.           http:///api/ou_text/0/NOSTR/ZAPS.
    1  STATS           96976           http:///api/ou_text/1/STATS/96935
    2  FROM.           3........       http:///api/ou_text/2/FROM./9........
    3  NOSTR           ............    http:///api/ou_text/3/NOSTR/............
    4  .BAND.          ............    http:///api/ou_text/4/.BAND./............
    5  ..........      ............    http:///api/ou_text/5/........../............
    6  ..........      ............    http:///api/ou_text/6/........../............
```

