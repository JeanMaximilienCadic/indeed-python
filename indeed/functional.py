import pandas as pd
from sklearn.model_selection import train_test_split
from indeed import cfg
import random
import pickle

def load_data(input_csv,
              xfeatures=cfg.features.cat+cfg.features.num,
              yfeatures=cfg.features.y,
              strict=True):
    data = pd.read_csv(input_csv)
    data = data[~pd.isnull(data.salary)] if strict else data
    X, y = data.filter(xfeatures), data.filter(yfeatures)
    return X, y

def split_data(X,
               y,
               test_size=0.5,
               random_state=42,
              ):

    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    return x_train, x_test, y_train.to_numpy().reshape(-1, ), y_test.to_numpy().reshape(-1, )


def random_train_features():
    features = cfg.features.cat +  cfg.features.num
    sample = sorted(random.sample(features, random.randint(1, len(features))))
    return sample

def normalize_features(xdf):
    # Normalize X_Train
    cat_feat = cfg.features.cat
    x_mu = cfg.etl.x.mu
    x_std = cfg.etl.x.std
    for c in cat_feat:
        xdf[c] = pd.factorize(xdf[c])[0]

    x_mu, x_std = list(vars(x_mu).values()), \
                  list(vars(x_std).values())
    xdf=(xdf-x_mu)/x_std

    return xdf

def denormalize(y):
    y = (y * cfg.etl.y.std ) + cfg.etl.y.mu
    return y


def save_best_model(grid, output_path, ascending=True):
    table = [(v["score"], v["_result"]["model"]) for v in grid.results.values()]
    df = pd.DataFrame.from_records(table, columns=["score", "model"])
    model = df.sort_values(by="score", ascending=ascending).filter(["model"]).to_numpy()[0][0]
    pickle.dump(model, open(output_path, "wb"))