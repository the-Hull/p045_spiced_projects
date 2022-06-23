FROM python:3.8
WORKDIR /app
COPY requirements.txt /app/ 
RUN pip install --trusted-host pypi.python.org -r requirements.txt
COPY 01_ETL.py utils.py /app/
# ENV TZ=Europe/Berlin
# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
CMD ["python", "01_ETL.py"]