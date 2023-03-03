# Developing for this Project

## 1. Tooling Prerequisites
This project is implemented in the Python Programming Language.  
Here is the tooling that you will need to install to get started:
- Python 3.10
- Poetry

## 2. Library Prerequisites
Installing these dependencies onto your Ubuntu/Linux system up-front will 
save you lots of compile-time headaches later   
```
sudo apt install openjdk-17-jdk
sudo apt install autoconf
sudo apt install libffi-dev
sudo apt install libssl-dev 
```


## 3. Compile Python Language from Source
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

## 6. Building the project for Android
### Serial Port Dependencies
Follow the instructions:
- https://github.com/frmdstryr/kivy-android-serial
- https://github.com/jacklinquan/usbserial4a


```commandline
buildozer android debug deploy run
```
The resulting .apk file can be found in ```./bin```

### Troubleshooting
Should the buildozer build fail, it is usually because of a missing
dependency. Should this happen, make sure to run a clean before
rebuilding:
```commandline
buildozer android clean
```

### Debugging
Install the Android Debug Bridge

1) Make sure you have permission for USB access
   - Check to see if you are part of the "dialout" group
     ```commandline
     groups ${USER}
     ```
   - Add yourself to the "dialout group if you are not in it
     (Note: I had to reboot for this to take effect)
     ```commandline
     sudo newgrp dialout
     sudo gpasswd --add ${USER} dialout
     ```

2) Install ADB
   ```commandline
   sudo apt install adb
   ```
3) Install the program from the linux command line
    ```commandline
     adb install -r bin/*.apk
    ```
4) Start the logger
    ```commandline
     adb logcat -s "python"
    ```
5) Launch the application
   - You should start to see log files appearing on the screen


# device_filter.xml
put this in:
```commandline
.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/mirp/src/main/res/xml/device_filter.xml
```
```commandline
<?xml version="1.0" encoding="utf-8"?>

<resources>
    <!-- <usb-device vendor-id="16c0" product-id="0483" />  -->
    <usb-device vendor-id="0403" product-id="6001" />
</resources>
```
