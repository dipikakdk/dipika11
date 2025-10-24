# Generated manually for QueueToken model enhancements

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0022_alter_queuetoken_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='queuetoken',
            name='priority',
            field=models.CharField(
                choices=[('normal', 'Normal'), ('urgent', 'Urgent'), ('emergency', 'Emergency')],
                default='normal',
                max_length=20
            ),
        ),
        migrations.AddField(
            model_name='queuetoken',
            name='called_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='queuetoken',
            name='started_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='queuetoken',
            name='completed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='queuetoken',
            name='estimated_wait_time',
            field=models.IntegerField(blank=True, help_text='Estimated wait time in minutes', null=True),
        ),
        migrations.AddField(
            model_name='queuetoken',
            name='actual_wait_time',
            field=models.IntegerField(blank=True, help_text='Actual wait time in minutes', null=True),
        ),
        migrations.AddField(
            model_name='queuetoken',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='queuetoken',
            name='called_by',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='called_tokens',
                to='hospital.doctor'
            ),
        ),
        migrations.AlterModelOptions(
            name='queuetoken',
            options={
                'ordering': ['-priority', 'created_at'],
            },
        ),
        migrations.AlterField(
            model_name='queuetoken',
            name='status',
            field=models.CharField(
                choices=[
                    ('waiting', 'Waiting'),
                    ('called', 'Called'),
                    ('in_progress', 'In Progress'),
                    ('completed', 'Completed'),
                    ('cancelled', 'Cancelled'),
                    ('no_show', 'No Show'),
                ],
                default='waiting',
                max_length=20
            ),
        ),
        migrations.AddIndex(
            model_name='queuetoken',
            index=models.Index(fields=['status', 'department'], name='hospital_qu_status_7f2b8b_idx'),
        ),
        migrations.AddIndex(
            model_name='queuetoken',
            index=models.Index(fields=['created_at'], name='hospital_qu_created_8a1c4f_idx'),
        ),
        migrations.AddIndex(
            model_name='queuetoken',
            index=models.Index(fields=['patient', 'status'], name='hospital_qu_patient_9d3e5g_idx'),
        ),
    ]
