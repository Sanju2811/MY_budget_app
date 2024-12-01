import json

def lambda_handler(event, context):
    # Simple function that returns a message
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
