FROM python:3.9-slim AS compiler
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN apt-get update && apt-get install -y wget curl
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./app.py" ]