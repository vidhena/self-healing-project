pipeline {
    agent any

    triggers {
        pollSCM('* * * * *')
    }

    stages {
        stage('Check Container') {
            steps {
                bat 'docker ps'
            }
        }

        stage('Monitor') {
            steps {
                powershell '.\\monitor.ps1'
            }
        }
    }
}