from django.core.management.base import BaseCommand, CommandError
from interface.models import Image, Rect, Tag
from django.contrib.auth.models import User
import random

class Command(BaseCommand):
	help = "Generates an example set of images users and tags"

	def handle(self, *args, **options):
		users = User.objects.all()
		user: User
		if len(users) == 0:
			user = User.objects.create_user(password="default123", email='example@example.org', username="defaultUser")
			user.save()
		else:
			user = random.choice(users)
		for i in range(20):
			im, created = Image.objects.get_or_create(pk=i, title="img"+str(i), sizex = 1000, sizey = 1000, description="Example image", user = user)
			if created:
				im.save()
			tag, created = Tag.objects.get_or_create(title = "tag" + str(i))
			if created:
				tag.save()
			im.tags.add(tag)
			for color in ["red", "blue", "green"]:
				x = random.randint(0,998)
				y = random.randint(0,998)
				rect = Rect(x=x, y=y, sizex = random.randint(1, 999 - x), sizey=random.randint(1, 999-y), image=im, color=color)
				rect.save()