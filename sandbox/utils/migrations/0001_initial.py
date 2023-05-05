# Generated by Django 4.2.1 on 2023-05-05 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('basket', '0001_initial'),
        ('wagtailcore', '0083_workflowcontenttype'),
    ]

    operations = [
        migrations.CreateModel(
            name='BasketSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basket_page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='basket.basketpage')),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.site')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
