# PyFlow

PyFlow to prosta biblioteka w języku Python służąca do definiowania, walidowania i planowania grafów workflow.

## Funkcjonalności

- Definiowanie zadań wraz z zależnościami i parametrami.
- Dodawanie zadań do workflow.
- Wykrywanie brakujących zależności i cykli w grafie.
- Wyznaczanie deterministycznej kolejności wykonywania zadań.
- Grupowanie zadań w warstwy wykonania.

## Wymagania

- Python 3.11 lub nowszy
- pip

## Instalacja

Utwórz środowisko wirtualne i je aktywuj:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Zainstaluj projekt wraz z zależnościami deweloperskimi:

```powershell
python -m pip install -e ".[dev]"
```

## Uruchamianie testów

Aby uruchomić testy jednostkowe, wykonaj polecenie:

```powershell
python -m pytest
```

## Przykład użycia

```python
from pyflow import Task, Workflow, topological_order, execution_layers


def przykladowa_funkcja(inputs, params):
    return None


workflow = Workflow()

workflow.add_task(
    Task(name="extract", function=przykladowa_funkcja)
)

workflow.add_task(
    Task(
        name="clean",
        function=przykladowa_funkcja,
        dependencies=frozenset({"extract"}),
    )
)

workflow.add_task(
    Task(
        name="report",
        function=przykladowa_funkcja,
        dependencies=frozenset({"clean"}),
    )
)

print(topological_order(workflow))
# ['extract', 'clean', 'report']

print(execution_layers(workflow))
# [['extract'], ['clean'], ['report']]
```

## Zastosowane algorytmy

Do wyznaczania kolejności topologicznej zastosowano wariant algorytmu Kahna. Algorytm wybiera zadania, których zależności zostały już przetworzone. Kolejność alfabetyczna zapewnia deterministyczny wynik.

Funkcja `execution_layers()` grupuje zadania, których zależności zostały spełnione w poprzednich warstwach. Zadania znajdujące się w tej samej warstwie mogą być rozważane do równoległego wykonania.

W obecnej implementacji złożoność czasowa obu algorytmów w najgorszym przypadku wynosi **O(V² + E)**, gdzie V oznacza liczbę zadań, a E liczbę zależności między zadaniami.

## Struktura projektu

```text
pyflow/
├── pyproject.toml
├── README.md
├── .gitignore
├── src/
│   └── pyflow/
│       ├── __init__.py
│       ├── models.py
│       └── graph.py
└── tests/
    ├── test_models.py
    └── test_graph.py
```
