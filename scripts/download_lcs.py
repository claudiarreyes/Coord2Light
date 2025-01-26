import lightkurve as lk
from astropy.table import Table
from astropy.io import ascii, fits
import os
import numpy as numpy

base_dir = '/Users/creyes/Projects/tables




df['coord_string'] = [ "{:.8f}".format(a) + ' ' + "{:.8f}".format(b) for a,b in zip(df['alpha'], df['delta'])]

for _, coords in df.iterrows():
    mytable = lk.search_lightcurve(coords['coord_string']).table
    file_path = os.path.join(base_dir, '{}.ecsv'.format(coords['target_name']))
    mytable.write(file_path, overwrite=True)


mission_list, nobs = [], []
for string in df.tel_object:
    try:
        t = Table.read(basedir +'/{}.ecsv'.format(string))
        mission_list.append([a for a in set(np.array(t['project']))])
        nobs.append(len(t))
    except FileNotFoundError:
        mission_list.append('')
        nobs.append(0)
        
df['mission'] = mission_list
df['number_of_lightcurves'] = nobs

# Extract all unique mission names from the 'mission' column
all_missions = set(mission for missions in df['mission'] for mission in missions)

# Create a new column for each unique mission ands sets boolean if LC available from that mission
for mission in all_missions:
    df[mission] = df['mission'].apply(lambda x: mission in x)

tables = []
for telobj in df.target_name:
    df[df.number_of_lightcurves>0].copy()
    try:
        name = '{}'.format(telobj).replace(' ', '_')
        t = Table.read('/Users/creyes/Projects/harps/tables/{}.ecsv'.format(name))
        tables.append(t)
    except FileNotFoundError:
        tables.append('No table')
df['tables'] = tables


# df = pd.read_pickle('/Users/creyes/Projects/harps/tables.pkl')



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
                fname = base_dir + '/lightcurves/{:05.0f}_{}_target_{}_MAST_targetname_{}_MAST_exptime_{}_MAST_mission_{}_MAST_author_{}.txt'.format(project_name, k, tel_object, target_name, exptime, mission, author)
                np.savetxt(fname, np.column_stack([tess_bjds, sap_fluxes, pdcsap_fluxes]))
