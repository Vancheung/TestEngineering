# 【Python标准库】【1】sys——系统相关的参数和函数

sys模块提供了一些变量和函数。这些变量可能被解释器使用，也可能由解释器提供。这些函数**会影响解释器**。本模块总是可用的。

### 常用函数和参数

#### 1、sys.argv

sys.argv是一个列表，包含了被传递给 Python 脚本的命令行参数 。

```python
import sys
if __name__ == '__main__':
    print(sys.argv)
    print(type(sys.argv))
```

通过命令行执行上面的程序，可以看到，执行时的参数会被添加到sys.argv这个列表中。

```python
$ python test2.py
['test2.py']
<class 'list'>

$ python test2.py -m
['test2.py', '-m']
<class 'list'>
```

因此，如果需要在执行时动态传入一些参数或文件，可以通过argv参数获取。

例如，一个将csv文件转换为json文件的脚本：

```python
from csv import DictReader
from json import dump
from sys import argv

if __name__ == '__main__':
    csv_file = argv[1]
    json_file = argv[2]
    with open(csv_file, 'r') as c, open(json_file, 'w') as j:
        reader = DictReader(c)
        datas = []
        for row in reader:
            datas.append(row)
        dump(datas, j)
```

通过命令行传参的方式运行：

```python
$ python csv2json.py environment.csv result.json
```

在PyCharm中Run-Edit Configuration可以配置命令行执行参数Parameters

![1570676911698](C:\Users\Z00423~1\AppData\Local\Temp\1570676911698.png)

配置完参数后可以直接通过PyCharm的Run和Debug运行和调试程序，不需要每次手动通过命令行执行。

#### 2、sys.path

> A list of strings that specifies the search path for modules. Initialized from the environment variable [`PYTHONPATH`](https://docs.python.org/zh-cn/3/using/cmdline.html#envvar-PYTHONPATH), plus an installation-dependent default. 

Python解释器使用sys.path的值来搜索模块，这个值由两部分组成：环境变量PYTHONPATH和安装解释器时默认的值。例如，在PyCharm中使用虚拟环境，print(sys.path)的结果如下：

```python
['D:\\exam',
'C:\\Users\\~\\AppData\\Local\\Programs\\Python\\Python37-32\\python37.zip', 'C:\\Users\\~\\AppData\\Local\\Programs\\Python\\Python37-32\\DLLs', 'C:\\Users\\~\\AppData\\Local\\Programs\\Python\\Python37-32\\lib', 'C:\\Users\\~\\AppData\\Local\\Programs\\Python\\Python37-32', 
'D:\\exam\\venv', 
'D:\\exam\\venv\\lib\\site-packages', 
'D:\\exam\\venv\\lib\\site-packages\\setuptools-40.8.0-py3.7.egg', 
'D:\\exam\\venv\\lib\\site-packages\\pip-19.0.3-py3.7.egg']
```

path[0]是python解释器运行的当前目录，如果解释器不可用（例如在交互式解释器中运行python或通过标准输入运行脚本），则path[0]为空字符串。

```python
>>> import sys
>>> sys.path
['', 'C:\\Users\\z00423280\\AppData\\Local\\Programs\\Python\\Python37-32\\Lib\\idlelib', 'C:\\Users\\z00423280\\AppData\\Local\\Programs\\Python\\Python37-32\\python37.zip', 'C:\\Users\\z00423280\\AppData\\Local\\Programs\\Python\\Python37-32\\DLLs', 'C:\\Users\\z00423280\\AppData\\Local\\Programs\\Python\\Python37-32\\lib', 'C:\\Users\\z00423280\\AppData\\Local\\Programs\\Python\\Python37-32', 'C:\\Users\\z00423280\\AppData\\Local\\Programs\\Python\\Python37-32\\lib\\site-packages', 'C:\\Users\\z00423280\\AppData\\Local\\Programs\\Python\\Python37-32\\lib\\site-packages\\pip-9.0.1-py3.7.egg']
```

有时，在运行中导入自己编写的python模块失败，是因为该模块所在的目录不在sys.path里。

例如，在使用locust进行压测的时候，编写locustfile.py，代码结构如下：

|-api/

|--AW.py

|-locustfile/

|--web_app.py

```python
# web_app.py
from api.AW import MyClass
class WebSiteTask(TaskSet):
	def on_start(self):
		self.client.me = MyClass()
```

直接运行locust web_app.py会报找不到模块，“ ModuleNotFoundError: No module named 'api' "

由于项目中目录结构固定，因此可以在web_app.py中使用sys.path.append()动态添加项目根目录到sys.path

```python
# web_app.py
from os import path as os_path
from sys import path as sys_path
sys_path.append(os_path.abspath(os_path.join(__file__,"../..")))

from api.AW import MyClass
# some code
```

#### 3、sys.stdin/stdout/stderr

sys.stdin/stdout/stderr是标准输入输出模块，可以被视为 file 对象

```python
in_stream = sys.stdin
f_stream = open('input.txt','r')
print(type(in_stream)==type(f_stream))
```

运行结果为true，即通过sys.stdin读入的文件与通过open()方法打开文件，返回的都是<class '_io.TextIOWrapper'>的实例。stdout和stderr的类型也相同。



标准输入输出模块的实际应用：

例如在做oj的时候，有一道题是通过标准输入读入json数据，格式如下：

```json
# in.json
{
	"string":"catsanddog",
	"word_list":["cat","cats","and","sand","dog"]
}
```

结果输出到标准输出，预期结果：

```json
{"result":["cat sand dog","cats and dog"]}
```

实现代码如下：

```python
import json
import sys


def myfunc(string, word_list):
    pass


if __name__ == '__main__':
    in_stream = sys.stdin
    j_str = json.load(in_stream)
    string = j_str.get('string')
    word_list = j_str.get('word_list')
    result = {
        'result': myfunc(string, word_list)
    }
    sys.stdout.write(json.dumps(result))
```

运行方式1，结果输出在标准屏幕上

```python
$ python test.py < in.json
{"result":["cat sand dog","cats and dog"]}
```

运行方式2，结果从控制台重定向到文件

```python
$ python test.py < in.json > result.json
```

如果在代码中，需要把print的部分输出到文件（例如错误日志打印），可以使用

```python
f_handler = open('out.log', 'w')
sys.stdout = f_handler
```

之后的print()调用的就是文件对象的write方法。
