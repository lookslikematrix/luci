pipeline {
    agent {
        docker {
            image "python:3.14"
            reuseNode true
        }
    }

    environment {
        XDG_CACHE_HOME  = "${WORKSPACE}/.cache"
    }

    stages {
        stage("🔶 Pre-Commit") {
            steps {
                sh '''
                set -e
                python -m venv .venv
                . ./.venv/bin/activate
                pip install -e .[test]
                pip install -e .[build]
                CHANGED_FILES=$(git diff --name-only ${TARGET_BRANCH:-origin/main}...HEAD)
                echo "[ $CHANGED_FILES | $TARGET_BRANCH ] 🔎 Changed files related to target branch."
                pre-commit run --files $CHANGED_FILES
                '''
            }
        }
        stage("🕵️ Software-Composition-Analysis") {
            steps {
                sh """
                set -e
                . ./.venv/bin/activate
                cyclonedx-py environment .venv --output-file src/luanti_cli/bom.json
                """
            }
        }
        stage("🔨 Build") {
            steps {
                sh """
                set -e
                . ./.venv/bin/activate
                python -m build
                """
            }
        }
        stage("🧪 Test") {
            steps {
                sh """
                set -e
                . ./.venv/bin/activate
                pytest --junit-xml junit.xml --cov src.luanti_cli --cov-report xml:cobertura.xml tests/
                """
                junit "junit.xml"
                discoverReferenceBuild()
                recordCoverage(tools: [[parser: 'COBERTURA']])
            }
        }
        stage("🚀 Deploy") {
            when {
                branch "main"
            }
            environment {
                UV_PUBLISH_TOKEN = credentials('luci_pypi_token')
            }
            steps {
                sh """
                set -e
                . ./.venv/bin/activate
                uv publish
                """
            }
        }
    }
}
