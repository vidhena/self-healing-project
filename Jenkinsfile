pipeline {
    agent any

    parameters {
        choice(
            name: 'ACTION',
            choices: ['MONITOR', 'START', 'STOP', 'RESTART'],
            description: 'Select Docker Container Action'
        )
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

        stage('Docker Version') {
            steps {
                bat 'docker version'
            }
        }
        stage('Check Python'){
            steps{
                bat 'python --version'
            }
    }
        stage('Container Action') {
            steps {
                script {

                    if (params.ACTION == "START") {
                        bat "docker start %CONTAINER_NAME%"
                    }

                    if (params.ACTION == "STOP") {
                        bat "docker stop %CONTAINER_NAME%"
                    }

                    if (params.ACTION == "RESTART") {
                        bat "docker restart %CONTAINER_NAME%"
                    }

                    if (params.ACTION == "MONITOR") {
                        bat '"C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python314\\python.exe" --version'
                    }
                }
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
            echo "Pipeline Completed Successfully."
        }

        failure {
            echo "Pipeline Failed."
        }

        always {
            echo "Self-Healing Docker Monitoring Completed."
        }
    }
}