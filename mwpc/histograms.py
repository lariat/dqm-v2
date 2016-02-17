import numpy as np

from classes import Histogram

def hits_histograms(hits_array, col, tdc_numbers, x_range):
    """ Returns a dictionary of MWPC TDC hits histograms. """
    histograms = {}
    number_bins = len(x_range)
    bin_width = x_range[1] - x_range[0]
    range_bins = (x_range[0], x_range[-1] + bin_width)
    name = { 0 : "channel", 1 : "timing" }
    for tdc in tdc_numbers:
        try:
            histogram_counts, histogram_bins = np.histogram(
                hits_array[tdc][:, col], bins=number_bins, range=range_bins)
            histogram_bins = histogram_bins[:-1]  # get rid of "overflow" bin
        except:
            histogram_counts = np.zeros(number_bins, dtype=np.int64)
            histogram_bins = np.arange(
                x_range[0], x_range[-1] + bin_width, bin_width)
        histograms[tdc] = Histogram("mwpc_tdc_{}_{}".format(tdc, name))
        histograms[tdc].histogram_to_db(
            histogram_bins, histogram_counts)
    return histograms
