import re
import json
from toolkit import re_search


def cur_to_requests(curl_cmd, filename):
    tmpl = """import requests


def main():
    url = "{}"
    headers = {}
    form = {}
    json = {}
    resp = requests.{}(url, headers=headers, json=json, data=form)
    print(resp.text)


main()
"""
    url = re.search(r"'(http.*?)'", curl_cmd).group(1)
    headers = json.dumps(
        dict(tuple(v.strip() for v in header.split(":", 1)) for header in re.findall(r"-H '(.*?)'", curl_cmd)), indent=10)
    form = re_search(r"--data '(.*?)'", curl_cmd, default=None)

    json_data = re_search(r"--data-binary '(.*?)'", curl_cmd, default=None)
    if form:
        form = json.dumps(dict(tuple(param.split("=", 1)) for param in form.replace("+", " ").split("&")), indent=10)
    if json_data:
        json_data = json.dumps(json.loads(json_data), indent=10)

    with open(filename, "w") as f:
        f.write(tmpl.format(
            url,
            headers,
            form,
            json_data,
            "post" if form or json_data else "get"))


cur_to_requests(
    """curl 'http://fanyi.qq.com/api/translate' -H 'Pragma: no-cache' -H 'Origin: http://fanyi.qq.com' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Cache-Control: no-cache' -H 'X-Requested-With: XMLHttpRequest' -H 'Cookie: pgv_info=ssid=s232042507; pgv_pvid=5761484344; pgv_pvi=8233938944; pgv_si=s4960854016; ptisp=cnc; ptui_loginuin=308299269; pt2gguin=o0308299269; uin=o0308299269; RK=IDRYxgn1Wm; ptcz=bdcf84ac23b72092b86457e42197309ef44bead58838c9f2f868bd9416b25228; o_cookie=308299269; pac_uid=1_308299269; skey=@jn3PLIjnK; fy_guid=9b87ef0c-ef17-4129-bcf0-6f56f5e63481; qtv=14076ec4350c20e9; qtk=zhw2FxxyHPbRBF2aIMKrtT9+Y0K/3k3U+xxTvTMGuuGlG8PVM4zwOkvlkChLIO7V+PnlW+bsvbL2SYMbnH2ee1urztQT9Oc2EYg+kbvwYV17o1vcuVHUoIjaQ1TAvoN5WMMp5oVZcl/wLTm5nc/FzA==; ts_last=fanyi.qq.com/; ts_uid=667983832; openCount=1' -H 'Connection: keep-alive' -H 'Referer: http://fanyi.qq.com/' --data 'source=auto&target=zh&sourceText=what+a+fuck+day+it+is!&sessionUuid=translate_uuid1522051994948' --compressed""",
    "test.py")