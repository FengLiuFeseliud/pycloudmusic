from setuptools import setup, find_packages

"""
打包指令: python setup.py sdist
twine upload dist/*
"""

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pycloudmusic",
    version="0.1.0",
    description="使用 Python 快速异步的调用音乐 api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    url="https://github.com/FengLiuFeseliud/pycloudmusic",
    author="FengLiuFeseliud",
    author_email="17351198406@qq.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[
        "aiofiles",
        "aiohttp"
    ],
    python_requires='>=3.9'
)