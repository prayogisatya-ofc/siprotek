from django.db import models
from website.models import *


# Courses Model
class Courses(models.Model):
    uuid = models.CharField(max_length=10, null=True, blank=True, editable=False)
    slug = models.SlugField(unique=True, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    thumbnail = models.ImageField(upload_to="thumbnail/")
    division = models.ForeignKey(Divisions, on_delete=models.SET_NULL, null=True, blank=True, related_name="course")

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
        course = Courses.objects.filter(slug=slugify(instance.title))
        if course.exists():
            if course.first().uuid == instance.uuid:
                instance.slug = slugify(instance.title)
            else:
                instance.slug = f"{slugify(instance.title)}-{uuid.uuid4().hex[:5]}"
        else:
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
    uuid = models.CharField(max_length=15, null=True, blank=True, editable=False)
    title = models.CharField(max_length=255)
    material = models.TextField(null=True, blank=True)
    video = models.CharField(max_length=50, null=True, blank=True)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name="meetings")

    def __str__(self):
        return f"{self.title - self.course.title}"
    
@receiver(post_save, sender=Meetings)
def create_meeting_uuid(sender, instance, created, **kwargs):
    if created:
        instance.uuid = "mt" + uuid.uuid4().hex[:5] + "-" + uuid.uuid4().hex[:7]
        instance.save()
    

# Enrolments Model
class Enrolments(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enrol")
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name="members")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member.first_name} - {self.course.title}"