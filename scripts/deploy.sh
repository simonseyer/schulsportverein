#!/usr/bin/env bash
set -o errexit #abort if any command fails

echo "Deploying..."

git config user.name "$GIT_DEPLOY_USERNAME"
git config user.email "$GIT_DEPLOY_EMAIL"

commit_title=`git log -n 1 --format="%s" HEAD`
commit_hash=` git log -n 1 --format="%H" HEAD`
commit_message="publish: $commit_title [ci skip]"
commit_message="$commit_message"$'\n\n'"generated from commit $commit_hash"

git checkout -b build
git add $GIT_DEPLOY_DIR
git commit -m "$commit_message"
git checkout $GIT_DEPLOY_BRANCH
git merge build

#--quiet is important here to avoid outputting the repo URL, which may contain a secret token
git push --quiet $GIT_DEPLOY_REPO $GIT_DEPLOY_BRANCH
