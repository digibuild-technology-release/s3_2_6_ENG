FROM python:3.9-slim

WORKDIR /app

ENV SKLEARN_ALLOW_DEPRECATED_SKLEARN_PACKAGE_INSTALL=True

ADD . /app/
COPY . /app/

RUN python -m pip install --upgrade pip 
RUN python -m pip install -r requirements.txt

EXPOSE 8090

# Run app.py when the container launches
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8090"]