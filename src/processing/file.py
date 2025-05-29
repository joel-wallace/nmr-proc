import nmrglue as ng

def process_1h_spectrum(base_path: str, experiment_number: str, p0=0, offset=0.0):
    h_path = f"{base_path}/{experiment_number}"
    
    dic, data = ng.bruker.read(h_path)
    data = ng.bruker.remove_digital_filter(dic, data)

    data = ng.proc_base.zf_size(data, 32768)
    data = ng.proc_base.fft(data)
    data = ng.proc_base.ps(data, p0=p0)
    data = ng.proc_base.di(data)
    # data = ng.proc_bl.baseline_corrector(data)
    data = ng.proc_base.rev(data)

    udic = ng.bruker.guess_udic(dic, data)
    uc = ng.fileiobase.uc_from_udic(udic)
    ppm_scale = uc.ppm_scale() - offset

    return ppm_scale, data

def baseline_1h_spectrum(data):
    return ng.proc_bl.baseline_corrector(data)

def process_sum_19f_spectra(base_path: str, exp1: str, exp2: str, offset=0.0):
    summed_data = None
    ppm_scale = None
    for exp in range(int(exp1), int(exp2) + 1):
        dic, data = ng.bruker.read_pdata(base_path + "/" + str(exp) + "/pdata/1")

        if summed_data is None:
            summed_data = data
        else: summed_data += data
        
        if ppm_scale is None:
            udic = ng.bruker.guess_udic(dic, data)
            uc = ng.fileiobase.uc_from_udic(udic)
            ppm_scale = uc.ppm_scale() - offset

    return ppm_scale, summed_data
