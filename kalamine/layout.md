# Layout Object Documentation

This document describes the structure and parsing logic of the `KeyboardLayout` object used in Kalamine.

## Table of Contents

1. [Layout Object Structure](#layout-object-structure)
2. [Layer Indices](#layer-indices)
3. [Key Codes](#key-codes)
4. [Cell Structure](#cell-structure)
5. [Parsing Logic](#parsing-logic)
6. [Special Keys](#special-keys)

## Layout Object Structure

The `KeyboardLayout` class represents a keyboard layout with multiple layers. The main data structure is:

```python
layout.layers[layer_index][key_code] -> character(s)
layout.legends[layer_index][key_code] -> label string
```

### Example Access

`layout.layers[0]["ad01"]` - Returns the base character for the first key in the top row

## Layer Indices

Layers represent different modifier states:

- **0** (`Layer.BASE`): Base layer (no modifiers)
- **1** (`Layer.SHIFT`): Shift modifier
- **2** (`Layer.ODK`): 1dk (One Dead Key / Accent layer)
- **3** (`Layer.ODK_SHIFT`): Shift + 1dk
- **4** (`Layer.ALTGR`): AltGr modifier
- **5** (`Layer.ALTGR_SHIFT`): Shift + AltGr

## Key Codes

Key codes follow a standardized naming convention based on their position:

### Row Prefixes

- `ae--`: Numeric/function row keys (top row)
- `ad--`: Top letter row keys (QWERTY)
- `ac--`: Home row keys (ASDF)
- `ab--`: Bottom letter row keys (ZXCV)

### Position Suffixes

- `--01`, `--02`, `--03`, etc.: Position in the row from left to right

### Special Key Codes

- `tlde`: Backtick/tilde key (top-left)
- `lsgt`: Less-than/greater-than key (ISO layouts, left of Z)
- `spce`: Space bar
- `bspc`: Backspace
- Other special keys retain their abbreviated names

### Example Application: ErgolR Layout

```txt
╭╌╌╌╌╌┰─────┬─────┬─────┬─────┬─────┰─────┬─────┬─────┬─────┬─────┰╌╌╌╌╌┬╌╌╌╌╌╮
┆ esc ┃ f2  │ f3  │ f4  │ f5  │ f6  ┃ f8  │ f9  │ f10 │ f11 │ f12 ┃ ins ┆     ┆
┆ tlde┃ ae01│ ae02│ ae03│ ae04│ ae05┃ ae06│ ae07│ ae08│ ae09│ ae10┃ ae11┆ae12 ┆
╰╌╌╌╌╌╂─────┼─────┼─────┼─────┼─────╂─────┼─────┼─────┼─────┼─────╂╌╌╌╌╌┼╌╌╌╌╌┤
·     ┃ Q   │ C   │ O   │ P   │ W   ┃ J   │ M   │ D   │ !   │ Y   ┃ del ┆     ┆
·     ┃ ad01│ ad02│ ad03│ ad04│ ad05┃ ad06│ ad07│ ad08│ ad09│ ad10┃ ad11┆ad12 ┆
· · · ┠─────┼─────┼─────┼─────┼─────╂─────┼─────┼─────┼─────┼─────╂╌╌╌╌╌┼╌╌╌╌╌┤
·     ┃ A   │ S   │ E   │ N   │ F   ┃ L   │ R   │ T   │ I   │ U   ┃ bspc┆     ┆
·     ┃ ac01│ ac02│ ac03│ ac04│ ac05┃ ac06│ ac07│ ac08│ ac09│ ac10┃ ac11┆ac12 ┆
╭╌╌╌╌╌╂─────┼─────┼─────┼─────┼─────╂─────┼─────┼─────┼─────┼─────╂╌╌╌╌╌┴╌╌╌╌╌╯
┆ lsft┃ Z   │ X   │ ?   │ V   │ B   ┃ :   │ H   │ G   │ ;   │ K   ┃     ·     ·
┆ lsgt┃ ab01│ ab02│ ab03│ ab04│ ab05┃ ab06│ ab07│ ab08│ ab09│ ab10┃     ·     ·
╰╌╌╌╌╌┸─────┴─────┴─────┴─────┴─────┸─────┴─────┴─────┴─────┴─────┚ · · · · · ·
```

## Cell Structure

Each key cell in the layout template contains up to 4 character positions arranged in 2 lines:

```txt
┼─────┼
│ TL  │   TL = Top-Left (shift layer character)
│ BL  │   BL = Bottom-Left (base layer character)
┼─────┼
```

For layouts with additional layers (altgr or 1dk), the right side positions are used:

```txt
┼──────┼
│ TL TR│  TL = Top-Left (shift layer)      TR = Top-Right (shift+modifier layer)
│ BL BR│  BL = Bottom-Left (base layer)    BR = Bottom-Right (modifier layer)
┼──────┼
```

### Position Mapping

#### `base` layout

- **Bottom-Left**: Base character (Layer 0)
- **Top-Left**: Shift character (Layer 1)
- **Bottom-Right**: 1dk character (Layer 2)
- **Top-Right**: Shift+1dk character (Layer 3)

#### `altgr` layout

- **Bottom-Left**: AltGr character (Layer 4)
- **Top-Left**: Shift+AltGr character (Layer 5)
- Dead keys are marked with `*` prefix in the left column

#### `full` layout

Contains both base and altgr layers combined:

- **Left positions**: Base + Shift (Layers 0, 1)
- **Right positions**: AltGr + Shift+AltGr (Layers 4, 5)

### Example Cells

**Simple letter (auto-derivation):**

```txt
┬─────┬
│ Q   │   Layer 1 (Shift): 'Q'
│   â │   Layer 0 (Base):  'q' (auto-derived from Shift lowercase)
┼─────┼   Layer 2 (1dk):   'â'
          Layer 3 (1dk+Shift): 'Â' (auto-derived from 1dk uppercase)
```

**Function key with space-separated 1dk character:**

```txt
┬─────┬
│ $   │   Layer 1 (Shift): '$'
│ f2 ¤│   Layer 0 (Base):  'f2' (special key name stored as value)
┼─────┼   Layer 2 (1dk):   '¤'
          Layer 3 (1dk+Shift): empty (no uppercase for '¤')
          
Label: "f2 ¤"
Split: base="f2", odk="¤"
```

**Function key with concatenated 1dk character:**

```txt
┬─────┬
│ @   │   Layer 1 (Shift): '@'
│ f12÷│   Layer 0 (Base):  'f12' (special key, no space needed)
┼─────┼   Layer 2 (1dk):   '÷'
          Layer 3 (1dk+Shift): empty
          
Label: "f12÷"
Split: base="f12" (special key detected), odk="÷"
```

**Dead key marker:**

```txt
┬─────┬
│ !   │   Layer 1 (Shift): '!'
│***  │   Layer 0 (Base):  empty (auto-derived from Shift)
┼─────┼   Layer 2 (1dk):   '**' (dead key marker - asterisk in column i-1)
          Layer 3 (1dk+Shift): empty
```

**AltGr layer dead key:**

```txt
┬─────┬
│  *^ │   Layer 5 (Shift+AltGr): '*^' (dead key - circumflex)
│   ^ │   Layer 4 (AltGr):        '^' (base character)
┼─────┼
```

## Parsing Logic

The parser (`_parse_template` method) processes the layout template to extract characters:

### 1. Template Structure

The layout template consists of rows with 3 lines per keyboard row:

- Line 0 - e.g. `┬─────┬`: Top border
- Line 1 - e.g. `│ Q   │`: Shift/top characters
- Line 2 - e.g. `│   â │`: Base/bottom characters
- Line 3 - e.g. `┼─────┼`: Bottom border (also serves as top border for next row)

**Character Position Indexing:**

Each cell is 6 characters wide (5 visible + 1 border). Within a cell:

```txt
Column:   0 1 2 3 4 5 6
          │ X     Y   │
  Border ─╯ │     │   ╰─ Right border / Left border of next cell
  BASE ─────╯     │      
            ┆     ╰───── ODK/ALTGR
col_offset: 0     2
```

- Position `i` (BASE layer): Extracts character at column offset 0
- Position `i+2` (ODK/ALTGR layer): Extracts character at column offset 2
- Dead key marker (`*`): Checked at position `i-1`
- Label extraction: Scans from cell border to cell border

### 2. Column Offset Calculation

```python
col_offset = 0 if layer_number == Layer.BASE else 2
```

The column offset determines which position in the cell to read:

```txt
Cell content: │ Q   â │
Columns:      0 1 2 3 4 5
              │     │ │
              │     │ └─ ODK/ALTGR layer reads from offset +2 (column 3)
              │     │
              │     └─── (column 2 is dead key marker for ODK)
              │
              └─────── BASE layer reads from offset +0 (column 1)
                        (column 0 is dead key marker for BASE)
```

- **BASE layer** (col_offset = 0): Reads characters from left side of cell
- **ODK/ALTGR layers** (col_offset = 2): Reads characters from right side of cell

Each key advances by 6 columns for the next key in the row.

### 3. Character Extraction

For each key position, the parser:

1. **Extracts base character** (bottom-left or bottom-right) \
   `base_key = ("*" if base[i - 1] == "*" else "") + base[i]`
   - Checks for dead key marker (`*`) in the column before the character
   - Combines marker with the character

2. **Extracts shift character** (top-left or top-right) \
   `shift_key = ("*" if shift[i - 1] == "*" else "") + shift[i]`

3. **Extracts labels** for both positions \
   `base_label = self._extract_cell_label(base, i)` \
   `shift_label = self._extract_cell_label(shift, i)`
   - Labels are extracted by scanning horizontally until a cell border is found
   - Used for identifying special keys (f1-f12, esc, ins, del, etc.)

### 4. Character Processing Rules

#### Empty Character Handling

```python
# In BASE layer, if base is empty, use lowercase shift
if base_key == " ":
    if layer_number == Layer.BASE:
        base_key = shift_key.lower()

# In other layers, if shift is empty, use uppercase base
elif shift_key == " ":
    if layer_number == Layer.ALTGR:
        shift_key = upper_key(base_key)
    elif layer_number == Layer.ODK:
        shift_key = upper_key(base_key)
```

Example :

```txt
╂─────┼
┃ Q   │ Shift ODK empty: ODK(â)   to_upper -> Â
┃   â │ Base empty     : Shift(Q) to_lower -> q
┠─────┼
```

💡 This allows defining only one character per cell when appropriate (e.g., Q → q automatically).

#### Special Key Detection and Label Splitting

Special keys are identified and extracted from cell labels using a two-step process:

**1. Special Key Extraction**

```python
def extract_special_key(label: str) -> Optional[str]:
    """Extract special key name from label, or None if not a special key."""
    if not label:
        return None
    label_lower = label.lower().strip()
    
    # Check explicit special keys at the start
    for special in ("esc", "ins", "del", "bspc"):
        if label_lower.startswith(special):
            if len(label_lower) == len(special) or not label_lower[len(special)].isalpha():
                return special
    
    # Check for function keys f1-f12 at the start
    if label_lower.startswith("f"):
        i = 1
        while i < len(label_lower) and label_lower[i].isdigit():
            i += 1
        if i > 1:  # Found at least one digit after 'f'
            fn_num = int(label_lower[1:i])
            if 1 <= fn_num <= 12:
                return label_lower[:i]  # Return "f2", "f12", etc.
    
    return None
```

Special keys recognized:

- **Explicit names**: `esc`, `ins`, `del`, `bspc`
- **Function keys**: `f1` through `f12` (pattern: 'f' followed by 1-2 digits)

**2. Label Splitting for Multi-Layer Cells**

When a cell contains both a special key and a 1dk character (e.g., `"f2 ¤"` or `"f12÷"`), the label is intelligently split:

```python
def split_label_for_layers(label: str) -> tuple[Optional[str], Optional[str]]:
    """Split a label into (base_value, odk_value).
    
    Examples:
    - "f2 ¤" → ("f2",  "¤")   # Space-separated
    - "f12÷" → ("f12", "÷")   # No space, special key prefix
    - "Q"    → ("Q",   None)  # Single value
    """
```

Splitting rules:

1. **Special key prefix**: If label starts with a special key name, split after it:
   - `"f12÷"` → BASE: `"f12"`, ODK: `"÷"`
   - `"esc"` → BASE: `"esc"`, ODK: `None`

2. **Space separation**: If no special key but contains space, split on first space:
   - `"$ €"` → BASE: `"$"`, ODK: `"€"`
   - `"Q â"` → BASE: `"Q"`, ODK: `"â"`

3. **Single value**: If neither applies, use for base only:
   - `"Q"` → BASE: `"Q"`, ODK: `None`

**3. Layer-Appropriate Application**

The split values are applied based on which layer is being parsed:

```python
is_base_layer = (layer_number == Layer.BASE)
base_split, odk_split = split_label_for_layers(base_label)

if is_base_layer:
    # Use the left (base) part
    if base_split and extract_special_key(base_split):
        base_key = base_split  # Use special key name
else:  # ODK or ALTGR layer
    # Use the right (odk) part if it exists
    if odk_split:
        base_key = odk_split  # Use the 1dk/altgr character
```

This ensures:

- **BASE layer** (offset 0): Extracts special keys like `"f2"` from `"f2 ¤"`
- **ODK layer** (offset 2): Extracts 1dk characters like `"¤"` from `"f2 ¤"`

#### Tab Character Handling

The tab symbol `⇥` is converted to the actual tab character `\t`.

```python
if base_key.endswith("⇥"):
    base_key = base_key[:-1] + "\t"
if shift_key.endswith("⇥"):
    shift_key = shift_key[:-1] + "\t"
```

### 5. Dead Key Tracking

Any character matching a known dead key definition is added to the active dead key set.

```python
for dk in DEAD_KEYS:
    if base_key == dk.char or shift_key == dk.char:
        self.dk_set.add(dk.char)
```

`DEAD_KEYS` is a table loaded from [dead_keys.yaml](../data/dead_keys.yaml).
`char` can be:

- `**`: 1dk
- `` *` ``: grave (ÀàÈèÌìǸǹÒòÙùẀẁỲỳЀѐЍѝ)
- `*‟`: doublegrave (ȀȁȄȅȈȉȌȍȐȑȔȕѶѷ)
- `*´`: acute (ÁáĆćÉéǴǵÍíḰḱĹĺḾḿŃńÓóṔṕŔŕŚśÚúẂẃÝýŹźΆάΈέΉήΊίΌόΎύΏώЃѓЌќ)
- `*”`: doubleacute (ŐőŰűӲӳ)
- `*^`: circumflex (circumflex)
- `*ˇ`: caron (ǍǎČčĎďĚěǦǧȞȟǏǐǨǩĽľŇňǑǒŘřŠšŤťǓǔŽžǮǯ₀₁₂₃₄₅₆₇₈₉₍₎₊₋₌)
- `*˘`: breve (ĂăĔĕĞğĬĭŎŏŬŭᾸᾰῘῐῨῠӐӑӖӗӁӂЙйЎў)
- `*⁻`: invertedbreve (ȂȃȆȇȊȋȎȏȖȗȒȓ)
- `*~`: tilde (ÃãẼẽĨĩÑñÕõŨũṼṽỸỹ≲≳≃)
- `*¯`: macron (ĀāǢǣĒēḠḡĪīŌōŪūȲȳ)
- `*¨`: diaeresis (ÄäËëḦḧÏïÖöẗÜüẄẅẌẍŸÿΪϊΫϋӒӓЁёӚӛӜӝӞӟӤӥЇїӦӧӪӫӰӱӴӵӸӹӬӭ)
- `*˚`: abovering (ÅåŮůẘẙ)
- `*¸`: cedilla (ÇçḐḑȨȩĢģḨḩĶķĻļŅņŖŗŞşŢţ)
- `*,`: belowcomma (ȘșȚț)
- `*˛`: ogonek (ĄąĘęĮįǪǫŲų)
- `*/`: stroke (ȺⱥɃƀȻȼĐđɆɇǤǥĦħƗɨɈɉŁłØøⱣᵽɌɍŦŧɄʉɎɏƵƶ≮≰≱≯≠)
- `*˙`: abovedot (ȦȧḂḃĊċḊḋĖėḞḟĠġḢḣİıȷĿŀṀṁṄṅȮȯṖṗṘṙṠṡṪṫẆẇẊẋẎẏŻż)
- `*.`: belowdot (ẠạḄḅḌḍẸẹḤḥỊịḲḳḶḷṂṃṆṇỌọṚṛṢṣṬṭỤụṾṿẈẉỴỵẒẓ)
- `*µ`: greek (ΑαΒβΔδΕεΦφΓγΗηΙιΘθΚκΛλΜμΝνΟοΠπΧχΡρΣσΤτΥυΩωΞξΨψΖζ)
- `*¤`: currency (₳؋₱฿₵₡₵¢₯₫₠€₣ƒ₲₲₴₴៛﷼₭₭₤£ℳ₥₦₦૱௹₧₰₨₢$₪₮৳৲৲圓元₩₩円¥)

### 6. Layer Assignment

Non-empty characters are assigned to their respective layers.

```python
if base_key != " ":
    self.layers[layer_number][key] = base_key
if shift_key != " ":
    self.layers[layer_number.next()][key] = shift_key
```

## Special Keys

### Definition

Special keys are keyboard keys that perform actions rather than producing printable characters:

- **Function keys**: `f1`, `f2`, `f3`, ..., `f12`
- **Navigation**: `ins` (Insert), `del` (Delete)
- **Editing**: `bspc` (Backspace)
- **System**: `esc` (Escape)

### Detection Method

The parser identifies and processes special keys through a multi-step approach:

1. **Label extraction**: `_extract_cell_label()` extracts the complete cell content
2. **Label splitting**: `split_label_for_layers()` intelligently splits multi-value labels:
   - Detects special keys at the start of the label
   - Separates base and ODK values (by special key prefix or space)
3. **Special key recognition**: `extract_special_key()` validates and extracts special key names:
   - Explicit keys: `esc`, `ins`, `del`, `bspc`
   - Function keys: `f1` through `f12` (must be f + 1-2 digits, validated range 1-12)
4. **Layer-appropriate application**: Uses base part for BASE layer, ODK part for ODK/ALTGR layers

### Label Extraction

The `_extract_cell_label()` method extracts the complete content of a cell:

```python
@classmethod
def _extract_cell_label(cls, line: List[str], index: int) -> str:
    if index >= len(line):
        return ""
    left = index
    # Scan left until border character
    while left > 0 and not cls._is_cell_border(line[left - 1]):
        left -= 1
    right = index
    max_index = len(line) - 1
    # Scan right until border character
    while right < max_index and not cls._is_cell_border(line[right + 1]):
        right += 1
    return "".join(line[left : right + 1]).strip()
```

This extracts the entire cell content as a label, which may contain:

- A single character (e.g., `"Q"`)
- A special key name (e.g., `"esc"`, `"f10"`)
- Multiple values separated by space (e.g., `"f2 ¤"`)
- Multiple values concatenated (e.g., `"f12÷"`)

The label is then processed by `split_label_for_layers()` to separate base and ODK values appropriately.

### Function Keys in Character Positions

Function keys are properly handled when they appear in character positions through label splitting.

Example from ErgolR layout:

```txt
┬─────┬
│ $   │
│ f2 ¤│
┼─────┼
```

Parsing behavior:

**BASE layer parsing** (offset 0):

- Label extracted: `"f2 ¤"`
- Split result: base=`"f2"`, odk=`"¤"`
- Special key detected: `"f2"` → Layer 0 gets `"f2"`
- Layer 1 (Shift): `"$"`

**ODK layer parsing** (offset 2):

- Label extracted: `"f2 ¤"` (same cell)
- Split result: base=`"f2"`, odk=`"¤"`
- Uses odk part → Layer 2 gets `"¤"`
- Layer 3 (ODK+Shift): empty (derived from Layer 2)

### Additional Context

The geometry data (`geometry.yaml`) defines the row structure:

- Each row has an `offset` (starting column position)
- Keys are spaced 6 columns apart in the template
- This means each cell occupies approximately 5 visible columns plus 1 border

The parser advances by 6 columns per key:

```python
i += 6  # Move to next key position
```

This coordinate system must align with the template's visual structure for proper character extraction.

## Summary

The layout object provides a structured representation of keyboard layouts with:

- Multiple layers for different modifier states
- Standardized key codes based on physical position
- Flexible cell structure supporting up to 4 characters per key
- Automatic derivation of shift/base relationships
- Dead key support with special markers
- Special key handling for function and editing keys

The parsing logic handles the complex task of extracting this information from visual ASCII-art templates, with specific rules for character precedence, special key detection, and layer assignment.
