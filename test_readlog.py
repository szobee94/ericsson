import numpy as np
import argparse
import sys
import glob

import rflog


argparser = argparse.ArgumentParser()
argparser.add_argument('log_dir', type=str, help='directory of logged chest files')

args = argparser.parse_args()

files = [fn for fn in glob.glob(str(args.log_dir) + "/chest_*.log")]
files.sort()
print "files:", files

sum_samples, burst_len, n_ports, n_rxant, n_rs, pilots, rsrp, rf_times = rflog.load_files(files)

#np.set_printoptions(threshold=sys.maxsize)
#print np.reshape(rf_times,(len(rf_times),1))

print "sum_samples:", sum_samples, "burst_len:", burst_len
print "n_ports, n_rxant, n_rs", n_ports, n_rxant, n_rs
print "rf_times.shape:", rf_times.shape
print "rsrp.shape:", rsrp.shape
print "pilots.shape:", pilots.shape

