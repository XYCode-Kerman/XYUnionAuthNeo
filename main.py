import fastapi

app = fastapi.FastAPI(title='XYUnionAuthNeo API')


@app.get('/ping', tags=['工具'])
def ping():
    return {
        'ping': 'pong'
    }
