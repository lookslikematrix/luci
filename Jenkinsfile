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
        stage("🧰 Prepare") {
            steps {
                sh '''
                set -e
                python -m venv .venv
                . ./.venv/bin/activate
                pip install uv
                uv sync --extra test --extra build
                '''
            }
        }
        stage("🔍️ Analyze") {
            failFast true
            parallel {
                stage("🔶 Pre-Commit") {
                    steps {
                        sh '''
                        set -e
                        . ./.venv/bin/activate
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
                allOf {
                    branch "main"
                    changeset "pyproject.toml"
                    anyOf {
                        changeset "src/**"
                        changeset "README.md"
                    }
                }
            }
            environment {
                UV_PUBLISH_TOKEN = credentials('luci_pypi_token')
            }
            steps {
                sh """
                set -e
                . ./.venv/bin/activate
                uv build
                uv publish
                """
            }
        }
    }
}
