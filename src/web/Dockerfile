
FROM python:3.7
RUN \
  pip --no-cache-dir install -U pip && \
  pip --no-cache-dir install azure-cli 

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
RUN chmod +x init.sh
EXPOSE 8000 
CMD ["/code/init.sh"]
