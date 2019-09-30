服务器性能监控平台demo
1、slave
在被监测的服务器上运行client.py, 性能监测数据存放在Perf.db中
在被监测的服务器上运行slave_server.py，可以通过rest接口查询性能数据，开放端口为5000，host为本机ip
具体接口为：
GET /data
实例：
http://ip:5000/data?item=CPU
