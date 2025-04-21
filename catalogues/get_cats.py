from astroquery.vizier import Vizier
import astropy.units as u


def query_vizier_catalog(
        catalog_id:str,
        out_path:str,
        out_format:str = "fits",
        max_rows:int = -1,
        ):
    """
    Find and download a catalog from VizieR.
    Parameters:
        catalog_id (str): The catalog ID to query. You can find it via the VizieR website.
        out_format (str): The output format for the catalog. Options are 'fits', 'csv', or 'votable'.
        out_path (str): The name of the output file.
        max_rows (int): The maximum number of rows to download. Default is -1, which means no limit.
    
    """
    vizier = Vizier()
    vizier.ROW_LIMIT = max_rows
    results = vizier.get_catalogs(catalog_id)
    print(results)
    results[0].write(out_path, format=out_format, overwrite=True)
    print(f"Catalog {catalog_id} downloaded to {out_path} in {out_format} format.")
    return


if __name__ == "__main__":
    # Example usage
    catalog_id = "VIII_92"  # Example catalog ID
    out_format = "fits"  # Output format
    out_name = f"./VLA_FIRST.{out_format}"  # Output file name
    
    # max_rows = 1000  # Maximum number of rows to download
    query_vizier_catalog(catalog_id, out_name, out_format)
