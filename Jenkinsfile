pipeline {
    agent {
        docker {
            image 'docker:latest'
            args "--entrypoint=''"
            args '--user root'
        }
    }
    
    stages {

        stage('Create dir') {
            steps {
                sh 'mkdir /.docker'
            }
        }

        stage('Build docker-compose-geral') {
            steps {
                script{
                    try{
                        sh "docker compose -f docker-compose-geral.yml down"
                        sh "docker image rm -f build-pymarket-app-pymarket"
                        sh "docker image rm -f build-pymarket-db-pymarket"
                        sh "docker compose -f docker-compose-geral.yml up -d"
                        sh "docker exec build-nginx-nginx nginx -s reload"
                    } catch(Exception e){
                        echo 'Não foi possível executar o primeiro comando, será executado o segundo. Motivo: ' + e.toString()
                        sh "docker compose -f docker-compose-geral.yml up -d"
                    }
                }
            }
        }
    }
}