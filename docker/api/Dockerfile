FROM python:3

# Ports
EXPOSE 5000

RUN apt-get update -y \
    && apt-get install -y python-pip python-dev

COPY . /data_manager
WORKDIR /data_manager

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python" ]
CMD [ "data_manager/app.py" ]
