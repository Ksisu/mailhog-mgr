FROM python:3.7.3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG BUILD_VERSION=dev
ENV VERSION=$BUILD_VERSION
ENV DOMAIN=localhost

EXPOSE 5000

CMD ["python", "main.py"]
