from argparse import ArgumentParser
from indeed.functional import load_data, random_train_features, save_best_model, split_data, denormalize
from indeed import cfg
from indeed.models import RegressionTree
from sklearn.metrics import r2_score, mean_squared_error
import random
from gnutools.grid import Grid


def main(x_train, x_test, y_train, y_test, max_depth, features, metric, **conn):
    model = RegressionTree(max_depth=max_depth, features=features)
    model.fit(x_train, y_train)
    conn.update({
        "score": metric(denormalize(y_test), denormalize(model(x_test))),
        "model": model
    })
    return conn


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--input_csv", default=cfg.etl.gold_csv)
    parser.add_argument("--model_path", default=cfg.model_path)
    args = parser.parse_args()
    grid = Grid()
    metric = r2_score
    ascending = metric == mean_squared_error

    # Load the data
    x_train, x_test, y_train, y_test = split_data(*load_data(input_csv=args.input_csv),
                                                  test_size=.3)
    grid.setup(
        config={
            "max_depth"    : random.sample(list(range(1, 101)), 50),
            "features"     : list([random_train_features() for _ in range(20)])
        },
    )
    analysis = grid.run(
        main,
        config = {
            "x_train"       : x_train,
            "x_test"        : x_test,
            "y_train"       : y_train,
            "y_test"        : y_test,
            "metric"        : metric
        },
        columns=["max_depth", "features"],
        limit=5,
        ascending=ascending
    )
    print(analysis)
    save_best_model(grid, args.model_path, ascending=ascending)