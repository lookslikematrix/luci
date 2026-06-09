def preCommit() {
    sh '''
        set -e
        . ./.venv/bin/activate
        CHANGED_FILES=$(git diff --name-only ${TARGET_BRANCH:-origin/main}...HEAD)
        echo "[ $CHANGED_FILES | $TARGET_BRANCH ] 🔎 Changed files related to target branch."
        pre-commit run --files $CHANGED_FILES
    '''
}

return this
