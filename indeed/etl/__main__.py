import os.path
from argparse import ArgumentParser
from indeed.functional import normalize_features
import pandas as pd
from indeed import cfg

def merge_data(xtrain_csv, xtest_csv, ytrain_csv, bronze_csv):
    try:
        assert os.path.exists(bronze_csv)
    except:
        xtrain_df, xtest_df = pd.read_csv(xtrain_csv), pd.read_csv(xtest_csv)
        ytrain_df = pd.read_csv(ytrain_csv)
        xtrain_df.set_index('jobId')
        xtest_df.set_index('jobId')
        ytrain_df.set_index('jobId')

        xtrain_df = xtrain_df.merge(ytrain_df)
        xtest_df[cfg.features.y] = None

        xdf = pd.concat((xtrain_df, xtest_df))
        xdf.to_csv(bronze_csv, index=False)
    finally:
        pd.read_csv(bronze_csv)


def normalize_salaries(df):
    mu, std = cfg.etl.y.mu,cfg.etl.y.std
    df = (df-mu)/std
    return df

def etl(
        bronze_csv,
        gold_csv,
    ):
    try:
        assert os.path.exists(gold_csv)
    except AssertionError:
        features = cfg.features.cat + cfg.features.num
        data = pd.read_csv(bronze_csv)
        data[cfg.features.y] = normalize_salaries(data[cfg.features.y])
        data[features] = normalize_features(data.filter(features))
        data.to_csv(gold_csv, index=False)
    finally:
        pd.read_csv(gold_csv)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--xtrain_csv",
                        default=cfg.etl.xtrain_csv)
    parser.add_argument("--xtest_csv",
                        default=cfg.etl.xtest_csv)
    parser.add_argument("--ytrain_csv",
                        default=cfg.etl.ytrain_csv)
    parser.add_argument("--bronze_csv",
                        default=cfg.etl.bronze_csv)
    parser.add_argument("--gold_csv",
                        default=cfg.etl.gold_csv)

    args = parser.parse_args()

    merge_data(args.xtrain_csv,
               args.xtest_csv,
               args.ytrain_csv,
               args.bronze_csv)
    etl(args.bronze_csv,
        args.gold_csv,
        )