FROM python:3.11

RUN apt-get update && apt-get install -y libgl1-mesa-glx

WORKDIR /app

COPY . /app

RUN pip install --trusted-host pypi.org -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
