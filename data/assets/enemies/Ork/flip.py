from PIL import Image, ImageFilter

def reverse(path):
    for o in range(3):
        for i in range(7):
            im = Image.open(str(o+1) + "_ORK/left/" + path + str(i) + ".png")
            img = im.transpose(Image.FLIP_LEFT_RIGHT)
            img.save(str(o+1) + "_ORK/left/" + path + str(i) + ".png")


reverse("ATTACK/ATTACK_00")
reverse("DIE/DIE_00")
reverse("HURT/HURT_00")
reverse("IDLE/IDLE_00")
reverse("JUMP/JUMP_00")
reverse("RUN/RUN_00")
reverse("WALK/WALK_00")
