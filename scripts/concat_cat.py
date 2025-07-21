import pandas as pd
from astropy.io import fits
import numpy as np
import os
from astropy.table import Table

# tables to be concatenated
sdss_galaxy = "../catalogues/dr16_galaxy_all.fits"
dr16q_short = "tmp_sdss.fits"
outname = "tmp_sdss16_comb.fits"

with fits.open(sdss_galaxy) as hdul:
    data = hdul[1].data 
    table_g = Table(data)  
df_g = table_g.to_pandas()  
with fits.open(dr16q_short) as hdul:
    data = hdul[1].data  
    table_q = Table(data) 
df_q = table_q.to_pandas()  

combined_df = pd.concat([df_q, df_g], ignore_index=True, sort=True)

# combined_df_sorted = combined_df.sort_values(by='SDSS_NAME', ascending=True)
# combined_df_sorted.reset_index(drop=True, inplace=True)

table_combined = Table.from_pandas(combined_df)
table_combined.write(outname, format='fits', overwrite=True)

print(f"Saved combined table with {len(combined_df)} rows to 'combined_sdss_sorted.fits'")

#Usage example:
# python concat_cat.py
