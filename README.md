folllow these steps to run the project in your system
1. create a directory in your pc
cd ~   # or any location you like
mkdir test-school-enrollment
cd test-school-enrollment
2. clone/download the project
git clone https://github.com/AbdulSamad-dev/school-enrollment-system.git
cd school-enrollment-system
3. Install dependencies (directly on your system)
pip freeze > requirements.txt
python manage.py migrate
python manage.py runserver

here you go...
username: admin
password: admin
