# -*- coding: UTF-8 -*-

"""
-------------------------------------------------------------------------------
Describe: 启用一个flask服务来展示数据
Created At: 2020-09-07,  15:36
Author:
-------------------------------------------------------------------------------
"""

from os import path as os_path
from flask import Flask, render_template, g

from common.db_utils import DatabaseApi
from common.indicators import Indicators
from perf.view_data import draw
from src import logger, BASEDIR

DEBUG_SETTING = True
app = Flask(__name__)


@app.route('/')
def index():
    db = DatabaseApi('sqlite', os_path.join(BASEDIR, 'perf.db'))
    g.db = db.db_api.conn
    servers = sorted(db.select_column('task_id'))
    logger.info(servers)
    return render_template('index.html', arr=servers)


@app.route('/<task_id>')
def task(task_id):
    items = [Indicators.CPU, Indicators.MEM, Indicators.GPU, Indicators.FPS, Indicators.IO_READ, Indicators.IO_WRITE]
    return render_template('task.html', arr=items, task_id=task_id)


@app.route('/<task_id>/<item>')
def data(task_id, item):
    db = DatabaseApi('sqlite', os_path.join(BASEDIR, 'perf.db'))
    bar = draw(db, task_id, item)
    return render_template('data.html', data=bar)


@app.teardown_request
def teardown_request(exception):
    g.db.close() if hasattr(g, 'db') else None


if __name__ == '__main__':
    logger.info('Server is running......')
    app.run(host='0.0.0.0', debug=DEBUG_SETTING)
