python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
django-admin startproject myproject
cd myproject
python3 manage.py startapp myapi