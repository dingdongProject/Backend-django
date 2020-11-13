# Generated by Django 3.1.2 on 2020-11-13 19:00

import datetime
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='None', max_length=100)),
                ('memberWrite', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Circle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='circle', max_length=100)),
                ('explanation', models.CharField(default='Circle Explaination', max_length=100)),
                ('picture', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='DUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.user')),
                ('picture', models.FileField(upload_to='')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='None', max_length=100)),
                ('content', models.CharField(default='None', max_length=1000)),
                ('created_at', models.DateField(default=datetime.date(2020, 11, 13))),
                ('updated_at', models.DateField(default=datetime.date(2020, 11, 13))),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='circle.board')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='circle.duser')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('content', models.CharField(default='None', max_length=500)),
                ('circle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='circle.circle')),
            ],
        ),
        migrations.CreateModel(
            name='Read',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hasRead', models.BooleanField(default=False)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='circle.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='circle.duser')),
            ],
        ),
        migrations.CreateModel(
            name='MemberShip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isAdmin', models.BooleanField(default=False)),
                ('isActive', models.BooleanField(default=False)),
                ('dateJoined', models.DateField(default=datetime.date(2020, 11, 13))),
                ('circle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='circle.circle')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='circle.duser')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(default='None', max_length=1000)),
                ('created_at', models.DateField(default=datetime.date(2020, 11, 13))),
                ('updated_at', models.DateField(default=datetime.date(2020, 11, 13))),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='circle.duser')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='circle.post')),
            ],
        ),
        migrations.AddField(
            model_name='board',
            name='circle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='circle.circle'),
        ),
    ]
