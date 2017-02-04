Data driver analysis problem

This folder contains files to help process the sales data, analyze the trends
and prepare backend systems necessary to relay them to the dashboard.

### Setup

1. Install miniconda to manage your Python environment
```bash
# miniconda setup
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
source ~/.bashrc
```
2. Use the attached `environment.yml` to duplicate the required environment for
   this folder
```bash
conda env create -f environment.yml
source activate hacktheworld
```
3. Installing `xgboost` after `source activate hacktheworld`.
```bash
git clone --recursive https://github.com/dmlc/xgboost
git submodule init
git submodule update
cd xgboost
make -j4
cd python-package
python setup.py install
```
4. Reading the data file into your program, you can use the library
[utils/reader.py](utils/reader.py). Run the sample code at
[analyze.py](analyze.py)
```bash
python analyze.py
```
