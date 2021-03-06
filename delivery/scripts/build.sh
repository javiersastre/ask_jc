#!/bin/bash

PYTHON=`command -v python3`
ASK_JC_VENV=$HOME/ask_jc_venv
SCRIPTFOLDER="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOTFOLDER="$SCRIPTFOLDER/../.."
DOCKER_USER="docker"
USER=`whoami`

echo "***************************************"
echo "* Deleting old virtualenv, if present *"
echo "***************************************"

if [ -n "$VIRTUAL_ENV" ]; then
  if [ -n "$(typeset -F | grep -o deactivate)" ]; then
    echo "Deactivating virtualenv"
    deactivate
  else
    echo "Error: cannot deactivate virtualenv; invoke this script with \"source $0\""
    exit 1
  fi
fi
if [ -n "$(ls -A $ASK_JC_VENV)" ]; then
   echo "Deleting virtualenv"
   rm -R $ASK_JC_VENV/*
fi

echo "************************************"
echo "* Creating new virtual environment *"
echo "************************************"

$PYTHON -m venv $ASK_JC_VENV

# Activate virtual environment
source $ASK_JC_VENV/bin/activate

echo "**********************************"
echo "* Installing global dependencies *"
echo "**********************************"
pip install --upgrade pip==20.0.2
pip install --upgrade setuptools==45.0.0
pip install --upgrade wheel==0.33.6
pip install -r $ROOTFOLDER/requirements.txt
if [ "$USER" != "$DOCKER_USER" ]; then
  pip install pytest==5.3.2
  pip install jupyterlab
  pip install ipywidgets
fi

echo "*****************************"
echo "* Installing Python package *"
echo "*****************************"

cd $ROOTFOLDER
pip install .
exit_code=$?
if [ $exit_code != 0 ]; then
	exit $exit_code
fi

echo "*****************************"
echo "* Installed Python packages *"
echo "*****************************"

pip freeze --all

echo "*****************"
echo "* Running tests *"
echo "*****************"

python setup.py test
