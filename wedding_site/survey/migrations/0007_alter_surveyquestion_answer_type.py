# Generated by Django 4.2 on 2023-05-04 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0006_alcoholanswer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveyquestion',
            name='answer_type',
            field=models.CharField(choices=[('rating', 'rating 1 - 5'), ('text', 'Text'), ('yes_no', 'yes - no'), ('yes_no_dc', "yes, no, don't care"), ('alcohol', 'Alcohol')], default='text', max_length=200),
        ),
    ]
