rm -r dist
rm -r src/build
rm -r src/bdomarket.egg-info
python -m build src --sdist --wheel --outdir dist