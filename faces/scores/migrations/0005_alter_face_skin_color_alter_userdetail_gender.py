# Generated by Django 5.0.6 on 2024-08-28 21:15

import scores.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scores', '0004_score_score_id_alter_face_skin_color_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='face',
            name='skin_color',
            field=models.CharField(choices=[('Black', 'Black'), ('White', 'White')], default='Black', max_length=100),
        ),
        migrations.AlterField(
            model_name='userdetail',
            name='gender',
            field=models.CharField(choices=[('Woman', 'Woman'), ('Man', 'Man'), ('Other', 'Other')], default='Other', max_length=100, validators=[scores.validators.gender_validator]),
        ),
    ]
