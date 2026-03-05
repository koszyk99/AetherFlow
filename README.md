# 🌊 AetherFlow: Serverless Fraud Detection System

A cloud-native, event-driven data pipeline built with **Terraform**, **LocalStack**, and **Python**. This system automatically detects high-value transactions and triggers security alerts in real-time.

---

## 🏗 Architecture
The system utilizes a modern serverless stack running on a **Kubernetes** cluster via **LocalStack**:

![AetherFlow Architecture](https://github.com/koszyk99/AetherFlow/blob/main/architecture.png?raw=true)

1. **Ingest:** JSON transaction files are uploaded to an **AWS S3** bucket.
2. **Compute:** An S3 Event triggers the **AetherFlow Processor** (AWS Lambda).
3. **Logic:** The Lambda evaluates the transaction amount:
    * **Amount < 1000:** Marked as `APPROVED`.
    * **Amount >= 1000:** Marked as `FLAGGED` and published to an **AWS SNS** Topic.
4. **Storage:** All results are archived in an **AWS DynamoDB** table for audit.
5. **Monitoring:** A custom **Python Dashboard** provides a live view of the pipeline.

---

## 🛠 Setup & Deployment

### 1. Prerequisites
* LocalStack running in your Kubernetes cluster.
* Terraform and Python 3.x installed.
* AWS CLI (configured for LocalStack).

### 2. Establish Connection (The Tunnel)
Since LocalStack is running inside K8s, you **must** expose the service to your localhost:
```bash
kubectl port-forward svc/localstack 4566:4566

*Keep this terminal window open during the entire session.*

### 3. Initialize Infrastructure
In a new terminal window (keep the tunnel running!) deploy the cloud resources:
```bash
cd terraform
terraform init
terraform apply -auto-approve

4. Run the Live Dashboard
Navigate to the root directory, activate your virtual environment, and launch the monitoring tool:

Bash

source venv/bin/activate
pip install pandas tabulate boto3
python3 dashboard.py

📊 Live Monitoring Preview
When the system is operational, the dashboard provides real-time statistics directly from DynamoDB:

Plaintext

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

🧹 Cleanup
To stop the services and remove the infrastructure from LocalStack (remember to empty the bucket first):

Bash

# Empty bucket to avoid BucketNotEmpty error
aws --endpoint-url=http://localhost:4566 s3 rm s3://aetherflow-transactions --recursive

# Destroy infrastructure
terraform destroy -auto-approve
