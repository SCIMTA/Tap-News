FROM python:3.8
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list
RUN apt-get update
RUN apt-get install -y google-chrome-stable
ENV DISPLAY=:99
RUN pip3 install -r requirements.txt

CMD [ "uvicorn","service:app","--host", "0.0.0.0","--port","4040"]