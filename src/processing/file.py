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

def baseline_19f_spectrum(ppm_scale, summed_data):
    import numpy as np

    # Baseline
    ppm_axis = ppm_scale[31000:35000]
    data_axis = summed_data[31000:35000]

    # Identify points outside the -60 to -65 ppm range for fitting
    mask = (ppm_axis < -60) & (ppm_axis > -65)  # Mask for exclusion

    # Baseline selection (only using points outside the exclusion zone)
    ppm_baseline = ppm_axis[~mask]
    data_baseline = data_axis[~mask]

    # Fit a polynomial (degree 3)
    degree = 4
    coeffs = np.polyfit(ppm_baseline, data_baseline, degree)

    # Evaluate baseline fit
    baseline_fit = np.polyval(coeffs, ppm_axis)

    # Apply baseline correction
    corrected_data = data_axis - baseline_fit

    return ppm_axis, corrected_data

def fit_lorentzian_curves(ppm_axis, corrected_data, num_peaks=1):
    from scipy.optimize import curve_fit
    import numpy as np
    def lorentzian(x, A, x0, gamma):
        return A * (gamma**2 / ((x - x0)**2 + gamma**2))

    # Select a region containing the peak (adjust if necessary)
    peak_mask = (ppm_axis > -65) & (ppm_axis < -58)  # Adjust range as needed
    ppm_peak = ppm_axis[peak_mask]
    data_peak = corrected_data[peak_mask]

    # Estimate initial parameters (A, x0, gamma)
    A_guess = max(data_peak)  # Peak height
    x0_guess = ppm_peak[np.argmax(data_peak)]  # Peak position
    gamma_guess = 0.2  # Approximate width, adjust as needed

    p0 = [A_guess, x0_guess, gamma_guess]

    # Perform curve fitting
    popt, _ = curve_fit(lorentzian, ppm_peak, data_peak, p0=p0)

    # Extract fitted parameters
    A_fit, x0_fit, gamma_fit = popt
    lorentzian_fit = lorentzian(ppm_peak, A_fit, x0_fit, gamma_fit)

    return ppm_peak, lorentzian_fit