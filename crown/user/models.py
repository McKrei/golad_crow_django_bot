from django.db import models
# Create your models here.

from app.models import Currency, Country, CurrencyPairs
from util.report import Reports


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    is_admin = models.BooleanField(default=False)

    def get_user(self, id):
        user = User.objects.filter(id=id)
        if user:
            user = user[0]
        else:
            user = User(id=id)
            user.save()
        return user


class UserWaiting(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pairs = models.ForeignKey(CurrencyPairs, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_more = models.BooleanField(default=True)

    def add(self, user_id, pairs_id, price, is_more):
        u = User()
        user = u.get_user(user_id)

        pairs = CurrencyPairs.objects.get(id=pairs_id)
        obj = UserWaiting(
                user=user,
                pairs=pairs,
                price=price,
                is_more=is_more
            )
        obj.save()
        return f'Я сообщу когда цена на {pairs.currency_receive.name}\n'\
               f'достигнет {price} руб.'


    def get(self, user_id):
        u = User()
        user = u.get_user(user_id)
        result = UserWaiting.objects.filter(
            user=user).values_list(
                'id',
                'pairs__id',
                'price',
                'is_more',
                )
        return list(result)


    def create_report_update_user_waiting(self, all_price: list):
        reports = Reports()
        for pairs, price in all_price:
            query = UserWaiting.objects.filter(
                    pairs=pairs,
                    price__lte=price,
                    is_more=True
                )
            reports.add_report_price_change(price, query)
            query = UserWaiting.objects.filter(
                    pairs=pairs,
                    price__gte=price,
                    is_more=False
                )
            reports.add_report_price_change(price, query)
        return reports


    def delete_by_param(self, params):
        uw = UserWaiting.objects.filter(**params).delete()



class UserPairs(models.Model):
    id = models.AutoField(primary_key=True)
    pairs = models.ForeignKey(CurrencyPairs, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_daily_report = models.BooleanField(default=True)


    def get(self, user_id):
        u = User()
        user = u.get_user(user_id)
        result = UserPairs.objects.filter(
            user=user).values_list(
                'pairs__id',
                'pairs__currency_receive__name',
                'pairs__country_receive__name',
                'pairs__price',
                'is_daily_report',
                )
        return list(result)

    def create_report_update_user_pairs(self):
        reports = Reports()
        users_pairs = UserPairs.objects.filter(
            is_daily_report=True)
        reports.add_update_report(users_pairs)
        return reports


    def add_or_on_or_of(self, user_id, pairs_id):
        u = User()
        user = u.get_user(user_id)
        pairs = CurrencyPairs.objects.get(id=pairs_id)
        up_obj = UserPairs.objects.filter(
            pairs=pairs,
            user=user
        )
        if up_obj:
            up_obj = up_obj[0]
            up_obj.is_daily_report = not up_obj.is_daily_report
        else:
            up_obj = UserPairs(
                pairs=pairs,
                user=user
            )
        up_obj.save()
        return up_obj.is_daily_report


    def delete_by_param(self, params):
        up = UserPairs.objects.filter(**params).delete()
