"""Plot 2D projections of the saved country embeddings."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE


HIGHLIGHTS = {
    "Q183": "Германия",
    "Q142": "Франция",
    "Q30": "США",
    "Q148": "Китай",
    "Q155": "Бразилия",
    "Q17": "Япония",
    "Q408": "Австралия",
}
LABEL_OFFSETS = {"Q183": (4, -10), "Q142": (4, 8)}


def plot_embeddings(results_dir=None):
    """Save PCA and t-SNE views of countries for each embedding model."""
    results_dir = Path(results_dir or Path(__file__).resolve().parent / "results")
    with np.load(results_dir / "embeddings.npz") as saved:
        entities = saved["entities"].tolist()
        entity_id = {entity: i for i, entity in enumerate(entities)}
        vectors = {
            "Структурные прогулки + SVD": saved["walk_vectors"],
            "TransE": saved["transe_entities"],
            "DistMult": saved["distmult_entities"],
        }

    # P47 connects countries; other entity embeddings include capitals and attributes.
    splits = [pd.read_csv(results_dir / f"{name}.tsv", sep="\t")
              for name in ("train", "validation", "test")]
    triples = pd.concat(splits, ignore_index=True)
    countries = sorted(set(triples.loc[triples.relation == "P47", "head"])
                       | set(triples.loc[triples.relation == "P47", "tail"]))
    country_index = {country: i for i, country in enumerate(countries)}
    indices = np.array([entity_id[country] for country in countries])
    if len(indices) < 4:
        raise ValueError("Для t-SNE нужны хотя бы четыре страны")

    figure, axes = plt.subplots(3, 2, figsize=(15, 15), constrained_layout=True)
    for row, (model, all_vectors) in enumerate(vectors.items()):
        data = all_vectors[indices]
        pca = PCA(n_components=2).fit(data)
        projections = (
            ("PCA", pca.transform(data)),
            ("t-SNE", TSNE(n_components=2, perplexity=min(30, (len(data) - 1) / 3),
                          init="pca", learning_rate="auto", random_state=2083).fit_transform(data)),
        )
        for col, (method, points) in enumerate(projections):
            ax = axes[row, col]
            ax.scatter(points[:, 0], points[:, 1], s=18, alpha=0.55, color="#4682b4")
            for country, name in HIGHLIGHTS.items():
                if country in country_index:
                    i = country_index[country]
                    ax.scatter(*points[i], s=42, color="#d1495b", zorder=3)
                    ax.annotate(name, points[i], xytext=LABEL_OFFSETS.get(country, (4, 4)),
                                textcoords="offset points", fontsize=8)
            title = f"{model} — {method}"
            if method == "PCA":
                title += f" ({pca.explained_variance_ratio_.sum():.0%} дисперсии)"
            ax.set_title(title)
            ax.set_xlabel("Компонента 1" if method == "PCA" else "Координата 1")
            ax.set_ylabel("Компонента 2" if method == "PCA" else "Координата 2")
            ax.grid(alpha=0.15)

    figure.suptitle(f"Проекции эмбеддингов стран (n={len(countries)})", fontsize=16)
    destination = results_dir / "embedding_projection.png"
    figure.savefig(destination, dpi=160, bbox_inches="tight")
    plt.close(figure)
    return destination


if __name__ == "__main__":
    print(plot_embeddings())
