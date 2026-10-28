# Topic 5: Wikidata geography and borders (variant 57)

The [seminar notebook](<Семинар_5_Вариант_57.ipynb>) obtains country and border data from the Wikidata SPARQL endpoint. It builds an RDF graph, trains small knowledge graph embedding models, and saves queries, responses, metrics, plots, and tabular outputs in [`results/`](results/).

The included `countries.csv` and `borders.csv` are an archive of an earlier manually prepared sample. The current notebook does not read them.

## Run

From this directory, install the notebook's Python dependencies:

```bash
python -m pip install numpy pandas requests rdflib matplotlib notebook nbclient nbformat
```

Then run `python run_seminar.py` to execute the notebook and draw the graph. This needs access to `https://query.wikidata.org/sparql`. The saved results are a snapshot; a new Wikidata query can return different data.

You can redraw the graph from the saved Turtle file with `python draw_geography_graph.py`. The script reads `results/geography57.ttl` and writes `results/graph_example.png`. For a different central country, use an option such as `--center Q142`.

See the [report](REPORT.md) for the recorded outcomes and the [sources and assumptions](SOURCES.md) for data limitations. Both documents, the notebook, and the [original guide](GUIDE_RU.md) are in Russian.
