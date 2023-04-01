from aiohttp import web
from models import Base, Session, engine, Advert
import json

app = web.Application()


async def app_context(app):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


@web.middleware
async def session_middleware(request, handler):
    async with Session() as session:
        request['session'] = session
        response = await handler(request)
        return response


app.cleanup_ctx.append(app_context)
app.middlewares.append(session_middleware)


async def get_advert(advert_id, session):
    advert = await session.get(Advert, advert_id)
    if not advert:
        raise web.HTTPNotFound(text=json.dumps({'status': 'error', 'message': f'here is no advert with id {advert_id}'}),
                               content_type='application/json')
    return advert


async def add_advert(session, **dict_):
    advert = Advert(**dict_)
    session.add(advert)
    await session.commit()
    return advert


async def patch_advert(advert, session, **dict_):
    for key, value in dict_.items():
        setattr(advert, key, value)
    session.add(advert)
    await session.commit()


async def delete_advert(advert, session):
    await session.delete(advert)
    await session.commit()


class AdvertView(web.View):

    async def get(self):
        advert = await get_advert(int(self.request.match_info['advert_id']), self.request['session'])
        return web.json_response({'id': advert.id,
                                  'title': advert.title,
                                  'description': advert.description,
                                  'creation_time': int(advert.creation_time.timestamp()),
                                  'user_name': advert.user_name})

    async def post(self):
        json_data = await self.request.json()
        new_advert = await add_advert(self.request['session'], **json_data)
        return web.json_response({'new advert id': new_advert.id})

    async def patch(self):
        advert = await get_advert(int(self.request.match_info['advert_id']), self.request['session'])
        json_data = await self.request.json()
        await patch_advert(advert, self.request['session'], **json_data)
        return web.json_response({'status': 'patched'})

    async def delete(self):
        advert = await get_advert(int(self.request.match_info['advert_id']), self.request['session'])
        await delete_advert(advert, self.request['session'])
        return web.json_response({'status': 'deleted'})


app.add_routes([web.get('/advert/{advert_id:\d+}/', AdvertView),
                web.post('/advert/', AdvertView),
                web.patch('/advert/{advert_id:\d+}/', AdvertView),
                web.delete('/advert/{advert_id:\d+}/', AdvertView)])

if __name__ == '__main__':
    web.run_app(app)
