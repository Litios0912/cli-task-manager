import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

from task import load, save, next_id, cmd_add, cmd_list, cmd_done, cmd_delete, cmd_search, cmd_stats


class TestTaskManager:
    def setup_method(self):
        self.tmp = tempfile.mkdtemp()
        self.db = Path(self.tmp) / ".tasks.json"
        self._patcher = patch("task.DB_PATH", self.db)
        self._patcher.start()

    def teardown_method(self):
        self._patcher.stop()

    def test_empty_list(self):
        assert load() == []

    def test_save_and_load(self):
        save([{"id": 1, "title": "Test"}])
        assert load() == [{"id": 1, "title": "Test"}]

    def test_next_id_empty(self):
        assert next_id([]) == 1

    def test_next_id_existing(self):
        assert next_id([{"id": 5}]) == 6

    def test_add_creates_task(self, capsys):
        class Args:
            title = "Mi tarea"
            desc = ""
            priority = "media"
        cmd_add(Args)
        tasks = load()
        assert len(tasks) == 1
        assert tasks[0]["title"] == "Mi tarea"
        assert tasks[0]["done"] is False

    def test_add_with_description(self, capsys):
        class Args:
            title = "Tarea importante"
            desc = "Descripcion detallada"
            priority = "alta"
        cmd_add(Args)
        tasks = load()
        assert tasks[0]["description"] == "Descripcion detallada"
        assert tasks[0]["priority"] == "alta"

    def test_list_shows_tasks(self, capsys):
        save([{"id": 1, "title": "T1", "done": False, "priority": "alta", "description": ""}])
        class Args:
            type = "todas"
        cmd_list(Args)
        captured = capsys.readouterr()
        assert "T1" in captured.out

    def test_done_marks_completed(self, capsys):
        save([{"id": 1, "title": "T1", "done": False, "priority": "media", "description": ""}])
        class Args:
            id = 1
        cmd_done(Args)
        assert load()[0]["done"] is True

    def test_done_not_found(self, capsys):
        class Args:
            id = 999
        cmd_done(Args)
        captured = capsys.readouterr()
        assert "no encontrada" in captured.out

    def test_delete_removes_task(self, capsys):
        save([{"id": 1, "title": "T1", "done": False, "priority": "baja", "description": ""}])
        class Args:
            id = 1
        cmd_delete(Args)
        assert load() == []

    def test_delete_not_found(self, capsys):
        save([{"id": 1, "title": "T1", "done": False, "priority": "media", "description": ""}])
        class Args:
            id = 999
        cmd_delete(Args)
        assert len(load()) == 1

    def test_search_finds_tasks(self, capsys):
        save([
            {"id": 1, "title": "Comprar pan", "description": "", "done": False, "priority": "media"},
            {"id": 2, "title": "Estudiar Python", "description": "", "done": False, "priority": "alta"},
        ])
        class Args:
            texto = "comprar"
        cmd_search(Args)
        captured = capsys.readouterr()
        assert "Comprar" in captured.out
        assert "Estudiar" not in captured.out

    def test_stats_counts(self, capsys):
        save([
            {"id": 1, "title": "T1", "done": True, "priority": "alta", "description": ""},
            {"id": 2, "title": "T2", "done": False, "priority": "alta", "description": ""},
            {"id": 3, "title": "T3", "done": False, "priority": "media", "description": ""},
        ])
        cmd_stats(None)
        captured = capsys.readouterr()
        assert "Total: 3" in captured.out
        assert "Completadas: 1" in captured.out
        assert "Pendientes: 2" in captured.out
        assert "alta pendientes: 1" in captured.out
