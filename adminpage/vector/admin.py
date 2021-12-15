from django.contrib import admin, messages
from django.utils.translation import ngettext
from .upload import upload_transactions, upload_exchange

from .send_upload import send_upload

from .models import exchange, replenish, withdraw, users, chat, codes, support, wallets, transactions, commission,\
    admins, email_codes
from .forms import adminsForm, walletsForm
# Register your models here.

@admin.register(admins)
class adminsAdmin(admin.ModelAdmin):
    list_display = ('id', 't_id', 'login_dt', 'permissions')
    form = adminsForm

@admin.register(exchange)
class exchangeAdmin(admin.ModelAdmin):
    list_display = ('id', 't_id', 'create_dt', 'type', 'commission', 'btc_value', 'rub_value', 'status',
                    'currency_btc', 'currency_usd', 'balance_btc_was', 'balance_rub_was', 'balance_btc', 'balance_rub',
                    'end_dt', 'admin_id')

    @admin.action(description='Выгрузить')
    def upload(self, request, queryset):
        x = upload_exchange(queryset.values())
        self.message_user(request, ngettext(
            '%d операция выгружена',
            '%d операций выгружены',
            x,
        ) % x, messages.SUCCESS)
        send_upload()

    actions = [upload]

@admin.register(replenish)
class replenishAdmin(admin.ModelAdmin):
    list_display = ('id', 't_id', 'create_dt', 'currency', 'btc_value', 'rub_value', 'status', 'commission', 'country',
                    'city', 'wallet_to', 'wallet_from', 'btc_balance', 'rub_balance', 'btc_balance_was',
                    'rub_balance_was', 'answer' , 'txid', 'end_dt')


@admin.register(withdraw)
class withdrawAdmin(admin.ModelAdmin):
    list_display = ('id', 't_id', 'create_dt', 'currency', 'btc_value', 'rub_value', 'btc_payment', 'rub_payment',
                    'status', 'commission', 'btc_balance', 'rub_balance', 'btc_balance_was', 'rub_balance_was',
                    'answer', 'txid', 'end_dt')


@admin.register(users)
class usersAdmin(admin.ModelAdmin):
    list_display = ('id', 't_id', 'username', 'phone_number', 'email', 'fio', 'rub_value', 'btc_value', 'invited_by',
                    'birth_date', 'address', 'status', 'history_email', 'history_telephone', 'bonuses', 'block')

    @admin.action(description='Заблокировать')
    def block_user(self, request, queryset):

        #print(queryset.values()[0])
        updated = queryset.update(block='Заблокирован')
        self.message_user(request, ngettext(
            '%d пользователь был  заблокирован',
            '%d пользователи были  заблокированы',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description='Разблокировать')
    def unblock_user(self, request, queryset):
        updated = queryset.update(block='Разблокирован')
        self.message_user(request, ngettext(
            '%d пользователь был  разблокирован',
            '%d пользователи были  разблокированы   ',
            updated,
        ) % updated, messages.SUCCESS)


    actions = [block_user, unblock_user]




@admin.register(chat)
class chatAdmin(admin.ModelAdmin):
    list_display = ('id', 't_id', 'dt', 'type', 'text')

    ordering = ['-id']


@admin.register(codes)
class codesAdmin(admin.ModelAdmin):
    list_display = ('id', 't_id', 'create_dt', 'currency', 'btc_balance_was_creator', 'rub_balance_was_creator',
                    'btc_balance_creator', 'rub_balance_creator', 'rub_value', 'btc_value', 'code', 'status',
                    'used_by_id', 'btc_balance_was_activator', 'rub_balance_was_activator',
                    'btc_balance_activator', 'rub_balance_activator', 'end_dt', )


@admin.register(support)
class supportAdmin(admin.ModelAdmin):
    list_display = ('id', 'time', 't_id', 'admin_id', 'message', 'from_who', 'connect_id')

    ordering = ['connect_id', 'time']


@admin.register(wallets)
class walletsAdmin(admin.ModelAdmin):
    list_display = ('id', 'wallet', 'currency')
    form = walletsForm


@admin.register(transactions)
class transactionsAdmin(admin.ModelAdmin):
    list_display = ('id', 't_id', 'dt', 'got', 'sent', 'balance_was', 'balance', 'type', 'commission', 'info', 'status',
                    'end_dt', 'answer', 'to_address', 'txid')

    @admin.action(description='Выгрузить')
    def upload(self, request, queryset):
        x = upload_transactions(queryset.values())
        self.message_user(request, ngettext(
            '%d операция выгружена',
            '%d операций выгружены',
            x,
        ) % x, messages.SUCCESS)
        send_upload()

    actions = [upload]


@admin.register(commission)
class commissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'replenish', 'exchange', 'withdraw_sber', 'withdraw_tink', 'withdraw_btc')


@admin.register(email_codes)
class emailcodesAdmin(admin.ModelAdmin):
    list_display = ('id', 't_id', 'create_dt', 'code', 'status', 'end_dt', 'email')