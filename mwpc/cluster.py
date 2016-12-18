from __future__ import division
import sys

import numpy as np
#import root_numpy as rnp
from sklearn.cluster import DBSCAN

import ROOT

def get_hits(file_path):

    tree = ROOT.TChain('DataQuality/mwpc')
    tree.Add(file_path)

    number_entries = tree.GetEntries()

    number_hits = []
    tdc_number = []
    hit_channel = []
    hit_time_bin = []

    for entry in xrange(number_entries):

        tree.GetEntry(entry)

        number_hits.append(tree.number_hits)
        tdc_number.append(np.array(tree.tdc_number))
        hit_channel.append(np.array(tree.hit_channel))
        hit_time_bin.append(np.array(tree.hit_time_bin))

        #print np.array(tree.tdc_number), np.array(tree.tdc_number).shape

    number_hits = np.array(number_hits)
    tdc_number = np.array(tdc_number)
    hit_channel = np.array(hit_channel)
    hit_time_bin = np.array(hit_time_bin)

    #print number_hits.shape, tdc_number.shape, hit_channel.shape, hit_time_bin.shape
    #print number_hits.size, tdc_number.size, hit_channel.size, hit_time_bin.size
    #print number_hits
    #for i in xrange(16):
    #    print tdc_number[i].shape
    #    print tdc_number[i]
    ##print number_hits, tdc_number, hit_channel, hit_time_bin

    #branch_list = [
    #    #'spill',
    #    #'tdc_time_stamp',
    #    #'trigger_counter',
    #    'number_hits',
    #    'tdc_number',
    #    'hit_channel',
    #    'hit_time_bin',
    #    ]

    #arr = rnp.root2array(file_path, 'DataQuality/mwpc', branch_list)

    ##spill = arr['spill'].astype(np.int64)
    ##tdc_time_stamp = arr['tdc_time_stamp'].astype(np.int64) #/ 106.208  # microseconds
    ##trigger_counter = arr['trigger_counter']
    #number_hits = arr['number_hits']
    #tdc_number = arr['tdc_number']
    #hit_channel = arr['hit_channel']
    #hit_time_bin = arr['hit_time_bin']

    #print number_hits.shape, tdc_number.shape, hit_channel.shape, hit_time_bin.shape
    #print number_hits.size, tdc_number.size, hit_channel.size, hit_time_bin.size
    #print number_hits
    #for i in xrange(16):
    #    print tdc_number[i].shape
    #    print tdc_number[i]
    ##print number_hits, tdc_number, hit_channel, hit_time_bin

    #number_entries = arr.size
    number_tdcs = 16

    time_bin_scaling = 1.0 / 1280.0
    channel_scaling = 1.0 / 64.0
    dbscan = DBSCAN(eps=4.0/64.0, min_samples=1)
    #colors = np.array([ x for x in 'bgrcmykbgrcmykbgrcmykbgrcmyk' ])
    #colors = np.hstack([colors] * 20)

    good_hit_array = [ [] for i in range(number_tdcs) ]
    bad_hit_array = [ [] for i in range(number_tdcs) ]

    for entry in xrange(number_entries):

        hit_time_buffer = [ [] for i in range(number_tdcs) ]
        hit_channel_buffer = [ [] for i in range(number_tdcs) ]

        for tdc_index in xrange(number_tdcs):
            flag = (tdc_number[entry] == tdc_index + 1)
            hit_time_buffer[tdc_index].extend(hit_time_bin[entry][flag])
            hit_channel_buffer[tdc_index].extend(hit_channel[entry][flag])

        for tdc_index in xrange(number_tdcs):

            data = np.array([
                    np.array(hit_channel_buffer[tdc_index]).astype(np.int64),
                    np.array(hit_time_buffer[tdc_index]).astype(np.int64)
                ]).T

            scaled_data = np.array([
                    np.array(hit_channel_buffer[tdc_index]).astype(np.int64) \
                    * channel_scaling,
                    np.array(hit_time_buffer[tdc_index]).astype(np.int64) \
                    * time_bin_scaling
                ]).T

            if len(scaled_data) != 0:
                dbscan.fit(scaled_data)
                if hasattr(dbscan, 'labels_'):
                    y_pred = dbscan.labels_.astype(np.int)
                else:
                    y_pred = dbscan.predict(scaled_data)

                #print '///////////////////////////////////////'
                cluster_indices = np.unique(y_pred)
                #print cluster_indices
                #print data.shape
                #print y_pred.shape
                #print y_pred
                for cluster_index in cluster_indices:
                    cluster = data[y_pred == cluster_index]
                    if len(cluster) > 10:
                        bad_hit_array[tdc_index].extend(cluster)
                        continue
                    # z is the earliest hit in the cluster
                    z = cluster[np.where(cluster[:, 1] == cluster[:, 1].min())]
                    if len(z) == 1:
                        good_hit_array[tdc_index].append(z[0])
                    else:
                        bad_hit_array[tdc_index].extend(cluster)
                        continue
                    #else:
                    #    mean_channel = np.mean(z[:, 0])

                    dtype = np.dtype((np.void, (cluster.shape[1] *
                                                cluster.dtype.itemsize)))
                    mask = np.in1d(cluster.view(dtype), z.view(dtype))
                    bad_hits = cluster[~mask]
                    bad_hit_array[tdc_index].extend(bad_hits)

                #print '///////////////////////////////////////'

    good_hit_array = np.array(
            [ np.array(hits) for hits in good_hit_array ]
        )
    bad_hit_array = np.array(
            [ np.array(hits) for hits in bad_hit_array ]
        )

    return good_hit_array, bad_hit_array

