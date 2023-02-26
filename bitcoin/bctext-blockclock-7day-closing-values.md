# 7-Day Bitcoin Closing Price

## Summary 

If you have a Blockclock Mini, you can use it to display the past 7-days closing price data for Bitcoin by making some API calls to retrieve the data, formatting it, and additional API calls to your blockclock to display it.

The goal is to look something like this, which is data as of this writing on 2023-02-26 3:29 AM

![image](https://user-images.githubusercontent.com/88121568/221390788-6b477359-df1a-48d3-a216-5832aecd3ce1.png)

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
nano 7dayclosing.sh
```

Copy and paste the contents as follows

```shell
#!/bin/bash

# Variable for Blockclock IP address (pass this as an argument when calling this script)
blockclockip=$1

# Variable for our text output. Will get populated
textoutput=""

# Get pricing data from coingecko : https://www.coingecko.com/en/api/documentation
# Returned data is an array where each element in the array is an array of [timeinmilliseconds,open,high,low,close]
ohlc=`curl -s -X 'GET' 'https://api.coingecko.com/api/v3/coins/bitcoin/ohlc?vs_currency=usd&days=7' -H 'accept: application/json'`

# Days
dayvalues=`echo ${ohlc} | jq '.[] | select(.[0] % 86400000 == 0) | .[0]|tonumber / 1000'`
while read line; do
  for word in $line; do
  dayname=`date -d @${word} | awk '{print $1}'`
  textoutput+=" ${dayname}"
  done
done <<< "$(echo -e "$dayvalues")"

# Closing values
closingvalues=`echo ${ohlc} | jq '.[] | select(.[0] % 86400000 == 0) | .[4] | floor'`
while read line; do
  textoutput="${textoutput} ${line}"
done <<< "$(echo -e "$closingvalues")"

# Remove leading and trailing spaces
textoutput=`echo $textoutput | awk '{$1=$1};1'`

# Send to the blockclock
bctext -wordalign -nopadding -texttoshow "${textoutput}" -blockclockip "${1}"
```

Save (press CTRL+O) and Exit (press CTRL+X) the file

Mark the file as executable

```shell
chmod +x 7dayclosing.sh
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
    0  SUN             24480           http:///api/ou_text/0/SUN/24480
    1  MON             24695           http:///api/ou_text/1/MON/24695
    2  TUE             24370           http:///api/ou_text/2/TUE/24370
    3  WED             24090           http:///api/ou_text/3/WED/24090
    4  THU             23807           http:///api/ou_text/4/THU/23807
    5  FRI             23095           http:///api/ou_text/5/FRI/23095
    6  SAT             23140           http:///api/ou_text/6/SAT/23140
```


