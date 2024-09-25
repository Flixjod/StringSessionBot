FROM python:3.11

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "bot.py"]
