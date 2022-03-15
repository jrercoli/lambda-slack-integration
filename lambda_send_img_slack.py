import os
import json
import urllib.parse
import boto3
import time
import requests

print('Loading function')

s3 = boto3.client('s3')

slack_url = os.environ['SLACK_URL']

headers = {
    'Content-Type': "application/json"
    }


def build_payload(obj_key, obj_url):
    
    payload = """{{
        "channel": "{0}",
        "username": "{1}",
        "text": "{2}",
        "icon_emoji": "{3}"
    }}
    """.format("#aws-lambda", "s3imageserver", "Provided by AWS lambda: send-new-img-s3-to-slack \n added image: "+ obj_key + " url: "+ obj_url, ":parachute:")
    
    return payload

def build_new_payload(obj_key, obj_url):
    my_slack_block = [
        {
    		"type": "section",
    		"text": {
    			"type": "mrkdwn",
    			"text": ":parachute: *S3-Lambda-ImageServer* send you a message:"
    		}
    	},
    	{
			"type": "section",
			"block_id": "section567",
			"text": {
				"type": "mrkdwn",
				"text": "<https://www.nytimes.com/interactive/2022/world/europe/ukraine-maps.html|NY Times, tracking the Russian invasion of Ukraine>"
			},
			"accessory": {
				"type": "image",
				"image_url": "https://static01.nyt.com/newsgraphics/2022/02/18/russia-ukraine-livepage/61e9f58a70151d65b663ca1703611e075dae201a/ukraine-fronts-900.jpg",
				"alt_text": "Status of the Russian invasion"
			}
		},
		{
    		"type": "section",
    		"text": {
    			"type": "mrkdwn",
    			"text": "<" + obj_url + "|added image in S3 bucket>"
    		}
    	}
    ]
    
    payload = """{{
        "blocks": {0}
    }}
    """.format(my_slack_block)
    
    return payload

def lambda_handler(event, context):
    # Event received from S3 put object
    # print("Received event: " + json.dumps(event, indent=2))

    # Get some properties of the object from the event 
    bucket = event['Records'][0]['s3']['bucket']['name']
    region = event['Records'][0]['awsRegion']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    # Get the url from the S3 object
    # location = s3.get_bucket_location(Bucket=bucket)['LocationConstraint']
    obj_url = f'https://{bucket}.s3.{region}.amazonaws.com/{key}'
    
    # Build payload with added obj name (key)
    payload = build_new_payload(key, obj_url)
    
    try:
        s3_response = s3.get_object(Bucket=bucket, Key=key)
        
        print("CONTENT TYPE: " + s3_response['ContentType'])
        print(key)
        print(event['Records'][0]['s3']['object'])
        
        # send request to Slack through 
        response = requests.request("POST", slack_url, data=payload, headers=headers)
        
        return s3_response['ContentType']
        
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e


