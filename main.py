import fastapi

from routers import user_router

app = fastapi.FastAPI(title='XYUnionAuthNeo API')
app.include_router(user_router)


@app.get('/ping', tags=['工具'])
def ping():
    return {
        'ping': 'pong'
    }
