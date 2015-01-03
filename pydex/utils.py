import os


def load_image(image_number, portrait=False):
    image_dir = "images/"
    if portrait and os.path.exists("%sportraits/%03d.png" % (image_dir, image_number)):
        return "%sportraits/%03d.png" % (image_dir, image_number)
    elif os.path.exists("%sicons/%03d.png" % (image_dir, image_number)):
        return "%sicons/%03d.png" % (image_dir, image_number)
    elif os.path.exists("%sicons/0.png" % image_dir):
        return "%sicons/0.png" % image_dir
    return "%sblank.png" % image_dir
