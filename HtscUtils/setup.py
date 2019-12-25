# -*- coding: utf-8 -*-

from setuptools import setup
from os.path import join, dirname
from setuptools import find_packages


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename, encoding='utf-8'))
    return [line for line in lineiter if line and not line.startswith("#")]


with open(join(dirname(__file__), './VERSION.txt'), 'rb') as f:
    version = f.read().decode('ascii').strip()

setup(
    name='HtscUtils',  # 模块名称
    version=version,  # 版本号
    description='Spider Utiles for Scrapy',  # 描述
    packages=find_packages(exclude=[]),
    author='st',
    author_email='K1131219@test.htsc.com.cn',
    license='',
    package_data={'': ['*.*']},
    url='#',
    install_requires=parse_requirements("requirements.txt"),  # 所需的运行依赖环境（包）
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
