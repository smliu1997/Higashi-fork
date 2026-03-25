import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
sys.path.append(str(REPO_ROOT))

import matplotlib.pyplot as plt
import seaborn as sns
from umap import UMAP

from higashi.Higashi_wrapper import Higashi


def main():
    config = REPO_ROOT / "Higashi_tutorial_data" / "4DN_sciHi-C_Kim et al" / "config_4DN_Kim.JSON"
    output_dir = SCRIPT_DIR / "output-4DN_sci-Hi-C_Kim"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Initialize the Higashi instance.
    higashi_model = Higashi(str(config))

    # Data processing only needs to be run once for a fresh temp/output dir.
    higashi_model.process_data()
    higashi_model.prep_model()

    # Stage 1 training.
    higashi_model.train_for_embeddings()

    # Visualize embedding results.
    cell_embeddings = higashi_model.fetch_cell_embeddings()
    print(cell_embeddings.shape)

    vec = UMAP(n_components=2, n_neighbors=25, random_state=0).fit_transform(cell_embeddings)
    cell_type = higashi_model.label_info["cell type"]
    batch = higashi_model.label_info["batch"]

    fig = plt.figure(figsize=(14, 5))

    ax = plt.subplot(1, 2, 1)
    sns.scatterplot(
        x=vec[:, 0],
        y=vec[:, 1],
        hue=cell_type,
        ax=ax,
        s=5,
        alpha=0.8,
        linewidth=0,
        hue_order=["GM12878", "IMR90", "HFF", "HAP1", "H1Esc"],
    )
    handles, labels = ax.get_legend_handles_labels()
    labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
    ax.legend(handles=handles, labels=labels, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0, ncol=1)

    ax = plt.subplot(1, 2, 2)
    sns.scatterplot(
        x=vec[:, 0],
        y=vec[:, 1],
        hue=batch,
        ax=ax,
        s=5,
        alpha=0.8,
        linewidth=0,
    )
    handles, labels = ax.get_legend_handles_labels()
    labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
    ax.legend(handles=handles, labels=labels, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0, ncol=1)

    plt.tight_layout()
    fig_path = output_dir / "cell_embeddings_umap.png"
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    print(f"Saved figure to {fig_path.resolve()}")
    plt.show()


if __name__ == "__main__":
    main()
