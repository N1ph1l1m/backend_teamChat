FROM python:3.12.3-slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD [" python", "manage.py"]