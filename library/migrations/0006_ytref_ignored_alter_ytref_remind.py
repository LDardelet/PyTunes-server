# Generated by Django 4.0.4 on 2022-05-23 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_rename_ytlink_ytref_rename_yt_link_music_yt_ref_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ytref',
            name='ignored',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ytref',
            name='remind',
            field=models.IntegerField(default=1),
        ),
    ]
