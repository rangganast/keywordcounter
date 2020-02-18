# Generated by Django 3.0.1 on 2020-02-03 09:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=30)),
                ('date_created', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='KeywordHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('time_created', models.TimeField(auto_now_add=True)),
                ('keywords', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='keywords', to='api.Keyword')),
            ],
        ),
    ]