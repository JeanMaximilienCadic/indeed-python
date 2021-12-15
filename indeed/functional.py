import pandas as pd
from sklearn.model_selection import train_test_split
from indeed import cfg
import random


def load_data(input_csv,
              test_size=0.5,
              random_state=42,
              xfeatures=cfg.features.cat+cfg.features.num,
              yfeatures=cfg.features.y,
              ):
    data = pd.read_csv(input_csv)
    X, y = data.filter(xfeatures), data.filter(yfeatures)
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    return x_train, x_test, y_train.to_numpy().reshape(-1, ), y_test.to_numpy().reshape(-1, )


def random_train_features():
    features = cfg.features.cat +  cfg.features.num
    sample = sorted(random.sample(features, random.randint(1, len(features))))
    return sample
