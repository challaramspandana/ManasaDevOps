pipeline {
    agent any

    stages {
        stage('Install Dependencies and Run Selenium Tests') {
            steps {
                bat 'pip install -r requirements.txt'
                bat 'start /B python app.py'
                bat 'ping 127.0.0.1 -n 6 > nul'
                bat 'python -m pytest -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t digital-notice-board:v1 .'
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_TOKEN'
                )]) {
                    bat 'echo %DOCKER_TOKEN% | docker login -u %DOCKER_USER% --password-stdin'
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                bat 'docker tag digital-notice-board:v1 spandana234/digital-notice-board:latest'
                retry(3) {
                    bat 'docker push spandana234/digital-notice-board:latest'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat 'kubectl apply -f deployment.yaml --validate=false'
                bat 'kubectl apply -f service.yaml'
                bat 'kubectl rollout status deployment/digital-notice-board --timeout=180s'
            }
        }
    }

    post {
        success { echo 'Digital Notice Board pipeline completed successfully!' }
        failure { echo 'Pipeline failed. Please check the console output.' }
    }
}
