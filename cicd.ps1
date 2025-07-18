# cicd.ps1
# This script automates the release process for the bdomarket package using Poetry and Git.
# Ensure you have Poetry installed and configured in your environment.
param(
    [string]$CommitMessage = ""
)
# Version bumping and tagging
# poetry version major
# poetry version minor
# poetry version patch
# Commit the version change and push to the main branch
$version = poetry version --short

if (![string]::IsNullOrWhiteSpace($CommitMessage)) {
    $fullMessage = "Release version v$version - $CommitMessage"
} else {
    $fullMessage = "Release version v$version"
}

git add .
git commit -am "$fullMessage"
git push origin master
git tag $version
git push origin --tags

# Build and upload the package (commented out for now)
# poetry build --clean -o build
# twine upload build/*

# * From cmd run: cicd.ps1 -CommitMessage "Your commit message here"