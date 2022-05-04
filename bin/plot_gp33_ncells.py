"""Plots the number of cells for each TCR for GP33."""
import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tap import Tap


class Args(Tap):
    data_path: Path  # Path to CSV file containing processed TCR data for GP33.
    save_dir: Path  # Path to directory where plots of cell counts will be saved.

    def process_args(self) -> None:
        self.save_dir.mkdir(parents=True, exist_ok=True)


def plot_gp33_ncells(args: Args) -> None:
    """Plots the number of cells for each TCR for GP33."""
    # Load data
    data = pd.read_csv(args.data_path)

    # Sort data by nCells
    data.sort_values(by='nCells', inplace=True)

    # Plot TCR counts
    max_ncells = data['nCells'].max()
    ymax = max_ncells * 1.02

    for tetramer, color in [('TetNeg', 'blue'), ('TetMid', 'orange'), ('TetPos', 'red')]:
        tet_data = data[data['tetramer'] == tetramer]

        plt.clf()
        plt.scatter(np.arange(len(tet_data)), tet_data['nCells'], color=color, label=tetramer)
        plt.ylim(ymin=0, ymax=ymax)
        plt.xlabel('TCR Index')
        plt.ylabel('nCells')
        plt.title(f'Number of Cells for {tetramer} TCR Sequences')
        plt.legend()
        plt.savefig(args.save_dir / f'{tetramer}_nCells.pdf')


if __name__ == '__main__':
    plot_gp33_ncells(Args().parse_args())
