from src.DataOperation.SlaveDb import SlaveDb
from src.slave import TOTAL_PERF, DBPATH
from flask import Flask, request, g
from flask_restful import Resource, Api

DEBUG_SETTING = True

app = Flask(__name__)
api = Api(app)


class Data(Resource):

    def get(self):
        d = SlaveDb(DBPATH)
        g.db = d.conn
        item = request.args.get('item')
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        msg = d.select(TOTAL_PERF, item=item, start_time=start_time,
                       end_time=end_time)
        return {'status': 'success', 'message': msg}


@app.teardown_request
def teardown_request(exception):
    g.db.close() if hasattr(g, 'db') else None


api.add_resource(Data, '/data')

if __name__ == '__main__':
    print('Server is running......')
    app.run(host='0.0.0.0', debug=DEBUG_SETTING)
