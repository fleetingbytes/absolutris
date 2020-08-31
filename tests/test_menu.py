#!/usr/bin/env python

import collections
import logging
from absolutris import menu


# Setup logger, because we will test logger output
logger = logging.getLogger(__name__)


def test_text_menu(caplog) -> None:
    tm = menu.Text_Menu()
    options = collections.OrderedDict((
        ("T", "Test option"),
        ("Q", "Quit"),
        ))
    with caplog.at_level(logging.INFO):
        menu_text = tm.show(options)
    for key, value in options.items():
        assert f"({key})" in caplog.text
        assert value in caplog.text
