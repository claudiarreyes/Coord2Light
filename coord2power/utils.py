import numpy as np
import os
from astropy.io import fits
from astroquery.gaia import Gaia
from astropy.coordinates import SkyCoord
from astropy import units as u
import pandas as pd

def create_coord_string(alpha, delta):
    """
    Create a coordinate string from alpha and delta values.
    """
    return [f"{a:.8f} {d:.8f}" for a, d in zip(alpha, delta)]

def save_lightcurves(table, target_name, output_dir):
    """
    Save lightcurves of type 'S' (science) to text files.
    """
    if table is None:
        return
    table_df = table.to_pandas()
    science_rows = table_df[table_df['type'] == 'S']
    for _, row in science_rows.iterrows():
        try:
            fits_url = f"https://mast.stsci.edu/api/v0.1/Download/file?uri={row['dataURL']}"
            with fits.open(fits_url, mode="readonly") as hdulist:
                tess_bjds = hdulist[1].data['TIME']
                sap_fluxes = hdulist[1].data['SAP_FLUX']
                pdcsap_fluxes = hdulist[1].data['PDCSAP_FLUX']
            filename = f"{target_name}_exptime_{row['exptime']}_mission_{row['mission']}_author_{row['author']}.txt"
            filepath = os.path.join(output_dir, filename)
            np.savetxt(filepath, np.column_stack([tess_bjds, sap_fluxes, pdcsap_fluxes]))
        except Exception as e:
            print(f"Failed to save lightcurve for {target_name}: {e}")

def query_gaia(df, output_dir, filename="with_lightcurves_gaiadr3.csv"):
    """
    Query Gaia DR3 for the closest match to coordinates in the DataFrame.
    Adds parallax-based distance modulus (DM) and absolute G magnitude (abs_gmag_estimated).
    
    Args:
        df (pd.DataFrame): DataFrame containing 'alpha' and 'delta' columns for coordinates.
        output_dir (str): Directory to save the resulting CSV file.
        filename (str): Name of the output file (default: 'with_lightcurves_gaiadr3.csv').

    Returns:
        pd.DataFrame: Updated DataFrame with Gaia DR3 results.
    """
    width = u.Quantity(50, u.arcsec)
    height = u.Quantity(50, u.arcsec)

    Gaia.ROW_LIMIT = 1
    h = []
    irow = []

    for i in df.index:
        coord = SkyCoord(ra=df.alpha.iloc[i], dec=df.delta.iloc[i], unit=(u.degree, u.degree), frame='icrs')
        r = Gaia.query_object_async(coordinate=coord, width=width, height=height)
        r = r.to_pandas()
        h.append(r)
        if len(r) == 1:
            irow.append(i)
        elif len(r) == 0:
            print(f"No match for index {i}")

    # Concatenate all Gaia results into a single DataFrame
    hsel = pd.concat(h).reset_index(drop=True)
    hsel.insert(0, 'irow', irow)

    # Save intermediate Gaia results
    gaia_output_path = f"{output_dir}/{filename}"
    hsel.to_csv(gaia_output_path, index=False)

    # Compute distance modulus (DM) and absolute G magnitude
    DM = []
    for px in hsel['parallax']:
        if px > 0:
            dm = 5 * (np.log10(1000 / px)) - 5
            DM.append(dm)
        else:
            DM.append(np.nan)

    hsel['DM'] = DM
    hsel['abs_gmag_estimated'] = hsel['phot_g_mean_mag'] - hsel['DM']

    # Join the Gaia results with the initial DataFrame
    full = df.join(hsel.set_index('irow'), on='irow')
    full_output_path = f"{output_dir}/joined_with_gaia.csv"
    full.to_csv(full_output_path, index=False)

    print(f"Results saved to {full_output_path}")
    return full
