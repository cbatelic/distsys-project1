import aiohttp
import asyncio
from aiohttp  import web

routes = web.RouteTableDef()

@routes.get("/start")
async def getStart(request):
    try:
        resDict = {}    
        async with aiohttp.ClientSession() as session:
            task = asyncio.create_task(session.get("http://localhost:5000/m"))
            data = await asyncio.gather(task)
            data = [await x.json() for x in data]
            data = data[0]
            res = data.get("data")
            
            for row in res:
                resDict[res.index(row)] = row
            
            assert isinstance(resDict, dict)
            
            async with session.post("http://localhost:5002/pass", json = resDict) as res:
                result = await res.json()
        return web.json_response(result, status=200)
    except Exception as e:
        return web.json_response({"status":"error", "response":e}, status=500)


app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port=5001)

