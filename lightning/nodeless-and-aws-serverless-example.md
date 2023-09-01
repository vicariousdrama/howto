# Nodeless and AWS Serverless Example
_An example of integrating AWS Serverless with Nodeless.io and accepting payments_

by @vicariousdrama

805752-??????


---

The steps at a high level

1. Register/Login to Nodeless.io
2. Register/Login to Setup AWS.com account
3. Nodeless: Setup Withdraw Settings
4. Nodeless: Create Store
5. Nodeless: Create API Token
6. AWS: Create API Gateway for Access
7. Nodeless: Create Webhook
8. AWS: Create s3 Bucket
9. AWS: Create Dynamo Table
10. AWS: Create Lambda for Nodeless Webhook and Order Processing
11. AWS: Create Lambda for Building Order
12. Modify Order Form with Endpoint
13. AWS: Upload Static Order Form Page to Bucket
14. AWS: Edit API Gateway for Access
15. AWS: Set any Roles and Policies

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

Amazon Web Services have been around for nearly two decades and is a leader in serverless technology.  This example will make use of API Gateway, DynamoDB, Lambda Functions and an s3 Bucket.

If you haven't already done so, [create an account](https://portal.aws.amazon.com/gp/aws/developer/registration/index.html) or [login](https://console.aws.amazon.com/console/home) to the console.

## Nodeless: Setup Withdraw Settings

From the Administration submenu on the left, choose `Withdraw`.  Then pick the Withdraw Settings.

Modify the settings on this page as appropriate to setup your Lightning Address and an On-chain Address. I recommend the Lightning Address as teh default payment method.

## Nodeless: Create Store

If you don't have an existing Nodeless Store, you can add a new one by clicking `Store` from the Payment submenu on the left, then the `Add Store` button in the upper right. Provide a name for the store.

Once you have a store you plan to use, make note of its ID.  This is the UUID looking identifier in the address bar, and a convenient copy button is provided next to the store name.

In this example, my store name is `test-store`, and the ID is `d809bb04-bb3a-4d84-8f75-eba51397e88a`. The copy link shows the first few characters

![image](https://github.com/vicariousdrama/howto/assets/88121568/606860f2-67ea-4e7f-8b2c-52d5190bd03b)

We will come back to this later to setup the webbook after defining the API Gateway for Access in AWS.

## Nodeless: Create API Token

From within Nodeless, click on your `Profile` from the App menu on the left, or from the dropdown on your email address in the upper right corner.

Next, select the `API Tokens` submenu on the Settings page of profile.

Click the button to `Generate Keys` and provide a label.  For this example, I just put `nodeless-example-apikey`

The API token value will be displayed. This is the only time it is displayed. You should save this to some place you can access it later. You will need it when continuing setup with the AWS Lambda function.

## AWS: Create s3 Bucket

The simple storage solution (s3) is where resulting products will be saved when generated, and permissions setup to allow accessing them over the web.

In the AWS Console, access [Amazon S3](https://s3.console.aws.amazon.com/s3/home?region=us-east-1#).

Click the [Create bucket](https://s3.console.aws.amazon.com/s3/bucket/create?region=us-east-1) button in the upper right corner.

You'll need to provide a bucket name.  The name itself doesn't matter but must be unique in the global namespace.  The global namespace is shared across all AWS accounts (nuts, I know, but S3 is like the granddaddy of serverless and they weren't considering namespaces at that time).  In the example below, I use the bucket name `nodeless-data-1693591359`, but you can just as easily use any bucket name, as long as its consistent. I do recommend logical naming, so perhaps you will go with `nodeless-data-` followed by numbers as a suffix. You could use your AWS account number, or the [Unix Epoch Time](https://www.epochconverter.com/). Whatever it takes to still be meaningful and unique.

Configure it as a public access bucket by **unchecking** the box labeled `Block all public access`, and also check the box below to acknowledge those settings might result in the bucket and objects within becoming public.

Leave the rest of the settings default and click `Create bucket` button at the bottom of the page.

On the [Amazon S3 Buckets page](https://s3.console.aws.amazon.com/s3/buckets?region=us-east-1&region=us-east-1), click your newly created bucket.  Then navigate to the `Permissions` view.  Verify that it has public access, and the Bucket Policy looks something like this

```json
{
    "Version": "2008-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": {
                "AWS": "*"
            },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::nodeless-data-1693591359/*"
        }
    ]
}
```

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

In the URL field, specify the value of the Invoke URL from the API Gateway, with the path appended as `/nodeless`. 

For example, my Invoke URL was `https://eahilxrhrg.execute-api.us-east-1.amazonaws.com`.

The URL I specify is `https://eahilxrhrg.execute-api.us-east-1.amazonaws.com/nodeless`

Make note of the generated Secret value.  You'll need to capture this and use in configuration later to properly validate signed messages sent from Nodeless to the webhook endpoint.

Choose these events
- Invoice Created
- Invoice Paid
- Invoice Expired

Click the `Save` button when complete.

At this point, you've setup everything needed on the Nodeless side, and you'll only need to come back to Nodeless to debug or trace orders.

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

Replace the existing contents of `index.mjs` with that from [nodeless-example/index.mjs](../nodeless-example/index.mjs)

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
- s3Bucket - The name of the s3 bucket previously established for storing the output (e.g. nodeless-data-1693591359)

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
