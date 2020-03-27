import sys, os, json
import urllib.request

def get_ip_area(ip): 
  try: 
    apiurl = "http://ip.taobao.com/service/getIpInfo.php?ip=%s" %ip 
    content = urllib.request.urlopen(apiurl).read() 
    data = json.loads(content)['data'] 
    code = json.loads(content)['code'] 
    if code == 0:  # success 
      print(data['country_id']) 
      print(data['area']) 
      print(data['city']) 
      print(data['region']) 
    else: 
      print(data) 
  except Exception as ex: 
    print(ex) 
if __name__ == '__main__': 
  ip = '123.125.114.144'
  #ip = 'www.baidu.com'  # invalid ip. 
  get_ip_area(ip)

