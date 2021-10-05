FROM python:3.8
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN pip3 install -r requirements.txt
CMD [ "uvicorn","service:app","--host", "0.0.0.0","--port","4040" ]