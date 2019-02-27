#!/bin/bash
eval "$(pyenv init -)"
export PYENV_VIRTUALENV_DISABLE_PROMPT=1
eval "$(pyenv virtualenv-init -)"VENV=pyf.api
pyenv install -s 3.7.2
pyenv virtualenv 3.7.2 $VENV
pyenv local $VENV
pyenv activate $VENV
pip install -e .[testing,dev] -c constraints.txt