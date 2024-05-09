import os
import numpy as np
import mrcfile
from pf_refinement.pdb_util import PDB


def wedge_mask(args, microtubule_volume, microtubule_mask, fit_tubulin_pdb, pf):
    pdb = PDB()
    pdb.read_file(fit_tubulin_pdb)
    com = pdb.calc_center()

    vol = mrcfile.mmap(microtubule_volume, 'r', permissive=True)
    mask = mrcfile.mmap(microtubule_mask, 'r', permissive=True)
    vol_data = vol.data * mask.data
    voxel_size = vol.voxel_size
    header = vol.header
    vol_dim = np.asarray(vol_data.shape)

    size = vol_dim[0] // 2
    x, y = np.meshgrid(np.arange(-size + 1, size + 1), np.arange(-size + 1, size + 1))
    radmatrix = np.remainder(np.arctan2(x, y) + 2 * np.pi, 2 * np.pi) - 2 * np.pi
    zline = np.arange(-size + 1, size + 1)

    edge_resolution = 20
    edge_width = args['micrograph_pixel_size'] * np.ceil(edge_resolution / (2 * args['micrograph_pixel_size']))
    cosmask_filter = np.fft.fftshift(spherical_cosmask(vol_dim, 0, edge_width / args['micrograph_pixel_size']))
    cosmask_filter_fft = np.fft.fftn(cosmask_filter) / np.sum(cosmask_filter)

    theta0 = np.arctan2(com[0], com[1]) + np.deg2rad(pf * args['twist_per_subunit'])
    z0 = (com[2] + args['rise_per_subunit'] * pf) / args['micrograph_pixel_size']
    zsubunits = (zline - z0) * args['micrograph_pixel_size'] / args['rise_per_repeat']
    theta = np.deg2rad((-args['twist_per_repeat']) * zsubunits) + theta0

    wedge = np.zeros(vol_dim.tolist())

    fudge = np.deg2rad(360.0 / (args['num_pfs'] * 2))

    for i in range(len(theta)):
        temp1 = np.remainder(theta[i] - fudge + 2 * np.pi, 2 * np.pi) - 2 * np.pi
        temp2 = np.remainder(theta[i] + fudge + 2 * np.pi, 2 * np.pi) - 2 * np.pi
        angles = [temp1, temp2]
        if max(angles) - min(angles) > 2 * fudge + .2:
            above = max(angles)
            below = min(angles)
            inds = np.logical_or(radmatrix > above, radmatrix < below)
        else:
            above = min(angles)
            below = max(angles)
            inds = np.logical_and(radmatrix > above, radmatrix < below)

        wedge[i, :, :][inds] = 1

    soft_m = np.real(np.fft.ifftn(cosmask_filter_fft * np.fft.fftn(wedge)))
    soft_m[soft_m < 0] = 0

    pf_dir = 'pf{}'.format(pf)
    if not os.path.isdir(pf_dir):
        os.mkdir(pf_dir)

    with mrcfile.new(os.path.join(pf_dir, 'pf_wedge.mrc'), overwrite=True) as mrc:
        mrc.set_data(soft_m.astype(np.float32))
        mrc.voxel_size = voxel_size
        mrc.header.nxstart, mrc.header.nystart, mrc.header.nzstart = (header.nxstart, header.nystart, header.nzstart)
        for coord in ['x', 'y', 'z']:
            mrc.header['origin'][coord] = header['origin'][coord]

    with mrcfile.new(os.path.join(pf_dir, 'pf_masked.mrc'), overwrite=True) as mrc:
        mrc.set_data(((1 - soft_m) * vol_data).astype(np.float32))
        mrc.voxel_size = voxel_size
        mrc.header.nxstart, mrc.header.nystart, mrc.header.nzstart = (header.nxstart, header.nystart, header.nzstart)
        for coord in ['x', 'y', 'z']:
            mrc.header['origin'][coord] = header['origin'][coord]

    return True


def spherical_cosmask(n,mask_radius, edge_width, origin=None):
    """mask = spherical_cosmask(n, mask_radius, edge_width, origin)
    """

    if type(n) is int:
        n = np.array([n])

    sz = np.array([1, 1, 1])
    sz[0:np.size(n)] = n[:]

    szl = -np.floor(sz/2)
    szh = szl + sz

    x,y,z = np.meshgrid( np.arange(szl[0],szh[0]),
                         np.arange(szl[1],szh[1]),
                         np.arange(szl[2],szh[2]), indexing='ij', sparse=True)

    r = np.sqrt(x*x + y*y + z*z)

    m = np.zeros(sz.tolist())

#    edgezone = np.where( (x*x + y*y + z*z >= mask_radius) & (x*x + y*y + z*z <= np.square(mask_radius + edge_width)))

    edgezone = np.all( [ (x*x + y*y + z*z >= mask_radius), (x*x + y*y + z*z <= np.square(mask_radius + edge_width))], axis=0)
    m[edgezone] = 0.5 + 0.5*np.cos( 2*np.pi*(r[edgezone] - mask_radius) / (2*edge_width))
    m[ np.all( [ (x*x + y*y + z*z <= mask_radius*mask_radius) ], axis=0 ) ] = 1

#    m[ np.where(x*x + y*y + z*z <= mask_radius*mask_radius)] = 1

    return m