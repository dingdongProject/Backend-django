# Backend-django
Backend server for dingdong project. <br>
Based on Django & Django-restframework.

## About Dingdong
<img src="https://github.com/dingdongProject/Backend-django/blob/master/image/dingdong.gif?raw=true" width="150"/>
Dingdong is an mobile app for managing circles(social clubs) and to communicate with the members of the circle. It started as a project for Software Engineering
class at HanYang University. It provides simple but useful functions for circle admins and members to use. This repository is for backend server of dingdong project.

## Project Setup
```
python3 -m venv venv
source venv/bin/activate (linux & mac)

pip install -U pip
pip install -U setuptools
pip install -r requirements.txt
```
Create AWS.py in dingdong3/dingdong3
```
class AWS:
  AWS_ACCESS_KEY_ID = "AKIARJNGMVAWQ77ZAXRE"
  AWS_SECRET_ACCESS_KEY = "M9ZOWpstz3muYOdasdasKM5dHYafO7wslC8X9WZ5sY9k"
```
(Not real Access Keys)

## Usage
```
$ python manage.py makemigrations --settings=dingdong3.settings.local
$ python manage.py migrate --settings=dingdong3.settings.local
$ python manage.py runserver --settings=dingdong3.settings.local
```
server will be running at http://127.0.0.1:8000/

## Package

- Django 3.1.2
- boto3 1.16.17
- Djangorestframework 3.12.1


## API
| Address                               | Method | Explanation                                              |
|---------------------------------------|--------|----------------------------------------------------------|
| ping                                  | POST   | returns "pong".  To check if connected.                  |
| signup                                | POST   | To signing up                                            |
| login                                 | POST   | To Login                                                 |
| user                                  | GET    | To get information  about the user                       |
| user/circles                          | GET    | To get information about  the circle user is a member of |
| users/<username>                      | GET    | To get information  about other users                    |
| membership                            | POST   | To join a circle                                         |
| membership                            | DELETE | To withdraw from a circle                                |
| circles                               | POST   | To create a circle                                       |
| circles                               | GET    | To get list of circles                                   |
| circles                               | DELETE | To remove a circle                                       |
| circles/<circle_name>                 | GET    | To get information  about a circle                       |
| circles/<circle_name> /members        | GET    | To get members of a circle                               |
| circles/<circle_name> /boards         | GET    | To get list of boards in a circle                        |
| circles/<circle_name> /boards         | POST   | To create a board for a circle                           |
| circles/<circle_name> /notices        | GET    | To get list of notices of a circle                       |
| board/<board_id>                      | GET    | To get information of a board                            |
| board/<board_id>                      | PUT    | To modify a board                                        |
| board/<board_id>/post                 | POST   | To create a post in a board                              |
| board/<board_id>/post                 | GET    | To get posts inside a board                              |
| post/<board_id>/read                  | POST   | To mark 'read' to a post                                 |
| post/<board_id>/comment               | POST   | To create a comment to a post                            |
| post/<board_id>/comment               | GET    | To get comment list of a post                            |
| post/<board_id>/comment /<comment_id> | DELETE | To delete a comment                                      |
| post/<board_id>/comment /<comment_id> | PUT    | To modify comment                                        |
| schedules                             | GET    | To get schedules of circle                               |
| schedules                             | POST   | To create a schedule for a cicle                         |

## To-do
- Vote function api
- Ladder game funciton api
- Modify user information
- Modify Circle information
- Modify Board
- Delete Board
- Set/change Board authorization
- Modify Post
- Delete Post


## Contributors

- [junseublim](https://github.com/junseublim)
- [colorful-ahn](https://github.com/colorful-ahn)
- [chh12497](https://github.com/chh12497)

## Related Repositories
- [dingdong-Frontend](https://github.com/dingdongProject/Frontend-react-native)
- [dingdong-documents](https://github.com/dingdongProject/documentation)
