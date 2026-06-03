# 🚀 Enterprise CI/CD Pipeline — Jenkins + Docker + AWS EKS

![CI/CD](https://img.shields.io/badge/CI%2FCD-Jenkins-red?style=for-the-badge&logo=jenkins)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)
![SonarQube](https://img.shields.io/badge/SonarQube-4E9BCD?style=for-the-badge&logo=sonarqube&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)

---

## 📌 Project Overview

A **production-grade, end-to-end CI/CD pipeline** that automatically builds, tests, and deploys a Dockerized Flask application to AWS EKS (Kubernetes) — triggered on every Git push.

Every code change goes through **automated code quality scanning** (SonarQube), **Docker containerization**, **AWS ECR registry**, and **zero-downtime Kubernetes rolling deployment** — all orchestrated by Jenkins.

> **From `git push` to live deployment in under 5 minutes — fully automated.**

---

## 🏗️ Architecture

```
Developer (git push)
        │
        ▼
   GitHub Repo
        │
        │ Poll SCM / Webhook Trigger
        ▼
  Jenkins Pipeline
        │
   ┌────┴─────────────────────────┐
   │                              │
   ▼                              ▼
SonarQube                   Docker Build
Code Scan                        │
   │                              ▼
   │ Quality                  AWS ECR
   │ Gate ✅                 (Image Store)
   └────────────┬─────────────────┘
                │
                ▼
           AWS EKS
        (Kubernetes)
         │        │
         ▼        ▼
       Pod 1    Pod 2
    (Flask App) (Flask App)
         │        │
         └────┬───┘
              ▼
        LoadBalancer
              │
              ▼
          Internet
              │
         ┌────┴────┐
         ▼         ▼
     Prometheus  Grafana
    (Metrics)  (Dashboard)
```

---

## 🛠️ Tech Stack

| Category | Technology | Purpose |
|---|---|---|
| **Application** | Python Flask | Lightweight web app |
| **Containerization** | Docker | Package app + dependencies |
| **Container Registry** | AWS ECR | Store Docker images |
| **CI/CD** | Jenkins | Pipeline automation |
| **Code Quality** | SonarQube | Bug & vulnerability scanning |
| **Orchestration** | Kubernetes (AWS EKS) | Container management |
| **Infrastructure** | Terraform | Infrastructure as Code |
| **Monitoring** | Prometheus | Metrics collection |
| **Visualization** | Grafana | Real-time dashboards |
| **Cloud** | AWS | EC2, EKS, ECR, VPC, IAM |
| **Version Control** | GitHub | Source code management |

---

## 📁 Project Structure

```
cicd-eks-pipeline/
│
├── app/
│   ├── app.py                  # Flask application
│   └── requirements.txt        # Python dependencies
│
├── terraform/
│   ├── main.tf                 # VPC, EKS, ECR, IAM resources
│   ├── variables.tf            # Configuration variables
│   └── outputs.tf              # Output values (URLs, IDs)
│
├── k8s/
│   ├── deployment.yaml         # Kubernetes deployment (2 replicas)
│   ├── service.yaml            # LoadBalancer service
│   ├── monitoring.yaml         # Prometheus + Grafana stack
│   └── hpa.yaml                # Horizontal Pod Autoscaler
│
├── sonarqube/
│   └── sonar-project.properties # SonarQube config
│
├── Dockerfile                  # Container build instructions
├── Jenkinsfile                 # Complete pipeline definition
├── .gitignore                  # Excludes binaries and secrets
└── README.md                   # Project documentation
```

---

## 🔄 Pipeline Stages

```
📥 Stage 1: Checkout Code
   └── Jenkins pulls latest code from GitHub

🔍 Stage 2: SonarQube Code Analysis
   └── Scans Python code for bugs, vulnerabilities, code smells
   └── Quality Gate must PASS to proceed

🐳 Stage 3: Docker Build
   └── Builds Docker image from Dockerfile
   └── Tags with build number for versioning

☁️  Stage 4: Push to AWS ECR
   └── Authenticates with AWS ECR
   └── Pushes versioned image to private registry

🚀 Stage 5: Deploy to EKS
   └── Updates kubeconfig for EKS cluster
   └── Applies Kubernetes manifests
   └── Rolling update — zero downtime deployment
   └── Waits for rollout to complete

📊 Stage 6: Deploy Monitoring Stack
   └── Deploys Prometheus + Grafana on Kubernetes
   └── Configures Node Exporter for system metrics
   └── Applies HPA for auto-scaling

✅ Stage 7: Verify Deployment
   └── Confirms all pods are Running
   └── Shows live service endpoints
```

---

## ⚡ Key Features

- **Zero Downtime Deployments** — Kubernetes rolling updates replace pods one by one
- **Automated Code Quality** — SonarQube scans every commit before build
- **Infrastructure as Code** — Entire AWS setup created with Terraform in one command
- **Auto Scaling** — HPA scales pods from 2 to 5 based on CPU/Memory load
- **Self Healing** — Kubernetes automatically restarts failed pods
- **Versioned Images** — Every build tagged with Jenkins build number
- **Real-time Monitoring** — Grafana dashboards show live cluster metrics
- **Poll SCM** — Jenkins automatically detects and deploys new code changes

---

## 🚀 How To Run

### Prerequisites
```bash
# Install required tools
- AWS CLI (configured with IAM credentials)
- Terraform
- Docker
- kubectl
- eksctl
- Jenkins
```

### Step 1 — Clone Repository
```bash
git clone https://github.com/Ravidhande/cicd-eks-pipeline
cd cicd-eks-pipeline
```

### Step 2 — Create AWS Infrastructure
```bash
cd terraform
terraform init
terraform plan
terraform apply
# Type 'yes' — takes 15-20 mins
```

### Step 3 — Connect kubectl to EKS
```bash
aws eks update-kubeconfig \
  --region ap-south-1 \
  --name cicd-cluster

# Verify nodes
kubectl get nodes
```

### Step 4 — Configure Jenkins Pipeline
```
1. Open Jenkins → New Item → Pipeline
2. Connect to GitHub repo
3. Add AWS + SonarQube credentials
4. Enable Poll SCM trigger
5. Run pipeline
```

### Step 5 — Trigger Pipeline
```bash
# Make any code change
git add .
git commit -m "Your change"
git push origin main
# Jenkins automatically detects and deploys!
```

### Step 6 — Access Your App
```bash
kubectl get service cicd-eks-service
# Open EXTERNAL-IP in browser
```

### Step 7 — View Monitoring
```bash
kubectl get service grafana-service -n monitoring
# Open EXTERNAL-IP:3000
# Login: admin / admin123
```

### Step 8 — Cleanup (Save AWS Costs)
```bash
cd terraform
terraform destroy
# Type 'yes'
```

---

## 📊 AWS Resources Created By Terraform

```
✅ VPC with public subnets (2 AZs)
✅ Internet Gateway + Route Tables
✅ Security Groups
✅ ECR Repository (private Docker registry)
✅ EKS Cluster (Kubernetes control plane)
✅ EKS Node Group (2x t3.medium EC2 instances)
✅ IAM Roles (EKS cluster + node group)
✅ Auto Scaling Group (1-3 nodes)
```

---

## 🔍 SonarQube Analysis

Code is automatically scanned for:
```
✅ Bugs
✅ Vulnerabilities
✅ Security Hotspots
✅ Code Smells
✅ Duplications
```

Pipeline **fails automatically** if Quality Gate is not passed — preventing bad code from reaching production.

---

## 📈 Monitoring Stack

| Tool | Purpose | Port |
|---|---|---|
| Prometheus | Metrics collection & storage | 9090 |
| Grafana | Visualization dashboards | 3000 |
| Node Exporter | System metrics (CPU, Memory, Disk) | 9100 |

### Grafana Dashboards:
- **Dashboard 1860** — Node metrics (CPU, Memory, Network, Disk)
- **Dashboard 6417** — Kubernetes cluster overview

---

## 🔧 Kubernetes Resources

```
Deployment:
  replicas: 2
  strategy: RollingUpdate
  resources:
    requests: 64Mi memory, 250m CPU
    limits:   128Mi memory, 500m CPU
  probes:
    liveness:  /health endpoint
    readiness: /health endpoint

HPA (Auto Scaling):
  min replicas: 2
  max replicas: 5
  CPU threshold: 70%
  Memory threshold: 80%
```

---

## 💡 Problems Solved During Development

| Problem | Solution |
|---|---|
| EKS version compatibility | Upgraded from 1.28 → 1.31 with full terraform destroy/apply |
| Port conflicts (Prometheus) | Used Docker network with container name resolution |
| Large files in git history | Used BFG Repo Cleaner to remove binaries |
| Jenkins PATH issues | Fixed environment PATH for jenkins user |
| SonarQube authentication | Added token via Jenkins credentials binding |
| GitHub webhook (local) | Used Poll SCM as alternative to webhook |
| Grafana data persistence | Added PersistentVolumeClaim to monitoring stack |

---

## 📸 Screenshots

> Add your screenshots here:
> - <img width="1917" height="911" alt="Screenshot from 2026-05-30 19-38-29" src="https://github.com/user-attachments/assets/f3c722a9-420b-4e80-af9b-50408ef70e72" />

> - <img width="1920" height="1080" alt="Screenshot from 2026-05-30 14-57-30" src="https://github.com/user-attachments/assets/74642621-9958-4a79-8b55-362969c33030" />

> - <img width="1906" height="362" alt="Screenshot from 2026-05-30 17-57-45" src="https://github.com/user-attachments/assets/3c981e8b-2f9e-434f-969f-427204758177" />

> - <img width="1920" height="1080" alt="Screenshot from 2026-05-30 19-45-16" src="https://github.com/user-attachments/assets/0e409a5d-ae6a-4932-9501-c77b7d3a4523" />

> - <img width="1920" height="1080" alt="Screenshot from 2026-05-30 15-06-20" src="https://github.com/user-attachments/assets/da864c79-0db6-4853-b7d5-7a8645f7480c" />

> - <img width="1920" height="1080" alt="Screenshot from 2026-05-30 15-02-16" src="https://github.com/user-attachments/assets/9a8ae80a-82a2-4faa-8303-1c7fe8dcaefa" />


---

## 👨‍💻 Author

**Ravi Dhande**
AWS Certified Cloud Engineer | DevOps Enthusiast

- 🔗 LinkedIn: [www.linkedin.com/in/ravi-dhande
- 💻 GitHub: [github.com/Ravidhande](https://github.com/Ravidhande)
- 📧 Email: dhanderavi32@gmail.com
- 🏆 AWS Certified Cloud Practitioner
- 🎓 AWS re/Start Graduate

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

> ⭐ **If this project helped you, please give it a star!**
