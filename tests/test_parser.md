# Layout object

`layout.layers[0]["ad01"]`

## Layer index

- 0: base
- 1: shift
- 2: 1dk
- 3: shift + 1dk
- 4: altgr
- 5: shift + altgr

## Key code

- `ae--`: numeric row keys
- `ad--`: top     row keys
- `ac--`: home    row keys
- `ab--`: bottom  row keys
- `--XX`: position in the row, from left to right: 01, 02, ...

Application with the ErgolR layout

```txt
╭╌╌╌╌╌┰─────┬─────┬─────┬─────┬─────┰─────┬─────┬─────┬─────┬─────┰╌╌╌╌╌┬╌╌╌╌╌╮
┆ esc ┃ f2  │ f3  │ f4  │ f5  │ f6  ┃ f8  │ f9  │ f10 │ f11 │ f12 ┃ ins ┆     ┆
┆ tlde┃ ae01│ ae02│ ae03│ ae04│ ae05┃ ae06│ ae07│ ae08│ ae09│ ae10┃ ae11┆     ┆
╰╌╌╌╌╌╂─────┼─────┼─────┼─────┼─────╂─────┼─────┼─────┼─────┼─────╂╌╌╌╌╌┼╌╌╌╌╌┤
·     ┃ Q   │ C   │ O   │ P   │ W   ┃ J   │ M   │ D   │ !   │ Y   ┃ del ┆     ┆
·     ┃ ad01│ ad02│ ad03│ ad04│ ad05┃ ad06│ ad07│ ad08│ ad09│ ad10┃ ad11┆     ┆
· · · ┠─────┼─────┼─────┼─────┼─────╂─────┼─────┼─────┼─────┼─────╂╌╌╌╌╌┼╌╌╌╌╌┤
·     ┃ A   │ S   │ E   │ N   │ F   ┃ L   │ R   │ T   │ I   │ U   ┃ bspc┆     ┆
·     ┃ ac01│ ac02│ ac03│ ac04│ ac05┃ ac06│ ac07│ ac08│ ac09│ ac10┃ ac11┆     ┆
╭╌╌╌╌╌╂─────┼─────┼─────┼─────┼─────╂─────┼─────┼─────┼─────┼─────╂╌╌╌╌╌┴╌╌╌╌╌╯
┆ lsft┃ Z   │ X   │ ?   │ V   │ B   ┃ :   │ H   │ G   │ ;   │ K   ┃     ·     ·
┆ lsgt┃ ab01│ ab02│ ab03│ ab04│ ab05┃ ab06│ ab07│ ab08│ ab09│ ab10┃     ·     ·
╰╌╌╌╌╌┸─────┴─────┴─────┴─────┴─────┸─────┴─────┴─────┴─────┴─────┚ · · · · · ·
```
