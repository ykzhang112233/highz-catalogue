import pandas as pd
from astropy.io import fits
import numpy as np
import os
from astropy.table import Table
from astropy.coordinates import SkyCoord
# tables to be concatenated
sdss_galaxy = "../catalogues/dr16_galaxy.fits"
sdss_galaxy_sup = "../catalogues/dr16_sup_galaxy.fits"
dr16q_short = "tmp_sdss.fits"
outname = "tmp_sdss16_comb.fits"

with fits.open(sdss_galaxy) as hdul:
    data = hdul[1].data 
    table_g = Table(data)  
df_galaxy = table_g.to_pandas()
# Generate the sdss name matching the dr16q style
source_coords = SkyCoord(ra=df_galaxy['PLUG_RA'], dec=df_galaxy['PLUG_DEC'], unit='deg')
ra = source_coords.ra.to_string(unit='hour', sep=':', precision=2, pad=True)
dec = source_coords.dec.to_string(unit='deg', sep=':', precision=1, pad=True)
for i in range(len(dec)):
    print(dec[i])
    if dec[i][0] == '-':
        dec[i] = dec[i]
    else:
        dec[i] = '+' + dec[i]  # add a plus sign for positive declinations
sdss_name = np.char.add('g', np.char.add(np.char.replace(ra, ':', ''), np.char.replace(dec, ':', '')))
#Cols_SDSSdr16q='keepcols "SDSS_NAME RA DEC Z SOURCE_Z Z_PIPE ZWARNING Z_VI Z_CONF \
#                          IS_QSO_QN Z_QN Z_10K Z_CONF_10K Z_PCA ZWARN_PCA"'
# for df_galaxy, make a J2000 name based on RA and DEC (decimal degrees)
new_df_galaxy = pd.DataFrame(
    {
        'SDSS_NAME': sdss_name,
        'RA': df_galaxy['PLUG_RA'],
        'DEC': df_galaxy['PLUG_DEC'],
        'CLASS': df_galaxy['CLASS'],
        'Z':df_galaxy['Z'],
        'ZWARNING': df_galaxy['ZWARNING'],
    }
)
# Then, work on the supplementary galaxy table, this is a litte different
with fits.open(sdss_galaxy_sup) as hdul:
    data = hdul[1].data 
    table_g2 = Table(data)  
df_galaxy_sup = table_g2.to_pandas()
df_update = df_galaxy_sup[df_galaxy_sup['f_zsp'] != 0]
df_update = df_update.reset_index(drop=True)
df_update['sdss_name'] = df_update['SDSS16'].str.replace('SDSS J', 'g')
# 初始化所有行为 NaN
df_update['Z'] = np.nan
df_update['SOURCE_Z'] = ''
# 有光谱红移的情况
mask_zsp = ~pd.isna(df_update['zsp'])
df_update.loc[mask_zsp, 'Z'] = df_update.loc[mask_zsp, 'zsp']
# SOURCE_Z 保持为 NaN
# 无光谱红移但有光度红移的情况
mask_zph = (~mask_zsp) & (~pd.isna(df_update['zph']))
df_update.loc[mask_zph, 'Z'] = df_update.loc[mask_zph, 'zph']
df_update.loc[mask_zph, 'SOURCE_Z'] = 'phot'
# 两种红移都没有的情况
mask_none = (~mask_zsp) & (~mask_zph)
df_update.loc[mask_none, 'SOURCE_Z'] = 'NOT_CLEAN'
new_df_galaxy_2 = pd.DataFrame(
    {
        'SDSS_NAME': df_update['sdss_name'],
        'RA': df_update['RA_ICRS'],
        'DEC': df_update['DE_ICRS'],
        'CLASS': 'GALAXY',
        'Z': np.where(df_update['Z'] < 3, df_update['Z'], 0.001),
        'ZWARNING': df_update['f_zsp'],
        'SOURCE_Z': df_update['SOURCE_Z'].astype(str)
    }
)
# the above critera for z is to discard unreliable redshifts from photometry or large z_warnings

with fits.open(dr16q_short) as hdul:
    data = hdul[1].data  
    table_q = Table(data) 
df_qso = table_q.to_pandas()  
#add the 'CLASS' column to df_qso and fill with 'QSO'
df_qso['CLASS'] = 'QSO'
combined_df = pd.concat([df_qso, new_df_galaxy, new_df_galaxy_2], ignore_index=True, sort=True)

# combined_df_sorted = combined_df.sort_values(by='SDSS_NAME', ascending=True)
# combined_df_sorted.reset_index(drop=True, inplace=True)

table_combined = Table.from_pandas(combined_df)
table_combined.write(outname, format='fits', overwrite=True)

print(f"Saved combined table with {len(combined_df)} rows to 'combined_sdss_sorted.fits'")

#Usage example:
# python concat_cat.py
