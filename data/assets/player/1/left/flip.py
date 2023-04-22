from PIL import Image, ImageFilter

def reverse(path):
    for i in range(5):
        im = Image.open(path + "RUN_00" + str(i) + ".png")
        img = im.transpose(Image.FLIP_LEFT_RIGHT)
        img.save(path + "RUN_00" + str(i) + ".png")


reverse("RUN/")

