# Pull base image
FROM python:3.9

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

# Install dependencies


RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --dev

COPY . .


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "&&", "alembic", "upgrade", "head"]





