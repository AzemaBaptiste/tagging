FROM python:3.8-alpine

COPY app.py /app/
COPY requirements.txt /app/
COPY db/tagging.sqlite3 /app/db/tagging.sqlite3

WORKDIR /app
RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["app.py"]
