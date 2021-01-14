# Setting up your Crownstone Virtual Environment
Crownstone has a number of separate python libraries in order to ensure that everyone can 
keep dependencies minimal and separate development into their natural domains. To facilitate
your dependencies and allow smooth upgrades when we improve our code base (with an occasional
breaking change of API), we suggest that developers work in a virtual environment. This tutorial
helps get you up and running in no time.

If you haven't ever done so before, chances are that you need to run the following command 
to install the `venv` module on your system.

```
python3 -m pip install venv
```

Afterwards you can create a virtual environment in your favourite directory like so:
```
cd ~/Documents/my_crownstone_env
python3 -m venv crownstone_env
```


# Activate virtual environment
Activating a virtual environment needs to be done every time ou reopen the console,
or after manual deactivation.
```
source crownstone_env/bin/activate
```

# Install the crownstone python libraries
This should only be necessary once, when setting up the venv, after activating the environment.

First of all, make sure that you install `wheel`.

```
python3 -m pip install wheel
```

### option one: follow major releases
There are basically two installation options that we suggest. First of which is the easiest. Just use te PiPy repository
to obtain the latest release of our libraries.

```
python3 -m pip install crownstone_core
python3 -m pip install crownstone_uart
python3 -m pip install crownstone_ble
python3 -m pip install crownstone_cloud
python3 -m pip install crownstone_sse
```

### option two: bleeding edge
If you really want a bleeding edge build, you can also clone our repositories from github and install
an editable build in your virtual environment. Cloning the repos is a breeze, just `cd` to your favourite
folder and `git clone` them like so:

```
cd ~/Documents
git clone https://github.com/crownstone/crownstone-lib-python-core.git
git clone https://github.com/crownstone/crownstone-lib-python-uart.git
git clone https://github.com/crownstone/crownstone-lib-python-ble.git
git clone https://github.com/crownstone/crownstone-lib-python-cloud.git
git clone https://github.com/crownstone/crownstone-lib-python-sse.git
```

After that step install them as editable through pip and you'll be able to
edit your cloned repositories, branch and play around without having to force any
reinstalls.

```
python3 -m pip install --editable ~/Documents/crownstone-lib-python-core/
python3 -m pip install --editable ~/Documents/crownstone-lib-python-uart/
python3 -m pip install --editable ~/Documents/crownstone-lib-python-ble/
python3 -m pip install --editable ~/Documents/crownstone-lib-python-cloud/
python3 -m pip install --editable ~/Documents/crownstone-lib-python-sse/
```

Fun last note: it's perfectly okay to install these two virtual environments side by side if you want to 
mess around with your clones and check if everything works on released versions in parallel.

# Running (ble) examples in your venv
This is only relevant to those that have installed the git repositories in editable mode. The examples are *not* included
in our PyPi releases.

As most of crownstones ble scripts will need to run in sudo mode due to access restrictions 
on the kernel bluetooth modules. By default, `sudo python3` will run your native `python3` 
installation, and not the venv we've just set up. To fix this, use the following commands to
create a helper file with a few environment variables that enable easy access to the libs
and the correct interpreter in sudo mode.

```
echo PYTHON3=~/Documents/crownstone_env/bin/python3 >> utility_env_variables
echo CRWN_CORE=~/Documents/crownstone-lib-python-core >> utility_env_variables
echo CRWN_UART=~/Documents/crownstone-lib-python-uart >> utility_env_variables
echo CRWN_BLE=~/Documents/crownstone-lib-python-ble >> utility_env_variables
echo CRWN_CLOUD=~/Documents/crownstone-lib-python-cloud >> utility_env_variables
echo CRWN_SSE=~/Documents/crownstone-lib-python-sse >> utility_env_variables
```

When you have created the file `utiltiy_env_variables` just `source` it once in a terminal session when needed.
```
source utility_env_variables
```

Now you can find and run your favourite example by means of the following, without encountering any access violations:

```
ls $CRWN_BLE/examples/example_*
sudo $PYTHON3 $CRWN_BLE/examples/example_continuous_scanning.py
```

Note: running in sudo mode is only necessary for the *ble* examples due to access restrictions of the bluetooth hardware.
You can choose to allow non-sudo users to the ble scanner background in this particular venv using the following line. 
(Be sure to replace the version suffix to match your venv python version.) If you execute this snippet, you can run the 
examples without sudo.  

```
sudo setcap 'cap_net_raw,cap_net_admin+eip' ./crownstone_env/lib/python3.8/site-packages/bluepy/bluepy-helper
``` 