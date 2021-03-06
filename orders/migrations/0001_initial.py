# Generated by Django 2.0.3 on 2020-05-28 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('trait', models.CharField(blank=True, choices=[('S', 'Small'), ('L', 'Large'), ('A', 'Addition')], max_length=1, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='items',
            name='menu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu', to='orders.Menu'),
        ),
    ]
