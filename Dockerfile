# FROM python:3.11.4

# WORKDIR /app

# COPY ./ ./

# RUN pip install -r requirements.txt

# LABEL author.name="Le Minh Huy"
# LABEL author.email="leminhhuy.hcmus@gmail.com"

# EXPOSE 8050
# CMD ["python", "./main.py"]

FROM ubuntu:latest

RUN apt-get update -y && apt upgrade