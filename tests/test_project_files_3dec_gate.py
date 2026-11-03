"""The reproduction path: a task ends and the bridge lists its script.

On 3DEC 9.00.184 that call crashed the GUI twice (ucrtbase.dll,
0xc0000409) after the task had already completed, in both cases straight
after the ``Data file queued for the GUI project`` line. The candidate
keeps the registration off on that host and leaves every other host as it
was. These tests drive the exact call shapes the task teardown uses:
``script.py`` calls ``register(path, force=True)``, ``program_call`` calls
``register(path)`` and later ``flush_deferred()``.
"""

from __future__ import annotations

import logging

import pytest

from itasca_mcp_bridge.console import project_files

import test_project_files as harness


@pytest.fixture(autouse=True)
def _fresh(monkeypatch):
    project_files.reset()
    project_files._disabled_logged = False
    yield
    project_files.reset()
    project_files._disabled_logged = False


def _host(monkeypatch, executable):
    monkeypatch.setattr(project_files.sys, "executable", executable, raising=False)


def _gui(monkeypatch, layout="9.x"):
    gui, registrar = harness._registrar(layout)
    monkeypatch.setattr(project_files, "_get_registrar", lambda: registrar)
    return gui, registrar


def _script(tmp_path):
    script = tmp_path / "build_3dec_initial_075.py"
    script.write_text("print('build')\n", encoding="utf-8")
    return script


THREE_DEC_GUI = r"D:\Program Files\Itasca\ItascaSoftware900\exe64\3dec900_gui.exe"
PFC_GUI = r"D:\Program Files\Itasca\ItascaSoftware900\exe64\pfc3d900_gui.exe"


def test_3dec_skips_the_teardown_registration(tmp_path, monkeypatch):
    """script.py: register(path, force=True) while the task is still running."""
    _host(monkeypatch, THREE_DEC_GUI)
    gui, registrar = _gui(monkeypatch)
    monkeypatch.setattr(project_files, "_task_executing", lambda: True)

    assert project_files.register(str(_script(tmp_path)), force=True) is False
    gui.timers.flush()

    assert gui.editor.calls == []
    assert gui.listed_paths == []
    assert registrar._pending == set()
    assert gui.activated == []


def test_3dec_holds_nothing_back_for_the_program_call_flush(tmp_path, monkeypatch):
    """program_call.py: register(path) during a task, then flush at its end."""
    _host(monkeypatch, THREE_DEC_GUI)
    gui, registrar = _gui(monkeypatch)
    monkeypatch.setattr(project_files, "_task_executing", lambda: True)

    assert project_files.register(str(_script(tmp_path))) is False
    assert registrar._deferred == []

    monkeypatch.setattr(project_files, "_task_executing", lambda: False)
    project_files.flush_deferred()
    registrar.flush_deferred()
    gui.timers.flush()

    assert gui.editor.calls == []


def test_3dec_still_refreshes_the_editors(tmp_path, monkeypatch):
    """Only the listing is off: the foreground reload check stays on."""
    _host(monkeypatch, THREE_DEC_GUI)
    gui, registrar = _gui(monkeypatch)
    invoked = []
    registrar._core.QMetaObject.invokeMethod = (
        lambda obj, method, kind, *a: invoked.append((obj, method, kind)) or True
    )

    project_files.refresh_editors()
    assert invoked == [(gui.editor, "onApplicationActivated", 2)]


def test_pfc_gui_keeps_listing_the_file(tmp_path, monkeypatch):
    """The gate is 3DEC only; the measured PFC path must not change."""
    _host(monkeypatch, PFC_GUI)
    gui, registrar = _gui(monkeypatch)
    monkeypatch.setattr(project_files, "_task_executing", lambda: False)
    script = _script(tmp_path)

    assert project_files.register(str(script)) is True
    gui.timers.flush()

    target = str(script).replace("\\", "/")
    assert gui.editor.calls == [("open", target, True), ("close", target)]
    assert project_files.normalize(str(script)) in registrar.listed()


