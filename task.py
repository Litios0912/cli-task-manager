#!/usr/bin/env python3
"""
Task Manager CLI
Administrador de tareas desde terminal con subcomandos.
Uso: task <comando> [opciones]

Comandos:
  task add <titulo> [-d <desc>] [-p alta|media|baja]
  task list [-t todas|pendientes|completadas]
  task done <id>
  task delete <id>
  task search <texto>
  task stats
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

DB_PATH = Path.home() / ".tasks.json"


def load():
    if DB_PATH.exists():
        return json.loads(DB_PATH.read_text())
    return []


def save(tasks):
    DB_PATH.write_text(json.dumps(tasks, indent=2, ensure_ascii=False))


def next_id(tasks):
    return max([t["id"] for t in tasks], default=0) + 1


def cmd_add(args):
    tasks = load()
    task = {
        "id": next_id(tasks),
        "title": args.title,
        "description": args.desc or "",
        "priority": args.priority or "media",
        "done": False,
        "created": datetime.now().isoformat(),
    }
    tasks.append(task)
    save(tasks)
    print(f"Tarea #{task['id']} creada: {task['title']}")


def cmd_list(args):
    tasks = load()
    if args.type == "pendientes":
        tasks = [t for t in tasks if not t["done"]]
    elif args.type == "completadas":
        tasks = [t for t in tasks if t["done"]]
    if not tasks:
        print("No hay tareas.")
        return
    for t in tasks:
        status = "x" if t["done"] else " "
        prio = {"alta": "!", "media": "*", "baja": "."}[t["priority"]]
        print(f"[{status}] #{t['id']:3d} ({prio}) {t['title']}")
    print(f"\nTotal: {len(tasks)} tareas")


def cmd_done(args):
    tasks = load()
    for t in tasks:
        if t["id"] == args.id:
            t["done"] = True
            t["completed"] = datetime.now().isoformat()
            save(tasks)
            print(f"Tarea #{args.id} marcada como completada")
            return
    print(f"Tarea #{args.id} no encontrada")


def cmd_delete(args):
    tasks = load()
    before = len(tasks)
    tasks = [t for t in tasks if t["id"] != args.id]
    if len(tasks) < before:
        save(tasks)
        print(f"Tarea #{args.id} eliminada")
    else:
        print(f"Tarea #{args.id} no encontrada")


def cmd_search(args):
    tasks = load()
    q = args.texto.lower()
    results = [t for t in tasks if q in t["title"].lower() or q in t["description"].lower()]
    if not results:
        print(f"Sin resultados para '{args.texto}'")
        return
    for t in results:
        status = "x" if t["done"] else " "
        print(f"[{status}] #{t['id']:3d} {t['title']}")
    print(f"\n{len(results)} resultados")


def cmd_stats(args):
    tasks = load()
    total = len(tasks)
    done = sum(1 for t in tasks if t["done"])
    pending = total - done
    alta = sum(1 for t in tasks if t["priority"] == "alta" and not t["done"])
    print(f"Total: {total}")
    print(f"Completadas: {done}")
    print(f"Pendientes: {pending}")
    print(f"Prioridad alta pendientes: {alta}")


def main():
    parser = argparse.ArgumentParser(
        description="Task Manager CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  task add "Comprar pan" -d "Pan integral" -p alta
  task list
  task list -t pendientes
  task done 1
  task delete 1
  task search "comprar"
  task stats
        """,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Crear nueva tarea")
    p_add.add_argument("title", help="Titulo de la tarea")
    p_add.add_argument("-d", "--desc", help="Descripcion")
    p_add.add_argument("-p", "--priority", choices=["alta", "media", "baja"], default="media")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="Listar tareas")
    p_list.add_argument("-t", "--type", choices=["todas", "pendientes", "completadas"], default="todas")
    p_list.set_defaults(func=cmd_list)

    p_done = sub.add_parser("done", help="Marcar tarea como completada")
    p_done.add_argument("id", type=int, help="ID de la tarea")
    p_done.set_defaults(func=cmd_done)

    p_del = sub.add_parser("delete", help="Eliminar tarea")
    p_del.add_argument("id", type=int, help="ID de la tarea")
    p_del.set_defaults(func=cmd_delete)

    p_search = sub.add_parser("search", help="Buscar tareas")
    p_search.add_argument("texto", help="Texto a buscar")
    p_search.set_defaults(func=cmd_search)

    p_stats = sub.add_parser("stats", help="Estadisticas de tareas")
    p_stats.set_defaults(func=cmd_stats)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
