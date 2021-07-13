import pytest
import task1

def test_limits(qtbot):
    widget = task1.form()
    qtbot.addWidget(widget)

    # click in plot botton and make sure error message appears
    qtbot.mouseClick(widget.button, Qt.LeftButton)

    messages = [(m.type, m.message.strip()) for m in qtlog.records]
    assert messages == [(Warning, "this is a WARNING message")]

test_limits()