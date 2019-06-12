import numpy as np

def load_files(files):

    sum_samples = np.uint(0)
    n_ports = 0
    n_rs = 0
    n_rxant = 0

    for fname in files:
        with open(fname, "rb") as f:
            n_rs = np.frombuffer(f.read(4),'i')[0]
            print "Read in n_rs:", n_rs
            n_ports = np.frombuffer(f.read(4),'i')[0]
            print "Read in n_ports:", n_ports
            n_samples = np.frombuffer(f.read(8),dtype=np.uint)[0]
            print "Read in n_samples:", n_samples
            tti_period = np.frombuffer(f.read(8),dtype=np.uint)[0]
            print "Read in tti_period:", tti_period
            burst_len = np.frombuffer(f.read(8),dtype=np.uint)[0]
            print "Read in burst_len:", burst_len
            sum_samples += n_samples * burst_len
            ts_start = np.frombuffer(f.read(8),dtype=np.int)[0]
            print "Read in ts_start:", ts_start
            n_rxant = np.frombuffer(f.read(4),'i')[0]
            print "Read in n_rxant:", n_rxant

            f.close()

    print "sum_samples:", sum_samples, type(sum_samples)
    print "n_ports, n_rxant, n_rs:", n_ports, n_rxant, n_rs, type(n_ports), type(n_rs)
    pilot_est = np.zeros((sum_samples, n_ports*n_rs/2*n_rxant), dtype=np.complex64)
    rsrp = np.zeros((sum_samples, 4), dtype=np.float)
    times = np.zeros((sum_samples,), dtype=np.int64)
    
    s_idx = 0;
    for fname in files:
        with open(fname, "rb") as f:
            n_rs = np.frombuffer(f.read(4),'i')[0]
            n_ports = np.frombuffer(f.read(4),'i')[0]
            n_samples = np.frombuffer(f.read(8),dtype=np.uint)[0]
            tti_period = np.frombuffer(f.read(8),dtype=np.uint)[0]
            burst_len = np.frombuffer(f.read(8),dtype=np.uint)[0]
            ts_start = np.frombuffer(f.read(8),dtype=np.int)[0]
            n_rxant = np.frombuffer(f.read(4),'i')[0]

            n_items = 0
            while True:
                ts = np.frombuffer(f.read(8),dtype=np.int)[0]
                #chest_buff = f.read(8*n_ports*1200)
                pilot_buff = f.read(8*n_ports*n_rs/2*n_rxant)
                rsrp_buff = f.read(4*4)  # reading 4 float types
                if n_items < n_samples*burst_len and (len(pilot_buff) < 8*n_ports*n_rs/2*n_rxant or len(rsrp_buff) < 4*4):
                    print "Error: Cannot read required number of bytes", len(pilot_buff), len(rsrp_buff)
                    break

                times[s_idx] = ts
                pilot_est[s_idx,:] = np.expand_dims(np.squeeze(np.frombuffer(pilot_buff, dtype = np.dtype((np.complex64, n_ports*n_rs/2*n_rxant)))), axis=0)
                rsrp[s_idx,:] = np.expand_dims(np.squeeze(np.frombuffer(rsrp_buff, dtype = np.dtype((np.float32, 4)))), axis=0)

                n_items += 1
                s_idx += 1
                if s_idx >= sum_samples:
                    break
                if n_items >= n_samples*burst_len:
                    break

    return (sum_samples, burst_len, n_ports, n_rxant, n_rs, pilot_est, rsrp, times)
    
