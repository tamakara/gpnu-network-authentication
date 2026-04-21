import logging
import re
import urllib.parse

import requests

logger = logging.getLogger(__name__)


def check_network(timeout=10):
    test_url = "http://www.msftconnecttest.com/connecttest.txt"
    logger.debug("开始检测网络连通性，url=%s，timeout=%s", test_url, timeout)
    try:
        response = requests.get(
            test_url,
            timeout=timeout,
        )
    except requests.RequestException:
        logger.exception("网络检测请求异常，视为未连通")
        return False

    is_connected = response.status_code == 200 and response.text == "Microsoft Connect Test"
    logger.debug(
        "网络检测完成，status_code=%s，body_len=%d，connected=%s",
        response.status_code,
        len(response.text),
        is_connected,
    )
    return is_connected


def extract_query_string(text):
    logger.debug("开始提取 queryString，输入文本长度=%d", len(text))
    match = re.search(r"top\.self\.location\.href='[^'?]+\?([^']*)'", text)
    if match:
        query = match.group(1)
        logger.debug("提取 queryString 成功，长度=%d", len(query))
        return query

    logger.warning("提取 queryString 失败，未匹配到目标模式")
    return None


def get_redirect_query_string(timeout=10):
    redirect_url = "http://www.msftconnecttest.com/redirect"
    logger.debug("开始获取重定向页面，url=%s，timeout=%s", redirect_url, timeout)
    try:
        response = requests.get(
            redirect_url,
            timeout=timeout,
            allow_redirects=True,
        )
    except requests.RequestException:
        logger.exception("获取重定向页面异常")
        return None

    logger.debug(
        "重定向请求完成，最终url=%s，status_code=%s，body_len=%d",
        response.url,
        response.status_code,
        len(response.text),
    )
    query_string = extract_query_string(response.text)
    if query_string:
        logger.debug("从重定向页面获取 queryString 成功")
    else:
        logger.warning("从重定向页面未获取到 queryString")
    return query_string


def create_request_data(student_id, password, query_string):
    logger.debug(
        "开始构造登录参数，student_id=%s，raw_query_len=%d",
        student_id,
        len(query_string),
    )
    payload = {
        "userId": student_id,
        "password": password,
        "service": "",
        "queryString": urllib.parse.quote(query_string, safe=""),
        "operatorPwd": "",
        "operatorUserId": "",
        "validcode": "",
        "passwordEncrypt": "false",
    }
    logger.debug("登录参数构造完成，encoded_query_len=%d", len(payload["queryString"]))
    return payload
