from math import floor, ceil, sqrt, gamma, pi
from statistics import mean, variance, stdev
from collections import namedtuple
from scipy.stats import t, norm

def line(m, b):
    def func(x):
        return m*x + b
    return func

class Model:
    def __init__(self, name, fn, **kwargs):
        self.name = name
        self.fn = fn
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)

class ModelWithConfidence(Model):
    def __init__(self, name, fn, error_est, **kwargs):
        super().__init__(name, fn, **kwargs)
        self.p = 0.95
        self.error_est = error_est

    def __call__(self, *args, **kwargs):
        center = super().__call__(*args, **kwargs)
        error = self.error_est(*args, p=self.p, **kwargs)
        return (center-error, center+error)

class Dataset:

    LinearRegressionResult = namedtuple("LinearRegressionResult", ["m", "b", "chi2", "r2", "stderr_m", "stderr_b"])

    def __init__(self, data: dict):
        self.models = {}
        self._data = data
        self.N = len(data)
        self.datapoints, self.weights, self.errors, self.variances = {}, {}, {}, {}
        for x, y in data.items():
            if isinstance(y, list):
                y_avg, y_err, y_var = mean(y), stdev(y), variance(y)
            else:
                y_avg, y_err, y_var = y, sqrt(y), abs(y)
            self.datapoints[x] = y_avg
            self.weights[x] = y_avg**2/y_var
            self.errors[x] = y_err
            self.variances[x] = y_var
        self._W = sum(self.weights.values())
        self.x_avg, self.y_avg = mean(self.xs), mean(self.ys)
        self.x_wavg = self._wavg(self.xs)
        self.y_wavg = self._wavg(self.ys)

    @property
    def xs(self):
        return self.datapoints.keys()

    @property
    def ys(self):
        return self.datapoints.values()

    def _wavg(self, it):
        return sum(self.weights[x]*z for x, z in zip(self.xs, it))/self._W

    def do_linear_regression(self, name="weighted_linear"):
        result = self._weighted_linear_regression()
        self.models[name] = ModelWithConfidence(
                name,
                line(result.m, result.b), 
                error_est=self._estimate_linear_error,
                **result._asdict()
            )

    def _weighted_linear_regression(self):
        wavg_dx2 = self._wavg((x - self.x_wavg)**2 for x in self.xs)
        wavg_dxdy = self._wavg((x - self.x_wavg)*(y - self.y_wavg) for x, y in self.datapoints.items())
        m = wavg_dxdy/wavg_dx2
        b = self.y_wavg - self.x_wavg*m
        cov_00 = (1.0 + self.x_wavg**2/wavg_dx2)/self._W
        cov_01 = -self.x_wavg/(self._W*wavg_dx2)
        cov_11 = 1.0/(self._W*wavg_dx2)
        chi2 = self._wavg((m*x + b - y)**2 for x, y in self.datapoints.items())
        return self.LinearRegressionResult(m=m, b=b, chi2=chi2, r2=None, stderr_m=sqrt(cov_11), stderr_b=sqrt(cov_00))


    def _estimate_linear_error(self, x, p=0.95):
        return norm.ppf(p)*sqrt((1.0/self._W) * self._wavg((y - self.y_wavg)**2 for y in self.ys) * \
                (x - self.x_avg)**2/self._wavg((z - self.x_wavg)**2 for z in self.xs))

    def terminal_plot(self, with_errors=True, xscale=1.0, yscale=1.0, bucket="average"):
        from os import get_terminal_size
        cols, rows = get_terminal_size()
        cols = ceil(yscale*cols)
        rows = ceil(xscale*rows)
        x_min, x_max = min(self.xs), max(self.xs)
        y_min, y_max = min(self.ys), max(self.ys)
        lmargin = max(len(str(x_min)), len(str(x_max)))
        bucket = ceil((x_max-x_min)/rows)
        if bucket > 1:
            lmargin += 2
        
        def num_to_numChars(axis, num):
            num = abs(num)
            if axis == "x":
                return floor((rows - 1)*(num - x_min)/(x_max - x_min))
            elif axis == "y":
                return floor((cols - lmargin - 3)*(num - y_min)/(y_max - y_min))

        xl, xr = x_min, x_min + bucket - 1

        for r in range(rows):
            xl += bucket
            if xl > x_max:
                break
            elif len([x for x in self.xs if xl <= x < xl + bucket]) == 0:
                line = "/"
            else:
                W_bucket = sum([self.weights[x] for x in self.xs if xl <= x < xl + bucket])
                y_bucket = sum(
                        [self.weights[x]*y for x, y in self.datapoints.items() if xl <= x < xl + bucket]
                    ) / W_bucket
                w_bucket = sum(
                        [self.weights[x]*self.weights[x] for x, e in self.errors.items() if xl <= x < xl + bucket]
                    ) / W_bucket
                y = num_to_numChars("y", y_bucket)
                e = num_to_numChars("y", y_bucket/sqrt(w_bucket))
                if e > 0 and with_errors:
                    pt = "<" + (e-1)*"-" + "*" + (e-1)*"-" + ">"
                    line = "." * (y - e - 1) + pt
                else:
                    line = "." * (y - 1) + "*"
            coord_label = str(xl + bucket//2)
            if bucket > 1:
                coord_label = "<" + coord_label + ">"
            print(f"{coord_label.rjust(lmargin)}|{line}")


