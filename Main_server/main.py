#coding=utf-8
import os
import sys
import xml.etree.ElementTree as ET
import web
import wechat_config.get_wechatserverIP as wechatip
import Main_server.about_handler as about_handler
import Main_server.finder_handler as finder


# 重定向
PATH = os.path.abspath(os.path.dirname(sys.argv[0]))
urls = (
    '/wx','wechat'
)
token_url = "https://api.weixin.qq.com/cgi-bin/token"
class wechat:
    ip_list = ['127.0.0.1']
    log_file = None
    @staticmethod
    def init():
        with open(PATH+r'\..\Static\request_log',"a") as wechat.log_file:
            wechat.ip_list.extend(wechatip.getip(token_url=token_url))

    def POST(self):
        if web.ctx.ip not in wechat.ip_list:
            return "Unathorized request :)"
        xml_pkg=web.data().decode()
        # print(type(xml_pkg))
        # print(xml_pkg)
        # XML
        msg_root = ET.fromstring(xml_pkg)
        # print(msg_root[5].text)

        # 排重？

        if "about" in msg_root[5].text: # msg_root[5] == Event_key
            return about_handler.handler(msg_root)
            # print("about")
        elif "finder" in msg_root[5].text:
            return finder.handler(msg_root)
        # KEY word 重定向？

if __name__ == "__main__":
    wechat.init()
    app = web.application(urls,globals())
    app.run()
