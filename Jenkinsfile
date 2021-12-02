#!groovy
pipeline {
  agent {
    node {
      label 'ecs-builder-node14-rust'
    }
  }

  parameters {
    string defaultValue: 'termlink', name: 'module'
  }

  options {
    ansiColor('xterm')
    skipDefaultCheckout true
    timestamps()
  }
  
  stages {
    stage('checkout') {
      steps {
        dir('termlink') {
          checkout(
            changelog: true,
            poll: true,
            scm: [
              $class: 'GitSCM',
              branches: [
                [name: 'origin/pr/**'],
                [name: 'master']
              ],
              userRemoteConfigs: [
                [
                  credentialsId: 'github-app-lifeomic', 
                  url: 'https://github.com/lifeomic/termlink.git', 
                  refspec: '+refs/heads/*:refs/remotes/origin/* +refs/pull/*/head:refs/remotes/origin/pr/*'
                ]
              ]
            ]
          )
        }
        stash name: 'termlink-source', includes: 'termlink/**', allowEmpty: true
      }
    }

    stage('build package') {
      when { anyOf { branch 'master'; changeRequest target: 'master' } }
      steps {
        unstash 'termlink-source'
        dir('termlink') {
          buildPythonPackage('termlink')
        }
        stash name: 'termlink-package', includes: 'termlink/dist/** termlink/*.egg-info', allowEmpty: true
      }
    }

    stage('publish package') {
      when { branch 'master' }
      steps {
        unstash 'termlink-package'
        dir('termlink') {
          withCredentials([
            string(credentialsId: 'pypi-publish-api-token', variable: 'TWINE_PASSWORD')
          ]) {
            withEnv([
              'TWINE_NONINTERACTIVE="true"',
              'TWINE_USERNAME="__token__"'
            ]) {
              publishPyPIPackage('termlink')
            }
          }
        }
      }
    }
  }
}
