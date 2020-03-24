# -*- encoding: utf-8 -*-
import re
import time
from datetime import datetime

# line = '182.254.52.17 - - [23/Mar/2020:22:33:25 +0800] "GET http://www.raozp.com/s.php HTTP/1.1" 404 146 "-" "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0"'

def extract(line):
    pattern = '''(?P<remote_addr>[\d\.]{7,}) - - (?:\[(?P<request_time>[^\[\]]+)\]) "(?P<request>[^"]+)" (?P<status>\d+) (?P<size>\d+) "(?:[^"]+)" "(?P<user_agent>[^"]+)"'''
    regex = re.compile(pattern)
    matcher = regex.match(line)
    return matcher.groupdict()


def get_log(line):
    log = {}

    #日志格式key与对应的处理函数,进一步对日志格式化处理 'request': 'GET /o2o/media.html?menu=3 HTTP/1.1'
    #对request分别切割成请求方式(method)，请求地址(url)，协议版本(protocol)
    log_format_func = {
        'request': lambda request: dict(zip(('method', 'url', 'protocol'), request.split())),
        'size': int,
        'status': int,
        'request_time': lambda timestr: time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.mktime(time.strptime(timestr, "%d/%b/%Y:%H:%M:%S %z"))))
    }

    #写入新字典，key,value
    for k,v in extract(line).items():
        # print(k, v)
        log[k] = log_format_func.get(k, lambda x:x)(v)
    return log

def get_logs(filename):
    logs = []
    with open(filename, 'r') as f:
        lines = f.readlines()

    for line in lines:
        log = get_log(line)
        logs.append(log)
    return logs

if __name__ == '__main__':
    print(get_logs('access.log'))

