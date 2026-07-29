pipeline {
    agent any

    triggers {
        cron('H/1 * * * *')
    }

    environment {
        CONTAINER_NAME = "flask-monitor"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Monitor Container') {
            steps {
                bat 'python monitor.py'
            }
        }

        stage('Container Status') {
            steps {
                bat 'docker ps -a'
            }
        }
    }

    post {
        success {
            echo 'Pipeline Completed Successfully.'
        }

        failure {
            echo 'Pipeline Failed.'
        }

        always {
            echo 'Self-Healing Docker Monitoring Completed.'
        }
    }
}