from kalamine import KeyboardLayout

from .util import get_layout_dict


def load_layout(filename: str, angle_mod: bool = False) -> KeyboardLayout:
    return KeyboardLayout(get_layout_dict(filename), angle_mod)

# Layers convention:
# 0: base
# 1: shift
# 2: 1dk (if any)
# 3: shift + 1dk (if any)
# 4: altgr (if any)
# 5: shift + altgr (if any)

# Keys convention (XKB / ISO 9995):
# > aeXX: numeric row keys
# > adXX: top     row keys (QCOPW row for Ergo-L, otherwise QWERTY, AZERTY...)
# > acXX: home    row keys (ASENF row for Ergo-L)
# > abXX: bottom  row keys (ZXCVB row for Ergo-L)
# >   XX: position in the row, from left to right: 01..12 (or more)

def test_ansi():
    layout = load_layout("ansi")
    assert layout.layers[0]["ad01"] == "q"
    assert layout.layers[1]["ad01"] == "Q"
    assert layout.layers[0]["tlde"] == "`"
    assert layout.layers[1]["tlde"] == "~"
    assert not layout.has_altgr
    assert not layout.has_1dk
    assert "**" not in layout.dead_keys

    # ensure angle mod is NOT applied
    layout = load_layout("ansi", angle_mod=True)
    assert layout.layers[0]["ab01"] == "z"
    assert layout.layers[1]["ab01"] == "Z"


def test_prog():  # AltGr + dead keys
    layout = load_layout("prog")
    assert layout.layers[0]["ad01"] == "q"
    assert layout.layers[1]["ad01"] == "Q"
    assert layout.layers[0]["tlde"] == "`"
    assert layout.layers[1]["tlde"] == "~"
    assert layout.layers[4]["tlde"] == "*`"
    assert layout.layers[5]["tlde"] == "*~"
    assert layout.has_altgr
    assert not layout.has_1dk
    assert "**" not in layout.dead_keys
    assert len(layout.dead_keys["*`"]) == 18
    assert len(layout.dead_keys["*~"]) == 21


def test_intl():  # 1dk + dead keys
    layout = load_layout("intl")
    assert layout.layers[0]["ad01"] == "q"
    assert layout.layers[1]["ad01"] == "Q"
    assert layout.layers[0]["tlde"] == "*`"
    assert layout.layers[1]["tlde"] == "*~"
    assert not layout.has_altgr
    assert layout.has_1dk
    assert "**" in layout.dead_keys

    assert len(layout.dead_keys) == 5
    assert "**" in layout.dead_keys
    assert "*`" in layout.dead_keys
    assert "*^" in layout.dead_keys
    assert "*¨" in layout.dead_keys
    assert "*~" in layout.dead_keys
    assert len(layout.dead_keys["**"]) == 15
    assert len(layout.dead_keys["*`"]) == 18
    assert len(layout.dead_keys["*^"]) == 43
    assert len(layout.dead_keys["*¨"]) == 21
    assert len(layout.dead_keys["*~"]) == 21

    # ensure the 1dk parser does not accumulate values from a previous run
    layout = load_layout("intl")
    assert len(layout.dead_keys["*`"]) == 18
    assert len(layout.dead_keys["*~"]) == 21

    assert len(layout.dead_keys) == 5
    assert "**" in layout.dead_keys
    assert "*`" in layout.dead_keys
    assert "*^" in layout.dead_keys
    assert "*¨" in layout.dead_keys
    assert "*~" in layout.dead_keys
    assert len(layout.dead_keys["**"]) == 15
    assert len(layout.dead_keys["*`"]) == 18
    assert len(layout.dead_keys["*^"]) == 43
    assert len(layout.dead_keys["*¨"]) == 21
    assert len(layout.dead_keys["*~"]) == 21

    # ensure angle mod is working correctly
    layout = load_layout("intl", angle_mod=True)
    assert layout.layers[0]["lsgt"] == "z"
    assert layout.layers[1]["lsgt"] == "Z"
    assert layout.layers[0]["ab01"] == "x"
    assert layout.layers[1]["ab01"] == "X"


