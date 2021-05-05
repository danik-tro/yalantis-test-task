FROM python:3.8

WORKDIR /usr/src/app

ADD app/ /user/src/app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
