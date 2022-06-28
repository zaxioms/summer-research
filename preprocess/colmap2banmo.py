import pdb
import numpy as np
import sys
import os
import cv2
import json
import pdb
import configparser

cam_path=sys.argv[1] # ....json
seqname=sys.argv[2] # cat-pikachiu05
out_path = '../banmo-bg/misc/rtks/%s/'%seqname

# load cameras
cams = json.load(open(cam_path))
num_frames = cams['tot_fr']
Kmat = np.asarray([cams['fl_x'], cams['fl_y'], cams['cx'], cams['cy']])
cams = sorted(cams['frames'], key=lambda x: x['file_path'])


id_map = []
cids = np.asarray([int(i['file_path'][:-4].split('-')[-1]) for i in cams]) # colmap idx
for tidx in range(0,num_frames):
    cidx = np.abs(tidx - cids).argmin()
    id_map.append(cidx) 

cam_mat = []
for tidx in range(0,num_frames):
    cam = cams[id_map[tidx]]
    print('%04d, %s'%(tidx,cam['file_path']))
    rt = np.asarray(cam['transform_matrix'])
    rmat = rt[:3,:3]
    tmat = rt[:3,3]
    camtxt = np.zeros((4,4))

    #camtxt[:3,:3] = rmat
    #camtxt[:3,3] = tmat
    camtxt[:3,:3] = rmat.T
    camtxt[:3,3] = -rmat.T.dot(tmat[...,None])[...,0]
    camtxt[3] = Kmat
    cam_mat.append(camtxt)
cam_mat = np.asarray(cam_mat)

os.makedirs(out_path, exist_ok = True)
for tidx in range(0,num_frames):
    camtxt = cam_mat[tidx]
    np.savetxt( '%s/cam-%05d.txt'%(out_path,tidx), camtxt)

#TODO add configs
config = configparser.RawConfigParser()
config['data'] = {
'dframe': '1',
'init_frame': '0',
'end_frame': '-1',
'can_frame': '-1'}

config['data_0'] = {
'ks': ' '.join( [str(i) for i in Kmat] ),
'datapath': 'database/DAVIS/JPEGImages/Full-Resolution/%s/'%seqname,
'rtk_path': 'misc/rtks/%s/cam'%seqname,
}

with open('configs/bg-%s.config'%(seqname), 'w') as configfile:
    config.write(configfile)
