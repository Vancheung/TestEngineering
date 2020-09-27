# -*- coding: UTF-8 -*-

"""
-------------------------------------------------------------------------------
Describe: 数据可视化查询
Created At: 2020-09-03,  11:01
Author: 
-------------------------------------------------------------------------------
"""
from typing import List
from csv import DictWriter
from plotly import utils
from plotly.graph_objects import Scatter
from json import dumps as json_dumps
from common.db_utils import DatabaseApi
from common.indicators import Indicators
from src import logger


def draw(db: DatabaseApi, run_id, item):
    """
    对外提供绘制图片的接口
    :param run_id:
    :param db:
    :param item: Indicators.CPU, Indicators.MEM, Indicators.GPU, Indicators.IO_READ, Indicators.IO_WRITE
    :return: json格式数据
    """
    y = [i for i in db.select_column(run_id, item) if i is not None]
    x = [i for i in range(len(y))]
    if len(y) == 0:
        logger.error('No data')
        return {}
    trace1 = Scatter(x=x, y=y, mode='lines', name=item)
    trace2 = Scatter(x=x, y=[(sum(y) / len(y))] * len(y), mode='lines', name='平均值')
    trace3 = Scatter(x=x, y=[max(y)] * len(y), mode='lines', name='峰值')
    data = [trace1, trace2, trace3]
    return json_dumps(data, cls=utils.PlotlyJSONEncoder)


def record_avg(db_api: DatabaseApi, csv_path):
    """
    记录数据文件
    :param db_api:
    :param csv_path: 存储结果文件路径
    :return:
    """
    items = [Indicators.CPU, Indicators.MEM, Indicators.GPU, Indicators.FPS, Indicators.IO_READ, Indicators.IO_WRITE]
    tasks = sorted(db_api.select_column('task_id'))
    result = []
    for task_id in tasks:
        task_id_split = task_id.split('_')
        data = {
            '序号': task_id_split[1],
            '拆分场景': task_id_split[2],
            '运行时间': task_id_split[3],
            '运行批次': task_id_split[-1]
        }
        for item in items:
            y = [i for i in db_api.select_column(task_id, item) if i is not None]
            data[item] = round(sum(y) / len(y), 2) if len(y) else '-'
            data[item + '置信度(%)'] = round(len([i for i in y if i]) * 100 / len(y), 2) if len(y) else '-'
        result.append(data)
    write_csv(csv_path, result)


def write_csv(csv_name, lines: List[dict]):
    """
    写入到csv文件
    :param csv_name:
    :param lines:
    :return:
    """
    if not lines:
        return
    header = lines[0].keys()
    with open(csv_name, "w", newline='') as f:
        writer = DictWriter(f, fieldnames=header)
        writer.writeheader()
        for data in lines:
            writer.writerow(data)
