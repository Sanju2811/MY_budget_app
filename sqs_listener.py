import boto3
import json
from botocore.exceptions import ClientError

# AWS Configuration
region_name = 'us-east-1'  # Ensure this is the correct region
sqs_queue_url = 'https://sqs.us-east-1.amazonaws.com/225489345950/BudgetLimitQueue'  # Replace with your SQS queue URL

# Initialize SQS client
sqs_client = boto3.client('sqs', region_name=region_name)

# Function to process the message from SQS
def process_expense_message(message_body):
    # Process the expense data from the message (this can include saving to another DB, sending email, etc.)
    print(f"Processing expense message: {message_body}")
    # Add custom logic to process the message here

# Function to poll the SQS queue
def poll_sqs_queue():
    while True:
        try:
            response = sqs_client.receive_message(
                QueueUrl=sqs_queue_url,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=20  # Long polling
            )

            if 'Messages' in response:
                for message in response['Messages']:
                    message_body = message['Body']
                    print(f"Received message: {message_body}")
                    process_expense_message(message_body)

                    # Delete the message from the queue after processing
                    receipt_handle = message['ReceiptHandle']
                    sqs_client.delete_message(
                        QueueUrl=sqs_queue_url,
                        ReceiptHandle=receipt_handle
                    )
                    print(f"Message deleted from queue: {receipt_handle}")
            else:
                print("No messages available in the queue.")
        except ClientError as e:
            print(f"Error receiving or deleting message from SQS: {e.response['Error']['Message']}")

# Start listening for messages
if __name__ == '__main__':
    poll_sqs_queue()
