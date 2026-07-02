# Task Manager CLI

Administrador de tareas desde terminal con subcomandos estilo `git`. Las tareas se guardan automaticamente en `~/.tasks.json`.

[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)](https://python.org)
[![CLI](https://img.shields.io/badge/CLI-ready-7C3AED)]()
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## Caracteristicas

- Subcomandos: `add`, `list`, `done`, `delete`, `search`, `stats`
- Prioridades: alta, media, baja
- Filtros: todas, pendientes, completadas
- Busqueda por titulo y descripcion
- Persistencia automatica en JSON
- Instalable como comando global via pip

## Instalacion

```bash
# Opcion 1: Instalar como comando global
pip install .
task add "Mi primera tarea"

# Opcion 2: Usar directamente con Python
python task.py add "Mi primera tarea"

# Opcion 3: Crear alias
echo 'alias task="python3 $(pwd)/task.py"' >> ~/.bashrc
source ~/.bashrc
```

## Comandos

### Crear tarea

```bash
task add "Comprar despensa"
task add "Estudiar FastAPI" -d "Completar el tutorial" -p alta
task add "Leer libro" -p baja
```

### Listar tareas

```bash
task list                  # Todas
task list -t pendientes    # Solo pendientes
task list -t completadas   # Solo completadas
```

### Marcar como completada

```bash
task done 1
```

### Eliminar tarea

```bash
task delete 1
```

### Buscar tareas

```bash
task search "comprar"
```

### Estadisticas

```bash
task stats
```

```
Total: 15
Completadas: 8
Pendientes: 7
Prioridad alta pendientes: 2
```

## Ejemplo completo

```bash
$ task add "Preparar presentacion" -d "Slides para la junta" -p alta
Tarea #1 creada: Preparar presentacion

$ task add "Enviar reporte"
Tarea #2 creada: Enviar reporte

$ task list
[ ] #  1 (!) Preparar presentacion
[ ] #  2 (*) Enviar reporte

$ task done 1
Tarea #1 marcada como completada

$ task stats
Total: 2
Completadas: 1
Pendientes: 1
Prioridad alta pendientes: 0
```

## Estructura del proyecto

```
cli-task-manager/
  task.py            # Codigo principal con todos los comandos
  pyproject.toml     # Configuracion del paquete pip
  README.md          # Este archivo
```

## Licencia

MIT
