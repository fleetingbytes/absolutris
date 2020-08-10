#!/usr/bin/env python

"""
Testing yield from
"""

class SpamException(Exception): pass


def writer():
    while True:
        try:
            w = (yield)
            print(f">> {w}")
        except SpamException:
            print("***")


def writer_wrapper(coro):
    # coro.send(None) # prime the coro
    # while True:
        # try:
            # x = (yield) # Capture the value that's sent to the wrapper
            # coro.send(x) # Send it to the wrapped coroutine
        # except StopIteration:
            # pass
    yield from coro


if __name__ == "__main__":
    w = writer()
    wrap = writer_wrapper(w)
    wrap.send(None) # prime the coroutine
    for i in [1, 2, 3, "spam", 4]:
        if i == "spam":
            wrap.throw(SpamException)
        else:
            wrap.send(i)

