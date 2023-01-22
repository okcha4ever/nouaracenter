from django.db import models

# Create your models here.


class Contact(models.Model):
    Full_Name = models.CharField(max_length=200)
    Email = models.EmailField(max_length=200)
    IsParent = models.CharField(
        max_length=20,
        choices=(('ولي أمر', 'ولي أمر'), ('تلميذ', 'تلميذ')),
        default='ولي أمر',
    )

    Content = models.TextField(max_length=400)

    def __str__(self):
        return self.Full_Name