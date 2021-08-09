FROM python:3

ENV PYTHONUNBUFFERED=0

WORKDIR /usr/src/app

COPY ../requirements/requirement.txt /usr/src/app
RUN pip install -r requirement.txt

COPY .. /usr/src/app

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "letterlog.wsgi:application"]