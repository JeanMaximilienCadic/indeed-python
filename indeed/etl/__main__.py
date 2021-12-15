import os.path

import pandas as pd
from indeed import cfg
from argparse import ArgumentParser

def etl(
        xtrain_csv,
        ytrain_csv,
        output_csv,
        cat_feat,
        num_feat,
        y_feat,
        x_mu,
        x_std,
        y_mu,
        y_std
    ):
    try:
        assert os.path.exists(output_csv)
    except AssertionError:
        features = cat_feat + num_feat

        # Normalize X
        xdf = pd.read_csv(xtrain_csv)
        xdf = xdf.filter(features)
        for c in cat_feat:
            xdf[c] = pd.factorize(xdf[c])[0]

        x_mu, x_std = list(vars(x_mu).values()), \
                      list(vars(x_std).values())
        xdf=(xdf-x_mu)/x_std

        # Normalize Y
        ydf = pd.read_csv(ytrain_csv)
        ydf = ydf.filter(y_feat)
        ydf=(ydf-y_mu)/y_std

        # Concatenate
        xdf[y_feat] = ydf[y_feat]
        xdf.to_csv(output_csv, index=False)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--xtrain_csv",
                        default=cfg.etl.xtrain_csv)
    parser.add_argument("--ytrain_csv",
                        default=cfg.etl.ytrain_csv)
    parser.add_argument("--cat_feat",
                        default=cfg.features.cat)
    parser.add_argument("--num_feat",
                        default=cfg.features.num)
    parser.add_argument("--y_feat",
                        default=cfg.features.y)
    parser.add_argument("--x_mu",
                        default=cfg.etl.y.mu)
    parser.add_argument("--x_std",
                        default=cfg.etl.y.std)
    parser.add_argument("--y_mu",
                        default=cfg.etl.y.mu)
    parser.add_argument("--y_std",
                        default=cfg.etl.y.std)
    parser.add_argument("--output_csv",
                        default=cfg.etl.output_csv)
    args = parser.parse_args()

    etl(**vars(args))