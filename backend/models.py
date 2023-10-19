from pathlib import Path
from typing import Any

import structlog
from pydantic import BaseModel, Json
from pydash.objects import merge
from ruamel.yaml import YAML

logger = structlog.get_logger()


class Journey(BaseModel):
    id: str
    clone: str | None = None
    title: str
    invitable: bool
    keyValues: dict[str, Any]
    clones: list["Journey"] = []

    @classmethod
    def load_tree_from_path(cls, dir: Path) -> "Journey":
        """
        Returns the root journey of the tree of journeys found in the path.
        """
        journeys = cls.get_journeys_from_path(dir)

        for journey in journeys.values():
            if journey.clone is not None:
                journeys[journey.clone].clones.append(journey)

        roots = [j for j in journeys.values() if j.clone is None]
        if len(roots) != 1:
            raise ValueError(f"Wrong number of root journeys: {len(roots)}.")

        cls._deep_merge_key_values(roots[0])

        return roots[0]

    @staticmethod
    def get_journeys_from_path(dir: Path) -> dict[str, "Journey"]:
        """Returns a flat dictionary of the journeys found in the dir."""
        journeys = {}
        yaml = YAML()

        for yaml_file in dir.glob("**/*.yaml"):
            data = yaml.load(yaml_file)
            data["id"] = yaml_file.stem.replace("-journey", "")
            if data["id"] in journeys:
                logger.error("Duplicate journey id.", id=data["id"])
                continue
            journeys[data["id"]] = Journey(**data)

        return journeys

    @staticmethod
    def _deep_merge_key_values(root: "Journey") -> None:
        """
        Deep merge the key values by getting the values from the parent and
        overwriting with the values of the child.
        """
        queue = [root]

        # Breadth-first traversal.
        while queue:
            journey = queue.pop(0)
            for clone in journey.clones:
                queue.append(clone)
                clone.keyValues = merge({}, journey.keyValues, clone.keyValues)


class JourneyResponse(BaseModel):
    data: Journey
