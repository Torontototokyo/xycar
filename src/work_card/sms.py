from dotenv import load_dotenv

# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import os
import sys
import json

from typing import List

from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_credentials.client import Client as CredentialClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient


def get_resource_path(relative_path):
    """获取打包后资源的绝对路径"""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # 程序被打包运行时，资源在 sys._MEIPASS 目录下
        base_path = sys._MEIPASS
    else:
        # 开发环境下，资源就在脚本的当前目录
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# 获取打包在内部的 .env 文件的路径
dotenv_path = get_resource_path('.env')

# 明确告诉 load_dotenv 从这个路径加载
load_dotenv(dotenv_path=dotenv_path)

ACCESS_KEY_ID:str = os.getenv("ACCESS_KEY_ID")
ACCESS_KEY_SECRET:str = os.getenv("ACCESS_KEY_SECRET")
TEMPLATE_CODE:str = os.getenv("TEMPLATE_CODE")
SIGN_NAME:str =os.getenv("SIGN_NAME")
class Sample:
    def __init__(self):
        pass

    @staticmethod
    def create_client() -> Dysmsapi20170525Client:
        """
        使用凭据初始化账号 Client
        @return: Client
        @throws Exception
        """
        # 工程代码建议使用更安全的无 AK 方式，凭据配置方式请参见：https://help.aliyun.com/document_detail/378659.html。
        credential = CredentialClient()
        config = open_api_models.Config(
            credential=credential,
            access_key_id=ACCESS_KEY_ID,
            access_key_secret=ACCESS_KEY_SECRET,
        )
        # Endpoint 请参考 https://api.aliyun.com/product/Dysmsapi
        config.endpoint = f'dysmsapi.aliyuncs.com'
        return Dysmsapi20170525Client(config)

    @staticmethod
    def main(
        args: List[str],
    ) -> None:
        client = Sample.create_client()
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            phone_numbers='13420789366',
            sign_name=SIGN_NAME,
            template_code=TEMPLATE_CODE,
            template_param=json.dumps({
                'car_no':"粤EK0943",
                'hour':"123"
            })
        )
        try:
            resp = client.send_sms_with_options(send_sms_request, util_models.RuntimeOptions())
            print(json.dumps(resp, default=str, indent=2))
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))

    @staticmethod
    def sms(
        car_no: str,
        hour,
        phone_numer
    ) -> None:
        client = Sample.create_client()
        
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            phone_numbers=phone_numer,
            sign_name=SIGN_NAME,
            template_code=TEMPLATE_CODE,
            template_param=json.dumps({
                'car_no':car_no,
                'hour':hour
            })
        )
        try:
            resp = client.send_sms_with_options(send_sms_request, util_models.RuntimeOptions())
            print(json.dumps(resp, default=str, indent=2))
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))

    @staticmethod
    async def main_async(
        args: List[str],
    ) -> None:
        client = Sample.create_client()
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            phone_numbers='your_value',
            sign_name='your_value'
        )
        try:
            resp = await client.send_sms_with_options_async(send_sms_request, util_models.RuntimeOptions())
            print(json.dumps(resp, default=str, indent=2))
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))


if __name__ == '__main__':
    # Sample.main(sys.argv[1:])
    Sample.sms(phone_numer='13420789366',car_no='粤KE2030',hour='123')

