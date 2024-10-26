pip install flask
pip install gunicorn
zip index.apk main.py phys_tools.py
rm -rf dist
mkdir dist
cp index.apk dist/index.apk
rm -f index.apk
cp index.html dist/index.html
