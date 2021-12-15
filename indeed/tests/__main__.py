import unittest
import pandas as pd
from indeed import cfg
import numpy as np


class IndeedTest(unittest.TestCase):
    def test_distrib_features(self):
        features = cfg.features.cat + cfg.features.num
        xdf = pd.read_csv(cfg.etl.xtrain_csv)
        xdf = xdf.filter(features)
        for c in  cfg.features.cat:
            xdf[c] = pd.factorize(xdf[c])[0]

        x_mu, x_std = list(vars(cfg.etl.x.mu).values()), \
                      list(vars(cfg.etl.x.std).values())
        self.assertTrue(np.array_equal(
            np.array(x_mu, dtype=int),
            np.array(xdf.mean().to_numpy(), dtype=int)
        ))
        self.assertTrue(np.array_equal(
            np.array(x_std, dtype=int),
            np.array(xdf.std().to_numpy(), dtype=int)
        ))

    def test_distrib_salaries(self):
        features = cfg.features.y
        ydf = pd.read_csv(cfg.etl.ytrain_csv)
        ydf = ydf.filter(features)
        y_mu, y_std = int(cfg.etl.y.mu),  int(cfg.etl.y.std)
        self.assertEqual(int(y_mu), int(ydf.mean()))
        self.assertEqual(int(y_std), int(ydf.std()))



if __name__ == '__main__':
    unittest.main()
