# -*- coding: UTF-8 -*-

"""
-------------------------------------------------------------------------------
Describe: Use xcrun xctrace to record performance and analyse trace file
Usage: 
    python3 TraceDecoder.py --trace tracename --time 3600 --process processname --template MyTemplate.tracetemplate --udid device_udid
Author: Vancheung
-------------------------------------------------------------------------------
"""
import argparse
import logging
from subprocess import Popen, PIPE, STDOUT
import xml.etree.ElementTree as ET

logFormatter = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(format=logFormatter, level=logging.DEBUG)
logger = logging.getLogger(__name__)


def record(template: str, save_file: str, udid: str, time_limit: int):
    """
    use xcrun xctrace to record a trace file
    :param template: template file path
    :param save_file: trace file save path
    :param udid: device id
    :param time_limit: time (second)
    :return:
    """
    cmd = "xcrun xctrace record --template %s --all-processes --output '%s' --device %s --time-limit %ss" % (
        template, save_file, udid, time_limit)
    logger.info(cmd)
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
    for line in p.stdout.readlines():
        logger.info(line.decode('utf-8'))
    p.wait()
    p.stdout.close()


def decode(xpath: str, trace_file: str, xml_file):
    """
    use xcrun xctrace to decode file
    :param xpath: '/trace-toc/run[@number="1"]/data/table[@schema="core-animation-fps-estimate"]',
              '/trace-toc/run[@number="1"]/data/table[@schema="activity-monitor-process-live"]'
    :param trace_file: xxx.trace
    :param xml_file:  xxx.xml
    :return:
    """
    cmd = "xcrun xctrace export --input %s --output %s --xpath '%s'" % (trace_file, xml_file, xpath)
    logger.info(cmd)
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
    p.wait()
    p.stdout.close()


def analyse(xml_file: str, save_path: str, process=None):
    """
    analyse a xml_file to a txt
    :param xml_file:
    :param save_path:
    :param process:
    :return:
    """
    pattern = generate_id_pattern(xml_file)
    tree = ET.parse(xml_file)
    root = tree.getroot()
    logger.info('start analyse %s to %s', xml_file, save_path)
    with open(save_path, 'w') as f:
        for c in root[0]:
            if c.tag != 'row' or (process and process not in get_value(c[2], pattern)):
                continue
            result = []
            for i in c:
                result.append(get_value(i, pattern) if get_value(i, pattern) else 'None')
            f.writelines(','.join(result) + '\n')


def get_value(item, pattern: dict):
    """
    get value from a item
    if item has 'id', return its 'fmt'
    else, search 'ref' in pattern
    :param item:
    :param pattern:
    :return:
    """
    return item.attrib.get('fmt') if item.attrib.get('id') else pattern.get(item.attrib.get('ref'))


def generate_id_pattern(xml_file) -> dict:
    """
    rows in xml file usually like this:
         <row>
            <start-time id="1" fmt="00:58.703.117">58703117000</start-time>
            <duration id="2" fmt="1.01 s">1012006000</duration>
            <fps id="3" fmt="14 FPS">14.000000000</fps>
            <percent id="4" fmt="4.0%">4.000000000</percent>
        </row>
        <row>
            <start-time id="7" fmt="00:56.682.021">56682021000</start-time>
            <duration id="8" fmt="1.01 s">1010226000</duration>
            <fps ref="3"/>
            <percent ref="4"/>
        </row>
    so we need to record the relationship between ref and id
    :param xml_file:
    :return:
    """
    logger.info('generate_id_pattern in %s', xml_file)
    tree = ET.parse(xml_file)
    root = tree.getroot()
    result = {}
    for item in root[0]:
        if item.tag == 'row':
            for i in item:
                if i.attrib.get('id'):
                    result[i.attrib.get('id')] = i.attrib.get('fmt')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Trace Decoder')
    parser.add_argument('--trace', type=str, default='recording',help='trace file name (without .trace)')
    parser.add_argument('--time', type=int, default=0,help='trace time (second)')
    parser.add_argument('--process', type=str, default=None,help='process name')
    parser.add_argument('--template', type=str, default=None,help='template file path')
    parser.add_argument('--udid', type=str, default=None,help='device udid')
    args = parser.parse_args()
    record_name = args.trace
    record(args.template, record_name + '.trace', args.udid, args.time)
    decode('/trace-toc/run[@number="1"]/data/table[@schema="core-animation-fps-estimate"]', record_name + '.trace',
           record_name + '_fps.xml')
    decode('/trace-toc/run[@number="1"]/data/table[@schema="activity-monitor-process-live"]', record_name + '.trace',
           record_name + '_activity.xml')
    analyse(record_name + '_fps.xml', record_name + '_fps.txt')
    analyse(record_name + '_activity.xml', record_name + '_activity.txt', process=args.process)
