# 🧠 AI-Based Notes Summarizer & Cloud Share 📄☁️
 This project uses AWS Serverless Architecture to allow users to upload notes (PDF/TXT), summarize them using Meta LLaMA 3 via Amazon Bedrock, and optionally send the results via SNS email. 

 
# Project Overview
This project is an AI-powered notes summarizer and cloud-sharing platform. It allows users to upload text or PDF files, which are then summarized using a large language model (LLM) and stored securely. Users can access their summaries via a unique link and receive email notifications when the summary is ready.

The application is built on a serverless architecture using various AWS services, ensuring scalability, cost-effectiveness, and high availability.

# Features :

1. File Upload:
 Users can upload .txt or .pdf files.

2. AI-Powered Summarization: 
    Utilizes Amazon Bedrock with a foundation model (e.g., Meta LLaMA 3) to generate concise summaries.

3. Cloud Storage:
    Summaries are stored securely in an Amazon DynamoDB table.

4. Unique Access Links:
    Each summary is associated with a unique ID, allowing for easy sharing and retrieval.

5. Email Notifications:
    Users receive email alerts via Amazon SNS when their summary has been processed and is ready to view.

6. Static Website Hosting:
    The frontend is hosted on Amazon S3 with static website hosting enabled.

7. Technology Stack
    The project is entirely deployed on AWS, leveraging a robust set of services to handle the backend logic, data storage, and frontend delivery.

--------------------------------------------------------------------------------------------
|       Service               |               Purpose                                      |
| --------------------------- | ---------------------------------------------------------- |
|   Amazon S3                 | Stores frontend files and user-uploaded text/PDF files.    |
|   AWS Lambda                | Manages backend logic for file handling and summarization. |
|   API Gateway               | Exposes Lambda functions as REST APIs for the frontend.    |
|   Amazon DynamoDB           | Stores summaries with unique note IDs.                     |
|   Amazon SNS                | Sends email notifications when a summary is created.       |
|   Amazon Bedrock            | Provides the large language model (LLM) for summarization. |
|   Amazon CloudWatch         | Monitors Lambda logs and alerts.                           |
|   AWS IAM                   | Manages permissions and roles securely.                    |
|   Amazon Route 53           | Handles custom domain mapping.                             |
|   AWS Certificate Manager   | Provides SSL certificates for HTTPS.                       |
|   AWS CloudFront            | Speeds up global access to the website.                    |
-------------------------------------------------------------------------------------------

# Deployment Guide
  This section provides a step-by-step guide to deploying the project from scratch using AWS services.

# Prerequisites
  An active AWS account.

# Basic familiarity with AWS services.

1. Configure Amazon S3
   Create an S3 bucket (e.g., rddi.xyz). The bucket name should match your custom domain name.
   
   Enable Static website hosting for the bucket.
   
   Upload the upload.html and view-summary.html files to the bucket.

2. Configure AWS IAM
   Create an IAM role for Lambda with the following managed policies attached:

   1.AmazonS3FullAccess

   2.AmazonDynamoDBFullAccess

   3.AmazonSNSFullAccess

   4.AmazonComprehendFullAccess (if not available, create a custom policy)

   5.CloudWatchFullAccess

   Name the role ai-notes-lambda-role.
  
Attach this role to both of your Lambda functions later.

3. Create AWS Lambda Functions
   You will need to create two Lambda functions.

   upload-handler: Handles the incoming text/PDF files, sends the content for summarization, and stores the initial data in DynamoDB.
   
   summary-handler: Retrieves the summary from DynamoDB based on the provided noteId.

   Create the two Lambda functions.

   Copy and paste the provided Python code for each function into the respective Lambda console.

   Upload the code as a .zip file if you are using a local IDE.

4. Configure Amazon DynamoDB
   Create a new DynamoDB table named note_summaries.

   Set the primary key to note_id.

5. Configure Amazon SNS
   Create a new SNS topic named NoteSummaryNotification (Standard type).

   Create a subscription for this topic with the protocol set to Email and your verified email address as the endpoint.

   Confirm the subscription via the link sent to your email.

6. Configure API Gateway
   Create a new HTTP API.

   Define the routes and integrations:

   POST /upload → Integrate with the upload-handler Lambda function.

   GET /get-summary → Integrate with the summary-handler Lambda function.

   Enable CORS for your API:

   Set Allow origins to * or your domain.

   Set Allow methods to GET, POST, OPTIONS.

   Set Allow headers to Content-Type.

   Deploy the API to a new stage (e.g., prod). Note the base URL provided.

7. Update Environment Variables
   Go to the Configuration > Environment variables section for each of your Lambda functions and add the following keys and values:

   For upload-handler:

   TABLE_NAME: note_summaries

   SNS_TOPIC_ARN: The ARN of your NoteSummaryNotification SNS topic.

   For summary-handler:

   TABLE_NAME: note_summaries

8. Set Up Domain and SSL (Optional but Recommended)
   ACM: Request a public SSL certificate for your custom domain (e.g., raju.rddi.xyz).

   Route 53: Create a hosted zone for your domain.

   CloudFront: Create a CloudFront distribution pointing to your S3 bucket, using the SSL certificate from ACM to enable HTTPS.

   Update your Route 53 A-record to point to the CloudFront distribution's domain name.

9. Frontend Code
   The project includes two frontend HTML files: upload.html and view-summary.html. These files handle the user interface, file reading, and API calls.

   upload.html
   This page allows users to select and upload a .txt or .pdf file. It reads the file content, sends it to the /upload API endpoint, and displays the generated noteId.

   view-summary.html
   This page takes a noteId as a query parameter, fetches the summary from the /get-summary API endpoint, and displays the result.

Note: Remember to update the API_ENDPOINT variable in both frontend HTML files to the base URL of your deployed API Gateway.





