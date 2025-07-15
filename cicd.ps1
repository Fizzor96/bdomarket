# cicd.ps1
# This script automates the release process for the bdomarket package using Poetry and Git.
# Ensure you have Poetry installed and configured in your environment.

# Version bumping and tagging
# poetry version major
# poetry version minor
poetry version patch
# Commit the version change and push to the main branch
$version = poetry version --short
git add .
git commit -am "Release version v$version"
git push origin master
git tag $version
git push origin --tags

# Build and upload the package (commented out for now)
# poetry build --clean -o build
# twine upload build/*