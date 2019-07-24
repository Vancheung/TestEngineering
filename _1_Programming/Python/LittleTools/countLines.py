'''统计某一路径下，指定后缀名的文件行数'''
# -- coding: utf-8 --
import os

filepath = 'D:\\NTETest' # 文件路径
filetype = '.py' # 文件后缀
savefile = 'count_jmx.txt'  # 结果保存文件

def file_name(file_dir,pattern):
    counts = {}
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == pattern:
                filename = os.path.join(root,file)
                print(filename)
                with open(filename, 'r', encoding='utf-8') as f:
                    counts[filename] = len(f.readlines())
    return counts

def sum(nums):
    result = 0
    for i in nums:
        if isinstance(i,int):
            result+=i
        if isinstance(i,str) and i.isdigit():
            result+=int(i)
    return result

if __name__ == '__main__':
    mapp = file_name(filepath,filetype)
    with open(savefile,'w+',encoding='utf-8') as f:
        f.write('filename\t\t\t count\n')
        for i in mapp:
            f.write('{} {}\n'.format(i,mapp[i]))
        f.write('total: {}'.format(sum(mapp.values())))
