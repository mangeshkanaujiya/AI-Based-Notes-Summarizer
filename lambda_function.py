import json
import boto3
import uuid
import os

# AWS services
dynamodb = boto3.resource('dynamodb')
comprehend = boto3.client('comprehend')
TABLE_NAME = os.environ.get("TABLE_NAME")

def lambda_handler(event, context):
    try:
        print("RAW EVENT:", event)
        body = json.loads(event.get("body", "{}"))
        print("BODY PARSED:", body)

        content = body.get("text")
        note_id = body.get("note_id") or str(uuid.uuid4())

        if not content or len(content.strip()) < 30:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"error": "Text too short or missing"})
            }

        print("🧠 Running Comprehend...")

        # Comprehend analysis
        key_phrases_resp = comprehend.detect_key_phrases(Text=content, LanguageCode='en')
        entities_resp = comprehend.detect_entities(Text=content, LanguageCode='en')
        sentiment_resp = comprehend.detect_sentiment(Text=content, LanguageCode='en')

        key_phrases = list({kp['Text'] for kp in key_phrases_resp['KeyPhrases']})
        entities = list({ent['Text'] for ent in entities_resp['Entities']})
        sentiment = sentiment_resp['Sentiment']

        # Filter phrases
        filtered_phrases = [p for p in key_phrases if len(p) > 3 and not p.lower().startswith("step")]
        filtered_entities = [e for e in entities if len(e) > 2]

        # Build summary
        summary = f"Tone: {sentiment.lower()}.\n"
        if filtered_entities:
            summary += "Topics: " + ', '.join(filtered_entities[:5]) + ".\n"
        if filtered_phrases:
            summary += "Key Ideas: " + ', '.join(filtered_phrases[:10]) + "."

        # Save to DynamoDB
        table = dynamodb.Table(TABLE_NAME)
        existing = table.get_item(Key={"note_id": note_id})
        previous = existing.get("Item", {}).get("summary", "")

        full_summary = previous + "\n\n" + summary if previous else summary

        table.put_item(Item={
            "note_id": note_id,
            "summary": full_summary
        })

        print("✅ Success. Returning summary.")

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "message": "Summary generated and merged successfully",
                "note_id": note_id,
                "summary": full_summary
            })
        }

    except Exception as e:
        print("❌ ERROR:", str(e))
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": str(e)})
        }
