from asgiref.sync import async_to_sync
from django.db import models
from parser.main import GetDataGoldCrown


class Currency(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=50)


class Country(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=50)


class CurrencyPairs(models.Model):
    id = models.AutoField(primary_key=True)
    # country_send = models.ForeignKey(Country, on_delete=models.CASCADE)
    # currency_send = models.ForeignKey(Currency, on_delete=models.CASCADE)
    currency_receive = models.ForeignKey(Currency, on_delete=models.CASCADE)
    country_receive = models.ForeignKey(Country, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def get_price(self, id) -> float:
        cur_pair = CurrencyPairs.objects.get(id=id)
        return float(cur_pair.price)

    def get_pairs_country(self):
        countries = Country.objects.all()
        result = []
        for country in countries:
            pairs = tuple(CurrencyPairs.objects.filter(
                country_receive=country).values_list(
                    'id',
                    'currency_receive__code',
                    'price'
                ))
            result.append((country.name, pairs))
        return result


# sending - откуда
# receiving - куда
class HistoryPrice(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    pairs = models.ForeignKey(CurrencyPairs, on_delete=models.CASCADE)


    def update_data(self):
        get_data = GetDataGoldCrown()
        countries = async_to_sync(
            get_data.get_all_send_countries)()
        if not countries: return
        all_price = []
        for country_id, country_name in countries:
            country_obj, _ = Country.objects.get_or_create(
                id=country_id,
                name=country_name
            )
            currencies = async_to_sync(
                get_data.get_receiving_currency)(country_id)
            if not currencies: continue

            country_obj.save()
            for cur_id, cur_code, cur_name in currencies:
                print(cur_id, cur_code, cur_name)
                cur_obj, _ = Currency.objects.get_or_create(
                    id=cur_id,
                    code=cur_code,
                    name=cur_name
                )
                cur_obj.save()
                price = async_to_sync(
                    get_data.get_price)(
                        receiving_country=country_id,
                        receiving_currency=cur_id
                    )

                pairs_obj, _ = CurrencyPairs.objects.get_or_create(
                    currency_receive=cur_obj,
                    country_receive=country_obj
                )
                print(cur_name, country_name, price)
                if price:
                    pairs_obj.price = price
                    pairs_obj.save()
                    his_price = HistoryPrice(
                        price=price,
                        pairs=pairs_obj
                    )
                    his_price.save()
                    all_price.append((pairs_obj, float(price)))
                else:
                    pairs_obj.save()

        return all_price
