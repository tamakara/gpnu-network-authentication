import os
import logging
from eportal import login
from time import sleep
from dotenv import load_dotenv
from utils import *

logger = logging.getLogger(__name__)


def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )


def load_config_from_env():
    student_id = os.getenv("STUDENT_ID")
    password = os.getenv("PASSWORD")
    default_url = os.getenv("DEFAULT_URL")

    missing_vars = [
        name
        for name, value in [
            ("STUDENT_ID", student_id),
            ("PASSWORD", password),
            ("DEFAULT_URL", default_url),
        ]
        if not value
    ]
    if missing_vars:
        raise ValueError(
            "缺少环境变量: {}。请先设置后再运行。".format(", ".join(missing_vars))
        )

    return student_id, password, default_url


def main():
    setup_logging()
    load_dotenv()
    logger.info("自动登录脚本启动")
    try:
        student_id, password, default_url = load_config_from_env()
    except ValueError as error:
        logger.error(str(error))
        return

    loop_count = 0
    while True:
        loop_count += 1
        logger.debug("开始第 %d 次网络状态检查", loop_count)

        if check_network():
            logger.info("网络已连通，5 秒后重试检测")
            continue

        logger.warning("检测到网络未连通，开始执行登录流程")
        query_string = (
            extract_query_string(f"top.self.location.href='{default_url}'")
            or get_redirect_query_string()
        )

        if not query_string:
            logger.error("未获取到 queryString，3 秒后重试")
            sleep(3)
            continue

        logger.debug("queryString 获取成功，长度=%d", len(query_string))
        payload = create_request_data(student_id, password, query_string)
        logger.debug(
            "登录请求参数已构建，userId=%s，queryString编码后长度=%d",
            student_id,
            len(payload["queryString"]),
        )

        try:
            login_response = login(payload)
            logger.info("登录请求完成，HTTP状态码=%s", login_response.status_code)
            logger.debug("登录响应内容: %s", login_response.text.strip())
            print(login_response.text)
        except Exception:
            logger.exception("登录请求发生异常，3 秒后重试")
            sleep(3)

        sleep(1)


if __name__ == "__main__":
    main()
