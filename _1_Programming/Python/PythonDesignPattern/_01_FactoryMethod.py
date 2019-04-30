# xml 和 json 文件处理
from xml.etree import ElementTree as etree
import json

class JSONConnector():
    def __init__(self,filepath):
        self.data = dict()
        with open(filepath,mode='r',encoding='utf-8') as f:
            self.data = json.load(f)

    @property
    def parsed_data(self):
        return self.data


class XMLConnector():
    def __init__(self,filepath):
        self.tree = etree.parse(filepath)

    @property
    def parsed_data(self):
        return self.tree

# 工厂方法
def connection_factory(filepath):
    if filepath.endswith('json'):
        connector = JSONConnector
    elif filepath.endswith('xml'):
        connector = XMLConnector
    else:
        raise ValueError('Cannot connect to {} '.format(filepath)+'\nWrong type of file')
    return connector(filepath)

# 处理文件的异常
def connect_to(filepath):
    factory = None
    try:
        factory = connection_factory(filepath)
    except ValueError as ve:
        print(ve)
    return factory

def client():
    # sqlite_factory = connect_to('requirements.txt') # 异常分支测试

    xml_factory = connect_to('person.xml')
    xml_data = xml_factory.parsed_data
    liars = xml_data.findall(".//{}[{}='{}']".format('person','lastName','Liar'))
    print('found: {} persons'.format(len(liars)))
    for liar in liars:
        print('first name: {}'.format(liar.find('firstName').text))
        print('last name: {}'.format(liar.find('lastName').text))
        [print('phone number ({}):'.format(p.attrib['type']), p.text) for p in liar.find('phoneNumbers')]
    print()

    json_factory = connect_to('donut.json')
    json_data = json_factory.parsed_data
    print('found: {} donuts'.format(len(json_data)))
    for donut in json_data:
        print('name: {}'.format(donut['name']))
    print('price: ${}'.format(donut['ppu']))
    [print('topping: {} {}'.format(t['id'], t['type'])) for t
     in donut['topping']]

if __name__ == '__main__':
    # with open('person.xml',mode='r',encoding='utf-8') as f:
    #     print(f)
    client()
