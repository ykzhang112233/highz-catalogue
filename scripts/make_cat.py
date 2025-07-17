# Just some utility functions to make the output catalogue more hunman-readable.
import pandas as pd
from astropy.io import fits
import numpy as np


# read the fits file and convert it to a Pandas DataFrame
file_path = 'final_matched_highz_catalogue.fits'  
with fits.open(file_path) as hdul:
    data = hdul[1].data  # 星表数据通常在第一个扩展（HDU 1）中
    df = pd.DataFrame(data)  # 转换为 Pandas DataFrame

# Change the column names to be more human-readable
columns = [
    "FIRST_r1", "NVSS_r2", "GLEAM_r3", "RACS-DR1_r4",
    "Fpeak_r1", "Fint_r1", "Rms_r1", "S1.4_r2", "e_S1.4_r2",
    "Fpwide_r3", "e_Fpwide_r3", "Fintwide_r3", "e_Fintwide_r3",
    "Fpk_r4", "e_Fpk_r4", "Ftot_r4", "e_Ftot_r4"
]

new_columns = [
    "FIRST", "NVSS", "GLEAM", "RACS-DR1",
    "Fpeak_first", "Fint_first", "Rms_first", "S1.4_nvss", "e_S1.4_nvss",
    "Fpwide_gleam", "e_Fpwide_gleam", "Fintwide_gleam", "e_Fintwide_gleam",
    "Fpk_racs", "e_Fpk_racs", "Ftot_racs", "e_Ftot_racs"
]
df.rename(columns={old: new for old, new in zip(columns, new_columns)}, inplace=True)
df.replace([-32768,-2147483648], 'NA', inplace=True)

sources = df['sdss_name']
# Add a new column for source_tier_flag as a binary flag
# make the empty pd.sereries based on all source numbers
df['source_tier_flag'] = pd.Series(dtype='int')
for i in range(len(sources)):
    # extract the non-nan values from the source_tier columns
    a0 = 1 if not pd.isna(df['source_tier_first'][i]) else 0
    a1 = 1 if not pd.isna(df['source_tier_racs'][i]) else 0
    a2 = 1 if not df.loc[i, 'source_tier_nvss'] == 1 else 0
    a3 = 1 if not df.loc[i, 'source_tier_gleam'] == 1 else 0
    df.loc[i, 'source_tier_flag'] = a0*1 + a1*2 + a2*4 + a3*8

df.to_csv('../final_matched_highz_catalogue.csv', index=False)

#Usage example:
# python make_cat.py
