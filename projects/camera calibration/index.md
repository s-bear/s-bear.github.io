---
title: Camera Spectral Calibration
author: Samuel B Powell
#contact: samuel.powell@uq.edu.au
copyright: 2022, Samuel B Powell
#orphan: true
---

This document describes a rigorous approach to estimating the relative spectral sensitivities of a
digital camera. We show how to maintain a chain of calibration, from certified calibrated light
sources through to the digital camera, to ensure consistent results. The goal of this process is to
determine the relative spectral sensitivity of an image sensor or camera, which requires
illuminating the sensor with a wide variety of known spectral irradiances. One of the best
instruments for producing consistent and controllable narrow-band light is a monochromator, which
of course requires calibration itself. That is achieved by measuring its output spectral irradiance
with an optical spectrometer, which has itself been calibrated against known light sources—a gas
discharge lamp with well-defined emission lines at known wavelengths, and a deuterium-halogen lamp
with a known, broad-band spectral irradiance. See {numref}`chain-of-calibration`.

Such involved calibration is only necessary for unusually precise work, such as visual modelling.
For most purposes, a camera’s colour response can be calibrated by simply taking a photo of a
standardized colour chart (e.g., the X-Rite ColorChecker).

It is important to keep track of what precisely is being calibrated and to keep in mind the
precision of that calibration. This procedure only describes how to determine the relative spectral
sensitivity of a camera’s pixels—determining absolute sensitivities would require a more
sophisticated apparatus and significantly more care.

:::{figure} chain-of-calibration.svg
:name: chain-of-calibration
:alt: alt-text

The calibration chain starts with two already-calibrated lamps: a gas discharge lamp that produces
emission lines at known wavelengths and a broad-spectrum halogen lamp with a known spectral
irradiance. These are used to calibrate an optical spectrometer, which is used to calibrate a
monochromator, which is used to calibrate the camera.
:::

## Calibrating the spectrometer

Digital optical spectrometers, hereafter “spectrometers”, split incident light by wavelength across
an array of photodetectors (often a linear CCD). Each photodetector element serves as a bin,
counting the incident photons within a narrow wavelength band during the device’s integration time.
These devices require two stages of calibration: first, we must determine which wavelengths each
bin is capturing (i.e., wavelength calibration), and second, we must determine how the
photodetectors’ counts correspond to physical units(i.e., irradiance calibration). Wavelength
calibration is performed by measuring the output of a gas discharge lamp with well-known emission
lines, which are used to identify which wavelengths align with which bins. Once the wavelength
range of each bin is understood, we measure the output of a broad-spectrum lamp with known spectral
irradiance. We then compare our uncalibrated spectrometer’s measurement to the known spectrum and
determine a set of coefficients to map our measurement onto the true value.

In practice, these procedures tend to be included in a spectrometer’s operating software and are
straightforward to execute. A spectrometer’s wavelength alignment typically changes slowly, if at
all, and thus wavelength calibration only needs to be performed rarely. The device’s spectral
sensitivity depends on the spectral transmission of the light-collecting optics as well as the
photodetector array’s optoelectronic characteristics—which may depend on the electronic
configuration of the device as well as the ambient temperature. During field work we recalibrate
our spectrometers’ irradiance response daily, if not more often.

## Calibrating the monochromator

Once the spectrometer is calibrated, it is used to calibrate the monochromator. Monochromators are
essentially spectrometers in reverse: a broad-spectrum light source is split by wavelength, and a
system of rotating mirrors is used to focus a narrow band of wavelengths out of the device’s exit
slit and typically into a fibre optic. The calibration procedure is to set the nominal wavelength
of the monochromator to each wavelength of interest (e.g., we use every 5 nm from 300 nm to 800 nm)
and measure its output with the spectrometer. These measurements give us the actual peak wavelength
of each output, the bandwidth, and may reveal any sidebands or light leakage. One could use this
information to adjust the monochromator—correct any wavelength misalignments and adjust the light
intensity to emit a desired photon flux at each wavelength—but such is largely unnecessary here.
Digital cameras can tolerate a wide range of intensities by varying shutter speeds with no ill
effects on the calibration procedure. Minor deviations in peak wavelength are also
inconsequential.

Monochromators require regular recalibration as their lamps’ spectral irradiance change with age.
With use, metal from the lamp’s filament will slowly vaporize and deposit on the interior surface
of the glass bulb, changing its effective spectrum. LEDs also change spectrum with age, though due
to other mechanisms. We consider it best practice to recalibrate every 50 hours of use, following
the guidelines for recertification of officially certified calibrated lamps.

