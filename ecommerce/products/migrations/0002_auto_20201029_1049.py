# Generated by Django 3.0.3 on 2020-10-29 05:19

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=1, max_length=100)),
                ('firstp', models.CharField(default=1, max_length=20000)),
                ('secondp', models.CharField(default=1, max_length=20000)),
                ('mission', models.CharField(default=1, max_length=20000)),
                ('vision', models.CharField(default=1, max_length=20000)),
            ],
        ),
        migrations.AlterField(
            model_name='book',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(default='desc'),
        ),
    ]
