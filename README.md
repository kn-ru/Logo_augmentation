# Logo Augmentation
A class is presented that allows you to do hard augmentation for any logos (brands). Refers to the task of detecting logos / brands in image
### Prerequisites
* Python 3.5+
* opencv, imutils, numpy, random, math, pillow
### Usage

    # Import class
    from logo_augmentation import HardAugmentation as HA
    # Define path to logo and image
    logo_path = '../MAC.png'
    image_path = '../sample1.jpg'
    
    logo = cv2.imread(logo_path, cv2.IMREAD_COLOR)
    img = cv2.imread('../sample1.jpg', cv2.IMREAD_COLOR)
    
