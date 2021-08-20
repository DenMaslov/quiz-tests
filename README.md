**Dockerhub**  https://hub.docker.com/repository/docker/denmaslov/quiz

use **docker pull denmaslov/quiz:dz**  - to download image

**docker run -p 8000:8000 denmaslov/quiz:dz** - to run



### INSTALLATION:
1. git clone --branch docker https://github.com/DenMaslov/quiz-tests.git
2. cd quiz-tests
3. pipenv shell
4. pipenv install
5. cd survey_models_django
6. py manage.py migrate **or** you can use already created db https://drive.google.com/file/d/1r9jSjdQmVALtr5RVXZQQY_3mEoySDkcI/view?usp=sharing for testing functionality


### TESTED WITH:
* Windows 10
* Chrome
* python 3.9
