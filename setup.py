from setuptools import setup, find_packages

"""
打包指令: python3 setup.py sdist
python3 -m twine upload dist/*
"""

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pycloudmusic",
    version="0.1.4.5",
    description="优雅的异步高性能 Python 音乐 API 库 (网易云音乐)",
    keywords=[
        "cloudmusic",
        "asyncio",
        "netease-cloud-music",
        "netease",
        "api"
    ],
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