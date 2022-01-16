FROM python:3.8

WORKDIR /app

COPY . .

EXPOSE 5005

RUN pip install -r requirements.txt

CMD [ "gunicorn", "-w", "3", "-b", "0.0.0.0:5005", "flasky:app" ] 