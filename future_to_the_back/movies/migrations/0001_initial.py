from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_name', models.CharField(max_length=100)),
                ('rank', models.IntegerField()),
                ('target_dt', models.CharField(max_length=10)),
                ('rank_old_and_new', models.CharField(max_length=10)),
                ('open_dt', models.CharField(max_length=100)),
                ('sales_share', models.FloatField()),
                ('sales_change', models.FloatField()),
                ('sales_acc', models.BigIntegerField()),
                ('audi_cnt', models.IntegerField()),
                ('audi_change', models.FloatField()),
                ('audi_acc', models.BigIntegerField()),
                ('scrn_cnt', models.IntegerField()),
                ('show_cnt', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MovieDetail',
            fields=[
                ('movie', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='movies.movie')),
                ('overview', models.TextField()),
                ('poster', models.URLField()),
                ('staff1', models.CharField(blank=True, max_length=50, null=True)),
                ('staff2', models.CharField(blank=True, max_length=50, null=True)),
                ('staff3', models.CharField(blank=True, max_length=50, null=True)),
                ('staff4', models.CharField(blank=True, max_length=50, null=True)),
                ('staff5', models.CharField(blank=True, max_length=50, null=True)),
                ('thumb_staff1', models.URLField(blank=True, null=True)),
                ('thumb_staff2', models.URLField(blank=True, null=True)),
                ('thumb_staff3', models.URLField(blank=True, null=True)),
                ('thumb_staff4', models.URLField(blank=True, null=True)),
                ('thumb_staff5', models.URLField(blank=True, null=True)),
                ('netizen_score', models.FloatField()),
                ('special_score', models.FloatField()),
                ('running_time', models.CharField(max_length=10)),
                ('genre', models.CharField(max_length=10)),
                ('grade', models.CharField(max_length=10)),
                ('download_url', models.URLField(blank=True, null=True)),
                ('best_line1_character', models.CharField(blank=True, max_length=50, null=True)),
                ('best_line1', models.CharField(blank=True, max_length=100, null=True)),
                ('best_line2_character', models.CharField(blank=True, max_length=50, null=True)),
                ('best_line2', models.CharField(blank=True, max_length=100, null=True)),
                ('relate_movie1', models.CharField(blank=True, max_length=50, null=True)),
                ('relate_movie2', models.CharField(blank=True, max_length=50, null=True)),
                ('relate_movie3', models.CharField(blank=True, max_length=50, null=True)),
                ('relate_movie4', models.CharField(blank=True, max_length=50, null=True)),
                ('relate_movie5', models.CharField(blank=True, max_length=50, null=True)),
                ('relate_movies_thumb1', models.URLField(blank=True, null=True)),
                ('relate_movies_thumb2', models.URLField(blank=True, null=True)),
                ('relate_movies_thumb3', models.URLField(blank=True, null=True)),
                ('relate_movies_thumb4', models.URLField(blank=True, null=True)),
                ('relate_movies_thumb5', models.URLField(blank=True, null=True)),
                ('aka_info', models.CharField(max_length=50)),
                ('viewer_img', models.URLField(blank=True, null=True)),
            ],
        ),
    ]
