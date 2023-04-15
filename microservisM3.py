from aiohttp  import web
import aiofiles
import os


routes = web.RouteTableDef()

podaci = []

async def addFile(element, index, name):
  try:    
            if(index < 9):
                async with aiofiles.open(f'gatherData/0{index+1}-{name}.txt', 'w') as f:
                    await f.write(str(element))
            else:
                async with aiofiles.open(f'gatherData/{index+1}-{name}.txt', 'w') as f:
                    await f.write(str(element))
  except Exception as e:
        return e

@routes.post("/gatherData")
async def gatherData(request):
    try:
        data = await request.json()

        if(len(data) > 10):
            for index, el in enumerate(data):
                name = el.get("username")
                print(index, el)
            await addFile()

        return web.json_response({"status": "works"}, status=200)
    except Exception as e:
        return web.json_response({"status": "error", "message": e}, status=500)

app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port=5003)


