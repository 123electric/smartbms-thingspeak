from setuptools import find_packages, setup

setup(
    name="smartbms-thingspeak",
    version="0.1.0",
    description="123\\SmartBMS to Thingspeak",
    author="123electric",
    author_email="info@123electric.eu",
    url="https://123electric.eu",
    python_requires=">=3.6",
    packages=find_packages(exclude=["*.tests"]),
    install_requires=[
        'aiohttp>=3.7',
	'pyserial-asyncio>=0.5'
    ],
    setup_requires=[
    ],
    tests_require=[
    ],
    entry_points={
        "console_scripts": [
            "smartbms=smartbms.__main__:main",
        ],
    },
)