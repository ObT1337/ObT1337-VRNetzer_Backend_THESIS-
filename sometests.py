
import PIL
from PIL import Image
import random
import numpy

new_menu = ['Hawaiian', 'Margherita', 'Mushroom', 'Prosciutto', 'Meat Feast', 'Hawaiian', 'Bacon', 'Black Olive Special', 'Sausage', 'Sausage']

final_new_menu = list(dict.fromkeys(new_menu))

print(final_new_menu)

im = Image.open('static/projects/sphere/layouts/3DimSphere_layoutXYZ.bmp', 'r')
width, height = im.size
pixel_values = list(im.getdata())
print(pixel_values[len(pixel_values)-1])

for x in pixel_values:
    if x[0] == 0 and x[1] == 0 and x[1] == 0:
        y = 100
    else:
        print(x[0])
print(len(pixel_values))







def write_image():
    new_im = Image.new('RGB', (128, 128))
    i = 0
    k = random.randrange(10,255)
    l = random.randrange(10,255)
    m = random.randrange(10,255)
    for y in range (128):
        for x in range (128):
            r = (i % k)
            h = (i % l)
            q = (i % m)
            #new_im.putpixel((x, y), ((128 - x)*2, x*2, y*2))\
            new_im.putpixel((x, y), (r, h, q))

            i+=1
    #print(h)
    url = 'static/img/test.bmp'
    new_im.save(url)
    
def rescaleImg():
    new_im = Image.new('RGB', (512, 512))

    img = PIL.Image.open("test10.bmp").convert("RGB")
    imgarr = numpy.array(img)
    print(imgarr[0][0,0])
    #for i in imgarr[0]:
    #   print(imgarr[0][i])

#rescaleImg()