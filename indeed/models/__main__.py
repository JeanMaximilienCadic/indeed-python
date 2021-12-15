import numpy as np
from sklearn.metrics import r2_score, mean_squared_error
from argparse import ArgumentParser
from indeed import cfg
from indeed.functional import load_data, split_data, denormalize
from indeed.models import RegressionTree
import random
import seaborn as sns
from matplotlib import pyplot as plt
import pandas as pd
import os
import pickle

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--input_csv",
                        default=cfg.etl.gold_csv)
    parser.add_argument("--max_depth",
                        default=cfg.models.regression_tree.max_depth)
    parser.add_argument("--best_features",
                        default=cfg.features.best)
    parser.add_argument("--model_path",
                        default=cfg.model_path)

    args = parser.parse_args()
    x_train, x_test, y_train, y_test = split_data(*load_data(input_csv=args.input_csv),
                                                  test_size=.3)
    if not os.path.exists(args.model_path):
        model = RegressionTree(max_depth=args.max_depth,
                               features=args.best_features)
        model.fit(x_train, y_train)
    else:
        model = pickle.load(open(args.model_path, "rb"))

    _y_test = model(x_test)
    score = mean_squared_error(denormalize(y_test), denormalize(_y_test))

    inds = random.sample(list(range(len(_y_test))), 100)
    _y_test = np.array([list(range(100)), _y_test[inds], ["pred"] * 100]).swapaxes(0, 1)
    y_test = np.array([list(range(100)), y_test[inds], ["gt"] * 100]).swapaxes(0, 1)

    data = pd.DataFrame.from_records(
        np.concatenate((_y_test, y_test)),
        columns=["x", "salary", "y"]
    )
    data["salary"] = data["salary"].astype(float)
    plot = sns.relplot(
        data=data,
        kind="line",
        x="x",
        y="salary",
        hue="y",
        height=9,
        aspect=16/9,
    )

    plot.set(xticklabels=[])
    plot.fig.suptitle(f"RMSE: {'{:.2f}'.format(score)} | 100 random points in dev ",
                     fontsize=20, fontdict={"weight": "bold"})
    plt.savefig("figure.png")

    plt.show()
