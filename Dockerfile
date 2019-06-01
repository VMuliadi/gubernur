FROM jfloff/alpine-python

COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "app.py"]
