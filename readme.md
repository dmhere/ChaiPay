# Chai Pay Challenge

Welcom to telnyx deployment steps

## Installation
Install python 3.6 or above [Python](https://www.python.org/downloads/)
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.
MongoDB installation required and to be run on localhost:27017 
[MongoDB](https://www.mongodb.com/try/download/community) 
With credentials - Please create a user with the access to db and update the 
username and password configuration acording after encryption using Fernet Encrypt
in utilities/encryptor 

```bash
pip install -r requirements.txt 
```
##Setup 
Add encrypted stripe key to db chai_pay_schema and collection stripe_data
as {"type": "stripe_key", "value":"<encrypted_key>"}
## Usage

Run  to see the project on http://localhost:8000
```bash 
python manage.py runserver
```

This gives the apis as asked on the local host

Run  to see the project on ip:8000/80
```bash 
python manage.py runserver 0.0.0.0:8000 
```
or 
```bash 
python manage.py runserver 0.0.0.0:80 
```

This gives the apis as asked on the http://ip_address:8000 and http://ip_address respectively for 80 and 8000





 
