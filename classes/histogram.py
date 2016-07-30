import numpy as np

#import log

# PostgreSQL's int type's range is -2147483648 to +2147483647
max_int = 2147483647

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
        self.bin_indices = np.array([], dtype=np.int64)
        self.bin_indices_sparse = np.array([], dtype=np.int64)
        self.number_bins = 0

    def histogram_to_db(self, bins, counts):

        self.bins = bins
        self.counts = counts
        self.min_bin = bins[0]
        self.max_bin = bins[-1]
        self.bin_width = bins[1] - bins[0]
        self.counts_sparse = counts[counts != 0]
        self.number_bins = bins.size
        self.bin_indices = np.arange(bins.size, dtype=np.int64)
        self.bin_indices_sparse = self.bin_indices[counts != 0]
        self.counts_sparse[self.counts_sparse > max_int] = max_int

    def db_to_histogram(
            self, bin_indices_sparse, counts_sparse, bin_width, number_bins,
            min_bin, max_bin):

        self.counts_sparse = counts_sparse
        self.min_bin = min_bin
        self.max_bin = max_bin
        self.bin_width = bin_width
        self.number_bins = number_bins
        self.bin_indices_sparse = bin_indices_sparse

        self.bins = np.arange(min_bin, max_bin + bin_width, bin_width)
        self.bin_indices = np.arange(number_bins)

        bin_indices_zeros_ = np.setdiff1d(self.bin_indices, bin_indices_sparse)

        bin_indices_ = np.concatenate((bin_indices_sparse, bin_indices_zeros_))
        counts_ = np.concatenate(
            (counts_sparse, np.zeros(bin_indices_zeros_.size, dtype=np.int64)))

        self.counts = counts_[bin_indices_.argsort()]

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

    number_bins = x.size
    bin_indices_sparse = np.arange(x.size)[y != 0]

    h1 = Histogram('h1')
    h1.histogram_to_db(x, y)

    h2 = Histogram('h2')
    h2.db_to_histogram(bin_indices_sparse, y_sparse, x[1]-x[0], number_bins,
                       x[0], x[-1])

    h3 = Histogram('h3')
    h3.histogram_to_db(x, z)

    h4 = h1 + h3
    h5 = h1 + h2 + h3 + h4

    h6 = h1
    h6 += h3

    print
    print x
    print y
    print
    print x_sparse
    print y_sparse

    print
    print h1.bins
    print h1.counts
    print h1.bin_indices
    print
    print h1.bin_indices_sparse
    print h1.counts_sparse
    print h1.bin_indices_sparse

    print
    print h2.bins
    print h2.counts
    print h2.bin_indices
    print
    print h2.counts_sparse
    print h2.bin_indices_sparse

    print
    print h3.bins
    print h3.counts
    print h3.bin_indices
    print
    print h3.counts_sparse
    print h3.bin_indices_sparse

    print
    print h4.bins
    print h4.counts
    print h4.bin_indices
    print
    print h4.counts_sparse
    print h4.bin_indices_sparse

    print
    print h5.bins
    print h5.counts
    print h5.bin_indices
    print
    print h5.counts_sparse
    print h5.bin_indices_sparse

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

    print
    print h1.counts, "+"
    print h3.counts, "="
    print h6.counts

