from fastapi import FastAPI , Query , Depends
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="The Evil Searcher API ")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/search")
async def search(query: str = Query(...,min_length=1)):
    print("OK")
    return {"query": query}