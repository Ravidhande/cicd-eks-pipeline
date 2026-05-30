pipeline {
    agent any

    environment {
        AWS_REGION      = 'ap-south-1'
        ECR_REPO        = '354918370166.dkr.ecr.ap-south-1.amazonaws.com/cicd-eks-app'
        IMAGE_TAG       = "${BUILD_NUMBER}"
        CLUSTER_NAME    = 'cicd-cluster'
        SONAR_URL       = 'http://localhost:9000/'
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
                echo 'Running SonarQube code quality scan...'
                withSonarQubeEnv('SonarQube') {
                    sh '''
                        sonar-scanner \
                        -Dsonar.projectKey=cicd-eks-pipeline \
                        -Dsonar.sources=app \
                        -Dsonar.host.url=${SONAR_URL} \
                        -Dsonar.language=py
                    '''
                }
            }
        }

        stage('✅ Quality Gate Check') {
            steps {
                echo 'Checking SonarQube quality gate...'
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
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
                echo 'Pushing image to AWS ECR...'
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

                    kubectl set image deployment/cicd-eks-app \
                    cicd-eks-app=${ECR_REPO}:${IMAGE_TAG}

                    kubectl rollout status deployment/cicd-eks-app
                """
            }
        }

        stage('📊 Deploy Monitoring Stack') {
            steps {
                echo 'Setting up Prometheus + Grafana...'
                sh '''
                    kubectl apply -f k8s/monitoring.yaml
                    kubectl get pods -n monitoring
                '''
            }
        }

        stage('✅ Verify Deployment') {
            steps {
                echo 'Verifying everything is running...'
                sh '''
                    kubectl get pods
                    kubectl get services
                    kubectl get pods -n monitoring
                '''
            }
        }
    }

    post {
        success {
            echo '🎉 Pipeline succeeded! App is live on EKS with monitoring!'
        }
        failure {
            echo '❌ Pipeline failed! Check logs above.'
        }
    }
}