pipeline {
    agent any

    environment {
        APP_DIR = '/home/ubuntu/to-do-app'
    }

    stages {

        stage('Deploy App') {
            steps {
                echo 'Starting Todo application...'
                sh """
                    cd ${APP_DIR} && git pull
                    docker-compose up -d
                """
                sleep(time: 20, unit: 'SECONDS')
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    pip3 install selenium pytest --break-system-packages
                '''
            }
        }

        stage('Run Selenium Tests') {
            steps {
                sh '''
                    mkdir -p test-results
                    pytest tests/test_todo_app.py -v \
                        --junit-xml=test-results/results.xml || true
                '''
            }
        }

        stage('Publish Results') {
            steps {
                junit allowEmptyResults: true,
                      testResults: 'test-results/results.xml'
            }
        }
    }

    post {
        always {
            emailext(
                subject: "Test Results - Build #${env.BUILD_NUMBER} - ${currentBuild.currentResult}",
                body: """
                    <h2>Build #${env.BUILD_NUMBER}</h2>
                    <p>Status: <b>${currentBuild.currentResult}</b></p>
                    <p>Todo App Selenium Tests completed.</p>
                    <p>See: <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                """,
                to: 'hamadkhan10052005@gmail.com',
                mimeType: 'text/html'
            )
        }
    }
}
