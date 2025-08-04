import pandas as pd
from astropy.io import fits
import numpy as np
import os
from astropy.table import Table
from astropy.coordinates import SkyCoord
# tables to be concatenated
sdss_galaxy = "../catalogues/dr16_galaxy.fits"
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

with fits.open(dr16q_short) as hdul:
    data = hdul[1].data  
    table_q = Table(data) 
df_qso = table_q.to_pandas()  
#add the 'CLASS' column to df_qso and fill with 'QSO'
df_qso['CLASS'] = 'QSO'
combined_df = pd.concat([df_qso, new_df_galaxy], ignore_index=True, sort=True)

# combined_df_sorted = combined_df.sort_values(by='SDSS_NAME', ascending=True)
# combined_df_sorted.reset_index(drop=True, inplace=True)

table_combined = Table.from_pandas(combined_df)
table_combined.write(outname, format='fits', overwrite=True)

print(f"Saved combined table with {len(combined_df)} rows to 'combined_sdss_sorted.fits'")

#Usage example:
# python concat_cat.py
