from absolutris.generators import randomorg

def test_randomorg():
    assert randomorg.pop() == 1