def test_a_plain_interpreter_keeps_the_previous_behaviour(tmp_path, monkeypatch):
    _host(monkeypatch, r"C:\Python310\python.exe")
    gui, registrar = _gui(monkeypatch)
    monkeypatch.setattr(project_files, "_task_executing", lambda: False)

    assert project_files.register(str(_script(tmp_path))) is True
    gui.timers.flush()
    assert [c[0] for c in gui.editor.calls] == ["open", "close"]


def test_a_directory_named_3dec_does_not_trip_the_gate(tmp_path, monkeypatch):
    """Matching is on the binary name, not on any '3dec' in the path."""
    _host(monkeypatch, r"D:\3dec-notes\venv\Scripts\python.exe")
    gui, registrar = _gui(monkeypatch)
    monkeypatch.setattr(project_files, "_task_executing", lambda: False)

    assert project_files.register(str(_script(tmp_path))) is True
    gui.timers.flush()
    assert [c[0] for c in gui.editor.calls] == ["open", "close"]


@pytest.mark.parametrize("executable", [
    r"D:\Itasca\3dec900_console.exe",
    r"D:\Itasca\3dec910_gui.exe",
    r"D:\Itasca\3dec900_gui.exe.backup",
    "", None,
])
def test_other_or_unknown_hosts_keep_registration(tmp_path, monkeypatch, executable):
    _host(monkeypatch, executable)
    gui, _ = _gui(monkeypatch)
    monkeypatch.setattr(project_files, "_task_executing", lambda: False)
    assert project_files.register(str(_script(tmp_path))) is True
    gui.timers.flush()
    assert [c[0] for c in gui.editor.calls] == ["open", "close"]


def test_direct_registration_and_existing_deferred_are_blocked(tmp_path, monkeypatch):
    _host(monkeypatch, THREE_DEC_GUI)
    gui, registrar = _gui(monkeypatch)
    monkeypatch.setattr(project_files, "_registrar", registrar)
    path = str(_script(tmp_path))
    registrar._deferred = [path]
    assert registrar.register(path, force=True) is False
    project_files.flush_deferred()
    assert registrar._deferred == [path]  # module guard leaves existing entries untouched
    registrar.flush_deferred()
    assert registrar._deferred == []  # direct flush discards entries; register remains gated
    gui.timers.flush()
    assert gui.editor.calls == []


def test_script_runner_teardown_hits_real_gate(tmp_path, monkeypatch, itasca_stub):
    from io import StringIO
    from itasca_mcp_bridge.execution.script import ScriptRunner
    from types import SimpleNamespace

    _host(monkeypatch, THREE_DEC_GUI)
    monkeypatch.chdir(tmp_path)
    calls = []
    real_register = project_files.register
    monkeypatch.setattr(project_files, "register", lambda path, force=False: calls.append((path, force)) or real_register(path, force))
    monkeypatch.setattr(project_files, "_get_registrar", lambda: pytest.fail("registration reached Qt"))
    monkeypatch.setattr(project_files, "refresh_editors", lambda: None)
    path = str(_script(tmp_path))
    result = ScriptRunner(None, SimpleNamespace(tasks={}))._execute(path, "result = 42", StringIO(), "gate-task")
    assert result["status"] == "success"
    assert calls == [(path, True)]


def test_program_call_entry_hits_real_gate(tmp_path, monkeypatch):
    from itasca_mcp_bridge.utils.program_call import expand_program_call

    _host(monkeypatch, THREE_DEC_GUI)
    monkeypatch.chdir(tmp_path)
    calls = []
    real_register = project_files.register
    monkeypatch.setattr(project_files, "register", lambda path, force=False: calls.append((path, force)) or real_register(path, force))
    monkeypatch.setattr(project_files, "_get_registrar", lambda: pytest.fail("registration reached Qt"))
    source = tmp_path / "test.dat"
    source.write_text("model new\n", encoding="utf-8")
    commands = []
    assert expand_program_call("program call 'test.dat'", commands.append) is True
    assert calls == [(str(source), False)]
    assert commands == ["model new"]


def test_the_gate_is_logged_once(monkeypatch, caplog):
    _host(monkeypatch, THREE_DEC_GUI)
    caplog.set_level(logging.INFO, logger="itasca-mcp-bridge")

    assert project_files.registration_disabled() is True
    project_files.registration_disabled()

    records = [r for r in caplog.records if "registration is off" in r.getMessage()]
    assert len(records) == 1
