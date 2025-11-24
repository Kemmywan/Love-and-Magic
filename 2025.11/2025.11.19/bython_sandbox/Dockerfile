FROM python:3.12-alpine

WORKDIR /app

COPY app/requirements.txt /app/
RUN pip3 install -r requirements.txt

COPY app /app

RUN chmod 755 -R /app
RUN chmod 777 -R /app/upload
RUN chmod 444 /app/upload/sandbox.by

RUN find /app/ -exec touch {} +

COPY start.sh /
CMD [ "sh", "/start.sh" ]
