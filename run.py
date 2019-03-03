#!/usr/bin/env python

from irastretto.config import read_irastretto_config
from irastretto.web.app import app

config = read_irastretto_config()
app.config.update(config)
print(app.config)
app.run()