if __name__ == '__main__':

    import argparse

    import matplotlib.pyplot as plt
    from matplotlib.ticker import AutoMinorLocator, MultipleLocator

    parser = argparse.ArgumentParser(description="Plot from ROOT file.")
    parser.add_argument("file", type=str, help="path to ROOT file")
    args = parser.parse_args()
    file_path = args.file

    print "Plotting from {}".format(file_path)

    good_hit_array, bad_hit_array = get_hits(file_path)

    fig, (
            ( ax1,  ax2,  ax3,  ax4),
            ( ax5,  ax6,  ax7,  ax8),
            ( ax9, ax10, ax11, ax12),
            (ax13, ax14, ax15, ax16),
            ) = plt.subplots(nrows=4, ncols=4, sharex=True, sharey=True)

    fig.suptitle("Relative timing distributions of clusters of TDC hits")
    fig.text(0.5, 0.04, "TDC time tick", ha='center', va='center')
    fig.text(0.06, 0.5, "Entries per TDC time tick", ha='center', va='center',
             rotation='vertical')

    axes = (
        ax1, ax2, ax3, ax4,
        ax5, ax6, ax7, ax8,
        ax9, ax10, ax11, ax12,
        ax13, ax14, ax15, ax16
        )

    for i in xrange(len(axes)):

        good_hit_list = []
        bad_hit_list = []

        try:
            good_hit_list = good_hit_array[i][:, 1]
        except:
            good_hit_list = []

        try:
            bad_hit_list = bad_hit_array[i][:, 1]
        except:
            bad_hit_list = []

        n, bin_edges, patches = axes[i].hist(
            #[ good_hit_array[i][:, 1], bad_hit_array[i][:, 1] ],
            [ good_hit_list, bad_hit_list ],
            bins=1024, range=(0, 1024), ec='none', color=['g', 'y'],
            alpha=0.75, histtype='stepfilled', stacked=True
            )

        snr = len(good_hit_array[i]) / len(bad_hit_array[i])

        axes[i].text(0.95, 0.925, "TDC {}".format(i+1),
                     horizontalalignment='right',
                     verticalalignment='top',
                     transform=axes[i].transAxes)
        axes[i].text(0.95, 0.8, "SNR: {:.2f}".format(snr),
                     horizontalalignment='right',
                     verticalalignment='top',
                     transform=axes[i].transAxes)
        axes[i].xaxis.set_minor_locator(AutoMinorLocator())
        axes[i].yaxis.set_minor_locator(AutoMinorLocator())
        axes[i].tick_params(which='major', length=7)
        axes[i].tick_params(which='minor', length=4)
        axes[i].tick_params(axis='both', which='major', labelsize=10)
        #axes[i].set_xlim([0, 320])
        #axes[i].set_xlim([-0.5, 1023.5])
        axes[i].set_xlim([250, 450])
        #axes[i].set_xlim([0, 1024])
        #axes[i].set_ylim([0, 800])
        plt.setp(axes[i].get_xticklabels(), visible=True)
        plt.setp(axes[i].get_yticklabels(), visible=True)

    axes[0].set_ylim([0, axes[0].get_ylim()[1]])

    fig.text(0.95, 0.82, "MWPC 1", ha='center', va='center',
             fontsize=12)
    fig.text(0.95, 0.61, "MWPC 2", ha='center', va='center',
             fontsize=12)
    fig.text(0.95, 0.40, "MWPC 3", ha='center', va='center',
             fontsize=12)
    fig.text(0.95, 0.19, "MWPC 4", ha='center', va='center',
             fontsize=12)

    plt.show()
    plt.close()

    fig, (
            ( ax1,  ax2,  ax3,  ax4),
            ( ax5,  ax6,  ax7,  ax8),
            ( ax9, ax10, ax11, ax12),
            (ax13, ax14, ax15, ax16),
            ) = plt.subplots(nrows=4, ncols=4, sharex=True, sharey=True)

    fig.suptitle("Channel occupancy of clusters of TDC hits")
    fig.text(0.5, 0.04, "TDC channel", ha='center', va='center')
    fig.text(0.06, 0.5, "Entries per TDC channel", ha='center', va='center',
             rotation='vertical')

    axes = (
        ax1, ax2, ax3, ax4,
        ax5, ax6, ax7, ax8,
        ax9, ax10, ax11, ax12,
        ax13, ax14, ax15, ax16
        )

    for i in xrange(len(axes)):

        good_hit_list = []
        bad_hit_list = []

        try:
            good_hit_list = good_hit_array[i][:, 0]
        except:
            good_hit_list = []

        try:
            bad_hit_list = bad_hit_array[i][:, 0]
        except:
            bad_hit_list = []

        n, bin_edges, patches = axes[i].hist(
            #[ good_hit_array[i][:, 0], bad_hit_array[i][:, 0] ],
            [ good_hit_list, bad_hit_list ],
            bins=64, range=(0, 64), ec='none', color=['g', 'y'],
            alpha=0.75, histtype='stepfilled', stacked=True
            )

        snr = len(good_hit_array[i]) / len(bad_hit_array[i])

        axes[i].text(0.95, 0.925, "TDC {}".format(i+1),
                     horizontalalignment='right',
                     verticalalignment='top',
                     transform=axes[i].transAxes)
        axes[i].text(0.95, 0.8, "SNR: {:.2f}".format(snr),
                     horizontalalignment='right',
                     verticalalignment='top',
                     transform=axes[i].transAxes)
        axes[i].xaxis.set_minor_locator(AutoMinorLocator())
        axes[i].yaxis.set_minor_locator(AutoMinorLocator())
        axes[i].tick_params(which='major', length=7)
        axes[i].tick_params(which='minor', length=4)
        axes[i].tick_params(axis='both', which='major', labelsize=10)
        axes[i].set_xlim([0, 64])
        plt.setp(axes[i].get_xticklabels(), visible=True)
        plt.setp(axes[i].get_yticklabels(), visible=True)

    axes[0].set_ylim([0, axes[0].get_ylim()[1]])

    fig.text(0.95, 0.82, "MWPC 1", ha='center', va='center',
             fontsize=12)
    fig.text(0.95, 0.61, "MWPC 2", ha='center', va='center',
             fontsize=12)
    fig.text(0.95, 0.40, "MWPC 3", ha='center', va='center',
             fontsize=12)
    fig.text(0.95, 0.19, "MWPC 4", ha='center', va='center',
             fontsize=12)

    plt.show()
    plt.close()
