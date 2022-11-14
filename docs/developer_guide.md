# Developing for this Project

## 1. Tooling Prerequisites
This project is implemented in the Python Programming Language.  
Here is the tooling that you will need to install to get started:
- Python 3.10
- Poetry

## 2. Install Library Prerequisites
Installing these dependencies onto your Ubuntu/Linux system up-front will 
save you lots of compile-time headaches later   
```
sudo apt install openjdk-17-jdk
sudo apt install autoconf
sudo apt install libffi-dev
sudo apt install libssl-dev 
```


## 3. Compile Python from Source
This compiles a custom version of Python that dynamically links against
the OpenSSL libraries that you installed in the last step. We will be 
using this Python rather than the prebuilt one you currently have 
installed on your system. Not doing this step will cause build errors 
later, so don't skip this.
```
mkdir -p ~/src/python_build 
cd ~/src/python_build 

wget https://www.python.org/ftp/python/3.10.0/Python-3.10.6.tgz 
tar -xvf Python-3.10.8.tgz 

cd Python-3.10.8 
./configure --prefix=$HOME/opt/python/python-3.10.8 --enable-optimizations 
make 

mkdir -p ~/opt/python 
make install 

# Clean our build directory. We don't need it anymore
rm -rf ~/src/python_build 
```

## 4. Fetching the Project Sources
```
cd ~/src/
git pull https://github.com/jhaslam/mirp.git
```

## 5. Setting up the Python Dev Environment
```commandline
cd ~/src/mirp
poetry config virtualenvs.in-project true
poetry init
poetry shell
python -m pip install --upgrade pip 
poetry install --no-root
```

## 6. Building the project
```commandline
buildozer android debug deploy run
```
The resulting .apk file can be found in ```./bin```

# Troubleshooting
Should the buildozer build fail, it is usually because of a missing
dependency. Should this happen, make sure to run a clean before
rebuilding:
```commandline
buildozer android clean
```
