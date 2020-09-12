#!/usr/bin/env python


from absolutris import plans
from absolutris import level
from absolutris import next_window
from absolutris import scoring
from absolutris import events
from absolutris import testhelper


# def test_plan_classes() -> None:
    # """
    # Checks if a Plan class is usable.
    # What makes a Plan class usable?
    # """
    # for _, PC in testhelper.find_plan_classes():
        # # Check if it generates instances of Plan
        # assert isinstance(PC(), plans.Plan)


def test_plan_instances() -> None:
    """
    Checks if every Plan instance is usable.
    """
    for _, pi in testhelper.find_plan_instances():
        assert pi
        # Check types
        assert type(pi.name) is str
        assert type(pi.version) is str
        for lvl in pi.levels:
            assert isinstance(lvl, level.Level)
            assert type(lvl.message) is str
            assert type(lvl.gravity) is int
            assert isinstance(lvl.scoring, scoring.Scoring)
            assert type(lvl.scoring.single) is int
            assert type(lvl.scoring.double) is int
            assert type(lvl.scoring.triple) is int
            assert type(lvl.scoring.tetris) is int
            assert callable(lvl.scoring.soft_drop)
            assert callable(lvl.scoring.hard_drop)
            assert callable(lvl.condition)
        assert type(pi.next_window) is next_window.Next_Window
        # Check values
        assert len(pi.levels) > 0
        assert type(pi.current_level) is level.Level
        for lvl in pi.levels:
            assert lvl.gravity >= 1
            for n in range(min(events.Row), max(events.Row) + 1):
                assert type(lvl.scoring.soft_drop(n)) is int
                assert type(lvl.scoring.hard_drop(n)) is int
