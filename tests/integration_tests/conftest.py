import asyncio

import os
import subprocess

from pytest import fixture

from gideon import connection_pool
from tests.factories import CategoryFactory


@fixture(scope='session')
def create_db():
    print('creating database...')
    # the password is in .pgpass file
    subprocess.call(['psql', '-U', os.environ['GIDEON_USER'], '-h', os.environ['GIDEON_HOST'], '-f',
                    f'{os.path.dirname(__file__)}/db.sql'])


@fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@fixture
async def connection():
    con = await connection_pool.acquire()
    yield con
    await connection_pool.release(con)


@fixture
async def db_transaction(connection):
    # TODO: refactor this for a better solution
    yield
    await connection.execute('TRUNCATE categories, movements_tags, tags, movements;')


@fixture
async def category():
    cat = CategoryFactory.build()
    await cat.save()
    return cat
