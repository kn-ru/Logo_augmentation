# Logo Augmentation
A class is presented that allows you to do hard augmentation for any logos (brands). Refers to the task of detecting logos / brands in image
### Prerequisites
* Python 3.5+
* opencv, imutils, numpy, random, math, pillow
### Usage
The logo image should contain a black background. Here is an example of the McDonalds logo
[![000.jpg](https://i.postimg.cc/85swJd7t/000.jpg)](https://postimg.cc/yg402ZXZ)

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
    #Result
    image, target = HA(img.copy(), logo)
```

---

```python
    ground_show = image.copy()
    plt.rcParams['figure.figsize'] = 18,10
    ground_show = cv2.rectangle(ground_show, (target[0], target[1]), (target[2], target[3]) , (0,0,255), 5)
    plt.imshow(cv2.cvtColor(ground_show, cv2.COLOR_BGR2RGB))
    plt.title('Result', fontsize=15)
    plt.axis('off');
```
### Reference
Part of the code for the logo rotate in 3D is taken from [here](https://github.com/eborboihuc/rotate_3d)
