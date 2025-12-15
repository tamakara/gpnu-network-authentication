import re
import time
import urllib.parse
import requests


def main():
    # 学号
    STUDENT_ID = "你的学号"
    # 密码
    PASSWORD = "你的校园网密码"
    # 间隔时长
    WAITING_SECONDS = 10
    # 204测试地址
    GENERATE_204_URL = "http://connect.rom.miui.com/generate_204"

    while True:
        network_login(STUDENT_ID, PASSWORD, GENERATE_204_URL)
        time.sleep(WAITING_SECONDS)


def extract_query_string(html_content):
    match = re.search(
        r"top\.self\.location\.href='https://ruijieportal\.gpnu\.edu\.cn:8443/eportal/index\.jsp\?([^']+)'",
        html_content
    )
    return match.group(1) if match else None


def create_request_headers(query_string):
    return {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",
        "Referer": f"http://10.0.6.247/eportal/index.jsp?{query_string}",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }


def create_request_data(student_id, password, query_string):
    return {
        "userId": student_id,
        "password": password,
        "service": "",
        "queryString": urllib.parse.quote(query_string, safe=''),
        "operatorPwd": "",
        "operatorUserId": "",
        "validcode": "",
        "passwordEncrypt": "false"
    }


def network_login(student_id, password, generate_204_url):
    try:
        print("测试网络连接...")
        response = requests.get(generate_204_url, timeout=5, allow_redirects=True)

        if response.status_code == 204:
            print("网络已连接。")
            return True

        print("连接失败，尝试认证...")

        query_string = extract_query_string(response.text)
        if not query_string:
            print("获取认证参数失败。")
            return False

        headers = create_request_headers(query_string)
        post_data = create_request_data(student_id, password, query_string)
        login_response = requests.post(
            "http://10.0.6.247/eportal/InterFace.do?method=login",
            headers=headers,
            data=post_data,
            timeout=10
        )

        if '"result":"success"' in login_response.text:
            print("登录成功。")
        else:
            print("登录失败。错误信息：")
            error_match = re.search(r'"message":"([^"]*)"', login_response.text)
            print(error_match.group(1).encode('latin-1').decode('utf-8'))

    except requests.exceptions.RequestException as e:
        print(f"网络请求错误：{str(e)}")


if __name__ == "__main__":
    main()