def test_ergol():
    layout = load_layout("ergol")
    assert layout.meta["locale"] == "fr"
    assert layout.meta["geometry"] == "ERGO"
    assert layout.has_altgr
    assert layout.has_1dk

    # Base layer
    assert layout.layers[0]["ad01"] == "q"
    assert layout.layers[1]["ad01"] == "Q"
    assert layout.layers[0]["ad09"] == "**"
    assert layout.layers[1]["ad09"] == "!"

    # ODK layer (1dk)
    assert layout.layers[2]["ad01"] == "â"
    assert layout.layers[2]["ad09"] == "*¨"

    # AltGr layer
    assert layout.layers[4]["ad01"] == "^"
    assert layout.layers[5]["ad01"] == "*^"
    assert layout.layers[4]["ad02"] == "<"
    assert layout.layers[5]["ad02"] == "≤"


def test_ergolr():
    layout = load_layout("ergolr")
    assert layout.meta["locale"] == "en"
    assert layout.meta["geometry"] == "ERGO"
    assert layout.has_altgr
    assert layout.has_1dk

    # Base layer
    assert layout.layers[0]["ae01"] == "f2"
    assert layout.layers[0]["ae10"] == "f12"
    assert layout.layers[0]["ad01"] == "q"
    assert layout.layers[1]["ad01"] == "Q"
    assert layout.layers[0]["ad09"] == "**" # dead key
    assert layout.layers[1]["ad09"] == "!"

    # ODK layer (1dk)
    assert layout.layers[2]["ae01"] == "¤"
    assert layout.layers[2]["ad01"] == "â"
    assert layout.layers[2]["ae02"] == "«"
    assert layout.layers[3]["ae02"] == "❝"
    assert layout.layers[3]["ae02"] == "❝"
    assert layout.layers[2]["ae10"] == "÷"

    # AltGr layer
    assert layout.layers[4]["ad01"] == "^"
    assert layout.layers[5]["ad01"] == "*^"
    assert layout.layers[4]["ad02"] == "<"
    assert layout.layers[5]["ad02"] == "≤"


def test_tab():
    layout_data = {
        "name": "tab-test",
        "geometry": "ANSI",
        "base": """\
┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┲━━━━━━━━━━┓
│     │     │     │     │     │     │     │     │     │     │     │     │     ┃          ┃
│     │     │     │     │     │     │     │     │     │     │     │     │     ┃ ⌫        ┃
┢━━━━━┷━━┱──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┺━━┯━━━━━━━┩
┃        ┃     │ ⇥   │     │     │     │     │     │     │     │     │     │     │       │
┃ ↹      ┃ ⇥   │     │     │     │     │     │     │     │     │     │     │     │       │
┣━━━━━━━━┻┱────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┲━━━━┷━━━━━━━┪
┃         ┃     │     │     │     │     │     │     │     │     │     │     ┃            ┃
┃ ⇬       ┃     │     │     │     │     │     │     │     │     │     │     ┃ ⏎          ┃
┣━━━━━━━━━┻━━┱──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┲━━┻━━━━━━━━━━━━┫
┃            ┃     │     │     │     │     │     │     │     │     │     ┃               ┃
┃ ⇧          ┃     │     │     │     │     │     │     │     │     │     ┃ ⇧             ┃
┣━━━━━━━┳━━━━┻━━┳━━┷━━━━┱┴─────┴─────┴─────┴─────┴─────┴─┲━━━┷━━━┳━┷━━━━━╋━━━━━━━┳━━━━━━━┫
┃       ┃       ┃       ┃                                ┃       ┃       ┃       ┃       ┃
┃ Ctrl  ┃ super ┃ Alt   ┃ ␣                              ┃ Alt   ┃ super ┃ menu  ┃ Ctrl  ┃
┗━━━━━━━┻━━━━━━━┻━━━━━━━┹────────────────────────────────┺━━━━━━━┻━━━━━━━┻━━━━━━━┻━━━━━━━┛
"""
    }
    layout = KeyboardLayout(layout_data)
    assert layout.layers[0]["ad01"] == "\t"
    assert layout.layers[1]["ad02"] == "	"  # Tab character too
