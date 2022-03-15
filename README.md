# lambda-slack-integration
Send a message through lambda to Slack when a new image is added into a s3 bucket

*Steps to configure* :
  1) Add a new incoming webhook in slack and add the channel where you want to receive the message. Go to api.slack.com - features - incoming webhook (incoming_url)
  2) Create a new lambda function, copy the code in : lambda_send_img_slack.py
  3) Add an env. var. in the lambda function : SLACK_URL and in the value paste (incoming_url)
  4) Create an S3 bucket (ex: slack_images) with public access and this bicket policy:
     {
        "Version": "2008-10-17",
        "Statement": [
            {
                "Sid": "AllowPublicRead",
                "Effect": "Allow",
                "Principal": {
                    "AWS": "*"
                },
                "Action": "s3:GetObject",
                "Resource": "arn:aws:s3:::slack-app-images/*"
            }
        ]
     }
  6) In the lambda create a new trigger from that S3, ObjectCreated event
 
 *Run the process*:
  Go to the S3 bucket and add a new image. 
  That action fires a trigger in the lambda function, to create the message and send that to the Slack channel.
  
