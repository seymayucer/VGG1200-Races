import os
import pandas as pd
import numpy
from PIL import Image


class CustomDatasetDataLoader():

    def __init__(self, opt):
        self.meta_file = opt.meta_file
        pair_data = pd.read_csv(opt.meta_file,index_col=[0], header=[0,1])

        self.A_paths = pair_data[('A','filename')].apply(lambda x: '%s/%s'%(self.opt.dataroot,x)).values
        self.B_paths = pair_data[('B','filename')].apply(lambda x: '%s/%s'%(self.opt.dataroot,x)).values
        print(len(self.A_paths),len(self.B_paths))

        self.A_size = len(self.A_paths)  # get the size of dataset A
        self.B_size = len(self.B_paths)  # get the size of dataset B
        btoA = self.opt.direction == 'BtoA'
    
    def __getitem__(self, index):

        A_path = os.path.join(self.opt.dataroot, self.A_paths[index])
        B_path =os.path.join(self.opt.dataroot, self.B_paths[index])

        A_img = Image.open(A_path).convert('RGB')
        B_img = Image.open(B_path).convert('RGB')
        # apply image transformation
        A = self.transform_A(A_img)
        B = self.transform_B(B_img)

        return {'A': A, 'B': B, 'A_paths': A_path, 'B_paths': B_path}
  

    def __len__(self):
        """Return the total number of images in the dataset.

        As we have two datasets with potentially different number of images,
        we take a maximum of
        """
        return max(self.A_size, self.B_size)