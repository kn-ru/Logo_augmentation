import numpy as np
from PIL import Image
import cv2
import random
import imutils
from image_transformer import ImageTransformer

class HardAugmentation(object):
    
    def __init__(self, logo_path, prob_color, prob_scale, prob_rotate, prob_rotate3d, prob_crop):
        self.logo_path = logo_path
        self.prob_color = prob_color
        self.prob_scale = prob_scale
        self.prob_rotate = prob_rotate
        self.prob_rotate3d = prob_rotate3d
        self.prob_crop = prob_crop
        self.it = ImageTransformer(self.logo_path, None)
    
    def __call__(self, ground, logo, two_step=False):
        rows_ground, cols_ground = ground.shape[:2]
        rows, cols, channels = logo.shape
        is_rotate=False
        is_scale=False
        # RANDOM ROTATE
        if random.random() < self.prob_rotate:
            is_rotate = True
            rotate_angle = random.randint(0,360)
            while rotate_angle%90==0:
                rotate_angle = random.randint(0,360)
            print('rotate_angle - ', rotate_angle)
            logo = self.rotate_image(logo, rotate_angle)
            rows, cols, channels = logo.shape
        #RANDON ROTATE 3D
        if random.random() < self.prob_rotate3d:
            is_rotate3d = True
            theta = random.randint(-70,70)
            phi = random.randint(-70,70)
            print('rotate3d - theta = {}, phi = {}'.format(theta, phi))
            logo = self.it.rotate_along_axis(theta=theta, phi=phi, dx = 5)
            rows, cols, channels = logo.shape

        if (max(logo.shape)) < ((ground.shape[1])/2):
            start_x = random.randint(1,ground.shape[1]-cols)
            start_y = random.randint(1,ground.shape[0]-rows)
            roi = ground[start_y:(start_y+rows), start_x:(start_x+cols)]
            
        else:
            logo = cv2.resize(logo, (int(ground.shape[1]/2), int(ground.shape[1]/2)))
            rows, cols, channels = logo.shape
            start_x = random.randint(1,ground.shape[1]-cols)
            start_y = random.randint(1,ground.shape[0]-rows)
            roi = ground[start_y:(start_y+rows), start_x:(start_x+cols)]
        # RANDOM SCALE
        if random.random() < self.prob_scale:
            is_scale = True
            scale_rate = random.randint(1,7)
            print('scale_rate - ', scale_rate)
            logo = cv2.resize(logo, (int(max(logo.shape)/scale_rate), int(max(logo.shape)/scale_rate)))
            rows, cols, channels = logo.shape
            rows_scale = rows
            cols_scale = cols
            start_x = random.randint(1,ground.shape[1]-cols)
            start_y = random.randint(1,ground.shape[0]-rows)
            roi = ground[start_y:(start_y+rows), start_x:(start_x+cols)]
               
        roi = ground[start_y:(start_y+rows), start_x:(start_x+cols)]
        logo_gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
        ret, mask_inv = cv2.threshold(logo_gray, 0, 255, cv2.THRESH_BINARY_INV)
        mask = cv2.bitwise_not(mask_inv)
        
        if random.random() < self.prob_crop:
            print('Random crop')
            mask[min(np.where(mask!=0)[0]):min(np.where(mask!=0)[0])+int(mask.shape[1]/10),:]=0
            mask_inv = cv2.bitwise_not(mask)
        
        
        ground_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
        logo_fg = cv2.bitwise_and(logo, logo, mask=mask)
        dst = cv2.add(ground_bg, logo_fg)
        _ = logo_fg.copy()
        # RANDOM COLOR
        if random.random() < self.prob_color:
            print('Random color')
            # set random color for each chanel
            _2 = (np.where(mask==255, np.random.randint(200,255, dtype='uint8'), 0))
            _1 = (np.where(mask==255, np.random.randint(200,255, dtype='uint8'), 0))
            _0 = (np.where(mask==255, np.random.randint(0,80, dtype='uint8'), 0))
            _[:,:,0] = _0
            _[:,:,1] = _1
            _[:,:,2] = _2
            dst = cv2.add(ground_bg, _)
        ground[start_y:(start_y+rows), start_x:(start_x+cols)] = dst
        target = (start_x,start_y,start_x+rows, start_y+cols)
        if is_rotate:
            target = (start_x+min(np.where(mask==255)[1]),start_y+min(np.where(mask==255)[0]),start_x+max(np.where(mask==255)[1]), start_y+max(np.where(mask==255)[0]))
        return ground, target
    
    @staticmethod
    def rotate_image(mat, angle):
        """
        Rotates an image (angle in degrees) and expands image to avoid cropping
        
        """

        height, width = mat.shape[:2] 
        image_center = (width/2, height/2) 
        rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1.)

        abs_cos = abs(rotation_mat[0,0]) 
        abs_sin = abs(rotation_mat[0,1])

        bound_w = int(height * abs_sin + width * abs_cos)
        bound_h = int(height * abs_cos + width * abs_sin)

        rotation_mat[0, 2] += bound_w/2 - image_center[0]
        rotation_mat[1, 2] += bound_h/2 - image_center[1]

        rotated_mat = cv2.warpAffine(mat, rotation_mat, (bound_w, bound_h))
        return rotated_mat