## 工具使用

### 远端Slave

#### windows

1. 将Slave_win文件夹复制到远端执行机
2. 按需修改文件夹中的config.ini
   - 记录进程性能功能未测试，当前仅支持记录整机性能数据
   - 默认运行时间为永久，可自定义
3. 双机运行client.exe，开始将本机性能数据记录到perf.db文件中
4. 如需从外部查询数据，启动salve_server.exe
   - 开放接口：GET /data
     - 例：http://IP:5000/data
   - 端口：5000
   - 开放参数（可选）
     - item
       - CPU
       - MEMORY
       - DISK
     - start_time
       - 时间戳
     - end_time
       - 时间戳
     - 例：/data?item=CPU&start_time=1571155171

#### Linux（未测试）

1. 需要支持python3.6及以上版本，以.py源码方式运行
2. 复制Slave_linux文件夹到执行机
   -cd src/slave
   - python client.py
   - python slave_server.py

### 本地Master

#### Windows

1. 在本地打开Master_win文件夹
2. 在config.ini中配置被观测节点的IP信息
3. 运行client.exe，开始拉取远端数据
   - client.exe保持运行时，每隔半小时拉取一次数据
   - client.exe重新运行，会读取当前Master.db中数据，从最新一条记录的时间开始拉取
4. 运行master_server.exe，可以从web查看数据
   - 查看服务器列表：http://master ip:5000
   - 查看具体节点：直接点击节点ip
   - 此处查看的是数据库中完整的信息，包含历史记录中运行过，但当前已不在config.ini中的节点

