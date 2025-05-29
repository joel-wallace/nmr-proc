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
