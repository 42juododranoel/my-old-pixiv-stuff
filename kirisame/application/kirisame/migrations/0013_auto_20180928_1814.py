# Generated by Django 2.1 on 2018-09-28 18:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kirisame', '0012_auto_20180923_1302'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArtistMeta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('published_at', models.DateTimeField(verbose_name='Published at')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
            ],
            options={
                'verbose_name': 'Artist',
                'verbose_name_plural': 'Artists',
            },
        ),
        migrations.CreateModel(
            name='ArtworkMeta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('published_at', models.DateTimeField(verbose_name='Published at')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
            ],
            options={
                'verbose_name': 'Artwork',
                'verbose_name_plural': 'Artworks',
            },
        ),
        migrations.AlterModelOptions(
            name='artist',
            options={'verbose_name': 'Artist', 'verbose_name_plural': 'Artists'},
        ),
        migrations.AlterModelOptions(
            name='artwork',
            options={'verbose_name': 'Artwork', 'verbose_name_plural': 'Artworks'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': 'Tag', 'verbose_name_plural': 'Tags'},
        ),
        migrations.AlterModelOptions(
            name='toot',
            options={'verbose_name': 'Toot', 'verbose_name_plural': 'Toots'},
        ),
        migrations.AddField(
            model_name='artworkmeta',
            name='artwork',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kirisame.Artwork', verbose_name='Artwork'),
        ),
        migrations.AddField(
            model_name='artistmeta',
            name='artist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kirisame.Artist', verbose_name='Artist'),
        ),
    ]