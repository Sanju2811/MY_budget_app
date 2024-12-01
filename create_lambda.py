import boto3

# Initialize the Lambda client
lambda_client = boto3.client('lambda', region_name='us-east-1')  # Update region as needed

# Specify Lambda function details
function_name = 'CPP_lambda'
runtime = 'python3.9'  # Supported runtimes: https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html
role_arn = '<Your-Execution-Role-ARN>'  # Replace with the ARN of your IAM role for Lambda
handler = 'lambda_function.lambda_handler'  # Specify module.function_name
zip_file_path = 'lambda_function.zip'

# Read the ZIP file containing the function code
with open(zip_file_path, 'rb') as f:
    zip_file_data = f.read()

# Create the Lambda function
response = lambda_client.create_function(
    FunctionName=function_name,
    Runtime=runtime,
    Role=role_arn,
    Handler=handler,
    Code={
        'ZipFile': zip_file_data
    },
    Description='My first Lambda function created programmatically',
    Timeout=15,  # Maximum execution time in seconds
    MemorySize=128,  # Memory allocated in MB
    Publish=True  # Publish the function immediately
)

print(f"Lambda function created: {response['FunctionArn']}")
