# Generated by Django 4.0.4 on 2022-07-22 00:56

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_delete_hireprofessionalrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrequirement',
            name='interested_prof',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=40), default=list, size=None),
        ),
        migrations.CreateModel(
            name='HireProfessionalRequest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('hire_date', models.DateField(blank=True, null=True)),
                ('descriptive_msg', models.TextField(null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('cancelled', 'Cancelled'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('completed', 'Completed')], default='pending', max_length=25)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date query made')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='date update made')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('prof_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.professionaluserservice')),
                ('subservice_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.subservice')),
            ],
        ),
    ]
