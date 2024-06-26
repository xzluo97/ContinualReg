# -*- coding: utf-8 -*-
"""
Spatial transformer module for image registration.

__author__ = Xinzhe Luo
__version__ = 0.1

"""
import torch
import torch.nn as nn
# import torch.nn.functional as F
from core.register.SpatialTransformer import SpatialTransformer


class VectorIntegration(nn.Module):
    def __init__(self, size, int_steps=0, **kwargs):
        super(VectorIntegration, self).__init__()
        self.size = size
        self.int_steps = int_steps
        self.kwargs = kwargs
        self.transform = SpatialTransformer(self.size)

    def forward(self, flow):
        """

        :param flow: tensor of shape [batch, dimension, *vol_shape]
        :return:
        """
        if self.int_steps:
            vec = torch.div(flow, 2**self.int_steps)
            # assert vec.norm(p=2, dim=1).max().item() < 0.5, "The maximal vector norm must be less than 0.5!"
            for _ in range(self.int_steps):
                vec = vec + self.transform(vec, vec, padding_mode='zeros')
            return vec
        else:
            return flow
