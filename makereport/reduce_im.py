from makereport.models import HoldsImages
from pdf_report.tasks import reduce_image


def reduce():
    images = HoldsImages.objects.get(report_id=48)

    for image in images.image.all():
        reduce_image.delay(image.image.path)
    for image in images.pp_photo.all():
        reduce_image.delay(image.photo.path)
    for image in images.o_images.all():
        reduce_image.delay(image.photos.path)
    for image in images.checks.all():
        reduce_image.delay(image.checks.path)
