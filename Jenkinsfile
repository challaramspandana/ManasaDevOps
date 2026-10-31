
pipeline {
    agent any

    stages {

        stage('Run Selenium Tests with pytest') {
            steps {
                echo "Running Selenium Tests using pytest"

                bat 'pip install -r requirements.txt'

                bat 'start /B python app.py'

                bat 'ping 127.0.0.1 -n 5 > nul'

                bat 'python -m pytest -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Build Docker Image"
                bat "docker build -t pet-adoption-platform:v1 ."
            }
        }

        stage('Docker Login') {
            steps {
                bat 'docker login -u spandana234 -p Spandana@23'
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                echo "Push Docker Image to Docker Hub"

                bat "docker tag pet-adoption-platform:v1 spandana234/pet-adoption-platform:latest"

                bat "docker push spandana234/pet-adoption-platform:latest"
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat 'kubectl apply -f deployment.yaml --validate=false'
                bat 'kubectl apply -f service.yaml'
            }
        }
    }

    post {
        success {
            echo 'Pet Adoption Platform Pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Please check the logs.'
        }
    }
}
