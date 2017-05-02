# -*- coding: utf-8 -*-
#
#  read.py
#  pangaea
#
#  Author : Alan D Snow, 2017.
#  License: BSD 3-Clause
"""pangea.read

    This module provides helper functions to read in
    land surface model datasets.
"""
import xarray as xr


def open_mfdataset(path_to_lsm_files,
                   lat_var,
                   lon_var,
                   time_var,
                   lat_dim,
                   lon_dim,
                   time_dim,
                   autoclose=True):
    """
    Wrapper to open land surface model netcdf files
    using :func:`xarray.open_mfdataset`.

    Parameters
    ----------
    path_to_lsm_files: :obj:`str`
        Path to land surface model files with wildcard.
        (Ex. '/path/to/files/*.nc')
    lat_var: :obj:`str`
        Latitude variable (Ex. lat).
    lon_var: :obj:`str`
        Longitude variable (Ex. lon).
    time_var: :obj:`str`
        Time variable (Ex. time).
    lat_dim: :obj:`str`
        Latitude dimension (Ex. lat).
    lon_dim: :obj:`str`
        Longitude dimension (Ex. lon).
    time_dim: :obj:`str`
        Time dimension (ex. time).
    autoclose: :obj:`str`
        If True, will use xarray's autoclose option with
        :func:`xarray.open_mfdataset`.

    Returns
    -------
    :func:`xarray.Dataset`
    """
    def define_coords(xds):
        """xarray loader to ensure coordinates are loaded correctly"""
        # remove time dimension from lat, lon coordinates
        if xds[lat_var].ndim == 3:
            xds[lat_var] = xds[lat_var].squeeze(time_dim)
        if xds[lon_var].ndim == 3:
            xds[lon_var] = xds[lon_var].squeeze(time_dim)
        # make sure coords are defined as coords
        if lat_var not in xds.coords \
                or lon_var not in xds.coords \
                or time_var not in xds.coords:
            xds.set_coords([lat_var, lon_var, time_var],
                           inplace=True)
        return xds

    xds = xr.open_mfdataset(path_to_lsm_files,
                            autoclose=autoclose,
                            preprocess=define_coords,
                            concat_dim=time_dim)
    xds.lsm.y_var = lat_var
    xds.lsm.x_var = lon_var
    xds.lsm.time_var = time_var
    xds.lsm.y_dim = lat_dim
    xds.lsm.x_dim = lon_dim
    xds.lsm.time_dim = time_dim
    xds.lsm.to_datetime()

    return xds
