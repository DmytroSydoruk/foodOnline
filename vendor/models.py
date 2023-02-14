from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_notification
from datetime import time, date, datetime


class Vendor(models.Model):
    user = models.OneToOneField(
        User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(
        UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_slug = models.SlugField(max_length=100, unique=True)
    vendor_license = models.ImageField(upload_to='vedor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def is_open(self) -> bool:
        today = date.today().isoweekday()
        current_day_hours = OpeningHour.objects.filter(vendor=self, day=today)
        now = datetime.now().strftime("%H:%M")
        is_open: bool = False
        for item in current_day_hours:
            open = str(datetime.strptime(item.from_hour, '%H:%M').time())
            close = str(datetime.strptime(item.to_hour, '%H:%M').time())
            if now > open and now < close:
                return True
            else:
                continue
        return is_open

    def __str__(self) -> str:
        return self.vendor_name

    def save(self, *args, **kwargs):
        if self.pk is not None:
            # Update
            orig: Vendor = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                email_template = 'admin_approval_email.html'
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved,
                }
                if self.is_approved == True:
                    # send
                    email_subject = 'Congratulations! Your resutaurant has been approved.'
                    send_notification.delay(
                        email_subject, email_template, context)
                else:
                    # send
                    email_subject = "We're sorry! You are not eligible for publishing your food menu on our marketplace."
                    send_notification.delay(
                        email_subject, email_template, context)
        return super(Vendor, self).save(*args, **kwargs)


class OpeningHour(models.Model):

    DAYS = (
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday'),
    )

    HOURS = tuple([(time(h, m).strftime("%H:%M"), time(h, m).strftime("%H:%M"))
                  for h in range(0, 24) for m in (0, 30)])

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS)
    from_hour = models.CharField(max_length=6, choices=HOURS, blank=True)
    to_hour = models.CharField(max_length=6, choices=HOURS, blank=True)
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return self.get_day_display()

    class Meta:
        ordering = ('day', '-from_hour')
        unique_together = ('vendor', 'day', 'from_hour', 'to_hour')
