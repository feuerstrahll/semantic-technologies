"""Run the Wikidata seminar notebook and save its outputs."""

from pathlib import Path

import nbformat
from nbclient import NotebookClient

from draw_geography_graph import draw_graph


folder = Path(__file__).resolve().parent
path = folder / "Семинар_5_Вариант_57.ipynb"
notebook = nbformat.read(path, as_version=4)
NotebookClient(
    notebook,
    timeout=1200,
    kernel_name="python3",
    resources={"metadata": {"path": str(folder)}},
).execute()
nbformat.write(notebook, path)
print(f"Executed: {path}")
image_path = folder / "results" / "graph_example.png"
draw_graph(folder / "results" / "geography57.ttl", image_path)
print(f"Graph image: {image_path}")
