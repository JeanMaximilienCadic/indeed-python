import unittest
import pandas as pd
from indeed import cfg
import numpy as np
from indeed.functional import  denormalize


class IndeedTest(unittest.TestCase):
    def test_that_it_is_possible_to_switch_between_bronze_and_gold(self):
        bronze_df = pd.read_csv(cfg.etl.bronze_csv).salary
        bronze_df = bronze_df[~pd.isnull(bronze_df)]
        gold_df = pd.read_csv(cfg.etl.gold_csv).salary
        gold_df = gold_df[~pd.isnull(gold_df)]
        _gold_df = denormalize(gold_df)
        u = int(np.linalg.norm(_gold_df.to_numpy()- bronze_df.to_numpy()))
        self.assertEqual(u, 0)

    def test_distrib_features_bronze(self):
        features = cfg.features.cat + cfg.features.num
        bronze_df = pd.read_csv(cfg.etl.bronze_csv)
        bronze_df = bronze_df.filter(features)
        for c in  cfg.features.cat:
            bronze_df[c] = pd.factorize(bronze_df[c])[0]

        x_mu, x_std = list(vars(cfg.etl.x.mu).values()), \
                      list(vars(cfg.etl.x.std).values())
        self.assertTrue(np.array_equal(
            np.array(x_mu, dtype=int),
            np.array(bronze_df.mean().to_numpy(), dtype=int)
        ))
        self.assertTrue(np.array_equal(
            np.array(x_std, dtype=int),
            np.array(bronze_df.std().to_numpy(), dtype=int)
        ))

    def test_distrib_features_gold(self):
        features = cfg.features.cat + cfg.features.num
        gold_df = pd.read_csv(cfg.etl.gold_csv)
        gold_df = gold_df.filter(features)
        self.assertTrue(
            {0},
            set(np.round(gold_df.mean().to_numpy(), 2))
        )
        self.assertTrue(np.array_equal(
            {1},
            set(np.round(gold_df.std().to_numpy(), 2))
        ))


if __name__ == '__main__':
    unittest.main()
