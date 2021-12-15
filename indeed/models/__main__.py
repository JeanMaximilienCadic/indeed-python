from sklearn.metrics import r2_score
from argparse import ArgumentParser
from indeed import cfg
from indeed.functional import load_data
from indeed.models import RegressionTree
from matplotlib import pyplot as plt
import random

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--input_csv",
                        default=cfg.etl.output_csv)
    parser.add_argument("--max_depth",
                        default=cfg.models.regression_tree.max_depth)
    parser.add_argument("--best_features",
                        default=cfg.features.best)
    args = parser.parse_args()
    x_train, x_test, y_train, y_test = load_data(input_csv=args.input_csv,
                                                 test_size=.3)
    model = RegressionTree(max_depth=args.max_depth,
                           features=args.best_features)
    model.fit(x_train, y_train)
    _y_test = model(x_test)
    _y_test = (_y_test*cfg.etl.y.std)+cfg.etl.y.mu
    y_test = (y_test*cfg.etl.y.std)+cfg.etl.y.mu
    score = r2_score(y_test, _y_test)

    inds = random.sample(list(range(len(_y_test))), 100)
    plt.plot(y_test[inds])
    plt.plot(_y_test[inds])
    plt.title(f"r2: {score}")
    plt.show()