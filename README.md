# Logo Augmentation
A class is presented that allows you to do hard augmentation for any logos (brands). Refers to the task of detecting logos / brands in image
### Prerequisites
* Python 3.5+
* opencv, imutils, numpy, random, math, pillow
### Usage
```python
    # Import class
    from logo_augmentation import HardAugmentation
    
    # Define path to logo and image
    logo_path = 'MAC.png'
    image_path = 'sample1.jpg'
    logo = cv2.imread(logo_path, cv2.IMREAD_COLOR)
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    
    #Сreate class instance
    HA = HardAugmentation(logo_path, prob_color = 0.0001, prob_scale = 0.6, prob_rotate = 0.99, 
                          prob_rotate3d = 0.999, prob_crop = 0.6)
    
    
```
