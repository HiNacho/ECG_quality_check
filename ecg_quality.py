import numpy as np
from scipy.signal import welch

def check_noise(sig, fs, noise_band=(40, 100), threshold=0.1):
    f, pxx = welch(sig, fs=fs)
    band_power = np.sum(pxx[(f >= noise_band[0]) & (f <= noise_band[1])])
    total_power = np.sum(pxx)
    ratio = band_power / total_power if total_power > 0 else 0
    return ratio < threshold, ratio

def check_baseline_wander(sig, fs, wander_band=(0.01, 0.5), threshold=0.2):
    f, pxx = welch(sig, fs=fs)
    wander_power = np.sum(pxx[(f >= wander_band[0]) & (f <= wander_band[1])])
    total_power = np.sum(pxx)
    ratio = wander_power / total_power if total_power > 0 else 0
    return ratio < threshold, ratio

def check_clipping(sig, clip_fraction=0.01, min_clip_len=10):
    min_val, max_val = np.min(sig), np.max(sig)
    min_clip = np.sum(sig == min_val)
    max_clip = np.sum(sig == max_val)
    clipped = (min_clip + max_clip) / len(sig)
    return clipped < clip_fraction, clipped

def check_lead_off(sig, var_threshold=1e-4):
    var = np.var(sig)
    return var > var_threshold, var

def check_amplitude(sig, min_amp=-5, max_amp=5):
    min_ok = np.min(sig) >= min_amp
    max_ok = np.max(sig) <= max_amp
    return min_ok and max_ok, (np.min(sig), np.max(sig))

def check_missing(sig):
    missing = np.isnan(sig).any()
    return not missing, missing

def assess_ecg_quality(sig, fs):
    results = {}
    results['noise_ok'], results['noise_ratio'] = check_noise(sig, fs)
    results['baseline_wander_ok'], results['wander_ratio'] = check_baseline_wander(sig, fs)
    results['clipping_ok'], results['clipped_fraction'] = check_clipping(sig)
    results['lead_off_ok'], results['variance'] = check_lead_off(sig)
    results['amplitude_ok'], results['amplitude_range'] = check_amplitude(sig)
    results['missing_ok'], results['missing'] = check_missing(sig)
    results['all_ok'] = all([
        results['noise_ok'],
        results['baseline_wander_ok'],
        results['clipping_ok'],
        results['lead_off_ok'],
        results['amplitude_ok'],
        results['missing_ok']
    ])
    return results
