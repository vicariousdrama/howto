# Nodeless and AWS Serverless Example
_An example of integrating AWS Serverless with Nodeless.io and accepting payments_

by @vicariousdrama

805752-??????




todo
- roles
- create s3 bucket
- s3 static page
- lambda builder -- need as zip file to uplaod including binary files
- guidance on env vars

---

# Nodeless.io

Nodeless lets you accept bitcoin and lightning payments without needing to setup the server infrastructure. You don't need to run your own node, or establish your own server payemnt provider. Instead, you can create an account with Nodeless and have it route finalized payments to lightning address or on chain address.  It works very well with custodial providers for the Bitcoin circular economy.

If you haven't already done so, [sign up for an account](https://nodeless.io/app/signup) with a dedicated email and password. Or, [login](https://nodeless.io/app/login) to your dashboard

# Amazon Web Services

Amazon Web Services have been around for nearly two decades and is a leader in serverless technology. 

TBD: create account or login

## Nodeless: Create Store

If you don't have an existing Nodeless Store, you can add a new one by clicking `Store` from the Payment submenu on the left, then the `Add Store` button in the upper right. Provide a name for the store.

Once you have a store you plan to use, make note of its ID.  This is the UUID looking identifier in the address bar, and a convenient copy button is provided next to the store name.

In this example, my store name is `test-store`, and the ID is `d809bb04-bb3a-4d84-8f75-eba51397e88a`. The copy link shows the first few characters

