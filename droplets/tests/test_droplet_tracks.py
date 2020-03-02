'''
Created on Jul 18, 2018

.. codeauthor:: David Zwicker <david.zwicker@ds.mpg.de>
'''

import tempfile

import pytest
import numpy as np

from pde.grids import UnitGrid
from pde.tools.misc import skipUnlessModule

from ..droplets import SphericalDroplet, DiffuseDroplet
from ..droplet_tracks import DropletTrack, DropletTrackList
from ..emulsions import Emulsion, EmulsionTimeCourse



def test_droplettrack():
    """ test some droplet track functions """
    t1 = DropletTrack()
    for i in range(4):
        t1.append(SphericalDroplet([i], i), i)
        
    for track, length in [(t1, 4), (t1[:2], 2)]:
        assert len(track) == length        
        assert track.dim == 1 
        assert track.start == 0
        assert track.end == length - 1
        assert track.times == list(range(length))
        assert [t for t, _ in track.items()] == list(range(length))
        assert isinstance(str(track), str)
        assert isinstance(repr(track), str)
        np.testing.assert_array_equal(track.data['time'], np.arange(length))
        
    assert t1 == t1[:]
    assert t1[3:3] == DropletTrack()
            


@skipUnlessModule("h5py")
def test_droplettrack_io():
    """ test writing and reading droplet tracks """
    t1 = DropletTrack()
    ds = [DiffuseDroplet([0, 1], 10, 0.5)] * 2
    t2 = DropletTrack(droplets=ds, times=[0, 10])
    
    for t_out in [t1, t2]:
        fp = tempfile.NamedTemporaryFile(suffix='.hdf5')
        t_out.to_file(fp.name)
        t_in = DropletTrack.from_file(fp.name)
        assert t_in == t_out
        assert t_in.times == t_out.times
        assert t_in.droplets == t_out.droplets
    
    
    
@skipUnlessModule("matplotlib")
def test_droplettrack_plotting():
    """ test writing and reading droplet tracks """
    ds = [DiffuseDroplet([0, 1], 10, 0.5)] * 2
    t = DropletTrack(droplets=ds, times=[0, 10])
    t.plot()
    t.plot(grid=UnitGrid([5, 5], periodic=True))
    
    t = DropletTrack()
    with pytest.raises(NotImplementedError):
        t.plot()
    


@skipUnlessModule("h5py")
def test_droplettracklist_io():
    """ test writing and reading droplet tracks """
    t1 = DropletTrack()
    ds = [DiffuseDroplet([0, 1], 10, 0.5)] * 2
    t2 = DropletTrack(droplets=ds, times=[0, 10])
    tl_out = DropletTrackList([t1, t2])
    
    fp = tempfile.NamedTemporaryFile(suffix='.hdf5')
    tl_out.to_file(fp.name)
    tl_in = DropletTrackList.from_file(fp.name)
    assert tl_in == tl_out
        
        
        
def test_conversion_from_emulsion_timecourse():
    """ test converting between DropletTrackList and EmulsionTimecourse """
    d1 = SphericalDroplet([0, 1], 5)
    d2 = SphericalDroplet([10, 15], 4)
    times = [0, 10]
    
    dt1 = DropletTrack([d1]*2, times=times)
    dt2 = DropletTrack([d2]*2, times=times)
    dtl1 = DropletTrackList([dt1, dt2])
    
    e = Emulsion([d1, d2])
    etc = EmulsionTimeCourse([e, e], times=times)
    dtl2 = DropletTrackList.from_emulsion_time_course(etc)

    assert dtl1 == dtl2
    