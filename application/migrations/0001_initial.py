# Generated by Django 4.2.6 on 2023-12-25 13:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AcceptedBookingRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_date', models.DateField()),
                ('description', models.TextField()),
                ('solo_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Users.solouser')),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(max_length=50)),
                ('message', models.TextField()),
                ('accepted_booking_request', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='offer_relation', to='application.acceptedbookingrequest')),
                ('solo_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='booked_by', to='Users.solouser')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('about', models.TextField()),
                ('works_done', models.PositiveIntegerField()),
                ('contacts', models.CharField(max_length=300)),
                ('email', models.EmailField(max_length=254)),
                ('members', models.ManyToManyField(limit_choices_to={'user_type': 'Team'}, related_name='teams', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(blank=True, default=0, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('createdat', models.DateTimeField(auto_now_add=True)),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='review_set', to='application.team')),
            ],
        ),
        migrations.CreateModel(
            name='RejectedOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('offer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='rejected_offer', to='application.offer')),
            ],
        ),
        migrations.CreateModel(
            name='RejectedBookingRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('booking_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rejected_booking_request', to='application.booking')),
            ],
        ),
        migrations.CreateModel(
            name='PendingOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('offer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pending_offer', to='application.offer')),
            ],
        ),
        migrations.CreateModel(
            name='PendingBookingRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('booking_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pending_booking_request', to='application.booking')),
            ],
        ),
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available_date', models.DateField()),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.team')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='application.team'),
        ),
        migrations.CreateModel(
            name='AcceptedOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('offer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='accepted_offer', to='application.offer')),
            ],
        ),
        migrations.AddField(
            model_name='acceptedbookingrequest',
            name='booking_request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accepted_booking_request', to='application.booking'),
        ),
    ]
