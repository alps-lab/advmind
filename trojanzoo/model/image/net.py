# -*- coding: utf-8 -*-
from ..imagemodel import _ImageModel, ImageModel

from collections import OrderedDict

import torch.nn as nn
from torch.utils import model_zoo
from torchvision.models.resnet import model_urls
import torchvision.models as models


class _Net(_ImageModel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.features = nn.Sequential(OrderedDict([
            ('conv1', nn.Conv2d(1, 32, 3, 1)),
            ('relu1', nn.ReLU()),
            ('conv2', nn.Conv2d(32, 64, 3, 1)),
            ('relu2', nn.ReLU()),
        ]))
        self.pool = nn.Sequential(OrderedDict([
            ('maxpool', nn.MaxPool2d(2)),
            ('dropout', nn.Dropout2d(0.25)),
        ]))


class Net(ImageModel):

    def __init__(self, name='net', model_class=_Net, **kwargs):
        super().__init__(name=name, model_class=model_class,
                         conv_dim=9216, fc_depth=2, fc_dim=128, **kwargs)
