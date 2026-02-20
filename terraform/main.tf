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
