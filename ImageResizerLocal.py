__author__ = 'Andrew'

from PIL import Image
sizes = [(120,120), (720,720), (1600,1600)]
files = ['test.jpg']

for img in files:
    for size in sizes:
        #Image.open(img).thumbnail(size).save("thumbnail_%s_%s" % (img, "_".join(size)))
        #print(size[0])
        im = Image.open(img)
        im.thumbnail(size)
        #print "thumbnail_%s_%s" % (str(size[0]), img)
        im.save("thumbnail_%s_%s" % (str(size[0]), img))
