# ------------------------------------------------------------------------------
# The code is from VPD (https://github.com/wl-zhao/VPD).
# For non-commercial purpose only (research, evaluation etc).
# ------------------------------------------------------------------------------

import os
import cv2
import numpy as np
from dataset.base_dataset import BaseDataset
import json
import random
import torch
import copy

class kitti(BaseDataset):
    def __init__(self, data_path, filenames_path='./dataset/filenames/',
                 is_train=True, crop_size=None, args=None):
        super().__init__(crop_size, args)
        self.is_train = is_train
        self.data_path = data_path
        self.args = args

        txt_path = os.path.join(filenames_path, 'kitti_eigen_split')
        if is_train:
            txt_path += '/eigen_train_files_with_gt.txt'
        else:
            txt_path += '/eigen_test_files_with_gt.txt'
        
        self.filenames_list = self.readTXT(txt_path) # debug
        phase = 'train' if is_train else 'test'
        print("Dataset: Kitti")
        print("# of %s images: %d" % (phase, len(self.filenames_list)))

    def __len__(self):
        return len(self.filenames_list)

    def __getitem__(self, idx):
        
        sample_path = self.filenames_list[idx]
        rgb_file = sample_path.split()[0]
        depth_file = os.path.join(sample_path.split()[0].split('/')[0], sample_path.split()[1])

        if self.args.use_right is True and random.random() > 0.5:
            rgb_file.replace('image_02', 'image_03')
            depth_file.replace('image_02', 'image_03')

        img_path = os.path.join(self.data_path , "KITTI", rgb_file)
        gt_path = os.path.join(self.data_path, "kitti_gt", depth_file)

        filename = img_path.split('/')[-4] + '_' + img_path.split('/')[-1]
        
        image = cv2.imread(img_path)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) 
        depth = cv2.imread(gt_path, cv2.IMREAD_UNCHANGED).astype('float32')

        if self.args.do_kb_crop is True:
            height = image.shape[0]
            width = image.shape[1]
            top_margin = int(height - 352)
            left_margin = int((width - 1216) / 2)
            image = image[top_margin:top_margin + 352, left_margin:left_margin + 1216, :]
            depth = depth[top_margin:top_margin + 352, left_margin:left_margin + 1216]
            
        if self.args.cutflip:
            image,depth = self.cutflip(image,depth,None)
        if self.is_train:
            image, depth = self.augment_training_data(image, depth)
        else:
            image, depth = self.augment_test_data(image, depth)
            
        depth = depth / (256.0) # convert gt depth to meters
        return {'image': image, 'depth': depth, 'filename': filename}
    
    def cutflip(self,image,depth,h_graft=None):

        p = random.random()
        if p<0.5:
            return image,depth
        depth = depth[:,:,np.newaxis]
        image_copy = copy.deepcopy(image)
        depth_copy = copy.deepcopy(depth)
        
        h,w,c = image.shape
        N = 2    # split numbers
        h_list=[]      
        h_interval_list = []        # hight interval
        for i in range(N-1):
            if h_graft!=None:
                h_list.append(h_graft)
            else:
                h_list.append(random.randint(int(0.2*h),int(0.8*h)))
        h_list.append(h)
        h_list.append(0)  
        h_list.sort()
        h_list_inv = np.array([h]*(N+1))-np.array(h_list)
        for i in range(len(h_list)-1):
            h_interval_list.append(h_list[i+1]-h_list[i])

        for i in range(N):
            image[h_list[i]:h_list[i+1],:,:] = image_copy[h_list_inv[i]-h_interval_list[i]:h_list_inv[i],:,:]
            depth[h_list[i]:h_list[i+1],:,:] = depth_copy[h_list_inv[i]-h_interval_list[i]:h_list_inv[i],:,:]
        return image,depth
    