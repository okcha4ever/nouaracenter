# Generated by Django 4.0.3 on 2022-03-13 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_contact_isparent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='IsParent',
            field=models.CharField(choices=[('ولي أمر', 'ولي أمر'), ('تلميذ', 'تلميذ')], default='ولي أمر', max_length=20),
        ),
    ]