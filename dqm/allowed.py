import itertools

#/////////////////////////////////////////////////////////////
# iterators for CAEN boards and channels
#/////////////////////////////////////////////////////////////
v1740_boards = range(0, 7+1)
v1751_boards = range(8, 10+1)
v1740b_boards = range(24, 24+1)
v1742_boards = range(11, 11+1)
#caen_boards = list(itertools.chain(v1740_boards, v1751_boards, v1740b_boards, v1742_boards))
caen_boards = list(itertools.chain(v1740_boards, v1751_boards, v1740b_boards))
caen_boards_a = list(itertools.chain(v1742_boards))
non_tpc_caen_boards = sorted(list(set(caen_boards) - set(v1740_boards[:-1])))

v1740_channels = range(64)
v1751_channels = range(8)
v1740b_channels = range(64)
v1742_channels = range(32)

tpc_channels = range(480)

#/////////////////////////////////////////////////////////////
# iterators for MWC TDCs
#/////////////////////////////////////////////////////////////
mwc_tdc_numbers = range(1, 16+1)
mwc_tdc_channels = range(64)
mwc_tdc_clock_ticks = range(1024)
 
