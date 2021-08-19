# Generated by Django 3.2.6 on 2021-08-19 23:25

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Postbox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=200, null=True)),
                ('is_public', models.BooleanField(default=True)),
                ('send_at', models.DateField()),
                ('closed_at', models.DateField()),
                ('days_to_close', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'postboxes',
            },
        ),
        migrations.CreateModel(
            name='Receiver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('postbox', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='postboxes.postbox')),
            ],
            options={
                'db_table': 'receivers',
            },
        ),
        migrations.CreateModel(
            name='Letter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=100)),
                ('image_url', models.CharField(max_length=2000)),
                ('caption', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('postbox', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='postboxes.postbox')),
            ],
            options={
                'db_table': 'letters',
            },
        ),
        migrations.AddConstraint(
            model_name='receiver',
            constraint=models.UniqueConstraint(fields=('postbox', 'email'), name='unique_postbox_email'),
        ),
    ]
