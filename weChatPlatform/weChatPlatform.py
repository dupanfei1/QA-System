from flask import Flask, request, make_response
import hashlib
import time
import xml.etree.ElementTree as ET

app = Flask(__name__)

xml_rep = "<xml>\
    <ToUserName><![CDATA[{0}]]></ToUserName>\
    <FromUserName><![CDATA[{1}]]></FromUserName>\
    <CreateTime>{2}</CreateTime>\
    <MsgType><![CDATA[text]]></MsgType>\
    <Content><![CDATA[{3}]]></Content>\
    <FuncFlag>0</FuncFlag>\
    </xml>"


@app.route("/wx", methods=['GET', 'POST'])
def wechat():
    if request.method == "GET":
        try:
            data = request.args
            token = "dandyqi"
            signature = data.get('signature', '')
            timestamp = data.get('timestamp', '')
            nonce = data.get('nonce', '')
            echostr = data.get('echostr', '')
            s = [timestamp, nonce, token]
            s.sort()
            s = ''.join(s)
            if hashlib.sha1(s).hexdigest() == signature:
                return make_response(echostr)
        except Exception as e:
            return e
    else:
        rec = request.stream.read()
        xml_rec = ET.fromstring(rec)
        to_user = xml_rec.find('ToUserName').text
        from_user = xml_rec.find('FromUserName').text
        content = xml_rec.find('Content').text.encode('utf-8')
        reply = content
        res = xml_rep.format(from_user, to_user, int(time.time()), reply)
        print(res)
        response = make_response(res)
        return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
