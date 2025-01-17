# Licensed under a 3-clause BSD style license - see LICENSE.rst

from astropy.io import fits

from ...core import Region, Regions
from ...core.registry import RegionsRegistry
from ..core import _to_shape_list, SkyRegion

__all__ = []


@RegionsRegistry.register(Region, 'serialize', 'fits')
@RegionsRegistry.register(Regions, 'serialize', 'fits')
def _serialize_fits(regions):
    for region in regions:
        if isinstance(region, SkyRegion):
            raise TypeError('Every region must be a pixel region')

    shape_list = _to_shape_list(regions, coordinate_system='image')
    return shape_list.to_fits()


@RegionsRegistry.register(Region, 'write', 'fits')
@RegionsRegistry.register(Regions, 'write', 'fits')
def _write_fits(regions, filename, header=None, overwrite=False):
    """
    Convert a list of `~regions.Region` to a FITS region table and write
    to a file.

    Parameters
    ----------
    regions : list
        A list of `~regions.Region` objects.

    filename : str
        The filename in which the table is to be written.

    header : `~astropy.io.fits.Header`, optional
        The FITS header.

    overwrite : bool, optional
        If True, overwrite the output file if it exists. Raises an
        `OSError` if False and the output file exists. Default is False.
    """
    output = _serialize_fits(regions)
    bin_table = fits.BinTableHDU(data=output, header=header)
    bin_table.writeto(filename, overwrite=overwrite)
