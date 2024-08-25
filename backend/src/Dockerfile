FROM python:3.10-slim@sha256:980b778550c0d938574f1b556362b27601ea5c620130a572feb63ac1df03eda5

ENV PYTHONUNBUFFERED True

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r  requirements.txt

ENV APP_HOME /root
WORKDIR $APP_HOME
COPY /. $APP_HOME/.

EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]