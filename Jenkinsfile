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
                sh '''
                set -e
                python -m venv .venv
                . ./.venv/bin/activate
                pip install poetry
                poetry install
                CHANGED_FILES=$(git diff --name-only ${TARGET_BRANCH:-origin/main}...HEAD)
                echo "[ $CHANGED_FILES | $TARGET_BRANCH ] 🔎 Changed files related to target branch."
                poetry run pre-commit run --files $CHANGED_FILES
                '''
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
                . ./.venv/bin/activate
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
