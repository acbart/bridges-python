import random
import time as time_


class SortingBenchmark:
    """
    @brief Benchmarks sorting algorithm

	Benchmarks sorting algorithms and add time series to a LineChart.

	The benchmark goes from an initial size controlled by
	setBaseSize() to a largest size controlled by setMaxSize(). One
	can also set a maximum time spent on a particular run using
	setTimeCap().

	The benchmark goes from a array size of n to the next one of
	geoBase  n + increment, where the base is controlled by
	geometric and increment is controlled by
	increment. For simpler use one can set a purley linear
	sampling with linear_range() or a purely geometric one with
	geometric_range().

	sorting algorithms can be passed to the run function for being benchmarked. A typical use would look something like

	\code{.py}
	def mysort(int array, int arraysize)
	lc = LineChart();
	sb SortingBenchmark(lc);
	sb.linear_range (100, 1000, 5);
	sb.run("mysortingalgorithm", mysort);
	\endcode

	@author Erik Saule
	@date 07/20/2019
    """
    def __init__(self, p):
        p.x_label = "Size of Array"
        p.y_label = "Runtime (in us)"
        self._plot = p
        self.r = random
        self._max_size = 1
        self._base_size = 1
        self._increment = 1
        self._geo_base = 1
        self._time_cap_ms = float('inf')
        self.debug = False

    @property
    def plot(self):
        return self._plot

    @plot.setter
    def plot(self, p):
        self._plot = p

    @property
    def max_size(self):
        return self._max_size

    @max_size.setter
    def max_size(self, size):
        self._max_size = size

    @property
    def base_size(self):
        return self._base_size

    @base_size.setter
    def base_size(self, size):
        self._base_size = size

    @property
    def increment(self):
        return self._increment

    @increment.setter
    def increment(self, inc):
        self._increment = inc

    @property
    def geometric(self):
        return self._geo_base

    @geometric.setter
    def geometric(self, base):
        self._geo_base = base

    @property
    def time_cap(self):
        return self._time_cap_ms

    @time_cap.setter
    def time_cap(self, cap_in_ms):
        self._time_cap_ms = cap_in_ms

    def linear_range(self, base_sz, max_sz, nb_point):
        self.base_size = base_sz
        self.max_size = max_sz
        self.increment = ((max_sz - base_sz) / nb_point)
        self.geometric = 1.0

    def geometric_range(self, base_sz, max_sz, base):
        self.base_size = base_sz
        self.max_size = max_sz
        self.increment = 0
        self.geometric = base
        if base <= 1.0:
            print("base should be > 1.0")

    def generate(self, arr, n):
        for i in range(0, n):
            arr.append(self.r.randint(0, 2*n))

    def check(self, arr, n):
        ok = True
        for i in range(1, n):
            if arr[i] < arr[i -1]:
                ok = False
                break
        return ok

    def run(self, algo_name, runnable):
        time = []
        x_data = []

        if self.debug:
            print(self.geometric)
            print(self.increment)

        n = self.base_size
        while n < self.max_size:
            arr = []
            self.generate(arr, int(n))

            start = int(round(time_.time() * 1000))
            runnable(arr)
            end = int(round(time_.time() * 1000))
            runtime = end - start

            if self.check(arr, int(n)) == False:
                print("Sorting algorithm " + algo_name + " is incorrect")

            time.append(float(runtime))
            x_data.append(float(n))

            if runtime > self.time_cap:
                break

            n = max(self.geometric * n + self.increment, n + 1)
        self.plot.set_x_data(algo_name, x_data)
        self.plot.set_y_data(algo_name, time)
