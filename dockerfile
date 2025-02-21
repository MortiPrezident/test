FROM python:3.12
COPY requirements.txt ./requirements.txt
workdir /home/test

ENV PYTHONPATH=/home
RUN pip install -r requirements.txt
COPY . ./home/test



CMD ["python", "main/main.py"]