pip uninstall -y bdomarket
cd src
python.exe setup.py egg_info sdist bdist_wheel
cd dist
Get-ChildItem *.whl | ForEach-Object { pip install $_.FullName }
cd ../..
pip list | Where-Object { $_ -match "bdomarket" }