# How to set up Python and Django on a new Developers PC

This is a quick guide explaining how to set up a dev environment on a new developers machine. This guide assumes that PyCharm is used as an IDE.

## Create VENV

A VENV is required to properly use the python and pip commands.

First create the VENV, since its not in version control due to the files being different based on OS and CPU architecture.

- Open PyCharm Settings
- Go to the project settings
- Open "Python Interpreter"
- Click "Add Interpreter" -> "Add local interpreter"
- Create the new VENV in the `venv` folder

Ensure that the VENV is activated on project launch:

- Open the settings
- Go to Tools
- Open the Terminal settings
- Ensure that "Activate virtualenv" is enabled

Now reboot PyCharm. When then opening the Terminal the VENV should be activated (visible by the `(venv)` prefix).

## Install Django

Now that the VENV is ready we can install Django in the project.

```
# Install Django and Django REST framework into the virtual environment
pip install django
pip install djangorestframework
```
(Source: https://www.django-rest-framework.org/tutorial/quickstart/)

## Launch the project

Now that everything is set up you can launch the project using the Run configuration. If there are any issues please document their cause and resolution in this document.