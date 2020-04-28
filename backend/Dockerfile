FROM python:3.8
WORKDIR /code
CMD ["uvicorn", "readyupper.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

RUN pip install -e ".[dev]"
