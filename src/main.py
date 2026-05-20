import logging
import uvicorn
logging.getLogger("pymongo").setLevel(logging.WARNING)
logging.getLogger("pymongo.topology").setLevel(logging.WARNING)
if __name__ == "__main__":
    uvicorn.run("infrastructure.api:app", host="localhost", port=8000, reload=True)