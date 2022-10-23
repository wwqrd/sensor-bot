FROM arm32v7/python:slim

RUN apt-get update -y && apt-get install -yq python3-smbus libmosquitto-dev libffi-dev gcc make

RUN mkdir /app
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "./sensor-bot.py"]
