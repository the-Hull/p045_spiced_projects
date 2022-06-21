FROM python:3.8
WORKDIR /app
COPY requirements.txt 01_collect.py utils.py /app/
# ENV TZ=Europe/Berlin
# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN pip install --trusted-host pypi.python.org -r requirements.txt
CMD ["python", "01_collect.py"]