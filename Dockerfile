FROM python:3.11.3-alpine

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 9000

CMD ["sh", "./bin/start.sh"]