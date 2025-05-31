pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
    }

    tools {
        python 'Python 3.10' // Set up Python tool from Jenkins Global Config
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        url: 'https://meenalsharma1@bitbucket.org/training_meenal/jenkinsdemorepo.git',
                        credentialsId: 'bitbucket-creds'
                    ]]
                ])
            }
        }

        stage('Set Up Environment') {
            steps {
                bat 'python -m venv venv'
                bat '.\\venv\\Scripts\\activate && pip install --upgrade pip'
                bat '.\\venv\\Scripts\\activate && pip install -r requirements.txt'
            }
        }

        stage('Load Environment Variables') {
            steps {
                withCredentials([file(credentialsId: 'ENV_FILE', variable: 'ENV_PATH')]) {
                    bat "copy %ENV_PATH% .env"
                }
            }
        }

        stage('Run Tests with Retries') {
            steps {
                bat '.\\venv\\Scripts\\activate && pytest tests/ --reruns 2 --reruns-delay 4 --html=reports/report.html --self-contained-html'
            }
        }

        stage('Archive Test Report') {
            steps {
                archiveArtifacts artifacts: 'reports/report.html', onlyIfSuccessful: false
            }
        }

        stage('Send Email Notification') {
            steps {
                emailext(
                    subject: "Test Report: ${env.JOB_NAME} - Build #${env.BUILD_NUMBER}",
                    body: "Test execution completed. Please find the attached HTML report.\n\nBuild URL: ${env.BUILD_URL}",
                    recipientProviders: [[$class: 'DevelopersRecipientProvider']],
                    attachmentsPattern: 'reports/report.html',
                    to: 'meenal.jprcity@gmail.com'
                )
            }
        }
    }

    post {
        always {
            echo 'Cleaning up workspace...'
            deleteDir()
        }
    }
}