## Calibrating the camera

We are now ready to calibrate a camera! The camera is set to photograph the monochromator output,
preferably filling most of the frame. Because we are only calibrating the spectral response of the
camera, it does not matter if the image is in focus—it is perfectly acceptable to put the
monochromator’s output very close to the camera’s lens. It is also reasonable to calibrate a camera
with no lens—though this means that any lens’s spectral transmission will need to be measured
separately. The monochromator is set to each wavelength of interest in turn, and the camera is used
to photograph the output. For the best signal-to-noise ratio (SNR), we want the pixels to be
well-exposed, but none over-exposed. We target a peak at about 75% on the image histogram. The
camera should be set to record RAW images in fully manual mode, including shutter speed, aperture,
ISO sensitivity/gain, and white balance. While we could technically use automatic shutter speed or
automatic aperture modes, in our experience most cameras do not adjust well to a black frame with a
single pure colour dot—exposure bracketing is a more reliable way to ensure at least one good
exposure in this scenario.

Once all of the images are recorded, we begin the data processing. Each image is converted to a
standard format and cropped to show just the monochromator output. We select the highest SNR image
from each exposure bracket, normalize by the exposure time, and record its mean pixel value. We
analyse the entire spectral image stack to determine the fixed-pattern noise (e.g., dust or
hot/dead pixels) and subtract it to determine each image’s temporal noise component (read noise and
shot noise). We then use the samples along with the monochromator spectral data to infer the
camera’s spectral sensitivities as a linear regression problem, described in detail below.

## Software

TODO

## Mathematics

### Spectrometer Model
A typical digital optical spectrometer's response may be modelled as
:::{math}
:label: spec-model
f_i = d_i + k \tau A \int_{\lambda_{i-1}}^{\lambda_i} g(\lambda) E(\lambda) d\lambda.
:::
Where...

$f_i \in \RR \units{counts} \textup{ for } i \in \{1, \dots, N\}$
: is the $i$'th spectral sample measurement. This measurement requires
  non-trivial calibration and signal processing to yield a useful value.

$d_i \in \RR \units{counts}$
: is the photodetector's dark response. This is a random variate which captures the effects of
  thermal and electronic noise with non-zero mean. Its distribution will vary with temperature,
  integartion time, and the electronic configuration of the photodetector. Most spectrometers
  include optically masked photodetectors to automatically estimate this parameter at the time of
  measurement, but this assumes the dark response will be uniform across all photodetectors.
  Another strategy for estimating the dark response is to measure a "dark frame" by blocking the
  spectrometer's input just before taking the actual measurement.

$k \in \RR, \tau \in \RR \units{s}, A \in \RR \units{cm^2}$
: are the electronic gain (unitless), integration time, and photodiode area, respectively.

$\lambda_i \in \RR \units{nm} \textup{ for } i \in \{0,\dots,N\}$
: is the $i$'th sample bin's right edge. We assume the bins don't overlap and there is no gap
  between them, so $\lambda_{i-1}$ is the bin's left edge. We also assume the bin widths are
  approximately uniform and that the sample rate (reciprocal bin width) exceeds the Nyquist rate of
  the incident irradiance (ie. no aliasing). The centre wavelength of each bin is $\lambda_{c,i} =
  (\lambda_{i-1} + \lambda_{i})/2$.

$g(\lambda) \in \RR \units{counts/\mu J}$
: is the spectrometer's spectral sensitivity. We assume $g(\lambda)$ varies smoothly and slowly, so
  that we can reasonably approximate it with a constant value over each spectral bin.

$E(\lambda) \in \RR \units{\mu W/cm^2/nm}$
: is the incident spectral irradiance, which we assume is constant over the duration of the
  integration time.

:::{note}
We have neglected the rounding error inherent to digital measurements. Approximating a real value
with a digital one introduces noise on the order of half of a least-significant digit, which
should be negligible relative to other measurement noise.
:::

:::{caution}
We have also assumed that the photodetector response is linear. In practice, linearity should not be
expected and $f_i$ should be linearized with some transfer function before applying this model.
This should be handled by the spectrometer's software, but it may be wise to double-check by e.g.
measuring the same irradiance with a series of different integration times. This, of course, pulls
the spectrometer's internal clock into the chain of calibration and maybe we should be calibrating
it too! The calibration rabbit-hole is infinite!
:::

#### Estimating the incident irradiance

