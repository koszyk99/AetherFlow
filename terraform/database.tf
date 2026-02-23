resource "aws_dynamodb_table" "transaction" {
    name            = "AetherFlow_Transactions"   # this must be identical to the python code
    billing_mode    = "PAY_PER_REQUEST"   # payment model
    hash_key        = "transaction_id"   # primary key

    attribute {
        name = "transaction_id"
        type = "S"
    }

    tags = {
        Environment     = "local"
        Project         = "AetherFlow"
    }
}
