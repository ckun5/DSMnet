#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import torch
from torch.autograd import Variable
import sys
sys.path.append("../")
import models
    
if __name__ == "__main__":
    img_shape = [1, 3, 257, 513]
    imL = Variable(torch.randn(img_shape), volatile=True).cuda()
    imR = Variable(torch.randn(img_shape), volatile=True).cuda()
    
    for modelname in models.dict_models:
        model = models.model_create_by_name(modelname)
        print("model: %s" % model.name)
        _, disps = model(imL, imR, mode="test")
        print("input: %s \noutput: %s \nPassed! \n" % (str(imL.shape), str(disps[0].shape)))

