from indeed.models import RegressionTree
from indeed.functional import load_data
from indeed import cfg
from argparse import ArgumentParser
from sklearn.metrics import r2_score


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--input_csv", default=cfg.etl.output_csv)
    parser.add_argument("--max_depth", default=cfg.models.regression_tree.max_depth)
    args = parser.parse_args()
    x_train, x_test, y_train, y_test = load_data(input_csv=args.input_csv)
    model = RegressionTree(max_depth=args.max_depth)
    model.fit(x_train, y_train)
    _y_test = model(x_test)
    score = r2_score(y_test, _y_test)
    print(score)
