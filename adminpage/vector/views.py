import datetime
import json

from decimal import Decimal

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import TemplateView

import buttons
from vector.models import users, commission, exchange, admins
from vector.service import (
    get_latest_currency_price, get_latest_crypto_price_usd
)


class IndexPageView(TemplateView):
    template_name = 'index.html'


class ExchangeView(LoginRequiredMixin, TemplateView):
    template_name = 'exchange.html'
    login_url = '/#open_login_modal'

    def get_context_data(self, **kwargs):
        context = super(ExchangeView, self).get_context_data(**kwargs)
        context['user_profile'] = users.objects.get(user=self.request.user)
        one_dollar_in_rub = Decimal(get_latest_currency_price('USD').value)
        one_btc_in_us = round(
            Decimal(get_latest_crypto_price_usd('bitcoin')[0]['close']),
            ndigits=2
        )
        one_btc_in_rub = round((one_dollar_in_rub * one_btc_in_us), ndigits=2)
        one_rub_in_us = round((1 / one_dollar_in_rub), ndigits=4)
        context['currency'] = {
            'one_dollar_in_rub': one_dollar_in_rub,
            'one_btc_in_us': one_btc_in_us,
            'one_btc_in_rub': one_btc_in_rub,
            'one_rub_in_us': one_rub_in_us,
        }
        context['user_exchange'] = exchange.objects.filter(
            user=self.request.user
        ).order_by('-id')
        context['min_value'] = commission.objects.first()

        return context

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode("utf-8"))
        value_with_commission = 0
        commission_value = 0
        one_dollar = Decimal(get_latest_currency_price('USD').value)
        one_cripto = Decimal(get_latest_crypto_price_usd('bitcoin')[0]['close'])
        commission_exchange = commission.objects.first().exchange
        current_val = Decimal(data.get('value'))
        if data.get('from_currency') == '₽':
            commission_value = round(current_val / 100 * commission_exchange,
                                     ndigits=2)
            value_with_commission = round(
                (1 / one_cripto * (
                            (current_val - commission_value) / one_dollar)),
                ndigits=8
            )
        elif data.get('from_currency') == '₿':
            value = one_cripto * current_val * one_dollar
            commission_value = round(value / 100 * commission_exchange,
                                     ndigits=2)
            value_with_commission = round((value - commission_value), ndigits=2)

        if data.get('exchange_save'):
            user_btc = 0
            user_rub = 0
            btc_val = 0
            rub_val = 0
            type_exchange = 0
            profile = users.objects.get(email=request.user.email)
            print('profile>>>>>>>', profile)
            create_dt = datetime.datetime.now()
            if data.get('from_currency') == '₽':
                type_exchange = 1
                btc_val = value_with_commission
                rub_val = current_val
                user_rub = profile.rub_value - rub_val
                user_btc = profile.btc_value + btc_val
            elif data.get('from_currency') == '₿':
                type_exchange = 0
                btc_val = current_val
                rub_val = value_with_commission
                user_btc = profile.btc_value - btc_val
                user_rub = profile.rub_value + rub_val
            try:
                obj = exchange(
                    user=request.user,
                    create_dt=create_dt,
                    btc_value=btc_val,
                    rub_value=rub_val,
                    commission=commission_value,
                    currency_usd=one_dollar,
                    currency_btc=round((one_dollar * one_cripto), ndigits=2),
                    end_dt=datetime.datetime.now(),
                    balance_btc_was=profile.btc_value,
                    balance_rub_was=profile.rub_value,
                    balance_btc=user_btc,
                    balance_rub=user_rub,
                    type=type_exchange,
                    status=1,
                    t_id=profile.t_id,
                )

                obj.save()

                admin_list = admins.objects.all()
                for admin in admin_list:
                    admin_t_id = admin.t_id
                    if type_exchange == 1:
                        settings.BOT_ADMIN.send_message(
                            admin_t_id,
                            f'🔁 Заявка №{obj.id}\n на продажу {rub_val} rub '
                            f'за {btc_val} btc\nID: {profile.t_id} '
                            f'username: @{profile.username}\n Данные пользователя:\n{profile.fio}\n{profile.email}',
                            reply_markup=buttons.get_exchange_admin_approve_keyboard(obj.id))
                    elif type_exchange == 0:
                        settings.BOT_ADMIN.send_message(
                            admin_t_id,
                            f'🔁 Заявка №{obj.id}\n на продажу {btc_val} btc '
                            f'за {rub_val} rub\nID: {profile.t_id} '
                            f'username: @{profile.username}\nДанные пользователя:\n{profile.fio}\n{profile.email}',
                            reply_markup=buttons.get_exchange_admin_approve_keyboard(
                                obj.id))

                return JsonResponse(dict(
                    success=True, message='success'
                ), status=200)

            except Exception:
                return JsonResponse(dict(
                    success=False, message='error',
                ), status=400)

        return JsonResponse(dict(
            success=True, message='success', data=value_with_commission,
            currency=current_val,
        ), status=200)
