FROM python:3.9
COPY src /usr/app/src
COPY .msgconfig /usr/app/src/.msgconfig
ENTRYPOINT ["python","/usr/app/src/main.py"]
