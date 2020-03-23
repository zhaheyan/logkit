import tornado.ioloop
import tornado.web
#从终端模块中导出define模块用于读取参数，导出options模块用于设置默认参数
from tornado.options import define, options

import core


# 定义端口用于指定HTTP服务监听的端口
# 如果命令行中带有port同名参数则会称为全局tornado.options的属性，若没有则使用define定义。
define("port", type=int, default=8000, help="run on the given port")
define("filename", type=str, default="/home/jiuchou/share/ops-agent/test/access.log", help="get nginx log")


# 创建请求处理器
# 当处理请求时会进行实例化并调用HTTP请求对应的方法
class MainHandler(tornado.web.RequestHandler):
    # 定义get方法对HTTP的GET请求做出响应
    def get(self):
        # 从querystring查询字符串中获取id参数的值，若无则默认为0.
        # id = self.get_argument("id", 0)
        # write方法将字符串写入HTTP响应
        # self.write("hello world id = " + id)
        # self.write("hello world")
        try:
            logs = core.get_logs(options.filename)
            self.set_status(200)
            print('get logs success')
            result = {
                "message": '日志信息获取成功',
                'status_code': 200,
                'logs': logs
            }
            self.write(result)
        except Exception as e:
            print(e)
            self.set_status(500)
            result = {
                "message": '日志信息获取失败: internal server error',
                'status_code': 500
            }
            self.write(result)
            #self.write(e)
            # self.send_error(500)


# 创建路由表
urls = [(r"/agent/get_logs", MainHandler),]


def main():
    # 解析命令行参数
    tornado.options.parse_command_line()
    app = tornado.web.Application(urls)
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()

