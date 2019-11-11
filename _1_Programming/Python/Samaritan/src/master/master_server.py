from flask import Flask, render_template, g

from src.DataOperation.MasterDb import MasterDb
from src.master import DBPATH, get_ip_from_tbl_name

DEBUG_SETTING = False
app = Flask(__name__)


@app.route('/')
def index():
    d = MasterDb(DBPATH)
    g.db = d.conn
    servers = d.get_table_names()
    servers = set([get_ip_from_tbl_name(i) for i in servers])
    return render_template('index.html', arr=servers)


@app.route('/slave/<slave_ip>')
def proc_data(slave_ip):
    d = MasterDb(DBPATH)
    pids = d.get_pids_and_name(slave_ip)
    return render_template('slave.html', slave_ip=slave_ip, arr=pids)


@app.route('/slave/<slave_ip>/total')
def total_data(slave_ip):
    d = MasterDb(DBPATH)
    bar = d.draw(slave_ip)
    return render_template('data.html', plot=bar)


@app.route('/pid/<slave_ip>/<pid>')
def data(slave_ip, pid):
    d = MasterDb(DBPATH)
    bar = d.draw(slave_ip, pid)
    return render_template('data.html', plot=bar)


@app.teardown_request
def teardown_request(exception):
    g.db.close() if hasattr(g, 'db') else None


if __name__ == '__main__':
    print('Server is running......')
    app.run(host='0.0.0.0', debug=DEBUG_SETTING)
