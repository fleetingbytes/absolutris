#!/usr/bin/env python


from absolutris import plans
from absolutris import testhelper


def test_plan_classes() -> None:
    """
    Checks if a Plan class is usable.
    What makes a Plan class usable?
    """
    for _, PC in testhelper.find_plan_classes():
        # Check if it generates instances of Plan
        assert isinstance(PC(), plans.Plan)


def test_plan_instances() -> None:
    """
    Checks if every Plan instance is usable.
    """
    for _, pi in testhelper.find_plan_instances():
        assert pi

