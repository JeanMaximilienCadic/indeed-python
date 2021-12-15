from argparse import ArgumentParser
from indeed.functional import load_data, random_train_features
from indeed import cfg
from indeed.models import RegressionTree
from sklearn.metrics import r2_score
import random
from gnutools.grid import Grid


def main(x_train, x_test, y_train, y_test, max_depth, features, **conn):
    model = RegressionTree(max_depth=max_depth, features=features)
    model.fit(x_train, y_train)
    conn.update({
        "score": r2_score(y_test, model(x_test)),
        "model": model
    })
    return conn


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--input_csv", default=cfg.etl.output_csv)
    args = parser.parse_args()
    grid = Grid()

    # Load the data
    x_train, x_test, y_train, y_test = load_data(input_csv=args.input_csv, test_size=.1)
    grid.setup(
        config={
            "max_depth"    : random.sample(list(range(1, 101)), 100),
            "features"     : list([random_train_features() for _ in range(10)])
        },
    )
    analysis = grid.run(
        main,
        config = {
            "x_train"       : x_train,
            "x_test"        : x_test,
            "y_train"       : y_train,
            "y_test"        : y_test,
        },
        columns=["max_depth", "features"],
        limit=5,
    )
    print(analysis)
