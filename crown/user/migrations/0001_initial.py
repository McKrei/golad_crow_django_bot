# Generated by Django 4.1.5 on 2023-01-10 11:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("is_admin", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="UserWaiting",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("price", models.DecimalField(decimal_places=2, max_digits=8)),
                ("is_more", models.BooleanField(default=True)),
                (
                    "pairs",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app.currencypairs",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="user.user"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserPairs",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("is_daily_report", models.BooleanField(default=True)),
                (
                    "pairs",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app.currencypairs",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="user.user"
                    ),
                ),
            ],
        ),
    ]
