from django.db import models
from django.core.files.base import ContentFile
import requests


class Audio(models.Model):
    text_up = models.CharField(
        'Текст сверху', max_length=255, blank=True, null=True)
    text_down = models.CharField(
        'Текст сверху', max_length=255, blank=True, null=True)
    seekbar = models.BooleanField('Доавить шкалу времени', default=False)
    src = models.CharField('Ссылка на источник',
                           max_length=255, blank=True, null=True)
    file = models.FileField('Файл', upload_to='audio', blank=True, null=True)

    class Meta:
        verbose_name = "Аудио"
        verbose_name_plural = "Аудио"

    def __str__(self) -> str:
        return f"{self.text_up}, {self.text_down}"[:50] + '...'

    def save(self, *args, **kwargs) -> None:
        if 'api.voicerss.org' in self.src:
            r = requests.get(self.src)
            new_id = Audio.objects.latest('id').id + 1
            self.file = ContentFile(r.content, f"{new_id}.mp3")
        return super().save(*args, **kwargs)


class GetCourseUser(models.Model):
    accountUserId = models.BigIntegerField('ID с GetCourse')
    audios = models.ManyToManyField(
        Audio,
        verbose_name='Аудио'
    )

    class Meta:
        verbose_name = "Пользователь GetCourse"
        verbose_name_plural = "Пользователи GetCourse"

    def get_audios(self):
        return "\n".join([str(p) for p in self.audios.all()])
