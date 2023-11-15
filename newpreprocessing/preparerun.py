import numpy as np
import glob
import casatasks
import multiprocessing as mp
import tqdm
import os

data_location = "/lustre/xhall/2023-08-19_24hour_run/"
log_location = "/lustre/xhall/logs/"
antenna = "79,150,201,224,229,215,221,242,246,272,294,299,332,334,33,34,37,38,41,42,44,92,51,21,190,154,56,29,28,222,126,127"

data_files = np.sort(glob.glob(data_location + "*.ms"))
bcal_file = "/fast/xhall/snapshots/ten_mintues/20230820_060021_73MHz.bcal"

def flagcal(file_name):
    #casatasks.casalog.filter("SEVERE")
    #log = os.path.join(log_location, file_name.split("/")[-1].split(".")[0] + ".log")
    #casatasks.casalog.setlogfile(log)
    casatasks.flagdata(str(file_name), antenna=antenna, datacolumn="all", flagbackup=False)
    casatasks.clearcal(str(file_name))
    casatasks.applycal(str(file_name), gaintable = bcal_file, flagbackup = False)
    casatasks.flagdata(str(file_name), mode = "rflag", antenna=antenna, datacolumn="CORRECTED", flagbackup=False)

if __name__ == '__main__':

    pool = mp.Pool(processes=80)
    r = pool.map_async(flagcal, data_files)
    r.wait()
    
    