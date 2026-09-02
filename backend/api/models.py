from django.db import models


class Trigger(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Template(models.Model):
    CHANNELS = (('wa', 'WhatsApp'), ('email', 'Email'), ('push', 'Web Push'))
    trigger = models.ForeignKey(Trigger, related_name='templates', on_delete=models.CASCADE)
    channel = models.CharField(max_length=10, choices=CHANNELS)
    content = models.TextField(blank=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        unique_together = ('trigger', 'channel')
