rm -r build -ErrorAction SilentlyContinue

# Define custom folders
$egginfo = "../build/egginfo"
$tempbuild = "../build/temp_build"
$dist = "../build/dist"

# Save current location and switch to src
Push-Location src

# Ensure output directories exist
New-Item -ItemType Directory -Force -Path $egginfo | Out-Null
New-Item -ItemType Directory -Force -Path $tempbuild | Out-Null
New-Item -ItemType Directory -Force -Path $dist | Out-Null

# Run the build commands
python setup.py `
    egg_info --egg-base $egginfo `
    build --build-base $tempbuild `
    sdist --dist-dir $dist `
    bdist_wheel --dist-dir $dist

# Go back to original folder
Pop-Location

# Optionally upload with twine
twine upload build/dist/*