# GPNU Network Login Script

用于广东药科大学（GPNU）校园网的自动登录脚本。  
脚本会先检测当前网络是否可用；如果未联网，再自动获取重定向参数并调用 `eportal` 登录接口。

## 功能

- 检测是否已联网（通过 `msftconnecttest`）。
- 自动获取并解析校园网重定向页面中的 `queryString`。
- 构造登录请求并提交到 `eportal`。
- 已联网时不重复登录。

## 项目结构

- `main.py`：主入口，串联检测、参数准备、登录流程。
- `utils.py`：工具函数（网络检测、重定向参数提取、请求体构造）。
- `eportal.py`：`eportal` 登录接口封装。

## 环境要求

- Python 3.8+
- 依赖：`requests`、`python-dotenv`

安装依赖：

```bash
pip install requests python-dotenv
```

## 快速开始

1. 设置环境变量：

```powershell
$env:STUDENT_ID="你的学号"
$env:PASSWORD="你的校园网密码"
$env:DEFAULT_URL="你的备用重定向URL"
```

或在项目根目录创建 `.env`（已在 `.gitignore` 中忽略）。
脚本启动时会自动加载该文件。

2. 运行脚本：

```bash
python main.py
```

脚本会输出登录接口返回内容，可用于判断登录是否成功。

## 执行流程

`main.py` 的核心逻辑如下：

1. 调用 `check_network()` 检查是否已联网。
2. 若已联网，直接退出。
3. 若未联网，优先通过 `get_redirect_query_string()` 获取 `queryString`。
4. 若获取失败，从 `default_url` 中回退提取 `queryString`。
5. 调用 `create_request_data()` 生成登录表单。
6. 调用 `login()` 发送请求并打印返回结果。

## 常见问题

1. `ModuleNotFoundError: requests`
   - 执行 `pip install requests python-dotenv` 安装依赖。
2. 登录失败或返回异常
   - 检查学号、密码是否正确。
   - 检查 `default_url` 是否过期，必要时更新为当前网络环境值。
3. 请求超时
   - 可能当前网络对 `msftconnecttest` 连通性有限制，可稍后重试。

## 安全建议

- 请勿将账号密码写入代码仓库。
- 当前版本使用环境变量读取 `STUDENT_ID`、`PASSWORD`、`DEFAULT_URL`，并已忽略 `.env` 文件。

## 可选：开机自动登录（Windows）

可将 `python main.py` 配置到任务计划程序，在开机或登录时自动执行。  
建议先手动运行稳定后再启用自动化。
