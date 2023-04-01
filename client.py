from aiohttp import ClientSession
from asyncio import run
import requests

URL = f'http://127.0.0.1:8080/advert'


def add_advert(title: str, description: str, user_name: str):
    request = requests.post(f'{URL}/', json={'title': title, 'description': description, 'user_name': user_name})
    print(f'{request.status_code=}')
    print(f'{request.json()=}')


async def get_advert(advert_id: str):
    async with ClientSession() as session:
        request = await session.get(f'{URL}/{advert_id}/')
        print(await request.json())


async def patch_advert(advert_id: str, **json):
    async with ClientSession() as session:
        request = await session.patch(f'{URL}/{advert_id}/', **json)
        print(await request.json())


async def delete_advert(advert_id: str):
    async with ClientSession() as session:
        request = await session.delete(f'{URL}/{advert_id}/')
        print(await request.json())

# add_advert(title='title_1', description='description_1', user_name='user_1')
# add_advert(title='title_2', description='description_2', user_name='user_2')
# add_advert(title='title_3', description='description_3', user_name='user_3')
#
# run(get_advert(advert_id='1'))
# run(get_advert(advert_id='2'))
# run(get_advert(advert_id='3'))
#
# run(delete_advert(advert_id='2'))
# run(get_advert(advert_id='1'))
#
# run(patch_advert(advert_id='3', json={'name': 'new_name'}))
