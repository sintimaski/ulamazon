# Assumptions

1. Per task, no need to use ModelViewSet for each view, Products could have 
   ReadOnlyModelViewSet, Order is fine with ModelViewSet

2. Per task, assuming all auth and permissions could be skipped, all relations with users 
   are made with declared ID in BODY

3. Assuming that both mobile and frontend teams would use the same API without separation

4. Assuming (GET + pagination + filtering for orders) AND (POST + PUT + DELETE) will 
   be added in later stages

5. For bigger applications, there would be better infrastructure -- CI/CD, 
   Pipenv/Poetry, containerization, etc.

6. Proper auth for tests

7. Proper library setup - formatters, linters, security checkers, etc.


# Run
1. pip install -r requirements.txt
2. python manage.py migrate 
3. python manage.py createsuperuser
5. python populate_db.py
6. python manage.py runserver


# TEST
1. python manage.py test


### Please note there is postman collection attached to the project

# Extra
- black is used for formatting
- isort is user for imports optimizing
