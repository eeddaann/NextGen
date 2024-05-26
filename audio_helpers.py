import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import numpy as np

import io
import urllib
import base64

def extract_peak_frequency(data, sampling_rate):
    fft_data = np.fft.fft(data)
    freqs = np.fft.fftfreq(len(data))
    
    peak_coefficient = np.argmax(np.abs(fft_data))
    peak_freq = freqs[peak_coefficient]
    
    return abs(peak_freq * sampling_rate)

def save_spectrogram(path):
    sample_rate, samples = wavfile.read(path)
    frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate, nperseg=2048)
    
    plt.pcolormesh(times, frequencies, spectrogram,vmax=500)
    plt.ylabel('Frequency [Hz]')
    plt.ylim(ymin=3)
    plt.xlabel('Time [sec]')
    plt.title("peak frequency found at %.3f[Hz]"%(extract_peak_frequency(samples, sample_rate)))
    plt.yscale('symlog')
    img = io.BytesIO()
    plt.savefig(img, format = 'png')
    img.seek(0)
    plot_data = urllib.parse.quote(base64.b64encode(img.read()).decode())
    return plot_data