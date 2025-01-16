FROM python:3.12.3-slim


WORKDIR /app/backend

# Копируем зависимости в контейнер
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копируем весь проект в контейнер
COPY . /app/

# Открываем порт 8000
EXPOSE 8000

# Запускаем manage.py из директории backend
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
