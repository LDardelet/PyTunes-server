# Generated by Django 4.0.4 on 2022-05-28 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0011_alter_profile_current_library'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='current_library',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='library.library'),
        ),
    ]