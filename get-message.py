#!/usr/bin/python3

import boto3
from botocore.exceptions import ClientError
import requests
import json

# Set up your SQS queue URL and boto3 client
url = "https://sqs.us-east-1.amazonaws.com/440848399208/rde6mn"
sqs = boto3.client('sqs')
listE = []
listM = []
def delete_message(handle):
    try:
        # Delete message from SQS queue
        sqs.delete_message(
            QueueUrl=url,
            ReceiptHandle=handle
        )
        print("Message deleted")
    except ClientError as e:
        print(e.response['Error']['Message'])

def get_message():
    
        try:
            # Receive message from SQS queue. Each message has two MessageAttributes: order and word
            # You want to extract these two attributes to reassemble the message
            response = sqs.receive_message(
                QueueUrl=url,
                AttributeNames=[
                    'All'
                ],
                MaxNumberOfMessages=1,
                MessageAttributeNames=[
                    'All'
                ]
            )
            # Check if there is a message in the queue or not
            if "Messages" in response:
                # extract the two message attributes you want to use as variables
                # extract the handle for deletion later
                order = response['Messages'][0]['MessageAttributes']['order']['StringValue']
                word = response['Messages'][0]['MessageAttributes']['word']['StringValue']
                #deletes message
                handle = response['Messages'][0]['ReceiptHandle']

                # Print the message attributes - this is what you want to work with to reassemble the message
                print(f"Order: {order}")
                print(f"Word: {word}")
                print(f"Handle: {handle}")

                listE.append([order, f"Order: {order}", f"Word: {word}", handle])
                delete_message(handle)

            # If there is no message in the queue, print a message and exit    
            else:
                print("No message in the queue")
                listE.sort()
                print(listE)
                for m in listE:
                    listM.append([m[1],m[2]])
                    

                print(listM)

                exit(1)
                
        # Handle any errors that may occur connecting to SQS
        except ClientError as e:
            print(e.response['Error']['Message'])

# Trigger the function
#if __name__ == "__main__":
#   get_message()



for x in range(10):
    get_message()

