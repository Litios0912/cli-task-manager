# Task Manager CLI

Administrador de tareas desde terminal con subcomandos similar a herramientas como git.

## Caracteristicas

- Subcomandos: add, list, done, delete, search, stats
- Prioridades: alta, media, baja
- Filtros: todas, pendientes, completadas
- Busqueda por texto
- Persistencia en JSON (~/.tasks.json)

## Uso

```bash
# Crear tarea
python task.py add "Comprar pan" -d "Pan integral" -p alta

# Listar tareas
python task.py list
python task.py list -t pendientes

# Marcar como completada
python task.py done 1

# Eliminar tarea
python task.py delete 1

# Buscar
python task.py search "comprar"

# Estadisticas
python task.py stats
```

## Instalacion como comando global

```bash
pip install .
# Ahora puedes usar: task add "Mi tarea"
```

## Instalacion manual (alias)

```bash
echo 'alias task="python3 ~/cli-task-manager/task.py"' >> ~/.bashrc
```
