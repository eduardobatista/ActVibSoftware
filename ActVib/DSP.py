import numpy as np

def easyFourier(x: np.ndarray, fs: float = 1.0):
  """
    Evaluate the magnitude Fourier spectrum in dB using the FFT.
    Parameters:
      x: vector containing the signal in time.
      fs: the sampling frequency. 
    Returns: (magdb,freqvec)
      magdb: vector containing the magnitude samples of the fft (dB).
      freqs: vector containing the frequency values (Hz).
  """
  nsamples = x.shape[0]
  magdb = 20*np.log10( 2*np.abs(np.fft.fft(x)/nsamples)[0:int(np.floor(nsamples/2))] )
  freqs = (np.fft.fftfreq(nsamples) * fs)[0:magdb.shape[0]]
  return magdb,freqs

class FIRNLMS:    

    def __init__(self,memorysize=100,stepsize=0.1,regularization=1e-6,wwavgwindow=None):
        """
            Parameters:
                memorysize, stepsize and regularization
        """
        self.N = memorysize
        self.mu = stepsize
        self.psi = regularization
        self.finished = False
        self.ww = None
        self.wwavgwindow = wwavgwindow
        self.wwavg = None

    def run(self,insignal,outsignal,maxiter=None):
        if not maxiter:
            rangesim = insignal.shape[0]
        else: 
            rangesim = min(insignal.shape[0],maxiter)
        if insignal.shape[0] != outsignal.shape[0]:
            raise Exception("Input and output must be vectors with same length.")
        self.xx = np.zeros(self.N)
        self.ww = np.zeros(self.N)
        self.sqerror = np.zeros(rangesim)
        if self.wwavgwindow:
            self.wwavg = np.zeros(self.N)
            for n in range(rangesim):
                self.xx[1:] = self.xx[0:-1]
                self.xx[0] = insignal[n]
                y = self.xx @ self.ww
                e = outsignal[n] - y
                self.ww = self.ww + self.mu * e * self.xx / (self.xx @ self.xx + self.psi)
                self.sqerror[n] = e**2
                if n >= (rangesim-self.wwavgwindow):
                  self.wwavg += self.ww
            self.wwavg = self.wwavg / self.wwavgwindow
        else:
            for n in range(rangesim):
                self.xx[1:] = self.xx[0:-1]
                self.xx[0] = insignal[n]
                y = self.xx @ self.ww
                e = outsignal[n] - y
                self.ww = self.ww + self.mu * e * self.xx / (self.xx @ self.xx + self.psi)
                self.sqerror[n] = e**2
        self.finished = True

