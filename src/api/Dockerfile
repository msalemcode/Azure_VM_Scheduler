
FROM python:3.7

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
COPY init.sh /usr/local/bin/
EXPOSE 5000 
CMD ["python","main.py"]
