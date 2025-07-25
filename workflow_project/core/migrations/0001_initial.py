# Generated by Django 3.2.25 on 2025-06-28 07:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FormSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted_by', models.CharField(max_length=100)),
                ('data', models.JSONField()),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='FormTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('schema', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='WorkflowInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_state', models.CharField(max_length=100)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('submission', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.formsubmission')),
            ],
        ),
        migrations.CreateModel(
            name='WorkflowDefinition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('states', models.JSONField()),
                ('form_template', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.formtemplate')),
            ],
        ),
        migrations.CreateModel(
            name='Transition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_state', models.CharField(max_length=100)),
                ('to_state', models.CharField(max_length=100)),
                ('allowed_roles', models.JSONField()),
                ('workflow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transitions', to='core.workflowdefinition')),
            ],
        ),
        migrations.AddField(
            model_name='formsubmission',
            name='form_template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.formtemplate'),
        ),
    ]
