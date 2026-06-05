pipeline {
    agent {
        docker {
            image "python:3.14"
            reuseNode true
        }
    }

    environment {
        XDG_CACHE_HOME = "${WORKSPACE}"
    }

    stages {
        stage("🔶 Pre-Commit") {
            steps {
                echo "Pre-Commit.."
            }
        }
        stage("🕵️ Software-Composition-Analysis") {
            steps {
                echo "Software-Composition-Analysis.."
            }
        }
        stage("🔨 Build") {
            steps {
                sh """
                set -e
                python -m venv .venv
                . ./.venv/bin/activate
                pip install poetry
                poetry build
                """
            }
        }
        stage("🧪 Test") {
            steps {
                sh """
                set -e
                . ./.venv/bin/activate
                poetry install
                poetry run pytest --cov luanti_cli --cov-report xml:cobertura.xml tests/
                """
                discoverReferenceBuild()
                recordCoverage(tools: [[parser: 'COBERTURA']])
            }
        }
        stage("🚀 Deploy") {
            when {
                branch "main"
            }
            environment { 
                POETRY_PYPI_TOKEN_PYPI = credentials('luci_pypi_token')
            }
            steps {
                sh """
                set -e
                . ./.venv/bin/activate
                poetry publish
                """
            }
        }
    }
}
