import fastapi

from routers import application_manager_router, user_router

app = fastapi.FastAPI(title='XYUnionAuthNeo API')
app.include_router(user_router)
app.include_router(application_manager_router)


@app.get('/ping', tags=['工具'])
def ping():
    return {
        'ping': 'pong'
    }
