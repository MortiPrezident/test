FROM python:3.12


COPY requirements.txt ./requirements.txt


ENV PYTHONPATH=/home
RUN pip install -r requirements.txt
COPY . .



CMD ["python", "main/main.py"]