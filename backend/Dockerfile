FROM python:3.8
WORKDIR /code
RUN mkdir app
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

COPY requirements.txt /code
RUN pip install -r requirements.txt
COPY app /code/app
