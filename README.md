# 🛎  Dingdong <img src="https://img.shields.io/badge/React%20Native-0.63.3-blue" /> 
**동아리를 위한 커뮤니티 앱 서비스: 딩동** 

<img src="https://github.com/dingdongProject/Backend-django/blob/master/image/dingdong.gif?raw=true" width="150"/>


## ❔  딩동이란 


### 🔍  왜 딩동이 나왔을까 

우리 팀의 팀원들은 모두 동아리, 대외활동을 최소 한 개 이상씩 참여하고 있습니다. 그러다 보니 여러 단체 카톡방에 초대되어 있었습니다. 또한 동아리마다 그룹별로 여러개의 카톡방을 운영하는 경우도 있죠. 그러다 보니 공지사항이나 스케쥴 등 필요한 정보들이 제각각 흩어져 있어서 한꺼번에 모아보기가 매우 불편했습니다. 특히 카톡에서는 공지를 하나밖에 띄우지 못하기 때문에 공지가 두개 이상이면 하나는 직접 스크롤을 올려서 확인해야 했습니다. 우리들은 이러한 방식이 불편하고 비효율적이라 생각했습니다. 

### 🖥  딩동의 기능 

따라서 우리는 "딩동"을 생각하게 되었습니다. 딩동은 동아리 관리, 소통을 위한 모바일 앱입니다. 딩동은 크게 3가지 기능으로 나눌 수 있습니다. 

#### 1. 동아리 페이지

각 동아리마다 페이지를 생성하여 페이지내에서 동아리원들끼리 정보를 공유할 수 있습니다. 페이지내에는 여러 개의 게시판을 생성할 수 있습니다. 게시판은 필요에 따라 생성하고 읽기, 쓰기 권한을 동아리원에게 부여하여서 게시판을 관리 할 수 있습니다. 예를 들어 공유해야하는 정보가 있다면 임원 게시판을 생성하여 임원들만이 읽기, 쓰기를 가능하게 하여서 게시판 내에서 임원들끼리 게시글을 작성하고, 읽을 수 있게 할 수 있습니다. 

부가적인 기능으로는 게시글에서 투표, 사다리 타기, '확인' 기능 이 있습니다. 이러한 기능들은 글 작성자가 선택하여 동아리원들에게 제공할 수 있습니다. 투표 기능을 사용한다면 회식 장소를 고를때 동아리원들이 원하는 메뉴가 무엇인지를 파악하기 쉬워지겠죠! 사다리 타기 기능을 사용한다면 역할 분담할 때 눈치를 볼 필요없이 '운'에 맡길 수 있게됩니다! '확인' 기능은 어떤 동아리원들이 게시글을 읽었거나 안읽었는지를 쉽게 파악할 수 있게 도와줍니다. 이러한 유용한 기능들을 통해 더욱 즐거운 동아리 활동을 할 수 있습니다.

#### 2. 스케쥴 관리

동아리에서 가장 중요한 공지는 당연히 일정에 관한 것이겠죠. 언제 어디서 무엇을 하는지를 동아리원들에게 잘 전달하는 것은 임원들의 숙제이자 역할이라고 할 수 있습니다. 이러한 부담을 덜어주기 위해 우리는 스케쥴 페이지를 따로 만들어 스케쥴을 동아리원들과 쉽게 공유할 수 있도록 도와주고자 하였습니다. 동아리 임원들은 일정을 추가하는 것만으로 쉽게 동아리원들에게 일정을 알려줄 수 있습니다. 동아리원들은 여러 동아리들의 일정을 확인하고 모아볼 수 있어서 유용할 것입니다.

#### 3. 동아리 찾기

자신이 원하는 동아리를 찾는 것은 쉽지않습니다. 반대로 동아리 임원들은 자신들의 동아리를 홍보하는 것이 매우 귀찮을 것입니다. 우리는 이 둘을 이어주고자 동아리를 홍보하고, 검색하여 지원할 수 있는 기능을 제공합니다. 동아리는 자신들의 동아리에 대한 간략한 설명과 해시태그를 설정하여 다른 사람들에게 홍보할 수 있습니다. 반대로 동아리를 찾고자하는 사람들은 자신들이 원하는 동아리를 선택하여 바로 지원할 수 있습니다.


#### 딩동에 관한 더 자세한 내용은 [dingdong-documents](https://github.com/dingdongProject/documentation) 레포지토리를 확인해주시면 감사하겠습니다!


## 📺  데모 링크 
###  자막을 키고 봐주시면 감사하겠습니다! 
[dingdong_demo](https://www.youtube.com/watch?v=3OvvbV-6EnE&t=188s)

## 🛠  Project Setup  
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
(실제 키는 아닙니다!)

## 🖱  실행 방법
```
$ python manage.py makemigrations --settings=dingdong3.settings.local
$ python manage.py migrate --settings=dingdong3.settings.local
$ python manage.py runserver --settings=dingdong3.settings.local
```
server will be running at http://127.0.0.1:8000/

## 📦  Packages 

- Django 3.1.2
- boto3 1.16.17
- Djangorestframework 3.12.1


## 📝  API
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

## 🗒  To-do 
- Vote function api
- Ladder game funciton api
- Modify user information
- Modify Circle information
- Modify Board
- Delete Board
- Set/change Board authorization
- Modify Post
- Delete Post


## 🔥 Contributors 🔥

- 🇰🇷 [junseublim](https://github.com/junseublim)
- 🇰🇷 [colorful-ahn](https://github.com/colorful-ahn)
- 🇰🇷 [chh12497](https://github.com/chh12497)

## 🔗  Related Repositories 
- [dingdong-Frontend](https://github.com/dingdongProject/Frontend-react-native)
- [dingdong-documents](https://github.com/dingdongProject/documentation)
