import os 
import re
from pathlib import Path 

import pytest 
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

SHOT_DIR = Path("screenshot")
SHOT_DIR.mkdir(exist_ok=True)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield 
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

@pytest.fixture
def driver(request):
    opts = Options()
    if os.getenv("HEADLESS", "1") == "1":
        opts.add_argument("_headless")
    opts.add_argument("--width=1920")
    opts.add_argument("--height=1080")

    drv = webdriver.Firefox(options=opts, service=Service(log_output="gecko.log"))
    yield drv

    rep = getattr(request.node, "rep_call", None)
    if rep is not None and rep.failed:
        safe = re.sub(r"[^\w-]", "_", request.node.name)
        drv.save_screenshot(str(SHOT_DIR / f"{safe}.png"))

        drv.quit()


