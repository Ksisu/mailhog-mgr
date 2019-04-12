from flask import Flask
from flask import request
from gevent.pywsgi import WSGIServer
import os
import docker
import json

version = str(os.environ['VERSION'])
domain = str(os.environ['DOMAIN'])

app = Flask(__name__)

client = docker.from_env()

def list_mailhog_containers():
    return client.containers.list(filters={"label":"mailhog.name"});

def find_container(name):
    containers = list_mailhog_containers()
    return list(filter(lambda x: x.labels['mailhog.name'] == name, containers))

def get_public_port(container, port):
    return container.attrs['NetworkSettings']['Ports'][port][0]['HostPort']

def container_to_dto(c):
    return {
            "name": c.labels['mailhog.name'], 
            "smtp": domain + ":" + get_public_port(c, '1025/tcp'),
            "ui": "http://" + domain + ":" + get_public_port(c, '8025/tcp')
            }

@app.route("/")
def root():
    return app.send_static_file('index.html')

@app.route("/api/healthCheck")
def health_check():
    return "{\"success\":true,\"version\":\"" + version + "\"}\n"

@app.route("/api/list")
def list_containers():
    containers = list_mailhog_containers()
    container_list = list(map(container_to_dto, containers))
    return json.dumps(container_list)

@app.route("/api/create/<name>", methods=['POST'])
def create(name):
    container_find = find_container(name)
    if container_find:
        return "{\"error\":\"" + name + " is already used\"}", 400
    else:
        client.containers.run(image="mailhog/mailhog", detach=True, labels={"mailhog.name":name}, publish_all_ports=True)
        return "{}"

@app.route("/api/delete/<name>", methods=['POST'])
def delete(name):
    container_find = find_container(name)
    if not container_find:
        return "{\"error\":\"" + name + " is not found\"}", 404
    else:
        client.containers.get(container_find[0].id).remove(force=True)
        return "{}"

if __name__ == "__main__":
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
