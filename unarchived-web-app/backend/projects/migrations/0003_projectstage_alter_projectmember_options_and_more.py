# Generated by Django 5.1 on 2025-07-16 12:11

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_project_projectmember_project_collaborators'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectStage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('order', models.PositiveIntegerField(default=0, help_text='Defines the sequence of stages for display.')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.AlterModelOptions(
            name='projectmember',
            options={'ordering': ['-joined_at']},
        ),
        migrations.RemoveField(
            model_name='project',
            name='collaborators',
        ),
        migrations.AddField(
            model_name='project',
            name='category',
            field=models.CharField(blank=True, help_text='e.g., Apparel, Electronics, Home Goods', max_length=100),
        ),
        migrations.AddField(
            model_name='project',
            name='members',
            field=models.ManyToManyField(related_name='projects', through='projects.ProjectMember', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('ACTIVE', 'Active'), ('ON_HOLD', 'On Hold'), ('COMPLETED', 'Completed'), ('ARCHIVED', 'Archived')], default='ACTIVE', max_length=20),
        ),
        migrations.AddField(
            model_name='projectmember',
            name='joined_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='owned_projects', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='projectmember',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to='projects.project'),
        ),
        migrations.AlterField(
            model_name='projectmember',
            name='role',
            field=models.CharField(choices=[('OWNER', 'Owner'), ('EDITOR', 'Editor'), ('VIEWER', 'Viewer')], default='VIEWER', max_length=20),
        ),
        migrations.AlterField(
            model_name='projectmember',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_memberships', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project',
            name='stage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='projects', to='projects.projectstage'),
        ),
        migrations.DeleteModel(
            name='KPI',
        ),
    ]
