from django.db import models

class MoreImgManager(models.Manager):

	def add_more_img(self,product,img1,img2,img3):

		add_member = self.create(
            product = product,
            img1 = img1,
            img2 = img2,
            img3 = img3,

        )
		return add_member