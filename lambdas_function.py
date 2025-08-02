import boto3
import json
import os

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ.get("TABLE_NAME")

def lambda_handler(event, context):
    try:
        params = event.get("queryStringParameters") or {}
        note_id = params.get("noteId")

        if not note_id:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Missing noteId"})
            }

        table = dynamodb.Table(TABLE_NAME)
        response = table.get_item(Key={"note_id": note_id})

        if 'Item' not in response:
            return {
                "statusCode": 404,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "No summary found for this Note ID."})
            }

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "summary": response['Item'].get('summary', '')
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Internal Server Error"})
        }
