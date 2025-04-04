# Generated by Django 4.0.1 on 2022-04-25 08:19

from django.db import migrations, models
import scores.validators


class Migration(migrations.Migration):

    dependencies = [
        ('scores', '0002_userdetail_alter_face_skin_color_score_user_detail'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetail',
            name='ethnicity',
            field=models.CharField(default='Black', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='face',
            name='skin_color',
            field=models.CharField(choices=[('Black', 'Black'), ('White', 'White')], default='Black', max_length=100),
        ),
        migrations.AlterField(
            model_name='userdetail',
            name='gender',
            field=models.CharField(max_length=100, validators=[scores.validators.gender_validator]),
        ),
        migrations.AlterField(
            model_name='userdetail',
            name='session',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
