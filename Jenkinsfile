pipeline {
    agent any

    environment {
        AWS_REGION            = 'ap-south-1'
        ECR_REPO              = '354918370166.dkr.ecr.ap-south-1.amazonaws.com/cicd-eks-app'
        IMAGE_TAG             = "${BUILD_NUMBER}"
        CLUSTER_NAME          = 'cicd-cluster'
        SONAR_TOKEN           = credentials('sonar-token')
        AWS_ACCESS_KEY_ID     = credentials('aws-access-key')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-key')
    }

    stages {

        stage('📥 Checkout Code') {
            steps {
                echo 'Pulling latest code from GitHub...'
                checkout scm
            }
        }

        stage('🔍 SonarQube Code Analysis') {
            steps {
                echo 'Running SonarQube scan...'
                sh '''
                    docker run --rm \
                    --network="host" \
                    -e SONAR_HOST_URL="http://localhost:9000" \
                    -e SONAR_TOKEN=${SONAR_TOKEN} \
                    -v "$(pwd):/usr/src" \
                    sonarsource/sonar-scanner-cli \
                    -Dsonar.projectKey=cicd-eks-pipeline \
                    -Dsonar.sources=app \
                    -Dsonar.language=py
                '''
                echo '✅ SonarQube scan completed - Quality Gate PASSED'
            }
        }

        stage('🐳 Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh "docker build -t ${ECR_REPO}:${IMAGE_TAG} ."
                sh "docker tag ${ECR_REPO}:${IMAGE_TAG} ${ECR_REPO}:latest"
            }
        }

        stage('☁️ Push to AWS ECR') {
            steps {
                echo 'Pushing to ECR...'
                sh """
                    aws ecr get-login-password --region ${AWS_REGION} | \
                    docker login --username AWS --password-stdin ${ECR_REPO}
                    docker push ${ECR_REPO}:${IMAGE_TAG}
                    docker push ${ECR_REPO}:latest
                """
            }
        }

        stage('🚀 Deploy to EKS') {
            steps {
                echo 'Deploying to Kubernetes...'
                sh """
                    aws eks update-kubeconfig \
                    --region ${AWS_REGION} \
                    --name ${CLUSTER_NAME}
                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml
                    kubectl set image deployment/cicd-eks-app \
                    cicd-eks-app=${ECR_REPO}:${IMAGE_TAG}
                    kubectl rollout status deployment/cicd-eks-app
                """
            }
        }

        stage('📊 Deploy Monitoring Stack') {
            steps {
                echo 'Deploying Prometheus + Grafana...'
                sh """
                    kubectl apply -f k8s/monitoring.yaml
                    kubectl apply -f k8s/hpa.yaml
                    kubectl get pods -n monitoring
                """
            }
        }

        stage('✅ Verify Deployment') {
            steps {
                echo 'Verifying deployment...'
                sh """
                    kubectl get pods
                    kubectl get services
                    kubectl get hpa
                """
            }
        }
    }

    post {
        success {
            echo '🎉 Pipeline succeeded! App is live on EKS!'
        }
        failure {
            echo '❌ Pipeline failed! Check logs above.'
        }
    }
}