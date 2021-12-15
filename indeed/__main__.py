from indeed.functional import denormalize
from indeed import cfg
from argparse import ArgumentParser
import pandas as pd
import pickle
import numpy as np
if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--input_csv", default=cfg.etl.gold_csv)
    parser.add_argument("--model_path", default=cfg.model_path)
    parser.add_argument("--output_csv", default=cfg.output_csv)
    parser.add_argument("--max_depth", default=cfg.models.regression_tree.max_depth)
    args = parser.parse_args()

    model = pickle.load(open(cfg.model_path, "rb"))
    test_df = pd.read_csv(args.input_csv)
    test_df = test_df[pd.isnull(test_df).salary]
    jobIds = test_df.jobId.to_numpy()
    test_df = test_df.filter(model.features)
    records = np.array([jobIds, denormalize(model(test_df))]).swapaxes(0, 1)
    df_result = pd.DataFrame.from_records(records, columns=["jobID", "salary"])
    print(df_result)
    df_result.to_csv(args.output_csv, index=False)