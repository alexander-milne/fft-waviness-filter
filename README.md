# Waviness Profile Calculator

A lightweight Python implementation for calculating the **waviness profile (W-profile)** of a 1D surface measurement using a frequency-domain low-pass filter.

This tool is intended for surface metrology applications and follows the cutoff wavelength selection guidance defined in ISO 4288.

---

## Overview

Surface texture analysis typically separates a measured surface into:

- **Roughness (R-profile)** – short-wavelength components  
- **Waviness (W-profile)** – longer-wavelength components  
- **Form** – very long-wavelength components  

This repository provides a function that extracts the **waviness profile** using an FFT-based low-pass filtering approach.

Unlike fixed-index filtering, this implementation dynamically calculates the FFT cutoff index to match a desired **physical cutoff wavelength (λc)** in micrometers.

---

## Repository Structure

```
waviness_function.py
README.md
```

---

## Function

### `calc_waviness_profile`

```python
calc_waviness_profile(
    _surface_profile,
    sample_distance=0.8,
    desired_cutoff_wavelength_um=800
)
```

### Parameters

| Parameter | Type | Description |
|------------|------|------------|
| `_surface_profile` | `np.array` | 1D array of surface height values |
| `sample_distance` | `float` | Physical distance between samples (µm) |
| `desired_cutoff_wavelength_um` | `float` | Cutoff wavelength λc (µm). Default = 800 µm (0.8 mm) |

### Returns

```
np.array
```

The calculated waviness profile (W-profile).

---

## ISO 4288 Cutoff Selection Guide

| Expected Ra Range (µm) | Cutoff λc (mm) | Eval. Length ln (mm) |
|------------------------|---------------|----------------------|
| 0.02 < Ra ≤ 0.1        | 0.25          | 0.25                 |
| 0.1  < Ra ≤ 2.0        | 0.8           | 0.8                  |
| 2.0  < Ra ≤ 10.0       | 2.5           | 2.5                  |
| 10.0 < Ra ≤ 80.0       | 8.0           | 8.0                  |

For the common 0.8 mm cutoff:

```python
desired_cutoff_wavelength_um = 800
```

---

## How It Works

### 1. Mirror Padding

The signal is mirrored on both sides before FFT filtering to reduce edge effects.

### 2. Dynamic Cutoff Calculation

The FFT cutoff index is calculated as:

```
k = (N * sample_distance) / desired_cutoff_wavelength_um
```

Where:

- `N` = padded signal length  
- `sample_distance` = µm per sample  
- `desired_cutoff_wavelength_um` = physical cutoff wavelength  

This ensures proper mapping between FFT frequency bins and real-world wavelength.

### 3. FFT-Based Low-Pass Filtering

- Perform FFT  
- Zero high-frequency components above cutoff (brick-wall filter)  
- Preserve low-frequency components  

> Note: ISO standards specify a Gaussian filter. This implementation uses a brick-wall filter for simplicity and clarity.

### 4. Inverse FFT

The inverse FFT is performed and the center portion (corresponding to the original signal) is returned as the waviness profile.

---

## Installation

Only NumPy is required.

```bash
pip install numpy
```

---

## Example Usage

```python
import numpy as np
from waviness_function import calc_waviness_profile

# Generate synthetic surface data
x = np.linspace(0, 10_000, 5000)
surface = (
    5 * np.sin(2 * np.pi * x / 2000) +     # Long wavelength component
    0.5 * np.sin(2 * np.pi * x / 50)       # Short wavelength component
)

waviness = calc_waviness_profile(
    surface,
    sample_distance=2.0,
    desired_cutoff_wavelength_um=800
)

print(waviness)
```

---

## Use Cases

This function is suitable for:

- Surface profilometry data  
- Research and experimentation  
- Pre-processing before roughness parameter calculations (Ra, Rq, etc.)  
- Educational demonstrations of FFT filtering  

Not intended for:

- Strict ISO-certified measurements (Gaussian filter required)  
- 2D or 3D surface topography  
- Automatic cutoff selection based on measured Ra  

---

## Requirements

- Python 3.x  
- NumPy  

---

## Limitations

- Uses brick-wall frequency filter (not ISO Gaussian filter)  
- 1D profiles only  
- No form removal  
- No automated parameter estimation  

---

## License

Add your preferred license (e.g., MIT, Apache 2.0).
