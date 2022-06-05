# -*- coding: utf-8 -*-
"""G_COLAB_dial_tone_decoder.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lKjl1XFY4u5asqMbojXltN-S62azMifv
"""

from google.colab import files

uploaded = files.upload()

from IPython.display import Audio
dial_up_internet = str(input("Enter the name of the audio file to decode: "))
display(Audio(dial_up_internet))

import librosa
fs_dial_up0, sample_rate = librosa.load(dial_up_internet)
print("MP3 from the Youtube")
print("sample_rate {}".format(sample_rate))
print("N of time points {}".format(len(fs_dial_up0)))
print("The length of time series {:3.2f} seconds".format(float(len(fs_dial_up0))/sample_rate))

import numpy as np
fs_dial_up = np.array(fs_dial_up0)[:int(6*sample_rate)]

import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning) 
Nxlim   = 10
ts_orig = np.arange(0,len(fs_dial_up),sample_rate)
ts_sec  = np.arange(0,len(ts_orig),1) 
plt.figure(figsize=(17,5))
plt.plot(fs_dial_up)
plt.xticks(ts_orig,ts_sec)
plt.xlabel("time (sec)")
plt.ylabel("Ampritude")
plt.title("The time domain plot")
plt.show()

fig = plt.figure(figsize=(17,5))
Pxx, freqs, bins, im = plt.specgram(fs_dial_up,
                                    Fs=sample_rate,
                                    NFFT=1000, noverlap=20)
plt.colorbar()
plt.xlabel("time (sec)")
plt.ylabel("Frequency (Hz)")
plt.title("Spectrogram")
plt.show()

# dual tone multi frequency (DTMF) signaling
DTFT_dials = np.array(
    [[697,1209], # 1
     [697,1336], # 2
     [697,1477], # 3
     [770,1209], # 4  
     [770,1336], # 5
     [770,1477], # 6
     [852,1209], # 7
     [852,1336], # 8 
     [852,1477], # 9
     [941,1209], # *
     [941,1336], # 0
     [941,1477]] # #
)
telephone_keypad = ["{}".format(i) for i in range(1,10)] + ["*","0","#"]

for t,hzs in zip(telephone_keypad,DTFT_dials):
    print("digit={:}: ({}Hz,{}Hz)".format(t,*hzs))


ifreqs, ibins = np.where(np.log10(Pxx )*10 > -50)
bins_tone = bins[ibins]
freqs_tone = freqs[ifreqs]
pick  = freqs_tone > 500
X = np.array([bins_tone[pick],
              freqs_tone[pick]]).T

## The extracted point data looks 
for icoord in range(X.shape[0]):
    print("Time ={:4.2f}sec, Frequency={:5.2f}Hz".format(*X[icoord,:]))


from sklearn.cluster import KMeans

Xcolstd = np.std(X,axis=0)
X_scale = X/Xcolstd

km = KMeans(n_clusters = 22)
km.fit(X_scale)


# rescale the cluster center
ccenter = km.cluster_centers_*Xcolstd
ccenter = np.array([np.round(ccenter[:,0],2),
                    np.round(ccenter[:,1],0)]).T
## reorder according to the time (sec)
ccenter = ccenter[np.argsort(ccenter[:,0]),:]
for icenter in range(ccenter.shape[0]):
    print("{:5.2f} sec {:7.0f}Hz".format(ccenter[icenter][0],
                                         ccenter[icenter][1]))


ccenter_xy0 = np.array([ccenter[1::2,1],
                       ccenter[::2,1]]).T

ccenter_xy = []
for icenter in range(ccenter_xy0.shape[0]):
    ccenter_xy.append(np.sort(ccenter_xy0[icenter]))
ccenter_xy = np.array(ccenter_xy)
ccenter_xy

def distDTFT(DTFT_dials, cent):
    return(np.sum((DTFT_dials - cent )**2,axis=1))
    
freq = []
for icenter in range(ccenter_xy.shape[0]):
    cent = ccenter_xy[icenter]
    dist2center = distDTFT(DTFT_dials, cent)
    i = np.argmin(dist2center)
    freq.append(telephone_keypad[i])
    
for i, f in enumerate(freq,1):
    print("{:02} dial pad button= {}".format(i,f))