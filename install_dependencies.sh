#! /bin/bash
if [ ! -d "repos" ]; then
    mkdir repos
fi
cd repos
git clone https://github.com/mathLab/PyGeM
cd PyGeM
python setup.py install
cd ../..
pip install scikit-learn scikit-gstat
# required for displaying matplotlib figures under Linux
if [ "$(uname -s)" == "Linux" ]; then
    pip install PyQt5
fi