FROM python:3.11

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./source /code/source

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5001

CMD ["uvicorn", "source.main:source", "--host", "0.0.0.0", "--port", "5001"]
