"""
Classes extending Spherical droplet to include two extra parameters related to mesh size and cavitation threshold


.. autosummary::
   :nosignatures:

   HeterogenousSphericalDroplet


The details of the classes are explained below:

.. codeauthor:: Estefania Vidal <estefania.vidal@ds.mpg.de>
"""

from abc import abstractmethod, ABCMeta
import logging
from typing import (List, Optional, TypeVar, Sequence, Dict,  # @UnusedImport
                    TYPE_CHECKING)  

import numpy as np
from numpy.lib.recfunctions import structured_to_unstructured
from scipy import integrate
from .droplets import SphericalDroplet



class HeterogenousSphericalDroplet(SphericalDroplet):
    """ Represents a single, spherical droplet with an associated mesh size
    and local cavitation pressure. """
    
    def __init__(self, position: Sequence[float], radius: float, 
                 mesh_size: float,
                barrier_height: float):
        r""" 
        Args:
            position (:class:`numpy.ndarray`):
                Position of the droplet center
            radius (float):
                Radius of the droplet
            mesh_size (float):
                Mesh size at the droplet location
            barrier_height (float):
                Local highest equilibrium concentration 
            
        """
        self._init_data(position=position)
        
        self.position = position
        self.radius = radius
        self.mesh_size = mesh_size
        self.barrier_height = barrier_height
        self.check_data()
        
    @classmethod
    def get_dtype(cls, position):
        position = np.atleast_1d(position)
        dim = len(position)
        return [('position', float, (dim,)), ('radius', float),('mesh_size',float),('barrier_height',float)]
    
#     Setters and getters
    @property
    def mesh_size(self) -> float:
        return float(self.data['mesh_size'])
    
    @mesh_size.setter
    def mesh_size(self, value: float):
        self.data['mesh_size'] = value
        
    @property
    def barrier_height(self) -> float:
        return float(self.data['barrier_height'])
    
    @barrier_height.setter
    def barrier_height(self, value: float):
        self.data['barrier_height'] = value


