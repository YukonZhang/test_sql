# -*- coding: utf-8 -*-
import sys
from boto3.session import Session
import boto3
import io
import requests
import re
import os


def to_s3(ccontent, file_name):
    """
    上传文章图片到s3
    :param url: 具体图片地址
    :return: down_url：s3中上传的图片的地址
    """
    aws_key = 'AKIAPLGCU6IYMAMPER5A'
    aws_secret = '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'
    session = Session(
        aws_access_key_id=aws_key,
        aws_secret_access_key=aws_secret,
        region_name='cn-north-1'
    )
    s3 = session.resource('s3')
    client = session.client('s3')
    # 判断是否存在对象
    # bucket = s3.Bucket('kf074fm01')
    # for obj in bucket.objects.all():
    #     print(obj.key)
    bucket = 'kf074fm01'  # 桶
    # 将文件上传到共享存储
    byte_stream = io.BytesIO(ccontent)
    objkey = 'pdf_file/' + file_name  # 上传路径 + 文件名
    try:
        file_obj = s3.Bucket(bucket).put_object(Key=objkey, Body=byte_stream)
        # print(file_obj)
        # print(file_obj.key)
        # print('上传成功！！！！！')
    except Exception as e:
        print(e)
    # 获取上传到s3的url
    down_url = client.generate_presigned_url(
        'get_object', Params={'Bucket': bucket, 'Key': objkey}, ExpiresIn=3600000
    )
    # print('down_url:%s' % down_url)
    return down_url


class UploatS3(object):
    def __init__(self):
        self.session = Session(
            aws_access_key_id='AKIAPLGCU6IYMAMPER5A',
            aws_secret_access_key='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',
            region_name='cn-north-1'
        )
        self.s3 = self.session.resource('s3')
        self.client = self.session.client('s3')
        self.bucket = 'kf074fm01'  # 桶

    def uploat(self, content, file_name, *args):
        byte_stream = io.BytesIO(content)
        path_ = '/'.join(args)
        objkey = 'medicine-policy/' + path_ + '/' + file_name  # 上传路径 + 文件名
        try:
            file_obj = self.s3.Bucket(self.bucket).put_object(Key=objkey, Body=byte_stream)
            # print(file_obj)
            # print(file_obj.key)
            # print('上传成功！！！！！')
            return self.get_filename(objkey)
        except Exception as e:
            # print("上传S3失败。。。。。。")
            return False

    def get_filename(self, objkey):
        # 获取上传到s3的url
        down_url = self.client.generate_presigned_url(
            'get_object', Params={'Bucket': self.bucket, 'Key': objkey}, ExpiresIn=3600000
        )
        # print('down_url:%s' % down_url)
        return down_url
