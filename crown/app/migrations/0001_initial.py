# Generated by Django 4.1.5 on 2023-01-10 11:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Country",
            fields=[
                (
                    "id",
                    models.CharField(max_length=5, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Currency",
            fields=[
                (
                    "id",
                    models.CharField(max_length=5, primary_key=True, serialize=False),
                ),
                ("code", models.CharField(max_length=10)),
                ("name", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="CurrencyPairs",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "price",
                    models.DecimalField(decimal_places=2, default=0, max_digits=8),
                ),
                (
                    "country_receive",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.country"
                    ),
                ),
                (
                    "currency_receive",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.currency"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="HistoryPrice",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("price", models.DecimalField(decimal_places=2, max_digits=8)),
                (
                    "pairs",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app.currencypairs",
                    ),
                ),
            ],
        ),
    ]