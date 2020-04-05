# Generated by Django 2.1 on 2018-09-29 09:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kirisame', '0014_auto_20180929_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='artistmeta',
            name='bot',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='kirisame.Bot', verbose_name='Bot'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='artworkmeta',
            name='bot',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='kirisame.Bot', verbose_name='Bot'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bot',
            name='account',
            field=models.CharField(default='artworkkun', max_length=255, verbose_name='Account'),
            preserve_default=False,
        ),
    ]
