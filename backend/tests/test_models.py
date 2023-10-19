import pytest

from models import Journey


def test_get_journeys_from_path(tmp_path):
    """Test reading a flat version of the journeys."""
    (tmp_path / "client-a-journey.yaml").write_text(
        """
title: Client A
invitable: true
keyValues:
    client: client-a
    joint: hip
"""
    )
    (tmp_path / "client-a-child-journey.yaml").write_text(
        """
clone: client-a
title: Client A child
invitable: true
keyValues:
    client: client-a-child
"""
    )

    journeys = Journey.get_journeys_from_path(tmp_path)

    assert journeys == {
        "client-a": Journey(
            id="client-a",
            clone=None,
            title="Client A",
            invitable=True,
            keyValues={
                "client": "client-a",
                "joint": "hip",
            },
        ),
        "client-a-child": Journey(
            id="client-a-child",
            clone="client-a",
            title="Client A child",
            invitable=True,
            keyValues={
                "client": "client-a-child",
            },
            clones=[],
        ),
    }


def test_get_journeys_from_path_with_duplicate_id(tmp_path, log):
    """
    If there's a journey with a duplicate id it should log the error and ignore
    the duplicate.
    """
    (tmp_path / "client-a-journey.yaml").write_text(
        """
title: Client A
invitable: true
keyValues:
    client: client-a
    joint: hip
"""
    )
    (tmp_path / "deep-path").mkdir()
    (tmp_path / "deep-path/client-a-journey.yaml").write_text(
        """
clone: client-a
title: Client A duplicate
invitable: true
keyValues: {}
"""
    )
    assert len(log.events) == 0

    journeys = Journey.get_journeys_from_path(tmp_path)

    assert journeys == {
        "client-a": Journey(
            id="client-a",
            clone=None,
            title="Client A",
            invitable=True,
            keyValues={
                "client": "client-a",
                "joint": "hip",
            },
        ),
    }

    assert log.events == [
        {"id": "client-a", "event": "Duplicate journey id.", "level": "error"}
    ]


def test_deep_merge_key_values():
    """Test deep merging of values in keyValues."""
    root = Journey(
        id="client-a",
        clone=None,
        title="Client A",
        invitable=True,
        keyValues={
            "a": "aaa",
            "b": {"c": "ccc"},
        },
        clones=[
            Journey(
                id="client-a-child",
                clone="client-a",
                title="Client A child",
                invitable=True,
                keyValues={
                    "b": {"c": "CCC"},
                    "d": "DDD",
                },
                clones=[],
            ),
        ],
    )

    Journey._deep_merge_key_values(root)

    assert root.clones[0].keyValues == {
        "a": "aaa",
        "b": {"c": "CCC"},
        "d": "DDD",
    }


def test_deep_merge_key_values_three_levels():
    """Test merging with three levels."""
    root = Journey(
        id="client-a",
        clone=None,
        title="Client A",
        invitable=True,
        keyValues={
            "a": 1,
            "b": 1,
        },
        clones=[
            Journey(
                id="client-a-child",
                clone="client-a",
                title="Client A child",
                invitable=True,
                keyValues={
                    "b": 2,
                    "c": 2,
                },
                clones=[
                    Journey(
                        id="client-a-child",
                        clone="client-a",
                        title="Client A child",
                        invitable=True,
                        keyValues={
                            "c": 3,
                            "d": 3,
                        },
                        clones=[],
                    ),
                ],
            ),
        ],
    )

    Journey._deep_merge_key_values(root)

    assert root.clones[0].keyValues == {
        "a": 1,
        "b": 2,
        "c": 2,
    }

    assert root.clones[0].clones[0].keyValues == {
        "a": 1,
        "b": 2,
        "c": 3,
        "d": 3,
    }


def test_errors_when_there_are_two_roots(tmp_path):
    """
    If there are >= 2 journeys that aren't clones, then there isn't a unique
    root to the tree and an exception should be raised.
    """
    (tmp_path / "client-a-journey.yaml").write_text(
        """
title: Client A
invitable: true
keyValues: {}
"""
    )
    (tmp_path / "client-b-journey.yaml").write_text(
        """
title: Client B
invitable: true
keyValues: {}
"""
    )

    with pytest.raises(ValueError) as e_info:
        Journey.load_tree_from_path(tmp_path)

    assert e_info.value.args[0] == "Wrong number of root journeys: 2."
