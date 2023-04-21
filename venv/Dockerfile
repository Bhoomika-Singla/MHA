FROM ubuntu

WORKDIR /app
COPY . /app

RUN apt update && \
    apt-get install -y python3-pip && \ 
    pip3 install --no-cache-dir -r requirements.txt 

EXPOSE 5000
ENV FLASK_APP=app.py

CMD ["flask","run","--host=0.0.0.0"]