# encoding=utf-8
from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.secret_key = "4pFwRNNXs+xQSOEaHrq4iSBwl+mq1UTdRuxqhM+RQpo="
Bootstrap(app)