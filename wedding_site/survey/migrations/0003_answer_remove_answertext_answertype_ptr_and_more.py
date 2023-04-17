# Generated by Django 4.2 on 2023-04-17 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0002_answertype_answer_dt'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_dt', models.DateTimeField()),
            ],
        ),
        migrations.RemoveField(
            model_name='answertext',
            name='answertype_ptr',
        ),
        migrations.RemoveField(
            model_name='answertype',
            name='question',
        ),
        migrations.RemoveField(
            model_name='answertype',
            name='respondent',
        ),
        migrations.AddField(
            model_name='surveyquestion',
            name='answer_type',
            field=models.CharField(choices=[('rating', 'rating 1 - 5'), ('text', 'Text'), ('yes_no', 'yes - no')], default='text', max_length=200),
        ),
        migrations.CreateModel(
            name='RatingAnswer',
            fields=[
                ('answer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='survey.answer')),
                ('value', models.IntegerField()),
            ],
            bases=('survey.answer',),
        ),
        migrations.CreateModel(
            name='TextAnswer',
            fields=[
                ('answer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='survey.answer')),
                ('text', models.TextField()),
            ],
            bases=('survey.answer',),
        ),
        migrations.CreateModel(
            name='YesNoAnswer',
            fields=[
                ('answer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='survey.answer')),
                ('value', models.BooleanField()),
            ],
            bases=('survey.answer',),
        ),
        migrations.DeleteModel(
            name='AnswerRating',
        ),
        migrations.DeleteModel(
            name='AnswerText',
        ),
        migrations.DeleteModel(
            name='AnswerType',
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.surveyquestion'),
        ),
        migrations.AddField(
            model_name='answer',
            name='respondent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.respondent'),
        ),
    ]
