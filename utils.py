from decimal import Decimal
import boto3
from botocore.exceptions import NoCredentialsError

def calculate_total_expenses(expenses):
    """Calculate the total expenses from a list of expense items."""
    try:
        return sum(Decimal(expense['amount']) for expense in expenses)
    except Exception as e:
        print(f"Error occurred while calculating expenses: {str(e)}")
        return Decimal('0.00')

# Function to format currency values
def format_currency(value):
    """Format a decimal value into a currency string."""
    try:
        return f"${value:,.2f}"
    except Exception as e:
        print(f"Error occurred while formatting currency: {str(e)}")
        return "$0.00"

def check_budget_limit(expenses, budget_limit, sns_client, sns_topic_arn):
    """Check if total expenses exceed the budget limit and send an SNS notification."""
    try:
        total_expenses = sum(Decimal(expense['amount']) for expense in expenses)
        if total_expenses > Decimal(budget_limit):
            message = (f"Warning! Your expenses have exceeded the budget limit of "
                       f"{format_currency(budget_limit)}. Total: {format_currency(total_expenses)}.")
            sns_client.publish(
                TopicArn=sns_topic_arn,
                Message=message,
                Subject='Budget Limit Exceeded'
            )
            print("Notification sent: Budget limit exceeded.")
    except NoCredentialsError:
        print("Error: AWS credentials not found.")
    except Exception as e:
        print(f"Error occurred while checking budget limit or sending SNS: {str(e)}")

# Function to send expense data to SQS
def send_expense_to_sqs(expense_data, sqs_client, queue_url):
    """Send expense data to an SQS queue."""
    try:
        response = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=str(expense_data)  # Convert to string before sending
        )
        print(f"Message sent to SQS with message ID: {response['MessageId']}")
    except Exception as e:
        print(f"Failed to send message to SQS: {e}")

# Function to send generic notifications
def send_notification(sns_client, topic_arn, message, subject="Notification"):
    """Send a notification using SNS."""
    try:
        sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject=subject
        )
        print("Notification sent successfully.")
    except Exception as e:
        print(f"Error occurred while sending notification: {str(e)}")
