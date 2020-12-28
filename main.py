# encoding=utf-8

import os
import json
from app import app 
from flask import Flask, flash, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, PasswordField, BooleanField 
from wtforms.fields.html5 import DateField 
from wtforms.validators import InputRequired, Email, Length
from routes import *
from logging import error, info
from subprocess import STDOUT, CalledProcessError, check_output
from itertools import islice
from kubernetes import client, config

app.register_blueprint(routes)

def get_namespaces():
    config.load_incluster_config()
    v1 = client.CoreV1Api()
    ns = v1.list_namespace()
    return ns

def get_tiller_namespaces():
    config.load_incluster_config()
    v1 = client.CoreV1Api()
    data = v1.list_deployment_for_all_namespaces(label_selector='name=tiller')
    return data

def get_deployments(namespace):
    config.load_incluster_config()
    v1 = client.CoreV1Api()
    data = v1.list_namespaced_deployment(namespace)
    return data

def get_charts(tiller_ns, namespace):
    command = "/usr/local/bin/helm --tiller-namespace " + tiller_ns + " list --output json" #helm2
    #command = "/usr/local/bin/helm -n " + namespace + " list -ojson" #helm3
    info(f"Running command: {command}")
    try:
        output = check_output(command.split(" "), stderr=STDOUT).decode("utf-8")
    except CalledProcessError as err:
        error(err.output.decode("utf-8"))
        raise err
    info(f"Output from command:\n{output}")
    if output:
        data = json.loads(output)
    else:
        data = 'EMPTY'
    return data

def sortRevision(n):
    return n['revision']

def get_chartdata(tiller_ns, namespace, chart, records):
    command = "/usr/local/bin/helm --tiller-namespace " + tiller_ns + " history " + chart + " --max " + records + " --output json" #helm2
    #command = "/usr/local/bin/helm -n " + namespace + " history " + chart + " -ojson" #helm3
    info(f"Running command: {command}")
    try:
        output = check_output(command.split(" "), stderr=STDOUT).decode("utf-8")
    except CalledProcessError as err:
        error(err.output.decode("utf-8"))
        raise err
    info(f"Output from command:\n{output}")
    data = json.loads(output)
    data.sort(reverse=True, key=sortRevision)
    for revision in data:
        revision['chartName'] = chart
        revision["namespace"] = namespace
        revision["tiller_ns"] = tiller_ns
    return data

def chartRollback(revision, chart, tiller_ns):
    command = "/usr/local/bin/helm --tiller-namespace " + tiller_ns + " rollback " + chart + " " + revision # helm2
    info(f"Running command: {command}")
    try:
        output = check_output(command.split(" "), stderr=STDOUT).decode("utf-8")
    except CalledProcessError as err:
        error(err.output.decode("utf-8"))
        raise err
    info(f"Output from command:\n{output}")
    return output

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
