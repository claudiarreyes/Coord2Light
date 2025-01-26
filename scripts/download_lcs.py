from astropy.table import Table
from astropy.io import fits
import numpy as numpy

base_dir = '/Users/creyes/Projects/lcs
df = pd.read_pickle('/Users/creyes/Projects/harps/tables.pkl')


for k in range(len(df)):
    if not df['tables'].iloc[k]=='No table':
        ta = df['tables'].iloc[k].to_pandas()
        tel_object = df.tel_object.iloc[k]
        for e in ta['exptime'].unique():
            tmp = ta[(ta['type']=='S')].copy()
            for e in tmp.index:         
                target_name = tmp['target_name'].iloc[e]
                exptime = tmp['exptime'].iloc[e]
                mission = tmp['mission'].iloc[e]
                author = tmp['author'].iloc[e]
                url = tmp['dataURL'].iloc[e]
                fits_file = 'https://mast.stsci.edu/api/v0.1/Download/file?uri=%s'%url
                with fits.open(fits_file, mode="readonly") as hdulist:
                    tess_bjds = hdulist[1].data['TIME']
                    sap_fluxes = hdulist[1].data['SAP_FLUX']
                    pdcsap_fluxes = hdulist[1].data['PDCSAP_FLUX']
                fname = base_dir + '/lightcurves/{:05.0f}_HARPS_target_{}_TESS_targetname_{}_TESS_exptime_{}_TESS_mission_{}_TESS_author_{}.txt'.format(k, tel_object, target_name, exptime, mission, author)
                np.savetxt(fname, np.column_stack([tess_bjds, sap_fluxes, pdcsap_fluxes]))
