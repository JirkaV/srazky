from flask import Flask, abort, make_response
from excel import vyrob_excel

app = Flask(__name__)

@app.route('/<int:ym>')
def get_excel(ym):
    y = int(ym / 100)
    m = ym % 100
    if not (2019 <= y < 2100  and 1 <= m <= 12):
        abort(404)
    response = make_response(vyrob_excel(str(ym)))
    response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response.headers['Content-Disposition'] = 'attachment; filename=Srazky-{}.xlsx'.format(ym)
    return response
