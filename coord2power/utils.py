import numpy as np
import os
from astropy.io import fits

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
