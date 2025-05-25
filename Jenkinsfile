pipeline {
    agent any

    environment {
        IMAGE_NAME = 'practice-questions'
    }

    stages {
        stage('Clone') {
            steps {
                echo 'Cloning repo...'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Run Container') {
            steps {
                echo 'Running the Docker container...'
                sh 'docker run -d -p 5000:5000 --name practice-questions-container $IMAGE_NAME || true'
            }
        }
    }

    post {
        always {
            echo 'Cleaning up old container (if exists)...'
            sh 'docker rm -f practice-questions-container || true'
        }
    }
}

