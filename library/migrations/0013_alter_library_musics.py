# Generated by Django 4.0.4 on 2022-05-28 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0012_alter_profile_current_library'),
    ]

    operations = [
        migrations.AlterField(
            model_name='library',
            name='musics',
            field=models.ManyToManyField(blank=True, to='library.music'),
        ),
    ]