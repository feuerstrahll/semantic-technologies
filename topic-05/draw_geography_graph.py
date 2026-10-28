"""Draw a readable RDF subgraph from run_seminar.py results.

Usage: python draw_geography_graph.py
The script reads results/geography57.ttl and writes results/graph_example.png.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch
from rdflib import Graph, Namespace


FOLDER = Path(__file__).resolve().parent
WD = Namespace("http://www.wikidata.org/entity/")
WDT = Namespace("http://www.wikidata.org/prop/direct/")
EX = Namespace("https://example.org/geography57/")

# Names are used only for display. Edges always come from the saved RDF graph.
NAMES = {
    "Q183": "Германия",
    "Q142": "Франция",
    "Q213": "Чехия",
    "Q29999": "Королевство\nНидерландов",
    "Q31": "Бельгия",
    "Q32": "Люксембург",
    "Q36": "Польша",
    "Q39": "Швейцария",
    "Q40": "Австрия",
    "Q756617": "Королевство\nДании",
    "Q64": "Берлин",
    "Q4916": "евро",
    "Q46": "Европа",
    "Q188": "немецкий язык",
}
RELATION_NAMES = {"P36": "столица", "P37": "официальный язык",
                  "P38": "валюта", "P30": "континент"}
SHARED_NAMES = {"sharesOfficialLanguageWith": "общий язык",
                "sharesCurrencyWith": "общая валюта"}
KIND_COLORS = {"land": "#40698b", "water": "#168090",
               "land+water": "#7653a3", "point": "#bd6c30",
               "unknown": "#9ba4ad"}


def qid(uri: object) -> str:
    return str(uri).rsplit("/", 1)[-1]


def label(entity: str) -> str:
    name = NAMES.get(entity)
    return f"{name}\n({entity})" if name else entity


def node(ax, x: float, y: float, entity: str, color: str) -> None:
    ax.text(
        x, y, label(entity), ha="center", va="center", fontsize=10,
        bbox={"boxstyle": "round,pad=0.45", "facecolor": color,
              "edgecolor": "#354656", "linewidth": 1.1},
        zorder=3,
    )


def edge(ax, start, end, *, bidirectional=False, color="#527494") -> None:
    dx, dy = end[0] - start[0], end[1] - start[1]
    length = math.hypot(dx, dy)
    if length == 0:
        return
    ux, uy = dx / length, dy / length
    margin = 0.50
    arrow = FancyArrowPatch(
        (start[0] + ux * margin, start[1] + uy * margin),
        (end[0] - ux * margin, end[1] - uy * margin),
        arrowstyle="<->" if bidirectional else "-|>",
        mutation_scale=13, linewidth=1.5, color=color, zorder=1,
    )
    ax.add_patch(arrow)


def draw_graph(source: Path, output: Path, center: str = "Q183",
               max_neighbors: int = 9) -> tuple[int, int]:
    graph = Graph().parse(str(source), format="turtle")
    subject = WD[center]
    neighbors = sorted({qid(x) for x in graph.objects(subject, WDT.P47)})
    if not neighbors:
        raise ValueError(f"No P47 neighbors for {center} in {source}")
    shown_neighbors = neighbors[:max_neighbors]

    attributes = [
        (relation, qid(value))
        for relation in RELATION_NAMES
        for value in sorted(graph.objects(subject, WDT[relation]), key=str)
    ]
    shared = {}
    for relation in SHARED_NAMES:
        for target in graph.objects(subject, EX[relation]):
            target_id = qid(target)
            if target_id == center:
                continue
            shared.setdefault(target_id, {})[relation] = True
    # Prefer countries that also appear in the border panel and share both properties.
    shared_targets = sorted(
        shared, key=lambda item: (-len(shared[item]), item not in shown_neighbors, item)
    )[:5]

    plt.rcParams["font.family"] = "DejaVu Sans"
    fig, (left, middle, right) = plt.subplots(
        1, 3, figsize=(22, 8), gridspec_kw={"width_ratios": [1.3, 0.85, 1]},
    )
    fig.patch.set_facecolor("white")

    # Left panel: P47 was symmetrized when the RDF graph was built.
    radius = 2.55
    for index, neighbor in enumerate(shown_neighbors):
        angle = 2 * math.pi * index / len(shown_neighbors) + math.pi / 2
        position = (radius * math.cos(angle), radius * math.sin(angle))
        target = WD[neighbor]
        land = (subject, EX.bordersByLand, target) in graph
        water = (subject, EX.bordersByWater, target) in graph
        point = (subject, EX.bordersAtPoint, target) in graph
        kind = ("land+water" if land and water else "land" if land else
                "water" if water else "point" if point else "unknown")
        edge(left, (0, 0), position, bidirectional=True,
             color=KIND_COLORS[kind])
        pair_id = "border_" + "_".join(sorted((center, neighbor)))
        border_objects = sorted(qid(item) for item in graph.objects(EX[pair_id], EX.borderObject))
        if border_objects:
            object_label = border_objects[0]
            if len(border_objects) > 1:
                object_label += f" (+{len(border_objects) - 1})"
            left.text(position[0] * 0.51, position[1] * 0.51,
                      object_label,
                      ha="center", va="center", fontsize=7.3, color="#273847",
                      bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.8, "pad": 0.8},
                      zorder=2)
        node(left, *position, neighbor, "#e7eef6")
    node(left, 0, 0, center, "#b9d7ef")
    left.set_title(f"P47: соседство ({len(shown_neighbors)} из {len(neighbors)})",
                   fontsize=14, pad=14)
    left.set_xlim(-3.7, 3.7)
    left.set_ylim(-3.65, 3.65)
    left.set_aspect("equal")
    left.axis("off")

    # Middle panel: direct resource relations in the same saved RDF graph.
    positions = [(3.0, y) for y in
                 reversed([i * 1.65 - (len(attributes) - 1) * 0.825
                           for i in range(len(attributes))])]
    for (relation, target), position in zip(attributes, positions):
        edge(middle, (0, 0), position, color="#a76d38")
        node(middle, *position, target, "#f5e6d0")
        middle.text(1.5, position[1] / 2 + 0.18, RELATION_NAMES[relation],
                   ha="center", fontsize=9, color="#6f4a2a")
    node(middle, 0, 0, center, "#b9d7ef")
    middle.set_title("Свойства страны", fontsize=14, pad=14)
    middle.set_xlim(-1.2, 5.15)
    middle.set_ylim(-3.65, 3.65)
    middle.set_aspect("equal")
    middle.axis("off")

    # Right panel: derived country-to-country links, verified in the saved RDF.
    y_positions = [2.5 - i * 1.25 for i in range(len(shared_targets))]
    for target_id, y in zip(shared_targets, y_positions):
        kinds = shared[target_id]
        if "sharesOfficialLanguageWith" in kinds:
            edge(right, (0, 0.16), (3.2, y + 0.16), bidirectional=True,
                 color="#4b8a53")
        if "sharesCurrencyWith" in kinds:
            edge(right, (0, -0.16), (3.2, y - 0.16), bidirectional=True,
                 color="#b67734")
        node(right, 3.2, y, target_id, "#e8f1e4")
    node(right, 0, 0, center, "#b9d7ef")
    right.set_title("Страны с общим языком / валютой", fontsize=14, pad=14)
    right.set_xlim(-1.2, 5.1)
    right.set_ylim(-3.65, 3.65)
    right.set_aspect("equal")
    right.axis("off")

    fig.suptitle("Фрагмент RDF-графа из результатов семинара", fontsize=17)
    kind_names = {"land": "суша", "water": "вода", "land+water": "суша и вода",
                  "point": "точка", "unknown": "тип не указан"}
    handles = [Line2D([0], [0], color=KIND_COLORS[kind], lw=2,
                      label=kind_names[kind]) for kind in KIND_COLORS]
    handles += [Line2D([0], [0], color="#4b8a53", lw=2, label="общий официальный язык"),
                Line2D([0], [0], color="#b67734", lw=2, label="общая валюта")]
    fig.legend(handles=handles, loc="lower center", ncol=7,
               bbox_to_anchor=(0.5, 0.07), frameon=False, fontsize=9)
    fig.text(0.5, 0.025,
             "Подписи на границах — QID объекта P805; тип показан только при наличии свидетельства Wikidata.",
             ha="center", fontsize=9, color="#4e5964")
    fig.tight_layout(rect=(0, 0.12, 1, 0.94))
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=170, facecolor="white")
    plt.close(fig)
    return len(shown_neighbors), len(attributes)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=FOLDER / "results/geography57.ttl")
    parser.add_argument("--output", type=Path, default=FOLDER / "results/graph_example.png")
    parser.add_argument("--center", default="Q183", help="Wikidata QID")
    parser.add_argument("--max-neighbors", type=int, default=9)
    args = parser.parse_args()
    if args.max_neighbors < 1:
        parser.error("--max-neighbors must be positive")
    count, attribute_count = draw_graph(
        args.source, args.output, args.center, args.max_neighbors,
    )
    print(f"Saved {args.output} ({count} P47 neighbors, "
          f"{attribute_count} other links)")


if __name__ == "__main__":
    main()
