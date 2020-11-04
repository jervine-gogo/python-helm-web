from flask import render_template, request, jsonify
from forms import deploySelectForm
from main import get_namespaces, get_charts, get_chartdata, get_tiller_namespaces, chartRollback
from . import routes
from tables import chartVersionTable
import json

@routes.route('/', methods=['GET', 'POST'])
def index():
    tiller_ns = get_tiller_namespaces()
    form = deploySelectForm()
    form.tiller_ns.choices = [(name['metadata']['namespace'], name['metadata']['namespace']) for name in tiller_ns['items']]
    return render_template('nameChartSelect.html', tiller_ns=tiller_ns, form=form)

@routes.route('/chartSelect', methods=['POST'])
def chartVersions():
    tiller_ns = request.form['tiller_ns']
    chart = request.form['chart']
    records = request.form['records']
    namespace = 'default'
    chartVersions = get_chartdata(tiller_ns, namespace, chart, records)
    table = chartVersionTable(chartVersions)
    table.border = True
    table.classes = ['table-striped', 'table-condensed', 'table-hover']
    return render_template('chartRevisionList.html', table=table)


@routes.route('/nsLookup/<tiller_ns>/<namespace>')
def namespaceLookup(tiller_ns, namespace):
    charts = get_charts(tiller_ns, namespace)
    return jsonify(charts)

@routes.route('/deployChartRevision/<revision>/<chart>/<tiller_ns>', methods=['POST'])
def deployChartRevision(revision, chart, tiller_ns):
    rollback = chartRollback(revision, chart, tiller_ns)
    return rollback