from sklearn.tree import DecisionTreeRegressor

class RegressionTree:
    def __init__(self,
                 max_depth,
                 features=None):
        self.max_depth = max_depth
        self.features = features
        self.__model = DecisionTreeRegressor(max_depth=self.max_depth)

    def fit(self, x_train, y_train):
        _x_train = x_train.filter(self.features) if self.features is not None else x_train
        self.__model.fit(_x_train, y_train)

    def __call__(self, x_test, *args, **kwargs):
        _x_test = x_test.filter(self.features) if self.features is not None else x_test
        return self.__model.predict(_x_test)