![image](https://github.com/vicariousdrama/howto/assets/88121568/606860f2-67ea-4e7f-8b2c-52d5190bd03b)

We will come back to this later to setup the webbook after defining the API Gateway for Access in AWS.

## Nodeless: Create API Token

From within Nodess, click on your `Profile` from the App menu on the left, or from the dropdown on your email address in the upper right corner.

Next, select the `API Tokens` submenu on the Settings page of profile.

Click the button to `Generate Keys` and provide a label.  For this example, I just put `nodeless-example-apikey`

The API token value will be displayed. This is the only time it is displayed. You should save this to some place you can access it later. You will need it when continuing setup with the AWS Lambda function.

## AWS: Create API Gateway for Access

You can think of an API Gateway as a basic contract or schematic of operations allowed to your backend service from the internet. It provides for an endpoint that can be called, and permits routing operations to handlers.

In the AWS Console, access the [API Gateway](https://us-east-1.console.aws.amazon.com/apigateway/main/apis?region=us-east-1).

Click the [Create API](https://us-east-1.console.aws.amazon.com/apigateway/main/precreate?region=us-east-1) button in upper right corner.

For this example, choose the simple HTTP API option.

On step one, specify a name for the api.  You can name it whatever you want to fit your nomenclature.  If you can't think of a name, use something simple like `nodeless-example-api`

For steps 2 through 4, click next and eventually create. This will create an empty API without any routes defined yet. We will come back to this later and fill them in.

Once created, you'll be looking at the details for the API, and you'll see an Invoke URL. This url is what will be referenced externally. You'll need it for both the Nodeless webhook, and the static HTML page for where user inputs should be sent to

For example, the Invoke URL that was created for my API is https://eahilxrhrg.execute-api.us-east-1.amazonaws.com

## Nodeless: Create Webhook

Back in Nodeless, navigate to the store page you had setup.  On the submenu that appears, you can choose `Webhooks`

Click the `New Webhook` action on the right side.

In the URL field, specify the value of the Invoke URL from the API Gateway, with the path appended as `/nodeless`. For example, my Invoke URL was `https://eahilxrhrg.execute-api.us-east-1.amazonaws.com`, so the URL I specify is `https://eahilxrhrg.execute-api.us-east-1.amazonaws.com/nodeless`

Make note of the generated Secret value.  You'll need to capture this and use in configuration later to properly validate signed messages sent from Nodeless to the webhook endpoint.

Choose these events
- Invoice Created
- Invoice Paid
- Invoice Expired

Click the `Save` button when complete.

## AWS: Create Dynamo Table

In the AWS Console, access the [DynamoDB Tables](https://us-east-1.console.aws.amazon.com/dynamodbv2/home?region=us-east-1#tables).

Click the [Create Table](https://us-east-1.console.aws.amazon.com/dynamodbv2/home?region=us-east-1#create-table) button in the upper right corner.

For the table name, indicate the name that will be referenced by the lambda functions we will create later. For example `nodeless-example-orders`

For the partition key, specify `id`

Leave the rest of the data defaulted and click `Create table` at the bottom.

## AWS: Create Lambda for Nodeless Webhook and Order Processing

This is the main lambda used for calls from users for placing orders, and for interfacing with Nodeless.

In the AWS Console, access the [AWS Lambda Functions](https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/functions).

Click the [Create Function](https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/create/function) button in the upper right corner.

Lambda functions have a variety of parameters possible. For now, choose a suitable function name and leave the defaults for Runtime (Node.js 18.x at time of writing) and Architecture (x86_64).

If you can't think of a name, choose something like `nodeless-example-api-handler`

Click the `Create function` button.

Replace the existing contents of `index.mjs` with the following

```js
import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import {
  DynamoDBDocumentClient,
  ScanCommand,
  PutCommand,
  UpdateCommand,
  GetCommand,
  DeleteCommand,
} from "@aws-sdk/lib-dynamodb";
import {LambdaClient, InvokeCommand, InvokeAsyncCommand} from "@aws-sdk/client-lambda";
import crypto from 'crypto';
import https from 'https';
const client = new DynamoDBClient({});
const dynamo = DynamoDBDocumentClient.from(client);
const lambdaclient = new LambdaClient({region:"us-east-1"});

// ---------- SET THESE VALUES AS ENVIRONMENT VARIALBES ----------- 
const nodelessStoreId = process.env.nodelessStoreId;
const nodelessApiKey = process.env.nodelessApiKey;
const nodelessWebhookSecret = process.env.nodelessWebhookSecret;
const dynamoTable = process.env.dynamoTable;

// part obfuscation, part recognizable words to reduce number transposition
function makeId(t) {
  let i1 = (t%2048);
  let i2 = (((t-i1)/2048)%2048);
  let i3 = (((((t-i1)/2048)-i2)/2048)%2048);
  let i4 = (((((((t-i1)/2048)-i2)/2048)-i3)/2048)%2048);
  let s = "";
  s += (b39[i1]+"98").substr(0,4);
  s += (b39[i2]+"76").substr(0,4);
  s += (b39[i3]+"54").substr(0,4);
  s += (b39[i4]+"32").substr(0,4);
  s = s.toUpperCase().split("").reverse().join("");
  s = s.substr(0,6) + "-" + s.substr(6,4) + "-" + s.substr(10,6);
  return s;
}

// Used for the MAZE2307 product type.
function getOverageBySize(metadata) {
  let overage = 0;
  let pixelAllotment = 2100000;
  let pixelBlockSize = 500000;
  let pixelBlockOverage = 500;
  let w = 1920;
  let h = 1080;
  if("width" in metadata) { w = metadata.width; }
  if("height" in metadata) { h = metadata.height; }
  let pixelcount = w*h;
  if(pixelcount > pixelAllotment) {
    let blocksOver = Math.ceil((pixelcount - pixelAllotment)/pixelBlockSize);
    overage = blocksOver * pixelBlockOverage;
  }
  return overage;  
}

function calcAmount(baseAmount, metadata, discount) {
  let finalAmount = baseAmount - discount;
  if("type" in metadata) {
    // custom for type of product
    if(metadata.type == "MAZE2307") {
      finalAmount = finalAmount + getOverageBySize(metadata);
    }
  }
  return finalAmount;
}

async function makeInvoice(satsAmount, orderId) {
  // https://nodeless.io/api/v1/store/{storeid}/invoice
  var payload = {
    "amount": satsAmount, 
    "currency": "SATS", 
    "metadata": {
      "orderId": orderId,
    }
  };
  var options = {
      host: 'nodeless.io',
      port: 443,
      path: '/api/v1/store/' + nodelessStoreId + '/invoice',
      method: 'POST',
      headers: {
          'Authorization': 'Bearer ' + nodelessApiKey,
          'Content-Type': 'application/json',
          'Accept': 'application/json',
      },
  };
  return new Promise((resolve,reject) => {
    const req = https.request(options, res => {
      let buffer = '';
      res.on('data', chunk => { buffer += chunk;});
      res.on('end', () => {
        try {
          resolve(JSON.parse(buffer));
        } catch (err) {
          reject(new Error(err));
        }
      });
    });
    req.on('error', err => {
      reject(new Error(err));
    });
    req.write(JSON.stringify(payload));
    req.end();
  });
}

async function getNodelessInvoice(id) {
  // https://nodeless.io/api/v1/store/{storeid}/invoice/{id}
  var options = {
      host: 'nodeless.io',
      port: 443,
      path: '/api/v1/store/' + nodelessStoreId + '/invoice/' + id + '/status',
      method: 'GET',
      headers: {
          'Authorization': 'Bearer ' + nodelessApiKey,
          'Content-Type': 'application/json',
          'Accept': 'application/json',
      },
  };
  return new Promise((resolve,reject) => {
    const req = https.request(options, res => {
      let buffer = '';
      res.on('data', chunk => { buffer += chunk;});
      res.on('end', () => {
        try {
          resolve(JSON.parse(buffer));
        } catch (err) {
          reject(new Error(err));
        }
      });
    });
    req.on('error', err => {
      reject(new Error(err));
    });
    req.end();
  });
}

function getValueCodeDiscount(c) {
  if(c == null) {
    return 0;
  }
  let valueCodes = process.env.valueCodes.split(",");
  let valueCodeIndex = 0;
  let valueCodesLength = valueCodes.length;
  for(valueCodeIndex=0; valueCodeIndex < valueCodesLength; valueCodeIndex ++) {
    let parameters = valueCodes[valueCodeIndex].split(':');
    let code = parameters[0];
    if(code == c && parameters.length > 1) {
      let discountAmount = parameters[1];
      if(parameters.length > 2) {
        let expirationTime = parameters[2];
        if (expirationTime > Date.now()) {
          return discountAmount;
        }
      } else {
        return discountAmount;
      }
    }
  }
  return 0;
}

function invokeBuilder(orderItem) {
  let functionName = null;
  // Map to the function to be called
  if(orderItem.metadata.type == "MAZE2307") {
    functionName = "build-maze-2307"; 
  }
  if(functionName == null) {
    console.log(`invokeBuilder called, but functionName could not be set from type: ${orderItem.metadata.type}`);
    return;
  }
  
  console.log(`Invoking lambda function: ${functionName}`);
  const input = { 
    FunctionName: functionName,
    InvocationType: "Event",
    LogType: "Tail",
    Payload: JSON.stringify({
      orderId: orderItem.id
    }),
  };
  const command = new InvokeCommand(input);
  const response = lambdaclient.send(command);
  console.log(`response object from invocation: ${JSON.stringify(response)}`);
}

export const handler = async (event, context) => {
  let body;
  let orderId;
  let orderItem;
  let statusCode = 200;
  let currentTimestamp = Date.now();
  
  const headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Headers": 'Content-Type,Authorization',
    "Access-Control-Allow-Methods": '*',      // CORS, allow any
    "Access-Control-Allow-Origin": '*',       // CORS, allow any
  };

  try {
    switch (event.routeKey) {
      case "OPTIONS":                                          // CORS PREFLIGHT
        break;
      case "POST /codes":                               // QUERY VALUE FOR VCODE
        body = {"discount":0};
        let codesData = JSON.parse(event.body);
        let vcode = codesData.vcode;
        body.discount = getValueCodeDiscount(vcode);
        break;
      case "GET /invoke/{id}":                       // INVOCATION TESTING ONLY
        orderId = event.pathParameters.id;
        orderItem = await dynamo.send(
          new GetCommand({
            TableName: dynamoTable,
            Key: {
              id: orderId,
            },
          })
        );
        orderItem = orderItem.Item;
        console.log("Calling invokeBuilder from GET /invoke/{id}")
        invokeBuilder(orderItem);      
        break;
      case "POST /nodeless":                                  // ACCEPT WEBHOOKS
        console.log("RECEIVED webhook call")
        // Authorization check with our secret
        let nodelessSig = event.headers["nodeless-signature"];
        if(nodelessSig.length == 0) {
          throw new Error(`nodeless-signature is missing`);
        }
        let hashedresult = crypto.createHmac(
          'sha256', 
          nodelessWebhookSecret,
        ).update(event.body).digest('hex');
        if(hashedresult != nodelessSig) {
          throw new Error(`nodeless-signature contains an unexpected value`);
        }
        // Proceed with storage to dynamo
        console.log("- store webhook in dynamo");
        let nodelessJSON = JSON.parse(event.body);
        await dynamo.send(
          new PutCommand({
            TableName: dynamoTable,
            Item: {
              id: "NODELESS-WH-" + nodelessJSON.uuid,
              time: currentTimestamp,
              amount: nodelessJSON.amount,
              metadata: nodelessJSON.metadata,
              status: nodelessJSON.status,
              uuid: nodelessJSON.uuid,
            },
          })
        );
        // Update order if status other than new
        if(nodelessJSON.status != "new") {
          console.log("- updatecommand because status is not new");
          orderId = nodelessJSON.metadata.orderId;
          let paidAt = null;
          if(nodelessJSON.status == "paid") {
              paidAt = currentTimestamp;
          }
          await dynamo.send(
            new UpdateCommand({
              TableName: dynamoTable,
              Key: {
                "id": orderId,
              },
              UpdateExpression: 'SET #i.#s = :s, updatedAt = :u, paidAt = :p',
              ExpressionAttributeNames: {
                '#i': 'invoice',
                '#s': 'status',
              },
              ExpressionAttributeValues: {
                ':s': nodelessJSON.status,
                ':u': currentTimestamp,
                ':p': paidAt,
              }
            })
          );
          // failing above this
          console.log("- get command to get full order");
          orderItem = await dynamo.send(
            new GetCommand({
              TableName: dynamoTable,
              Key: {
                id: orderId,
              },
            })
          );
          orderItem = orderItem.Item;
          console.log("- check if paid");
          if((orderItem.invoice.status == "paid") &&
             (orderItem.fulfillment.status == "pending")) {
               console.log("*** Calling invokeBuilder from POST /nodeless");
               invokeBuilder(orderItem);
          }
          
        }
        body = `Received item ${nodelessJSON.uuid}`;
        break;
      case "POST /orders":                                      // ACCEPT ORDERS
        let ordersJSON = JSON.parse(event.body);
        orderId = "ORDER-" + makeId(currentTimestamp);
        // Determine overall amount
        let discountAmount = getValueCodeDiscount(ordersJSON.discount.vcode);
        let satsAmount = calcAmount(7500, ordersJSON.metadata, discountAmount);
        // Use nodeless to make an invoice in the amount specified
        if(satsAmount > 0) {
          let nodelessInvoice = await makeInvoice(satsAmount, orderId);
          // Assemble item to insert into dynamo
          orderItem = {
            id: orderId,
            createdAt: currentTimestamp,
            updatedAt: currentTimestamp,
            discount: {
              code: ordersJSON.discount.vcode,
              amount: discountAmount,
            },
            invoice: {
              provider: "NODELESS",
              id: nodelessInvoice.data.id,
              satsAmount: nodelessInvoice.data.satsAmount,
              status: nodelessInvoice.data.status,
              createdAt: nodelessInvoice.data.createdAt,
              paidAt: null,
              lightningInvoice: nodelessInvoice.data.lightningInvoice,
              qrCode: nodelessInvoice.data.qrCodes.lightning,
            },
            metadata: ordersJSON.metadata,
            fulfillment: {
              status: "pending",
              url: null,
            },
          };
        } else {
          // The satsAmount is <= 0. Insert as paid
          orderItem = {
            id: orderId,
            createdAt: currentTimestamp,
            updatedAt: currentTimestamp,
            discount: {
              code: ordersJSON.discount.vcode,
              amount: discountAmount,
            },
            invoice: {
              provider: "NONE",
              id: 'not-applicable',
              satsAmount: 0,
              status: 'paid',
              createdAt: currentTimestamp,
              paidAt: currentTimestamp,
              lightningInvoice: null,
              qrCode: null,
            },
            metadata: ordersJSON.metadata,
            fulfillment: {
              status: "pending",
              url: null,
            },
          };
        }
        // Save to dynamo table
        await dynamo.send(
          new PutCommand({
            TableName: dynamoTable,
            Item: orderItem,
          })
        );
        // Prep response
        body = {
          "id": orderItem.id, 
          "status": orderItem.invoice.status, 
          "satsAmount": orderItem.invoice.satsAmount,
          "storeInvoiceId": orderItem.invoice.id,
          "lightningInvoice": orderItem.invoice.lightningInvoice,
          "qrCode": orderItem.invoice.qrCode,
          "metadata": orderItem.metadata,
          "fulfillment": orderItem.fulfillment,
        };
        break;
      case "GET /orders/{id}":                             // CHECK ORDER STATUS
      case "GET /orders/{id}/detailed":
        orderId = event.pathParameters.id;
        orderItem = await dynamo.send(
          new GetCommand({
            TableName: dynamoTable,
            Key: {
              id: orderId,
            },
          })
        );
        orderItem = orderItem.Item;
        if(event.routeKey == "GET /orders/{id}/detailed") {
          body = {
            "id": orderItem.id, 
            "status": orderItem.invoice.status,
            "satsAmount": orderItem.invoice.satsAmount,
            "lightningInvoice": orderItem.invoice.lightningInvoice,
            "qrCode": orderItem.invoice.qrCode,
            "metadata": orderItem.metadata,
            "fulfillment": orderItem.fulfillment,
          };
        } else {
          body = {
            "s": orderItem.invoice.status.substr(0,1), 
          };
          if(orderItem.fulfillment.status != "pending") {
            body.fs = orderItem.fulfillment.status.substr(0,1);
          }
          if(orderItem.fulfillment.url != null) {
            body.fu = orderItem.fulfillment.url;
          }
        }
        
        if(orderItem.invoice.satsAmount == 0 && orderItem.invoice.status == 'paid') {
          console.log("Calling invokeBuilder from GET /orders/{id} for FREE item")
          invokeBuilder(orderItem);
        } else {
          // If last update was more than 10 seconds ago, check for update
          if(orderItem.updatedAt + 10000 < currentTimestamp) {
            let nodelessInvoice = await getNodelessInvoice(orderItem.invoice.id);
            let lastUpdated = orderItem.updatedAt;
            let paidAt = orderItem.invoice.paidAt;
            if ((orderItem.invoice.status != nodelessInvoice.status) &&
                (nodelessInvoice.status == 'paid')) {
              orderItem.invoice.paidAt = currentTimestamp;
              console.log("Calling invokeBuilder from GET /orders/{id}")
              invokeBuilder(orderItem);
            }
            orderItem.updatedAt = currentTimestamp;
            orderItem.invoice.status = nodelessInvoice.status;
            if(event.routeKey == "GET /orders/{id}/detailed") {
              body.status = nodelessInvoice.status;
            } else {
              body.s = nodelessInvoice.status.substr(0,1);
            }
            await dynamo.send(
              new UpdateCommand({
                TableName: dynamoTable,
                Key: {
                  "id": orderItem.id,
                },
                UpdateExpression: 'SET #i.#s = :s, updatedAt = :u, paidAt = :p',
                ConditionExpression: "updatedAt = :t",
                ExpressionAttributeNames: {
                  '#i': 'invoice',
                  '#s': 'status',
                },
                ExpressionAttributeValues: {
                  ':s': orderItem.invoice.status,
                  ':u': currentTimestamp,
                  ':p': paidAt,
                  ':t': lastUpdated,
                }
              })
            );
          }
        }
        break;
      default:
        throw new Error(`Unsupported route: "${event.routeKey}"`);
    }
  } catch (err) {
    statusCode = 400;
    body = err.message;
  } finally {
    body = JSON.stringify(body);
  }

  return {
    statusCode,
    body,
    headers,
  };
};

const b39=`abandon ability able about above absent absorb abstract absurd abuse 
access accident account accuse achieve acid acoustic acquire across act action 
actor actress actual adapt add addict address adjust admit adult advance advice
aerobic affair afford afraid again age agent agree ahead aim air airport aisle
alarm album alcohol alert alien all alley allow almost alone alpha already
also alter always amateur amazing among amount amused analyst anchor ancient
anger angle angry animal ankle announce annual another answer antenna antique
anxiety any apart apology appear apple approve april arch arctic area arena
argue arm armed armor army around arrange arrest arrive arrow art artefact
artist artwork ask aspect assault asset assist assume asthma athlete atom
attack attend attitude attract auction audit august aunt author auto autumn
average avocado avoid awake aware away awesome awful awkward axis baby bachelor
bacon badge bag balance balcony ball bamboo banana banner bar barely bargain
barrel base basic basket battle beach bean beauty because become beef before
begin behave behind believe below belt bench benefit best betray better between
beyond bicycle bid bike bind biology bird birth bitter black blade blame blanket
blast bleak bless blind blood blossom blouse blue blur blush board boat body
boil bomb bone bonus book boost border boring borrow boss bottom bounce box
boy bracket brain brand brass brave bread breeze brick bridge brief bright
bring brisk broccoli broken bronze broom brother brown brush bubble buddy
budget buffalo build bulb bulk bullet bundle bunker burden burger burst bus
business busy butter buyer buzz cabbage cabin cable cactus cage cake call calm
camera camp can canal cancel candy cannon canoe canvas canyon capable capital
captain car carbon card cargo carpet carry cart case cash casino castle casual
cat catalog catch category cattle caught cause caution cave ceiling celery
cement census century cereal certain chair chalk champion change chaos chapter
charge chase chat cheap check cheese chef cherry chest chicken chief child
chimney choice choose chronic chuckle chunk churn cigar cinnamon circle citizen
city civil claim clap clarify claw clay clean clerk clever click client cliff
climb clinic clip clock clog close cloth cloud clown club clump cluster clutch
coach coast coconut code coffee coil coin collect color column combine come
comfort comic common company concert conduct confirm congress connect consider
control convince cook cool copper copy coral core corn correct cost cotton
couch country couple course cousin cover coyote crack cradle craft cram crane
crash crater crawl crazy cream credit creek crew cricket crime crisp critic
crop cross crouch crowd crucial cruel cruise crumble crunch crush cry crystal
cube culture cup cupboard curious current curtain curve cushion custom cute
cycle dad damage damp dance danger daring dash daughter dawn day deal debate
debris decade december decide decline decorate decrease deer defense define
defy degree delay deliver demand demise denial dentist deny depart depend
deposit depth deputy derive describe desert design desk despair destroy detail
detect develop device devote diagram dial diamond diary dice diesel diet differ
digital dignity dilemma dinner dinosaur direct dirt disagree discover disease
dish dismiss disorder display distance divert divide divorce dizzy doctor
document dog doll dolphin domain donate donkey donor door dose double dove
draft dragon drama drastic draw dream dress drift drill drink drip drive drop
drum dry duck dumb dune during dust dutch duty dwarf dynamic eager eagle early
earn earth easily east easy echo ecology economy edge edit educate effort egg
eight either elbow elder electric elegant element elephant elevator elite else
embark embody embrace emerge emotion employ empower empty enable enact end
endless endorse enemy energy enforce engage engine enhance enjoy enlist enough
enrich enroll ensure enter entire entry envelope episode equal equip era erase
erode erosion error erupt escape essay essence estate eternal ethics evidence
evil evoke evolve exact example excess exchange excite exclude excuse execute
exercise exhaust exhibit exile exist exit exotic expand expect expire explain
expose express extend extra eye eyebrow fabric face faculty fade faint faith
fall false fame family famous fan fancy fantasy farm fashion fat fatal father
fatigue fault favorite feature february federal fee feed feel female fence
festival fetch fever few fiber fiction field figure file film filter final
find fine finger finish fire firm first fiscal fish fit fitness fix flag flame
flash flat flavor flee flight flip float flock floor flower fluid flush fly
foam focus fog foil fold follow food foot force forest forget fork fortune
forum forward fossil foster found fox fragile frame frequent fresh friend
fringe frog front frost frown frozen fruit fuel fun funny furnace fury future
gadget gain galaxy gallery game gap garage garbage garden garlic garment gas
gasp gate gather gauge gaze general genius genre gentle genuine gesture ghost
giant gift giggle ginger giraffe girl give glad glance glare glass glide glimpse
globe gloom glory glove glow glue goat goddess gold good goose gorilla gospel
gossip govern gown grab grace grain grant grape grass gravity great green grid
grief grit grocery group grow grunt guard guess guide guilt guitar gun gym
habit hair half hammer hamster hand happy harbor hard harsh harvest hat have
hawk hazard head health heart heavy hedgehog height hello helmet help hen hero
hidden high hill hint hip hire history hobby hockey hold hole holiday hollow
home honey hood hope horn horror horse hospital host hotel hour hover hub huge
human humble humor hundred hungry hunt hurdle hurry hurt husband hybrid ice
icon idea identify idle ignore ill illegal illness image imitate immense immune
impact impose improve impulse inch include income increase index indicate
indoor industry infant inflict inform inhale inherit initial inject injury
inmate inner innocent input inquiry insane insect inside inspire install intact
interest into invest invite involve iron island isolate issue item ivory jacket
jaguar jar jazz jealous jeans jelly jewel job join joke journey joy judge juice
jump jungle junior junk just kangaroo keen keep ketchup key kick kid kidney
kind kingdom kiss kit kitchen kite kitten kiwi knee knife knock know lab label
labor ladder lady lake lamp language laptop large later latin laugh laundry
lava law lawn lawsuit layer lazy leader leaf learn leave lecture left leg legal
legend leisure lemon lend length lens leopard lesson letter level liar liberty
library license life lift light like limb limit link lion liquid list little
live lizard load loan lobster local lock logic lonely long loop lottery loud
lounge love loyal lucky luggage lumber lunar lunch luxury lyrics machine mad
magic magnet maid mail main major make mammal man manage mandate mango mansion
manual maple marble march margin marine market marriage mask mass master match
material math matrix matter maximum maze meadow mean measure meat mechanic
medal media melody melt member memory mention menu mercy merge merit merry
mesh message metal method middle midnight milk million mimic mind minimum minor
minute miracle mirror misery miss mistake mix mixed mixture mobile model modify
mom moment monitor monkey monster month moon moral more morning mosquito mother
motion motor mountain mouse move movie much muffin mule multiply muscle museum
mushroom music must mutual myself mystery myth naive name napkin narrow nasty
nation nature near neck need negative neglect neither nephew nerve nest net
network neutral never news next nice night noble noise nominee noodle normal
north nose notable note nothing notice novel now nuclear number nurse nut oak
obey object oblige obscure observe obtain obvious occur ocean october odor off
offer office often oil okay old olive olympic omit once one onion online only
open opera opinion oppose option orange orbit orchard order ordinary organ
orient original orphan ostrich other outdoor outer output outside oval oven
over own owner oxygen oyster ozone pact paddle page pair palace palm panda
panel panic panther paper parade parent park parrot party pass patch path
patient patrol pattern pause pave payment peace peanut pear peasant pelican
pen penalty pencil people pepper perfect permit person pet phone photo phrase
physical piano picnic picture piece pig pigeon pill pilot pink pioneer pipe
pistol pitch pizza place planet plastic plate play please pledge pluck plug
plunge poem poet point polar pole police pond pony pool popular portion position
possible post potato pottery poverty powder power practice praise predict
prefer prepare present pretty prevent price pride primary print priority prison
private prize problem process produce profit program project promote proof
property prosper protect proud provide public pudding pull pulp pulse pumpkin
punch pupil puppy purchase purity purpose purse push put puzzle pyramid quality
quantum quarter question quick quit quiz quote rabbit raccoon race rack radar
radio rail rain raise rally ramp ranch random range rapid rare rate rather
raven raw razor ready real reason rebel rebuild recall receive recipe record
recycle reduce reflect reform refuse region regret regular reject relax release
relief rely remain remember remind remove render renew rent reopen repair
repeat replace report require rescue resemble resist resource response result
retire retreat return reunion reveal review reward rhythm rib ribbon rice rich
ride ridge rifle right rigid ring riot ripple risk ritual rival river road
roast robot robust rocket romance roof rookie room rose rotate rough round
route royal rubber rude rug rule run runway rural sad saddle sadness safe sail
salad salmon salon salt salute same sample sand satisfy satoshi sauce sausage
save say scale scan scare scatter scene scheme school science scissors scorpion
scout scrap screen script scrub sea search season seat second secret section
security seed seek segment select sell seminar senior sense sentence series
service session settle setup seven shadow shaft shallow share shed shell sheriff
shield shift shine ship shiver shock shoe shoot shop short shoulder shove
shrimp shrug shuffle shy sibling sick side siege sight sign silent silk silly
silver similar simple since sing siren sister situate six size skate sketch
ski skill skin skirt skull slab slam sleep slender slice slide slight slim
slogan slot slow slush small smart smile smoke smooth snack snake snap sniff
snow soap soccer social sock soda soft solar soldier solid solution solve
someone song soon sorry sort soul sound soup source south space spare spatial
spawn speak special speed spell spend sphere spice spider spike spin spirit
split spoil sponsor spoon sport spot spray spread spring spy square squeeze
squirrel stable stadium staff stage stairs stamp stand start state stay steak
steel stem step stereo stick still sting stock stomach stone stool story stove
strategy street strike strong struggle student stuff stumble style subject
submit subway success such sudden suffer sugar suggest suit summer sun sunny
sunset super supply supreme sure surface surge surprise surround survey suspect
sustain swallow swamp swap swarm swear sweet swift swim swing switch sword
symbol symptom syrup system table tackle tag tail talent talk tank tape target
task taste tattoo taxi teach team tell ten tenant tennis tent term test text
thank that theme then theory there they thing this thought three thrive throw
thumb thunder ticket tide tiger tilt timber time tiny tip tired tissue title
toast tobacco today toddler toe together toilet token tomato tomorrow tone
tongue tonight tool tooth top topic topple torch tornado tortoise toss total
tourist toward tower town toy track trade traffic tragic train transfer trap
trash travel tray treat tree trend trial tribe trick trigger trim trip trophy
trouble truck true truly trumpet trust truth try tube tuition tumble tuna
tunnel turkey turn turtle twelve twenty twice twin twist two type typical ugly
umbrella unable unaware uncle uncover under undo unfair unfold unhappy uniform
unique unit universe unknown unlock until unusual unveil update upgrade uphold
upon upper upset urban urge usage use used useful useless usual utility vacant
vacuum vague valid valley valve van vanish vapor various vast vault vehicle
velvet vendor venture venue verb verify version very vessel veteran viable
vibrant vicious victory video view village vintage violin virtual virus visa
visit visual vital vivid vocal voice void volcano volume vote voyage wage wagon
wait walk wall walnut want warfare warm warrior wash wasp waste water wave way
wealth weapon wear weasel weather web wedding weekend weird welcome west wet
whale what wheat wheel when where whip whisper wide width wife wild will win
window wine wing wink winner winter wire wisdom wise wish witness wolf woman
wonder wood wool word work world worry worth wrap wreck wrestle wrist write
wrong yard year yellow you young youth zebra zero zone zoo`.split(/\s+/);
```

Once pasted, click the "Deploy" button in the menu bar

Thats a fairly lengthy file. Here's a summary of each function's purpose:

- makeId(timestamp) - converts a unix epoch time to words from the bip39 word list, reversed, and hyphenated
- getOverageBySize(metadata) - For image products, a trivial formula for paying based on resulting size and computation
- calcAmount(baseAmount, metadata, discount) - Based on the product type being ordered, the total can be increased based on order info
- makeInvoice(satsAmount, orderId) - Calls nodeless.io to create an invoice for the given amount
- getNodelessInvoice(id) - Using the nodeless invoice id, lookup the status of the invoice
- getValueCodeDiscount(code) - If a discount code was given, this function will determine if its valid (and not expired) and returns the discount amount to apply
- invokeBuilder(orderItem) - once an order has been paid for, this function calls a separate lambda to build the product in the background. There is hardcoding here that maps a product type `MAZE2307` to a function `build-maze-2307` that could be made more dynamic by lookup in dynamo table or other resource, but for simplicity is retained structured in the example

Following functions you'll see two constants

- export const handler - This is the entry point into the lambda and from which the functions above are called along with the intended API spec
- b39 - This is the bip39 word list, delimited by spaces, then split into a list for reference by the makeId function

### Configuration for Lambda

After saving the code for the lambda function. Click the `Configuration` tab. If not already presented with the environment variables, choose `Environment Variables` from the menu on the left.

This lambda function expects 5 environment variables to be setup as follows:

- dynamoTable - The name of the dynamo table created previously for this example (e.g. nodeless-example-orders)
- nodelessApiKey - The API Token you received from Nodeless.io
- nodelessStoreId - The store id for your store at Nodeless.io
- nodelessWebookSecret - The Webhook secret for your store at Nodeless.io
- valueCodes - For no discounts, just define as an empty string.  If you want to give discounts, then each discount code is comma delimted, and for each code configuration is colon delimited.  For example the value `CODE1:1000,CODE2:2000:1696118400` defines two codes (CODE1 and CODE2), where the first gives a discount of 1000 and the second 2000. The third argument on the second discount is an expiry time as defined in unix timestamp in seconds

Yes, I'm aware there are other ways to abstract out secrets such as the AWS Secrets Manager. For simplicity and reducing number of services needing to setup for this example they've been kept local.

Next, switch to the `General Configuration` tab.  Click `Edit`, and set memory to 128 MB and the Timeout to 5 seconds. Click `Save` to apply the changes.

## AWS: Create Lambda for Building Order

The previous lambda is somewhat general purpose to facilitate order placement.  This lambda is focused on work for the MAZE2307 product type mapped to a function named build-maze-2307.  

Another point of interest about this lambda, is that we'll be using a different runtime, accompanied by custom layers.  This sample leverages code from the [Nodeyez codebase](https://github.com/vicariousdrama/nodeyez), and as such requires using Python, and having available some key packages that do not come with the Python runtime by default.

In the AWS Console, access the [AWS Lambda Functions](https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/functions).

Click the [Create Function](https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/create/function) button in the upper right corner.

For function name, specify `build-maze-2307`. This should match the value referenced by the invokeBuilder function in the nodeless-example-api-handler

For Runtime, choose Python 3.10. And keep x86_64 as the architecture.

Click the `Create function` button.

Replace the existing contents of `lamba_function.py` with the following

```python
from scripts.blockhashdungeon import BlockHashDungeonPanel
from decimal import Decimal
import boto3 # for dynamo, s3
import hashlib
import json
import os
import requests
import sys
from urllib3.exceptions import InsecureRequestWarning

s3Client = boto3.client('s3')
s3Bucket = os.environ['s3Bucket']
dynamoClient = boto3.resource('dynamodb')
dynamoTable = os.environ['dynamoTable']

# Layers needed
#   arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p310-Pillow:2
#   arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p310-numpy:2
#   arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p310-requests:3
#   arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p310-boto3:3

def getOrderInfo(orderId):
    # get record from dynamo
    print(f'retrieving {orderId} from table: {dynamoTable}')
    data = dynamoClient.Table(dynamoTable).get_item(
        Key={
            'id': orderId 
        },
        ProjectionExpression='metadata, fulfillment, invoice'
    )
    orderInfo = data['Item']
    return dict(orderInfo)

def getBitcoinBlockhash(blocknumber):
    url = f'https://blockstream.info/api/block-height/{blocknumber}'
    proxies = {}
    headers = {}
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    output = requests.get(url=url,timeout=2,proxies=proxies,headers=headers).text
    return output

def setFulfillmentStatus(orderId, status, fulfillmentUrl = None):
    data = dynamoClient.Table(dynamoTable).update_item(
        Key={'id':orderId},
        UpdateExpression="SET #f.#s=:fs, #f.#u=:fu",
        ExpressionAttributeNames={
            '#f': 'fulfillment',
            '#s': 'status',
            '#u': 'url',
        },
        ExpressionAttributeValues={
            ':fs': status,
            ':fu': fulfillmentUrl,
        }
    )

def storeOrderImageInS3(filepath, orderId):
    s3Path = f'orders/maze2307/{orderId}.png'
    url = f'https://{s3Bucket}.s3.amazonaws.com/{s3Path}'
    s3Client.upload_file(Filename=filepath, Bucket=s3Bucket, Key=s3Path)
    print(f'uploaded file to s3 bucket. accessible at {url}')
    return url

def lambda_handler(event, context):
    weAreBuilding=False
    orderId = ""
    if "orderId" in event: orderId= event["orderId"]

    try:
        # defaults
        blockheight = 777777
        seedtype = 'blockheight'
        width = 1920
        height = 1080
        usertext = ''
        
        # Load the order
        if "orderId" not in event:
            raise Exception(f'orderId was not passed in event. event looks like {event}')
        orderInfo = getOrderInfo(orderId)
        if "metadata" not in orderInfo:
            raise Exception('metadata was not present on order')
        if "type" not in orderInfo["metadata"]:
            raise Exception('metadata.type was not present on order')
        if orderInfo["metadata"]["type"] != "MAZE2307":
            raise Exception('metadata.type was not expected value for this processor')
        if "invoice" not in orderInfo:
            raise Exception('order has no invoice')
        if "status" not in orderInfo["invoice"]:
            raise Exception('invoice.status was not present on order')
        if orderInfo["invoice"]["status"] != 'paid':
            raise Exception('order status is not paid')
        if "fulfillment" not in orderInfo:
            raise Exception('order has no fulfillment tracking')
        if "status" not in orderInfo["fulfillment"]:
            raise Exception('order has no fulfillment.status tracking')
        fulfillmentStatus = orderInfo["fulfillment"]["status"]
        match fulfillmentStatus:
            case 'pending':
                pass # continue building
            case 'building':
                return {
                    'statusCode': 200,
                    'body': json.dumps("Order is being built by another process")
                }
            case 'done':
                return {
                    'statusCode': 200,
                    'body': json.dumps("Order was completed by another process")
                }
            case other:
                raise Exception(f"unrecognized fulfillment status: {order.fulfillment.status}")

        # Update values based on order
        if "seedtype" in orderInfo["metadata"]:
            seedtype = orderInfo["metadata"]["seedtype"]
        if "width" in orderInfo["metadata"]:
            width = orderInfo["metadata"]["width"]
        if "height" in orderInfo["metadata"]:
            height = orderInfo["metadata"]["height"]
        if "bitcoin" in orderInfo["metadata"]:
            if "blockheight" in orderInfo["metadata"]["bitcoin"]:
                blockheight = orderInfo["metadata"]["bitcoin"]["blockheight"]
        if "usertext" in orderInfo["metadata"]:
            usertext = orderInfo["metadata"]["usertext"]

        # Sanity check the dimensions
        if int(width) > 3840: width = 3840       # 4K limit (8k too much recursion)
        if int(height) > 2160: height = 2160
        if int(width) < 480: width = 480
        if int(height) < 320: height = 320
        
        # Setup the panel
        p = BlockHashDungeonPanel()
        p.watermarkEnabled = False
        p.width = int(width)
        p.height = int(height)
        if seedtype == 'blockheight':
            p.blocknumber = int(blockheight)
            p.blockhash = getBitcoinBlockhash(p.blocknumber)
            p.headerText = f"Blockhash Dungeon|Level {p.blocknumber}"
        if seedtype == 'usertext':
            s = orderInfo["metadata"]["usertext"]
            p.headerText = s
            p.blockhash = hashlib.sha256(s.encode()).hexdigest()
            if(len(s) == 0): p.headerEnabled = 

        # Indicate we are building
        weAreBuilding=True
        setFulfillmentStatus(orderId, 'building')

        # Run it
        p.run()
        
        # Upload file to S3 
        #   from:   (/tmp/blockhashdungeon.png)
        #   to:     {s3bucket}/orderid.png
        url = storeOrderImageInS3('/tmp/blockhashdungeon.png', orderId)

        # Indicate we are done
        setFulfillmentStatus(orderId, 'done', url)
                
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        errs = f"Unexpected {err=}, {type(err)=}"
        print(errs)
        # revert as needed
        if weAreBuilding:
            setFulfillmentStatus(orderId, 'pending')
        return {
            'statusCode': 500,
            'body': json.dumps(errs)
        }

    # All good if reached here
    return {
        'statusCode': 200,
        'body': json.dumps(f'Finished! The file is available at {url}')
    }
```

In the file tree to the left, right click on the function name and choose `New Folder` from the menu.  Create folders for each of the following

- config
- data
- imageoutput
- images
- mock-data
- scripts




### Adding Layers

We will need to add layers for Pillow, numpy, requests, and boto3.  

For each of these, click Add a layer.  Then choose `Specify an ARN`, and provide the necessary ARN before clicking Add.

- arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p310-Pillow:2
- arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p310-numpy:2
- arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p310-requests:3
- arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p310-boto3:3

### Configuration for Lambda

After saving the code for the lambda function. Click the `Configuration` tab. 

If not already presented with the environment variables, choose `Environment Variables` from the menu on the left.

This lambda function expects 5 environment variables to be setup as follows:

- dynamoTable - The name of the dynamo table created previously for this example (e.g. nodeless-example-orders)
- s3Bucket - The name of the s3 bucket previously established for storing the output (e.g. nodeless-maze-2307)

Next, switch to the `General Configuration` tab.  Click `Edit`, and set memory to 256 MB and the Timeout to 30 seconds. Click `Save` to apply the changes.


  
-----

On step two, click next. We don't have the lambda setup for integration target, so no routes will be defined yet and we will come back to it.


On step two, define the routes.  For this example we need routes for the following
- /
  - OPTIONS
- /codes
  - POST
- /nodeless
  - POST
- /orders
  - POST
  - /{id}
    - GET
    - /detailed
      - GET
