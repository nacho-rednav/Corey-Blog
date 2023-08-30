# Generated by Django 3.1.6 on 2021-03-07 20:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_commentary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentary',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.post'),
        ),
    ]