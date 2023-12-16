# Welcome to shopX E-commerce

## Run this project locally

* Clone the repo `https://github.com/imrand-dev/shopX-backend.git`.
* Create virtual env `python -m venv <NameOfTheEnvironment>`.
* To activate the virtualenv
    * On macOS `source <NameOfTheEnvironment>/scripts/activate`
    * On Windows `<NameOfTheEnvironment>\Scripts\activate`
* To install all the dependencies type `pip install -r requirements/development.txt` in the command prompt. (optional)
* Enter the `projectile/` directory.
* To migrate the database `python manage.py migrate`.
* Run the server `python manage.py runserver`.
* Exit the virtual env `deactivate`.