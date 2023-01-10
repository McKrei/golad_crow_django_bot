
class Reports:
    class Report:
        def __init__(self, id, message):
            self.id = id
            self.message = message

    def __init__(self):
        self.reports = []


    def add_report_price_change(self, now_price, query):
        if query:
            data = query.values_list(
                'user__id',
                'pairs__currency_receive__name',
                'pairs__country_receive__name',
                'price',
                'is_more'
                )

            for user_id, cur, country, price, is_more in data:
                mes = f'Цена на {cur} {country} '
                mes += 'выросла' if is_more else 'упала'
                mes += f' до {price} р. \n'
                change = abs(now_price - price)
                mes += f'Изменение на {change:.2f} руб.  {(change / price) * 100:.2f}%'
                self.reports.append(Report(id=user_id, message=mes))


    def add_update_report(self, query):
        if query:
            data = query.values_list(
                    'user__id',
                    'pairs__currency_receive__name',
                    'pairs__country_receive__name',
                    'pairs__price'
                    )

            for user_id, cur, country, price in data:
                mes = f'Цена на {cur} {country} '
                mes += f'сегодня {price}'

                self.reports.append(Report(id=user_id, message=mes))



