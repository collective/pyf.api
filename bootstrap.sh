#!/bin/bash
eval "$(pyenv init -)"
export PYENV_VIRTUALENV_DISABLE_PROMPT=1
eval "$(pyenv virtualenv-init -)"
VENV=pyf.api
pyenv install -s 3.8.1
pyenv virtualenv 3.8.1 $VENV
pyenv local $VENV
pyenv activate $VENV
pip install -e .[testing,dev] -c constraints.txt
