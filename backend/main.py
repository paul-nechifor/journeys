from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import Journey, JourneyResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

YAML_DIR = Path(__file__).parent / "yamls"


# NOTE, `get-journeys` is not an ideal path since it sounds like a command
# rather than a resource. Just `/journeys` would be better.
@app.get("/get-journeys")
async def get_journeys() -> JourneyResponse:
    # If the files don't get changed, this should be cached.
    return {"data": Journey.load_tree_from_path(YAML_DIR)}
