---
produced_by: codex (gpt-6)
produced_at: 2026-11-03 17:05 +08:00
last_edit_by: codex (gpt-6)
last_edit_at: 2026-11-03 17:05 +08:00
---

# 3DEC 9.00.184 GUI compatibility: project registration and `&` data files

## Observations

- With unmodified Bridge 0.6.8, a pure Python task completed and the 3DEC GUI then exited without user action. The Windows Application Error for that process named `3dec900_gui.exe`, `ucrtbase.dll`, and exception `0xc0000409`. The Bridge log ended immediately after queuing the task script for the GUI Project pane. This identifies a suspect registration path, but no Qt stack trace isolates the exact failing slot.
- The 0.75 m case's `poly.dat` contains 17,453 `block create tetrahedron` commands, each written over six physical lines with a trailing `&` on the first five. Bridge's `program call` expansion split only `...` continuations. It reported 104,719 commands and stopped at the first incomplete `block create tetrahedron ... &` call.

## Changes

- `console/project_files.py` skips automatic Data Files registration only when the embedded interpreter's host binary basename is `3dec900_gui.exe`. The module and direct registrar paths use the same guard. Other hosts keep the existing behavior; the 3DEC 9.0 GUI no longer gets Bridge task scripts listed automatically in its Project pane.
- `utils/command_splitter.py` treats a separate trailing `&` as a continuation, as well as `...`, outside FISH definition blocks. The continuation marker is removed before one complete command is sent to the engine. The original `poly.dat` is unchanged.

## Verification on 2026-11-03

- Offline: 423 Bridge tests passed after merging upstream 0.6.8 into the user's fork. Static splitting of the unmodified `poly.dat` yields 17,454 complete commands including `program echo suppress`.
- Live: a newly started 3DEC 9.00.184 GUI loaded this isolated Bridge 0.6.8 source with `auto_upgrade=False` on port 19113. The log recorded the exact host registration guard. One build task, `a75e01`, completed in 1,933.41 s. Its final output reported 11,788 blocks, 56,936 gridpoints, 21,883 zones and a 436,185,245-byte initial `.sav`. The GUI remained responsive after task completion and after a later `project save` command.
- The engine marked the saved model state `unrepeatable` from its input record/data files. The case package retains the Python builder and original `poly.dat`; this warning is not a claim of scientific reproducibility.

## Scope

The observed GUI exit is mitigated for this host and these runs. The native Qt crash mechanism is not proven, and other 3DEC versions have not been tested. The 0.75 m **initial build** passed; UCS cycling to 5,000, contact/finalization, parameter calibration, and scientific acceptance remain separate steps. The isolated live run does not mean an installed PyPI or production Bridge instance has been updated.
