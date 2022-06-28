import sys
import cv2
import os
import glob
import numpy as np
import shutil
import pdb
odir=sys.argv[1] # ....json

ddir = 'database/DAVIS/JPEGImages/Full-Resolution/%s*'%odir
os.makedirs('tmp/%s'%odir, exist_ok=True)
os.makedirs('tmp/%s-mask'%odir, exist_ok=True)
os.makedirs('tmp/%s-masked'%odir, exist_ok=True)

for dpath in sorted(glob.glob(ddir)):
    seqname=dpath.rsplit('/',1)[1]
    for fpath in sorted(glob.glob('%s/*.jpg'%dpath)):
        print(fpath)
        fid=fpath.rsplit('/',1)[1]
        shutil.copyfile(fpath, 'tmp/%s/%s-%s'%(odir, seqname, fid))

        imgmask = cv2.imread(fpath.replace('JPEGImages', 'Annotations').replace('.jpg', '.png'),0)
        imgmask = imgmask==0
        cv2.imwrite('tmp/%s-mask/%s-%s.png'%(odir, seqname, fid), (imgmask).astype(int)*255)

        img = cv2.imread(fpath)
        imgmask = imgmask.astype(float)[...,None]
        h,w,_ = img.shape
        img_masked = img*imgmask + 255*np.random.rand(h,w,3)*(1-imgmask)
        #img_masked = img*imgmask + 128*(1-imgmask)
        cv2.imwrite('tmp/%s-masked/%s-%s'%(odir, seqname, fid), img_masked)
