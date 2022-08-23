
FROM python:3

WORKDIR /opt

ADD app/* .

RUN pip install -r requirements.txt

CMD ["/bin/bash"]
