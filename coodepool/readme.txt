1.create superuser
	in terminal cd path-to-coodepool-project
	python manage.py makemigrations
	python manage.py migrate
	python manage.py createsuperuser
	add your email, username and password

2.security:
	- Password hashers(included in settings)
		Install Argon2: python -m pip install argon2-cffi 

3.crispy forms:
	- pip install django-crispy-forms

4.I have no time to make test.
		