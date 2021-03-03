#!/bin/bash

version=$((`cat ./version`))
newversion=$(($version + 1))
echo $newversion > ./version

rm -rf build
rm -rf dist
rm -rf Python_Java_Stream.egg-info

python3 setup.py sdist bdist_wheel  
twine upload dist/*