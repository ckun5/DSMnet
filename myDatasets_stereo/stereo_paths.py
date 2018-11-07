#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
get paths of stereo dataset
'''

import os
import glob
import logging
#logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')

class paths_stereo(object):
    '''stereo_paths'''
    def __init__(self, rootpath):
        self.flag_dataset = None
        self.rootpath = rootpath
        self.n_root = len(rootpath)
        self.flag_img_left_right = [None, None]
        self.flag_img_disp_left = [None, None]
        self.flag_disp_left_right = [None, None]
        self.flag_img_type = None
        self.flag_disp_type = None
        self.flag_same_type = True
        self.str_filter = None
        self.paths_all = []

    def get_group_from_left(self, path_img_left):
        paths = [path_img_left]
        # 防止根路径中存在干扰信息
        subpath_img_left = path_img_left[self.n_root:]
        
        # subpath_img_right
        subpath_img_right = subpath_img_left.replace(*self.flag_img_left_right)
        paths.append(self.rootpath + subpath_img_right)
        
        # subpath_disp_left
        if(self.flag_img_disp_left[0] is None):
            return paths
        subpath_disp_left = subpath_img_left.replace(*self.flag_img_disp_left)
        if(not self.flag_same_type):
            subpath_disp_left = subpath_disp_left.replace(self.flag_img_type, self.flag_disp_type)
        paths.append(self.rootpath + subpath_disp_left)
        
        # subpath_disp_right
        if(self.flag_disp_left_right[0] is None):
            return paths
        subpath_disp_right = subpath_disp_left.replace(*self.flag_disp_left_right)
        paths.append(self.rootpath + subpath_disp_right)
        
        return paths

    def get_paths_all(self, str_filter_glob, flag_sort=False):
        logging.debug('str_filter_glob:' + str_filter_glob)
        paths_img_left = glob.glob(str_filter_glob)
        if(flag_sort): paths_img_left.sort()
        logging.debug('根据str_filter_glob得到的文件个数：%d' % len(paths_img_left))
        paths_group = []
        for path_img_left in paths_img_left:
            path_group = self.get_group_from_left(path_img_left)
            paths_group.append(path_group)
            #if(len(paths_group)>100):break
        return paths_group
    
    def get_paths_all_from_list(self, root, flag_sort=False):
        paths_group = []
        if(not os.path.isdir(root)):
            return paths_group
        path_list_all = os.path.join(root, 'paths_stereo.txt')
        if(not os.path.isfile(path_list_all)):
            return paths_group
        # 读取所有文件路径
        f = open(path_list_all, 'r')
        Lines = f.readlines()
        f.close()
        paths = []
        for i in range(len(Lines)):
            filename = Lines[i].strip()
            if(filename == ''):
                continue
            tpath = os.path.join(root, filename)
            assert os.path.isfile(tpath)
            paths.append([])
            f = open(tpath, 'r')
            tLines = f.readlines()
            f.close()
            for j in range(len(tLines)):
                filepath = tLines[j].strip()
                if(filepath == ''):
                    continue
                assert os.path.isfile(filepath)
                paths[-1].append(filepath)
            if(len(paths) > 1):
                assert len(paths[-1])==len(paths[-2])
        # 对文件路径进行重新分组
        for i in range(len(paths[0])):
            paths_group_t = []
            for j in range(len(paths)):
                paths_group_t.append(paths[j][i])
            paths_group.append(paths_group_t)
        
        return paths_group

    def get_paths_idx(self, idx):
        assert idx < len(self.paths_all), 'dataset[%s] do not exist!' % (self.flag_dataset)
        return self.paths_all[idx]

    @property
    def count(self):
        return len(self.paths_all)


class paths_list(paths_stereo):
    '''paths_list'''
    def __init__(self, rootpath):
        super(paths_list, self).__init__(rootpath)
        self.flag_dataset = 'list(%s)' % os.path.basename(rootpath)
        self.paths_all = self.get_paths_all_from_list(rootpath)

class paths_monkaa(paths_stereo):
    '''paths_monkaa'''
    def __init__(self, rootpath):
        super(paths_monkaa, self).__init__(rootpath)
        self.flag_dataset = 'monkaa'
        self.flag_img_left_right = ['left', 'right']
        self.flag_img_disp_left = ['frames_finalpass_webp', 'disparity'] # [None, None] # 
        self.flag_disp_left_right = ['left', 'right'] # [None, None] # 
        self.flag_img_type = '.webp'
        self.flag_disp_type = '.pfm'
        self.flag_same_type = False
        self.str_filter = rootpath + '/monkaa/frames_finalpass_webp/*/left/*.webp'
        self.paths_all = self.get_paths_all(self.str_filter)

class paths_driving(paths_stereo):
    '''paths_driving'''
    def __init__(self, rootpath):
        super(paths_driving, self).__init__(rootpath)
        self.flag_dataset = 'driving'
        self.flag_img_left_right = ['left', 'right']
        self.flag_img_disp_left = ['frames_finalpass_webp', 'disparity'] # [None, None] # 
        self.flag_disp_left_right = ['left', 'right'] # [None, None] # 
        self.flag_img_type = '.webp'
        self.flag_disp_type = '.pfm'
        self.flag_same_type = False
        self.str_filter = rootpath + '/driving/frames_finalpass_webp/*/*/*/left/*.webp'
        self.paths_all = self.get_paths_all(self.str_filter)

class paths_flyingthings3d_train(paths_stereo):
    '''paths_flyingthings3d_train'''
    def __init__(self, rootpath):
        super(paths_flyingthings3d_train, self).__init__(rootpath)
        self.flag_dataset = 'flyingthings3d-tr'
        self.flag_img_left_right = ['left', 'right']
        self.flag_img_disp_left = ['frames_finalpass_webp', 'disparity']
        self.flag_disp_left_right = ['left', 'right']
        self.flag_img_type = '.webp'
        self.flag_disp_type = '.pfm'
        self.flag_same_type = False
        self.str_filter = rootpath + '/flyingthings3d/frames_finalpass_webp/TRAIN/*/*/left/*.webp'
        self.paths_all = self.get_paths_all(self.str_filter)

class paths_flyingthings3d_test(paths_stereo):
    '''paths_flyingthings3d_test'''
    def __init__(self, rootpath):
        super(paths_flyingthings3d_test, self).__init__(rootpath)
        self.flag_dataset = 'flyingthings3d-te'
        self.flag_img_left_right = ['left', 'right']
        self.flag_img_disp_left = ['frames_finalpass_webp', 'disparity']
        self.flag_disp_left_right = ['left', 'right']
        self.flag_img_type = '.webp'
        self.flag_disp_type = '.pfm'
        self.flag_same_type = False
        self.str_filter = rootpath + '/flyingthings3d/frames_finalpass_webp/TEST/*/*/left/*.webp'
        self.paths_all = self.get_paths_all(self.str_filter)

class paths_kitti2015_train(paths_stereo):
    '''paths_kitti2015_train'''
    def __init__(self, rootpath):
        super(paths_kitti2015_train, self).__init__(rootpath)
        self.flag_dataset = 'kitti15-tr'
        self.flag_img_left_right = ['image_2', 'image_3']
        self.flag_img_disp_left = ['image_2', 'disp_occ_0']
        self.flag_disp_left_right = [None, None]
        self.flag_img_type = '.png'
        self.flag_disp_type = '.png'
        self.flag_same_type = True
        self.str_filter = rootpath + '/data_scene_flow/training/image_2/*_10.png'
        self.paths_all = self.get_paths_all(self.str_filter, flag_sort=True)

class paths_kitti2015_test(paths_stereo):
    '''paths_kitti2015_test'''
    def __init__(self, rootpath):
        super(paths_kitti2015_test, self).__init__(rootpath)
        self.flag_dataset = 'kitti15-te'
        self.flag_img_left_right = ['image_2', 'image_3']
        self.flag_img_disp_left = [None, None]
        self.flag_disp_left_right = [None, None]
        self.flag_img_type = '.png'
        self.flag_disp_type = '.png'
        self.flag_same_type = True
        self.str_filter = rootpath + '/data_scene_flow/testing/image_2/*_10.png'
        self.paths_all = self.get_paths_all(self.str_filter, flag_sort=True)

class paths_kitti2012_train(paths_stereo):
    '''paths_kitti2012_train'''
    def __init__(self, rootpath):
        super(paths_kitti2012_train, self).__init__(rootpath)
        self.flag_dataset = 'kitti12-tr'
        self.flag_img_left_right = ['colored_0', 'colored_1']
        self.flag_img_disp_left = ['colored_0', 'disp_occ']
        self.flag_disp_left_right = [None, None]
        self.flag_img_type = '.png'
        self.flag_disp_type = '.png'
        self.flag_same_type = True
        self.str_filter = rootpath + '/data_stereo_flow/training/colored_0/*_10.png'
        self.paths_all = self.get_paths_all(self.str_filter, flag_sort=True)

class paths_kitti2012_test(paths_stereo):
    '''paths_kitti2012_test'''
    def __init__(self, rootpath):
        super(paths_kitti2012_test, self).__init__(rootpath)
        self.flag_dataset = 'kitti12-te'
        self.flag_img_left_right = ['colored_0', 'colored_1']
        self.flag_img_disp_left = [None, None]
        self.flag_disp_left_right = [None, None]
        self.flag_img_type = '.png'
        self.flag_disp_type = '.png'
        self.flag_same_type = True
        self.str_filter = rootpath + '/data_stereo_flow/testing/colored_0/*_10.png'
        self.paths_all = self.get_paths_all(self.str_filter, flag_sort=True)

class paths_kitti_raw(paths_stereo):
    '''paths_kitti_raw'''
    def __init__(self, rootpath):
        super(paths_kitti_raw, self).__init__(rootpath)
        self.flag_dataset = 'kitti-raw'
        self.flag_img_left_right = ['image_02', 'image_03']
        self.flag_img_disp_left = [None, None]
        self.flag_disp_left_right = [None, None]
        self.flag_img_type = '.png'
        self.flag_disp_type = '.png'
        self.flag_same_type = True
        self.str_filter = rootpath + '/raw/*/*/image_02/data/*.png'
        self.paths_all = self.get_paths_all(self.str_filter)

class paths_stereo_by_name(object):
    '''dataset_paths'''
    def __init__(self, flag_dataset='kitti-raw', rootpath='./'):
        self.__init_sucessed__ = False
        self.flag_dataset = flag_dataset
        self.rootpath = rootpath
        self.paths_all = self.get_paths_all_from_dataset(flag_dataset, rootpath)

    def get_paths_all_from_dataset(self, flag_dataset, rootpath):
        paths_all = []
        if(flag_dataset.lower()=='kitti-raw'):
            paths_all = paths_kitti_raw(rootpath).paths_all
        elif(flag_dataset.lower()=='kitti2012-te'):
            paths_all = paths_kitti2012_test(rootpath).paths_all
        elif(flag_dataset.lower()=='kitti2012-tr'):
            paths_all = paths_kitti2012_train(rootpath).paths_all
        elif(flag_dataset.lower()=='kitti2015-te'):
            paths_all = paths_kitti2015_test(rootpath).paths_all
        elif(flag_dataset.lower()=='kitti2015-tr'):
            paths_all = paths_kitti2015_train(rootpath).paths_all
        elif(flag_dataset.lower()=='flyingthings3d-te'):
            paths_all = paths_flyingthings3d_test(rootpath).paths_all
        elif(flag_dataset.lower()=='flyingthings3d-tr'):
            paths_all = paths_flyingthings3d_train(rootpath).paths_all
        elif(flag_dataset.lower()=='driving'):
            paths_all = paths_driving(rootpath).paths_all
        elif(flag_dataset.lower()=='monkaa'):
            paths_all = paths_monkaa(rootpath).paths_all
        elif(flag_dataset.lower()=='stereo-list'):
            self.flag_dataset = 'list(%s)' % os.path.basename(rootpath)
            paths_all = paths_list(rootpath).paths_all
        else:
            msg = '暂不支持的数据集: \n '
            msg = '目前只支持以下数据集: \n '
            msg += 'kitti-raw \n '
            msg += 'kitti2012-te \n kitti2012-tr \n '
            msg += 'kitti2015-te \n kitti2015-tr \n '
            msg += 'flyingthings3d-te \n flyingthings3d-tr \n '
            msg += 'driving \n monkaa \n '
            msg += 'stereo-list \n '
            msg += '你想要使用的数据集名称为　\n %s \n ' % flag_dataset.lower()
            msg += '请检查数据集名称! \n '
            logging.info(msg)
        if(paths_all==[]):
            self.__init_sucessed__ = False
        else:
            self.__init_sucessed__ = True
        return paths_all

    def get_paths_idx(self, idx):
        assert self.__init_sucessed__, 'dataset[%s] do not exist!' % (self.flag_dataset)
        return self.paths_all[idx]

    @property
    def count(self):
        return len(self.paths_all)

