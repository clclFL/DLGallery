FROM python:3.12

COPY . /app/

RUN pip install -r /app/requirements.txt

WORKDIR /app

EXPOSE 5000

CMD [ "python","app.py" ]