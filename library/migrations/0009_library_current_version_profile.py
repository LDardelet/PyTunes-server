# Generated by Django 4.0.4 on 2022-05-27 14:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library', '0008_ytref_is_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='library',
            name='current_version',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_version', models.IntegerField(null=True)),
                ('current_library', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='library.library')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]