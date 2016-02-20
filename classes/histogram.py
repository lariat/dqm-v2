import numpy as np

#import log

class Histogram:
    """ Histogram. """

    def __init__(self, name):

        self.name = name

        self.bins = np.array([])
        self.couts = np.array([])
        self.min_bin = 0
        self.max_bin = 0
        self.bin_width = 0
        self.counts_sparse = np.array([], dtype=np.int64)
        self.bins_sparse = np.array([])

    def histogram_to_db(self, bins, counts):

        self.bins = bins
        self.counts = counts
        self.min_bin = bins[0]
        self.max_bin = bins[-1]
        self.bin_width = bins[1] - bins[0]
        self.bins_sparse = bins[counts != 0]
        self.counts_sparse = counts[counts != 0]

    def db_to_histogram(
        self, bins_sparse, counts_sparse, min_bin, max_bin, bin_width):

        self.bins_sparse = bins_sparse
        self.counts_sparse = counts_sparse
        self.min_bin = min_bin
        self.max_bin = max_bin
        self.bin_width = bin_width

        self.bins = np.arange(min_bin, max_bin + bin_width, bin_width)

        bins_zeros_ = list(set(self.bins) - set(bins_sparse))

        bins_ = list(bins_sparse)
        bins_.extend(bins_zeros_)
        counts_ = list(counts_sparse)
        counts_.extend(np.zeros(len(bins_zeros_)))

        bins_counts_ = np.array(
            sorted(zip(bins_, counts_), key=lambda pair: pair[0]))

        self.counts = np.array(bins_counts_[:, 1], dtype=np.int64)

    def __add__(self, other):

        histogram = Histogram("NULL")

        if not isinstance(other, Histogram):
            print "Can only add Histogram with another Histogram."
            return histogram

        if ((self.bins != other.bins).all() or
            self.counts.shape != other.counts.shape):
            print "Mismatched binning!"
            return histogram

        counts = self.counts + other.counts
        bins = self.bins

        histogram.name = self.name + " + " + other.name
        histogram.histogram_to_db(bins, counts)

        return histogram

if __name__ == '__main__':

    x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    y = np.array([0, 1, 0, 3, 4, 4, 3, 2, 1, 0])
    z = np.roll(y, 2)

    x_sparse = x[y != 0]
    y_sparse = y[y != 0]

    h1 = Histogram('h1')
    h1.histogram_to_db(x, y)

    h2 = Histogram('h2')
    h2.db_to_histogram(x_sparse, y_sparse, x[0], x[-1], x[1]-x[0])

    h3 = Histogram('h3')
    h3.histogram_to_db(x, z)

    h4 = h1 + h3
    h5 = h1 + h2 + h3 + h4

    print
    print x
    print y
    print
    print x_sparse
    print y_sparse

    print
    print h1.bins
    print h1.counts
    print
    print h1.bins_sparse
    print h1.counts_sparse

    print
    print h2.bins
    print h2.counts
    print
    print h2.bins_sparse
    print h2.counts_sparse

    print
    print h3.bins
    print h3.counts
    print
    print h3.bins_sparse
    print h3.counts_sparse

    print
    print h4.bins
    print h4.counts
    print
    print h4.bins_sparse
    print h4.counts_sparse

    print
    print h5.bins
    print h5.counts
    print
    print h5.bins_sparse
    print h5.counts_sparse

    print
    print h1.counts, "+"
    print h3.counts, "="
    print h4.counts

    print
    print h1.counts, "+"
    print h2.counts, "+"
    print h3.counts, "+"
    print h4.counts, "="
    print h5.counts

