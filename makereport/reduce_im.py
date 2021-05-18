from .models import HoldsImages
from pdf_report.tasks import reduce_image

images = HoldsImages.objects.get(report_id=48)

for image in images.image.all():
    reduce_image.delay(image.image)
for image in images.pp_photo.all():
    reduce_image.delay(image.photo)
for image in images.o_images.all():
    reduce_image.delay(image.photos)
for image in images.checks.all():
    reduce_image.delay(image.checks)