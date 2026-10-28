# Semantic Technologies — seminar materials

This repository contains seminar notebooks and supporting files for a university course on Semantic Technologies. The notebooks and coursework artifacts are in Russian; this index is in English.

## Contents

| Topic | Seminar materials | Supporting files |
| --- | --- | --- |
| [1. Knowledge graphs and RDF](topic-01/) | [RDF and Turtle](<topic-01/! Тема_1_Семинар_1_Семантические_сети_RDF_Turtle_final (1).ipynb>); [RDF stores and SPARQL](<topic-01/Тема_1_Семинар_2_RDF_хранилища_SPARQL_final (1).ipynb>) | `university.ttl` is created in seminar 1 and reused in seminar 2. |
| [2. Ontologies and linked data](topic-02/) | [Public vocabularies and a conceptual model](<topic-02/Тема_2_Семинар_1_Публичные_словари_и_концептуальная_модель_.ipynb>); [RDFS, OWL, SHACL, and Linked Data](<topic-02/Тема_2_Семинар_2_RDFS_OWL_SHACL_Linked_Data_.ipynb>) | `ontology_draft.ttl` flows into `ontology.ttl`, `data.ttl`, and `shapes.ttl`. The `example_university_*.ttl` files are a separate worked example. [HTML preview](topic-02/variant57_preview.html). |
| [3. Large knowledge bases and SPARQL](topic-03/) | [Wikidata](<topic-03/! Тема_3_Семинар_1_Wikidata_.ipynb>); [SPARQL](<topic-03/Тема_3_Семинар_2_SPARQL_.ipynb>) | The notebooks create their own local demonstration files when run. |
| [4. Knowledge bases](topic-04/) | [Knowledge-base workflow](<topic-04/! Тема_4_Базы_знаний_.ipynb>) | `Исходные_данные.7z` contains source inputs. The notebook creates `theme4_seminar1/` with run outputs. |
| [5. Wikidata geography, variant 57](topic-05/) | [Geography and borders notebook](<topic-05/Семинар_5_Вариант_57.ipynb>) | [Topic guide](topic-05/README.md), [original Russian guide](topic-05/GUIDE_RU.md), [report](topic-05/REPORT.md), [sources](topic-05/SOURCES.md), scripts, and saved results. |

## Working with the notebooks

Open each notebook from its **topic directory** and use that directory as the working directory. Several cells refer to Turtle files by relative name, and the topic 5 notebook writes to `results/` under the current directory. Run the notebooks in seminar order within each topic when you want to reproduce the handoff between lessons.

The notebooks use Python and Jupyter. Install the packages required by the notebook you run; common packages include `rdflib`, `pandas`, `requests`, and `matplotlib`. Some examples also need `pyshacl`, `numpy`, `nbformat`, or `nbclient`. Topic 5 can be run from `topic-05/` with `python run_seminar.py`; it queries the live Wikidata SPARQL endpoint, so new results may differ from the saved snapshot. The saved files in `topic-05/results/` make that run inspectable without rerunning it.

## File conventions

- Original notebook content and coursework artifacts are preserved in Russian.
- Turtle files sit beside the notebooks that read them, so their relative paths remain valid.
- Generated Python caches and Jupyter checkpoints are excluded from Git.
