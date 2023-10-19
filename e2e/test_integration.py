import json
from time import sleep

from playwright.sync_api import expect


def test_sanity_check(page):
    """A simple sanity check to verify that the popup renders."""

    page.goto("http://localhost:3000")

    page.get_by_role("button", name="Load Journeys").click()

    # NOTE amcharts 5 uses the Canvas API (verson 4 used SVG) which means it's
    # difficult to write tests since you can't know the position of elements
    # you need to interact with (such as the nodes in this case).
    #
    # You also can't know when something has finished rendering, so I'm using
    # sleep.
    #
    # I'm selecting the root element since I know it has to be at the
    # top/center of the page.
    sleep(2)
    width = page.viewport_size["width"]
    page.locator("#chartdiv").click(position={"x": width / 2, "y": 5})

    json_text = json.dumps(
        {
            "id": "mr-op",
            "clone": None,
            "title": "Base operation",
            "invitable": False,
            "keyValues": {},
        },
        indent=2,
    )
    expect(page.get_by_text(json_text)).to_be_visible()
