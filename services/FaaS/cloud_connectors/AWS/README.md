# AWS cloud connectors

Karbon Platform Services expects certain permissions from each AWS services to be able to write data to it. This README documents the permissions required for each service.

### S3
**s3:ListBucket**: Needed for listing of existing buckets and for HEAD Bucket operation.   
**s3:CreateBucket**: Needed for bucket create operation if the bucket is not already present.   
**s3:PutObject**: Needed to write objects to S3 buckets.   
Check the [S3 Permissions](https://docs.aws.amazon.com/AmazonS3/latest/dev/using-with-s3-actions.htm) page for more details on the permissions and related actions.

### Kinesis
**stream:DescribeStream**: Needed for checking if the Kinesis Data Stream exists and is active before attempting to write records.   
**stream:CreateStream**: Needed for creating a Kinesis Data Stream if it does not already exist.   
**stream:PutRecord**: Need for writing records to Kinesis Data Streams.   
**stream:PutRecords**: Need for writing a batch of records to Kinesis Data Streams.   
Check the [Kinesis Permissions](https://docs.aws.amazon.com/IAM/latest/UserGuide/list_amazonkinesis.html) page for more details on the permissions and related actions.

### SQS
**sqs:ListQueues**: Needed for checking if the Queue already exists.   
**sqs:CreateQueue**: Needed for creating a Queue before writing to it.   
**sqs:SendMessage**: Needed for sending messages to a Queue.   
**sqs:SendMessageBatch**: Needed for sending a batch of messages to a Queue.   
Check the [SQS Permissions](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-api-permissions-reference.html) page for more details on the permissions and related actions.
