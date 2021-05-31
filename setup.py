from setuptools import setup

setup(
    name="vkpm",
    version="0.1",
    py_modules=["vkpm", "commit", "redis_core"],
    install_requires=[
        "Click",
    ],
    entry_points="""
        [console_scripts]
        vkpm=vkpm:cli
    """,
)
