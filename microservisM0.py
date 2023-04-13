import aiohttp
import asyncio
import aiosqlite
import aiofiles
import json
from aiohttp  import web

routes = web.RouteTableDef()

@routes.get("/m")
async def getM(req):
    try:
        response = {
            "data": [],
        }

        async with aiosqlite.connect("database.db") as db:
            async with db.execute("SELECT * FROM podaci LIMIT 100") as cur:
                async for row in cur:
                    data = {'username': row[0], 'ghlink': row[1], 'filename': row[2], 'content': row[3]}
                    response["data"].append(data)
            await db.commit()

        return web.json_response(response)
    except Exception as e:
        return web.json_response({"M0": "error", "response": str(e)}, status=500)

async def checkBase():
    async with aiosqlite.connect("database.db") as db:  # provjera
        async with db.execute("SELECT COUNT(*) FROM podaci") as cur:
            count = await cur.fetchone()
            if count[0] == 0:
                print("U bazi nema elemenata")
                await fillBase()

async def fillBase():
    async with aiofiles.open("fakeData.json", mode="r") as file:
        x = 0
        async for row in file: #popunjavanje
            data = json.loads(row)
            repo_name = data["repo_name"]
            username, _ = repo_name.split("/")
            ghlink = f"https://github.com/{repo_name}"
            path = data["path"]
            filename = path.split("/")[-1]
            content = data["content"]
            async with aiosqlite.connect("database.db") as db:
                await db.execute(
                    "INSERT INTO podaci (username,ghlink,filename,content) VALUES (?,?,?,?)",
                    (username, ghlink, filename, content)
                )
                await db.commit()
            x += 1
            if x == 10000:
                return

app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port=5000)