To estimate $E(\lambda)$ using {eq}`spec-model`, we assume that $g(\lambda)$ is constant across
the bin which allows us to factor it out of the integral. Then we rearrange to yield:
:::{math}
:label: spec_estimate
\hat{E}_i = \frac{f_i - \hat{d}_i}{k \tau A \hat{g}_i} 
   \approx \int_{\lambda_{i-1}}^{\lambda_i} E(\lambda) d\lambda.
:::
Where...

$\hat{E}_i \in \RR \units{\mu W/cm^2/nm}$
: is the estimated spectral irradiance at wavelength $\lambda_{c,i}$.

$\hat{d}_i \in \RR \units{counts}$
: is the estimated dark offset, from either the optically masked photodetectors or from a previously
  measured "dark frame.

$\hat{g}_i \in \RR \units{counts/\mu J}$
: is the estimated spectral response, as produced by the spectrometer's calibration procedure.


#### Resampling spectral measurements
Spectrometers often have non-uniformly spaced bin centres, which is not ideal. A common post-processing
step is to resample the data to uniform spacing, or in other words, estimate the $\hat{E}_i$ that
would have been measured if the bins were centered on different wavelengths.

Let $\lambda'_i$ for $i \in \{0,\dots,N\}$ be the new bin edges. The cumulative sum of $\hat{E}_i$
will approximate the integral of $E(\lambda)$ from the beginning of the spectrometer's range.
:::{math}
:label: rebin_cumsum
\hat{F}_i = \sum_{j=1}^{i}\hat{E}_j \approx \int_{\lambda_0}^{\lambda_i} E(\lambda) d\lambda.
:::
Interpolating the cumulative sum at the new bin edges will approximate the integral from the orignal
left-most edge, $\lambda_0$, to the new bin's right edge.
:::{math}
:label: rebin_interp
\hat{F}'_i = \underset{\lambda'_i}{\mathrm{interp}} \left\{ (\lambda_i, \hat{F}_i) : i \in 0,\dots, N \right\}
\approx \int_{\lambda_0}^{\lambda'_i} E(\lambda) d\lambda.
:::
Differencing adjacent samples of $\hat{F}'_i$ yields the spectral irradiance integrated over the new
bins.
:::{math}
:label: rebin_diff
\hat{E}'_i = \hat{F}'_i - \hat{F}'_{i-1} \approx \int_{\lambda'_{i-1}}^{\lambda'_i} E(\lambda) d\lambda.
:::

The accuracy of this method depends on how well the interpolation function can estimate the original
underlying spectral irradiance. If the original sampling rate (reciprocal bin width) exceeds the
Nyquist rate of the irradiance, then an appropriate interpolation filter will result in minimal
resampling error.

### Camera Model
The spectral response of a typical digital camera's pixel may be modelled as:
:::{math}
:label: cam-model
f = d + k \tau A \int_{\lambda_{min}}^{\lambda_{max}} g(\lambda) E(\lambda) d\lambda.
:::

$f \in \RR^c \units{counts}$
: is the pixel value, with dimensionality $c$ for the number of colour channels.

$d \in \RR^c \units{counts}$
: is the pixel's dark response. This is a random variate with non-zero mean that captures the
  effects of thermal and electronic noise. It will vary with temperature, gain, and integration time.
  Many modern cameras have features that will automatically compensate for it (e.g. Nikon's "Long
  Exposure Noise Reduction"). Otherwise, it can be estimated by capturing "dark frames" by capping
  the lens and taking a photo using the same settings.

$k \in \RR^{c\times c}, \tau \in \RR \units{s}, A \in \RR \units{cm^2}$
: are the electronic gain / colour matrix (unitless), integration time, and pixel area, respectively.

$\lambda_{min} \le \lambda \le \lambda_{max} \in \RR \units{nm}$
: is the sensitive wavelength range of the camera.

$E(\lambda) \in \RR \units{\mu W/cm^2/nm}$
: is the incident spectral irradiance.

$g(\lambda) \in \RR^c \units{counts/\mu J}$
: is the pixel's spectral sensitivity, with $c$ colour channels.

:::{caution}
Again, we have assumed a linear response. This is not true in general and is explicitly untrue
for most common image and video formats. In practice, it is necessary to use the camera's raw image
format and render them into 16-bit TIFFs with a linear profile. Such images will not "look good"
but they will allow error-free mathematical manipulation!
:::

#### Estimating the camera's spectral response
While the camera's pixel response {eq}`cam-model` follows the same form as the spectrometer 
{eq}`spec-model`, we can't make the same assumption that the spectral sensitivity, $g(\lambda)$,
is constant over the integral and factor it out. In some cases it's possible to "un-mix" such an
integral using deconvolution techniques, but the application would not be straightforward here.
Instead, we move into the discrete (sampled) domain and infer the camera's spectral response as a
regression problem.
:::{math}
:label: cam-matrix-model
\begin{align}
f_i &= d_i + k_i \tau_i A \sum_{j=1}^{N} E_{i,j} g_j \\
\hat{f}_i &= \frac{f_i - d_i}{k_i \tau_i A} = \sum_{j=1}^{N} E_{i,j} g_j \\
\mat{\hat{F}} &= \mat{E G}
\end{align}
:::

$\mat{\hat{F}} = (\hat{f}_1,\dots,\hat{f}_i,\dots,\hat{f}_M )^\trans \in \RR^{M\times c} \units{counts/s/cm^2}$
: is the matrix of (normalized) measured pixel values. The matrix has $M$ rows corresponding to 
  measurements with $c$ columns for the colour channels.

$\mat{G} = (g_1,\dots,g_j,\dots,g_N )^\trans \in \RR^{N\times c} \units{counts/\mu J}$
: is the pixel's discrete spectral sensitivity matrix, with $N$ rows for the spectral samples and $c$ columns for the colour channels.

$\mat{E} = \left( E_{1,1}, \ddots, E_{i,j}, \ddots, E_{M,N} \right) \in \RR^{N\times M} \units{\mu W/cm^2/nm}$
: is the incident spectral irradiance matrix, with $M$ rows for the measurements and $N$ columns for the spectral samples.

Solving {eq}`cam-matrix-model` for $\mat{G}$ appears to be a straightforward linear regression
:::{math}
:label: cam-regression-naive
\mat{\hat{G}} = \underset{\mat{G}}{\mathrm{argmin}} \| \mat{\hat{F}} - \mat{E G} \|_2^2
:::
but has a few significant caveats due to the nature of the measurements.

We use a monochromator to generate spectral irradiances with smooth, narrow bands that we sweep over the sensitive range of the camera.
We (somewhat arbitrarily) set our monochromator output bandwidth to 10 nm full-width at half-maximum (FWHM), and sweep the output in wavelength by 5 nm steps, corresponding to the Nyquist rate for the 10 nm bandwidth.
This is significantly greater than our spectrometer's sampling period of 1 nm[^sn-sampling], leading to an under-determined system when we try to solve {eq}`cam-matrix-model` for the spectral sensitivity matrix $\mat{G}$.
That is, there are infinitely many $\mat{G}$'s that could explain our measurements and we must introduce additional information to the system, in the form of a regularization term, to select the "right" $\mat{G}$.
Here, we use a generalized ridge regression[^sn-ridge] to impose a smoothness constraint on the $\mat{G}$ corresponding to the Nyquist rate of the system.
:::{math}
:label: cam-regression-ridge
\mat{\hat{G}} = \underset{\mat{G}}{\mathrm{argmin}} \| \mat{\hat{F}}-\mat{EG} \|_2^2 + \|\mat{\Gamma} \mat{G} \|_2^2
:::

$\mat{\Gamma} \in \RR^{N\times N}$
: is the Tikhonov matrix. $\mat{\Gamma} = \alpha \mat{I}$ yields the standard ridge regression, which penalises solutions with large L-2 norm and selects lower "energy" solutions. Setting $\mat{\Gamma} = \mat{I}\ast h$, where $\ast$ is convolution and $h$ is a high-pass filter kernel[^sn-convolution], penalises solutions with content above $h$'s frequency cut-off and thus selects lower-frequency, smooth solutions.

[^sn-sampling]: We could maybe address this issue by resampling the monochromator output spectra down to the 5 nm sample spacing?
[^sn-ridge]: Also known as linear regression with [Tikhonov regularization](https://en.wikipedia.org/wiki/Ridge_regression#Tikhonov_regularization).
[^sn-convolution]: Here, $h \in \RR^{1 \times n}$ is a row vector and $(\mat{I} \ast h)\_{i,j}$ $= h\_{i-j+\lceil n/2\rceil}$, or zero if the index is out of bounds.

This regression has a closed-form solution given by
:::{math}
:label: cam-ridge-solution
\mat{\hat{G}} = \left(\mat{E}^\trans \mat{E} + \mat{\Gamma}^\trans \mat{\Gamma} \right)^{-1} \mat{E}^\trans \mat{\hat{F}}
:::
or it may be solved by minimization techniques if the system becomes too large.