FROM python:3.12
COPY requirements.txt ./requirements.txt
workdir /home

RUN pip install -r requirements.txt
COPY . .
ENV PYTHONPATH=/home


CMD ["python", "test/main/main.py"]