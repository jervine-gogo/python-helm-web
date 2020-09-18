from flask_table import Table, Col, LinkCol, ButtonCol

class chartVersionTable(Table):
    revision = Col('Chart Revision')
    updated = Col('Updated')
    status = Col('Status')
    namespace = Col('Namespace')
    tiller_ns = Col('Tiiler Namespace')
    chart = Col('Chart Version')
    description = Col('Description')
    deploy = ButtonCol('Deploy', 'routes.deployChartRevision', url_kwargs=dict(revision='revision', chart='chartName', namespace='namespace', tiller_ns='tiller_ns'), button_attrs={"type" : "submit", "class" : "btn btn-danger"})
