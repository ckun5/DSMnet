import torch
import torch.nn.functional as F
from torch.autograd import Variable
from math import exp

def gaussian(window_size, sigma):
    gauss = torch.Tensor([exp(-(x - window_size//2)**2/float(2*sigma**2)) for x in range(window_size)])
    return gauss/gauss.sum()

def create_window(window_size, channel):
    _1D_window = gaussian(window_size, 1.5).unsqueeze(1)
    _2D_window = _1D_window.mm(_1D_window.t()).float().unsqueeze(0).unsqueeze(0)
    window = Variable(_2D_window.expand(channel, 1, window_size, window_size).contiguous(), requires_grad=False)
    return window

def smooth_gaussian(img, window_size=7):
    (_, channel, _, _) = img.size()
    window = create_window(window_size, channel)
    if img.is_cuda:
        window = window.cuda(img.get_device())
    window = window.type_as(img)
    return F.conv2d(img, window, padding = window_size//2, groups = channel)

def _ssim(img1, img2, window, window_size, channel):
    window = window.transpose(0,1) / channel
    mu1 = F.conv2d(img1, window, padding = window_size//2, groups = 1)
    mu2 = F.conv2d(img2, window, padding = window_size//2, groups = 1)

    mu1_sq = mu1.pow(2)
    mu2_sq = mu2.pow(2)
    mu1_mu2 = mu1*mu2

    sigma1_sq = F.conv2d(img1*img1, window, padding = window_size//2, groups = 1) - mu1_sq
    sigma2_sq = F.conv2d(img2*img2, window, padding = window_size//2, groups = 1) - mu2_sq
    sigma12 = F.conv2d(img1*img2, window, padding = window_size//2, groups = 1) - mu1_mu2

    scale = 1
    C1 = (scale * 0.01)**2
    C2 = (scale * 0.03)**2

    ssim_map = ((2*mu1_mu2 + C1)*(2*sigma12 + C2))/((mu1_sq + mu2_sq + C1)*(sigma1_sq + sigma2_sq + C2))
    return ssim_map

def _ssim1(img1, img2, window, window_size, channel):
    mu1 = F.conv2d(img1, window, padding = window_size//2, groups = channel)
    mu2 = F.conv2d(img2, window, padding = window_size//2, groups = channel)

    mu1_sq = mu1.pow(2)
    mu2_sq = mu2.pow(2)
    mu1_mu2 = mu1*mu2

    sigma1_sq = F.conv2d(img1*img1, window, padding = window_size//2, groups = channel) - mu1_sq
    sigma2_sq = F.conv2d(img2*img2, window, padding = window_size//2, groups = channel) - mu2_sq
    sigma12 = F.conv2d(img1*img2, window, padding = window_size//2, groups = channel) - mu1_mu2

    scale = 1
    C1 = (scale * 0.01)**2
    C2 = (scale * 0.03)**2

    ssim_map = ((2*mu1_mu2 + C1)*(2*sigma12 + C2))/((mu1_sq + mu2_sq + C1)*(sigma1_sq + sigma2_sq + C2))
    return ssim_map

def _ssim0(img1, img2, window, window_size, channel):
    mu1 = F.conv2d(img1, window, padding = window_size//2, groups = channel)
    mu2 = F.conv2d(img2, window, padding = window_size//2, groups = channel)

    mu1_sq = mu1.pow(2)
    mu2_sq = mu2.pow(2)
    mu1_mu2 = mu1*mu2

    dimg1 = (img1 - mu1)
    dimg2 = (img2 - mu2)
    sigma1_sq = F.conv2d(dimg1*dimg1, window, padding = window_size//2, groups = channel)
    sigma2_sq = F.conv2d(dimg2*dimg2, window, padding = window_size//2, groups = channel)
    sigma12 = F.conv2d(dimg1*dimg2, window, padding = window_size//2, groups = channel)

    scale = 1
    C1 = (scale * 0.01)**2
    C2 = (scale * 0.03)**2

    ssim_map = ((2*mu1_mu2 + C1)*(2*sigma12 + C2))/((mu1_sq + mu2_sq + C1)*(sigma1_sq + sigma2_sq + C2))
    return ssim_map

def ssimfun(img1, img2, window_size = 11):
    (_, channel, _, _) = img1.size()
    window = create_window(window_size, channel)
    
    if img1.is_cuda:
        window = window.cuda(img1.get_device())
    window = window.type_as(img1)
    
    return _ssim(img1, img2, window, window_size, channel)

class SSIM(torch.nn.Module):
    def __init__(self, window_size = 11):
        super(SSIM, self).__init__()
        self.window_size = window_size
        self.channel = 1
        self.window = create_window(window_size, self.channel)

    def forward(self, img1, img2):
        (_, channel, _, _) = img1.size()

        if channel == self.channel and self.window.data.type() == img1.data.type():
            window = self.window
        else:
            window = create_window(self.window_size, channel)
            
            if img1.is_cuda:
                window = window.cuda(img1.get_device())
            window = window.type_as(img1)
            
            self.window = window
            self.channel = channel


        return _ssim(img1, img2, window, self.window_size, channel)
