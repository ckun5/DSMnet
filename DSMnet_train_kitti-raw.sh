#!/usr/bin/env bash
# -*- coding: UTF-8 -*-

dir_kitti=/media/qjc/D/data/kitti
dataset=kitti-raw
root=$dir_kitti
dataset_val=kitti2012-tr_kitti2015-tr
root_val=$dir_kitti
net=dispnetcorr # dispnet/dispnetcorr/iresnet/gcnet
loss_name=depthmono-mask # supervised/(common/depthmono/SsSMnet/Cap_ds_lr)[-mask]
bt=4


python main.py --mode train --net $net --loss_name $loss_name --batchsize $bt --epochs 100 \
               --lr 0.0001 --lr_epoch0 40 --lr_stride 15 \
               --dataset $dataset --root $root --dataset_val $dataset_val --root_val $root_val \
               --val_freq 1 --print_freq 20
