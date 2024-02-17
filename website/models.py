from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save
import uuid, os, qrcode
from django.utils.text import slugify
from io import BytesIO
from django.core.files import File

# Majors Model
class Majors(models.Model):
    uuid = models.CharField(max_length=10, null=True, blank=True, editable=False)
    code = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
@receiver(post_save, sender=Majors)
def create_major_uuid(sender, instance, created, **kwargs):
    if created:
        instance.uuid = "MJR" + uuid.uuid4().hex[:7]
        instance.save()


# User Model
class User(AbstractUser):
    uuid = models.CharField(max_length=10, null=True, blank=True, editable=False)
    telp = models.CharField(max_length=15, null=True, blank=True)
    role = models.CharField(max_length=6)
    major = models.ForeignKey(Majors, on_delete=models.CASCADE, null=True, blank=True, related_name='users')
    
    def __str__(self):
        return self.uuid
    
@receiver(post_save, sender=User)
def create_user_uuid(sender, instance, created, **kwargs):
    if created:
        instance.uuid = "USR" + uuid.uuid4().hex[:7]
        instance.save()


# Courses Model
class Courses(models.Model):
    uuid = models.CharField(max_length=10, null=True, blank=True, editable=False)
    slug = models.SlugField(unique=True, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to="thumbnail/")
    tutor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title
    
@receiver(post_save, sender=Courses)
def create_course_uuid(sender, instance, created, **kwargs):
    if created:
        instance.uuid = "CRS" + uuid.uuid4().hex[:7]
        instance.save()

@receiver(pre_save, sender=Courses)
def update_course_slug(sender, instance, **kwargs):
    if instance.title:
        instance.slug = slugify(instance.title)

@receiver(post_delete, sender=Courses)
def delete_course_thumbnail(sender, **kwargs):
    ins = kwargs['instance']
    try:
        ins.thumbnail.delete(save=False)
    except:
        pass

@receiver(pre_save, sender=Courses)
def update_course_thumbnail(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_file = Courses.objects.get(pk=instance.pk).thumbnail
        except Courses.DoesNotExist:
            return False
        else:
            new_file = instance.thumbnail
            if old_file and old_file.url != new_file.url:
                old_file.delete(save=False) 


# Meetings Model
class Meetings(models.Model):
    title = models.CharField(max_length=255)
    material = models.TextField()
    video = models.CharField(max_length=50, null=True, blank=True)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    

# Enrolments Model
class Enrolments(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member.first_name} - {self.course.title}"
    

# Division Model
class Divisions(models.Model):
    uuid = models.CharField(max_length=10, null=True, blank=True, editable=False)
    name = models.CharField(max_length=100)
    tutor = models.OneToOneField(User, on_delete=models.CASCADE , related_name='division')

    def __str__(self):
        return self.name
    
@receiver(post_save, sender=Divisions)
def create_division_uuid(sender, instance, created, **kwargs):
    if created:
        instance.uuid = "DVS" + uuid.uuid4().hex[:7]
        instance.save()
    

# Presences Model
class Presences(models.Model):
    uuid = models.CharField(max_length=10, null=True, blank=True, editable=False)
    division = models.ForeignKey(Divisions, on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now_add=True)
    note = models.TextField()
    qrcode = models.ImageField(upload_to="qrcode/")
    
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = "PRS" + uuid.uuid4().hex[:7]

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.uuid)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer)
        buffer.seek(0)

        self.qrcode.save(f'{self.uuid}.png', File(buffer), save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.uuid}"

@receiver(post_delete, sender=Presences)
def delete_presence_qrcode(sender, **kwargs):
    ins = kwargs['instance']
    try:
        ins.qrcode.delete(save=False)
    except:
        pass
    

# Detail Presence Model
class DetailPresence(models.Model):
    presence = models.ForeignKey(Presences, on_delete=models.CASCADE, related_name='detail')
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.presence.uuid} - {self.member.first_name}"