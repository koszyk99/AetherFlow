# ~/AetherFlow/terraform/main.tf

# our data "inlet" - this is where transactions in JSON will land
resource "aws_s3_bucket" "transaction_bucket" {
    bucket = "aetherflow-transactions"
}

# our database - here we will record whether the transaction was fraudulent
resource "aws_dynamodb_table" "fraud_results" {
    name         = "FraudSentinel_Result"
    billing_mode = "PAY_PER_REQUEST"
    hash_key     = "transaction_id"

attribute {
    name = "transaction_id"
    type = "S"   # mean string
    }
}

# this block automatically creates a ZIP file from code
data "archive_file" "lambda_zip" {
    type            = "zip"
    source_file     = "processor.py"
    output_path     = "lambda_function.zip"
}

# this block creates a Lambda in LocalStack
resource "aws_lambda_function" "processor_lambda" {
    filename        = "lambda_function.zip"
    function_name   = "AetherFlow_Processor_Final"
    role            = "arn:aws:iam::000000000000:role/lambda-role"
    handler         = "processor.lambda_handler"
    runtime         = "python3.10"
}

# permission for s3 to call lambda
resource "aws_lambda_permission" "allow_bucket" {
    statement_id = "AllowExecutionFromS3Bucket"
    action = "lambda:InvokeFunction"
    function_name = aws_lambda_function.processor_lambda.arn
    principal = "s3.amazonaws.com"
    source_arn = aws_s3_bucket.transaction_bucket.arn
}

# bucket notification configuration
resource "aws_s3_bucket_notification" "bucket_notification" {
    bucket = aws_s3_bucket.transaction_bucket.id

        lambda_function {
            lambda_function_arn     = aws_lambda_function.processor_lambda.arn
            events                  = ["s3:ObjectCreated:*"]
        }
        depends_on = [aws_lambda_permission.allow_bucket]
}
