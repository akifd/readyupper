from setuptools import setup

requires = [
    'alembic',
    'fastapi',
    'psycopg2',
    'sqlalchemy',
    'uvicorn',
]

dev_requires = [
    'pytest',
]

setup(
    name='readyupper',
    install_requires=requires,
    extras_require={
        'dev': dev_requires,
    },
)
