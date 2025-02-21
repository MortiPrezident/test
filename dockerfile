FROM python:3.12
COPY requirements.txt ./requirements.txt
workdir /home

RUN pip install -r requirements.txt
COPY . ./test
RUN export PYTHONPATH=/home && echo "PYTHONPATH set to $PYTHONPATH"


CMD ["python", "test/main/main.py"]