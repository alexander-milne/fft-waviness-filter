def calc_waviness_profile(
    _surface_profile, 
    sample_distance=0.8, 
    desired_cutoff_wavelength_um=800
):
    """
    Calculates the waviness profile using a frequency-domain filter with a 
    dynamically calculated cutoff index to match a desired physical wavelength.

    Args:
        _surface_profile (np.array): 1D array of the surface profile data.
        sample_distance (float): The physical distance between data points (in µm).
        desired_cutoff_wavelength_um (float): The desired physical cutoff 
                                             wavelength (λc) in µm. For the 
                                             0.8 mm standard, this should be 800.
    # ISO 4288 Cutoff Selection Guide
    # --------------------------------------------------------------------
    # Expected Ra Range (µm)    | Cutoff λc (mm) | Eval. Length ln (mm)
    # --------------------------------------------------------------------
    # (0.02 < Ra <= 0.1)        |      0.25      |         0.25
    # (0.1  < Ra <= 2.0)        |      0.8       |         0.8
    # (2.0  < Ra <= 10.0)       |      2.5       |         2.5
    # (10.0 < Ra <= 80.0)       |      8.0       |         8.0
    # --------------------------------------------------------------------
    Returns:
        np.array: The calculated waviness profile.
    """
    # --- 1. Pad the signal to reduce edge effects ---
    # Using mirror padding is a standard technique for FFT-based filtering.
    flipped = _surface_profile[::-1]
    profile = np.concatenate([flipped, _surface_profile, flipped])
    
    # --- 2. Calculate the correct FFT index 'k' ---
    # This is the key correction: 'k' is now calculated dynamically.
    N = len(profile)  # N is the total length of the padded signal

    # The formula to find the index 'k' that corresponds to our desired wavelength
    k_cutoff_index = (N * sample_distance) / desired_cutoff_wavelength_um

    # --- 3. Perform the FFT and apply the low-pass filter ---
    filtered = np.fft.fft(profile)

    # Use the dynamically calculated index for filtering.
    # The index must be an integer and at least 1 to avoid the DC component (k=0).
    k_int = max(1, int(round(k_cutoff_index)))
    
    # Apply a "brick-wall" low-pass filter by zeroing high-frequency components.
    # Note: For strict ISO compliance, a Gaussian-shaped filter is specified,
    # but we use this one.
    filtered[k_int:-k_int] = 0
    
    # --- 4. Perform the inverse FFT and extract the original profile ---
    # The result is the W-profile (waviness).
    waviness_profile = np.real(np.fft.ifft(filtered))
    
    # Slice out the middle part that corresponds to the original, un-padded signal.
    start_index = len(flipped)
    end_index = start_index + len(_surface_profile)
    
    return waviness_profile[start_index:end_index]