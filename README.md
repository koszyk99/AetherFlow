# AetherFlow: Serverless Fraud Detection System

A cloud-native, event-driven pipeline built with **Terraform**, **LocalStack**, and **Python**. This system automatically detects high-value transactions and triggers security alerts in real-time.

## 🏗 Architecture
The system utilizes a modern serverless stack:
* **Storage:** AWS S3 (Inbound transaction files)
* **Compute:** AWS Lambda (Business logic & fraud detection)
* **Database:** AWS DynamoDB (Result archiving)
* **Alerting:** AWS SNS (Security notification system)
* **Infrastructure:** Terraform (IaC)

## 🚀 How it Works
1.  A JSON transaction file is uploaded to the S3 bucket.
2.  An S3 Event triggers the **AetherFlow Processor** (Lambda).
3.  The Lambda evaluates the transaction amount:
    * **Amount < 1000:** Marked as `APPROVED`.
    * **Amount >= 1000:** Marked as `FLAGGED` and sent to the SNS Topic.
4.  All results are saved in the **FraudSentinel_Result** DynamoDB table.

## 🛠 Setup & Deployment
1.  **Initialize Infrastructure:**
    ```bash
    cd terraform
    terraform init
    terraform apply -auto-approve
    ```
2.  **Run the Dashboard:**
    ```bash
    python3 dashboard.py
    ```

## 📊 Sample Output
```text
=================================================================
                AETHERFLOW - LIVE MONITORING
=================================================================
 STATUS: OPERATIONAL | Transactions: 3 | SNS Alerts: 2
 Total Blocked Amount: 17500.00 USD
-----------------------------------------------------------------
+----+---------------+-------------+------------------+
|    | S3 Object Key | Amount (USD)| Detection Status |
+====+===============+=============+==================+
|  0 | tx_ok.json    |         150 | APPROVED         |
|  1 | tx_alert.json |       12000 | FLAGGED          |
|  2 | tx_fraud.json |        5500 | FLAGGED          |
+----+---------------+-------------+------------------+
=================================================================
