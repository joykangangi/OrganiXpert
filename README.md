## OrganiXpert - Organic Fertilizer Recommender System

### Prerequisites
- [Django](https://www.djangoproject.com/)
- [Python](https://www.python.org/)
- [Pip](https://pypi.org/project/pip/)
- [Virtualenv](https://virtualenv.pypa.io/en/latest/)
- [SQLite3](https://www.sqlite.org/index.html)

### Installation
1. Clone the repository
2. Create a virtual environment, using `virtualenv` or `venv` run `virtualenv venv` or `python3 -m venv venv` 
3. Activate your virtual environment `source venv/bin/activate` or cd into the directory and run `venv\Scripts\activate`
4. Install the requirements `pip install -r requirements.txt`
5. Create an `env` file in the root directory i.e. `organixpert/` and copy the contents of `env.example` to it
6. Run the migrations `python manage.py migrate`
6. Create a superuser `python manage.py createsuperuser`
8. Run the server `python manage.py runserver`

### Contributing
1. Fork the repository
2. Create a new branch `git checkout -b <branch-name>`
3. Make the changes and commit them `git commit -m "<commit-message>"`
4. Push the changes to the branch `git push origin <branch-name>`
5. Create a pull request



