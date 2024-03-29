# Generated by Django 4.0.6 on 2022-08-18 05:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flavors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flavor_id', models.CharField(max_length=50)),
                ('flavor_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_id', models.CharField(max_length=50)),
                ('image_name', models.CharField(max_length=20)),
                ('image_status', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Networks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('network_id', models.CharField(max_length=50)),
                ('network_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Routers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('router_id', models.CharField(max_length=50)),
                ('router_name', models.CharField(max_length=20)),
                ('external_gateway', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Subnets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subnet_id', models.CharField(max_length=50)),
                ('subnet_name', models.CharField(max_length=20)),
                ('subnet_cidr', models.CharField(max_length=20)),
                ('network_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guiclient.networks')),
                ('router_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='guiclient.routers')),
            ],
        ),
        migrations.CreateModel(
            name='Servers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server_id', models.CharField(max_length=50)),
                ('server_name', models.CharField(max_length=20)),
                ('public_ip', models.GenericIPAddressField(null=True)),
                ('private_ip', models.GenericIPAddressField(null=True)),
                ('status', models.CharField(max_length=10)),
                ('flavor_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='guiclient.flavors')),
                ('image_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='guiclient.images')),
                ('network_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guiclient.networks')),
            ],
        ),
    ]
