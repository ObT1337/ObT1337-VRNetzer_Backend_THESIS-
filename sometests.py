
from PIL import Image
import random


row = [406943]

sl = int(row[0]) % 128
s = int(int(row[0]) / 128) % 128
sb = int(int(row[0]) / 16384)

reverse = sb * 16384 + s * 128 + sl

print(str(row[0]) + ' -> r = ' + str(s) + ' g = ' + str(sl) + ' b = ' + str(sb) + " --> " + str(reverse))

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
    