#!groovy

pipeline {
    agent none

    stages {
        stage('Test') {
            
            agent { 
                label "ecs-builder" 
            }

            steps {
                initBuild()
                sh 'yarn test'
            }
        }
    }
}