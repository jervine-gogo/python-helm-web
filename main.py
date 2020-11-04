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

app.register_blueprint(routes)

def get_namespaces():
    command = "/usr/local/bin/kubectl get ns -ojson"
    info(f"Running command: {command}")
    try:
        output = check_output(command.split(" "), stderr=STDOUT).decode("utf-8")
    except CalledProcessError as err:
        error(err.output.decode("utf-8"))
        raise err
    info(f"Output from command:\n{output}")
    data = json.loads(output)
    return data

def get_tiller_namespaces():
    command = "/usr/local/bin/kubectl get deploy --all-namespaces -l name=tiller -ojson"
    info(f"Running command: {command}")
    try:
        output = check_output(command.split(" "), stderr=STDOUT).decode("utf-8")
    except CalledProcessError as err:
        error(err.output.decode("utf-8"))
        raise err
    info(f"Output from command:\n{output}")
    data = json.loads(output)
    return data

def get_deployments(namespace):
    command = "/usr/local/bin/kubectl -n " + namespace + " get deploy -ojson"
    info(f"Running command: {command}")
    try:
        output = check_output(command.split(" "), stderr=STDOUT).decode("utf-8")
    except CalledProcessError as err:
        error(err.output.decode("utf-8"))
        raise err
    info(f"Output from command:\n{output}")
    data = json.loads(output)
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
        error(f"Output found")
        data = json.loads(output)
        return data
    else:
        error(f"Output not found")
        #data = '{"Next":"","Releases":[{"Name":"","Revision":2,"Updated":"","Status":"","Chart":"","AppVersion":"","Namespace":""},{"Name":"helm-web","Revision":1,"Updated":"Thu Oct  8 05:28:25 2020","Status":"DEPLOYED","Chart":"helm-web-0.1.0","AppVersion":"latest","Namespace":"infra-tools"},{"Name":"logstash-dev","Revision":1,"Updated":"Thu Oct  8 03:11:26 2020","Status":"DEPLOYED","Chart":"logstash-2.3.0","AppVersion":"7.1.1","Namespace":"monitoring"},{"Name":"nginx-dev","Revision":3,"Updated":"Thu Oct  8 05:24:16 2020","Status":"DEPLOYED","Chart":"ingress-nginx-2.0.0","AppVersion":"0.31.0","Namespace":"ingress"},{"Name":"oauth2-proxy","Revision":2,"Updated":"Wed Oct 21 03:49:52 2020","Status":"FAILED","Chart":"oauth2-proxy-3.2.2","AppVersion":"5.1.0","Namespace":"infra-tools"}]}'
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