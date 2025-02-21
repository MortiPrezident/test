FROM python:3.12


COPY requirements.txt ./requirements.txt


ENV PYTHONPATH=/home/test
RUN pip install -r requirements.txt
COPY ./main ./main
COPY ./tests ./tests


CMD ["python", "main/main.py"]