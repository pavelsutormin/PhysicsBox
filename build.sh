pip install flask
mkdir assets
cp main.py assets/main.py
cp phys_tools.py assets/phys_tools.py
zip -r index.apk assets
rm -rf assets
rm -rf dist
mkdir dist
cp index.apk dist/index.apk
rm -f index.apk
cp index.html dist/index.html
