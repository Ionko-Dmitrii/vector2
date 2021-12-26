from django.db import models


class admins(models.Model):
    t_id = models.IntegerField(
        verbose_name='ID админа',
        null=True
    )
    login_dt = models.DateTimeField(
        verbose_name='Дата входа',
        null=True
    )
    permissions = models.TextField(
        verbose_name='Разрешения',
        null=True,
        blank=True
    )

    def __str__(self):
        return f'Админ {self.t_id}'

    class Meta:
        verbose_name = 'админ'
        verbose_name_plural = 'админы'
        db_table = 'admins'


class exchange(models.Model):
    t_id = models.IntegerField(
        verbose_name='ID пользователя',
        null=True
    )
    user = models.ForeignKey(
        to='account.User',
        verbose_name='web user',
        on_delete=models.CASCADE,
        related_name='profile_exchange',
        null=True,
    )
    create_dt = models.DateTimeField(
        verbose_name='Время создания',
        null=True
    )
    type = models.IntegerField(
        verbose_name='Тип',
        null=True
    )
    btc_value = models.DecimalField(
        verbose_name='BTC',
        null=True,
        max_digits=24,
        decimal_places=8
    )
    rub_value = models.DecimalField(
        verbose_name='RUB',
        null=True,
        max_digits=16,
        decimal_places=2
    )
    status = models.IntegerField(
        verbose_name='Статус',
        null=True
    )
    commission = models.DecimalField(
        max_digits=24,
        decimal_places=8,
        verbose_name='Комиссия',
        null=True
    )
    currency_btc = models.FloatField(
        verbose_name='Курс BTC',
        null=True
    )
    currency_usd = models.FloatField(
        verbose_name='Курс USD',
        null=True
    )
    end_dt = models.DateTimeField(
        verbose_name='Время окончания',
        null=True
    )
    admin_id = models.IntegerField(
        verbose_name='ID администратора',
        null=True
    )
    balance_btc_was = models.DecimalField(
        verbose_name='Баланс BTC был',
        null=True,
        max_digits=24,
        decimal_places=8
    )
    balance_rub_was = models.DecimalField(
        verbose_name='Баланс RUB был',
        null=True,
        max_digits=16,
        decimal_places=2
    )
    balance_btc = models.DecimalField(
        verbose_name='Баланс BTC стал',
        null=True,
        max_digits=24,
        decimal_places=8
    )
    balance_rub = models.DecimalField(
        verbose_name='Баланс RUB стал',
        null=True,
        max_digits=16,
        decimal_places=2
    )
    answer = models.TextField(
        verbose_name='Причина отказа',
        null=True
    )

    def __str__(self):
        return f'Обмен №{self.id}'

    class Meta:
        verbose_name = 'обмен'
        verbose_name_plural = 'обмен'
        db_table = 'exchange'


class replenish(models.Model):
    t_id = models.IntegerField(
        verbose_name='ID пользователя',
        null=True
    )
    create_dt = models.DateTimeField(
        verbose_name='Время создания',
        null=True
    )
    currency = models.CharField(
        max_length=3,
        verbose_name='Валюта',
        null=True
    )
    btc_value = models.DecimalField(
        verbose_name='BTC',
        null=True,
        max_digits=24,
        decimal_places=8
    )
    rub_value = models.DecimalField(
        verbose_name='RUB',
        null=True,
        max_digits=16,
        decimal_places=2
    )
    status = models.IntegerField(
        verbose_name='Статус',
        null=True
    )
    country = models.TextField(
        verbose_name='Страна',
        null=True
    )
    city = models.TextField(
        verbose_name='Город',
        null=True
    )
    commission = models.DecimalField(
        decimal_places=8,
        max_digits=24,
        verbose_name='Комиссия',
        null=True
    )
    wallet_to = models.TextField(
        verbose_name='На кошелек',
        null=True
    )
    btc_balance = models.DecimalField(
        verbose_name='Баланс BTC',
        null=True,
        max_digits=24,
        decimal_places=8
    )
    rub_balance = models.DecimalField(
        verbose_name='Баланс RUB',
        null=True,
        max_digits=16,
        decimal_places=2
    )
    answer = models.TextField(
        verbose_name='Причина отказа',
        null=True
    )
    wallet_from = models.TextField(
        verbose_name='С кошелька',
        null=True
    )
    txid = models.TextField(
        verbose_name='txid',
        null=True
    )
    end_dt = models.DateTimeField(
        verbose_name='Время окончания',
        null=True
    )
    btc_balance_was = models.DecimalField(
        verbose_name='Баланс BTC был',
        null=True,
        max_digits=24,
        decimal_places=8
    )
    rub_balance_was = models.DecimalField(
        verbose_name='Баланс RUB был',
        null=True,
        max_digits=16,
        decimal_places=2
    )

    def __str__(self):
        return f'Пополнение №{self.id}'

    class Meta:
        verbose_name = 'пополнение'
        verbose_name_plural = 'пополнение'
        db_table = 'replenish'


class withdraw(models.Model):
    t_id = models.IntegerField(
        verbose_name='ID пользователя',
        null=True
    )
    create_dt = models.DateTimeField(
        verbose_name='Время создания',
        null=True
    )
    currency = models.TextField(
        verbose_name='Валюта',
        null=True
    )
    btc_value = models.DecimalField(
        verbose_name='BTC',
        null=True,
        max_digits=24,
        decimal_places=8
    )
    rub_value = models.DecimalField(
        verbose_name='RUB',
        null=True,
        max_digits=16,
        decimal_places=2
    )
    btc_payment = models.TextField(
        verbose_name='Кошелек BTC',
        null=True
    )
    rub_payment = models.TextField(
        verbose_name='Реквизиты RUB',
        null=True
    )
    status = models.IntegerField(
        verbose_name='Статус',
        null=True
    )
    commission = models.DecimalField(
        decimal_places=8,
        max_digits=24,
        verbose_name='Комиссия',
        null=True
    )

    btc_balance = models.DecimalField(
        verbose_name='Баланс BTC',
        null=True,
        max_digits=24,
        decimal_places=8
    )
    rub_balance = models.DecimalField(
        verbose_name='Баланс RUB',
        null=True,
        max_digits=16,
        decimal_places=2
    )
    btc_balance_was = models.DecimalField(
        verbose_name='Баланс BTC был',
        null=True,
        max_digits=24,
        decimal_places=8
    )
    rub_balance_was = models.DecimalField(
        verbose_name='Баланс RUB был',
        null=True,
        max_digits=16,
        decimal_places=2
    )
    answer = models.TextField(
        verbose_name='Причина отказа',
        null=True
    )
    txid = models.IntegerField(
        verbose_name='txid',
        null=True
    )
    end_dt = models.DateTimeField(
        verbose_name='Время окончания',
        null=True
    )
    bank = models.TextField(
        verbose_name='Банк',
        null=True
    )

    def __str__(self):
        return f'Вывод №{self.id}'

    class Meta:
        verbose_name = 'вывод'
        verbose_name_plural = 'вывод'
        db_table = 'withdraw'


class users(models.Model):
    t_id = models.IntegerField(
        verbose_name='ID пользователя',
        null=True
    )
    user = models.OneToOneField(
        to='account.User',
        verbose_name='web user',
        on_delete=models.CASCADE,
        related_name='profile',
        null=True,
    )
    username = models.TextField(
        verbose_name='Username',
        null=True,
        blank=True
    )
    phone_number = models.IntegerField(
        verbose_name='Номер телефона',
        null=True,
        blank=True

    )
    email = models.TextField(
        verbose_name='email',
        null=True,
        blank=True
    )
    fio = models.TextField(
        verbose_name='ФИО',
        null=True,
        blank=True
    )
    btc_value = models.DecimalField(
        verbose_name='Баланс BTC',
        null=True,
        max_digits=24,
        decimal_places=8
    )
    rub_value = models.DecimalField(
        verbose_name='Баланс RUB',
        null=True,
        max_digits=16,
        decimal_places=2
    )
    invited_by = models.IntegerField(
        verbose_name='Кем приглашен',
        null=True,
        blank=True
    )
    birth_date = models.DateField(
        verbose_name='Дата рождения',
        null=True,
        blank=True
    )
    address = models.TextField(
        verbose_name='Адрес',
        null=True,
        blank=True
    )
    status = models.IntegerField(
        verbose_name='Статус',
        null=True
    )
    bonuses = models.DecimalField(
        decimal_places=2,
        max_digits=16,
        verbose_name='Бонусы',
        null=True
    )
    history_email = models.TextField(
        verbose_name='История email',
        null=True,
        blank=True
    )
    history_telephone = models.TextField(
        verbose_name='История телефона',
        null=True,
        blank=True
    )
    block = models.TextField(
        verbose_name='Блокировка',
        null=True,
        blank=True
    )

    def __str__(self):
        return f'Пользователь {self.t_id}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        db_table = 'users'


class chat(models.Model):
    dt = models.DateTimeField(
        verbose_name='Время действия',
        null=True
    )
    t_id = models.IntegerField(
        verbose_name='ID пользователя',
        null=True
    )
    type = models.TextField(
        verbose_name='Тип',
        null=True
    )
    text = models.TextField(
        verbose_name='Текст',
        null=True
    )

    def __str__(self):
        return f'№{self.id}'

    class Meta:
        verbose_name = 'история действий'
        verbose_name_plural = 'история действий'
        db_table = 'chat'


class codes(models.Model):
    create_dt = models.DateTimeField(
        verbose_name='Время создания',
        null=True
    )
    t_id = models.IntegerField(
        verbose_name='ID пользователя',
        null=True
    )
    currency = models.TextField(
        verbose_name='Валюта',
        null=True
    )
    btc_value = models.DecimalField(
        verbose_name='BTC',
        null=True,
        max_digits=24,
        decimal_places=8

    )
    rub_value = models.DecimalField(
        verbose_name='RUB',
        null=True,
        max_digits=16,
        decimal_places=2
    )
    code = models.TextField(
        verbose_name='Код',
        null=True
    )
    status = models.IntegerField(
        verbose_name='Статус',
        null=True
    )
    used_by_id = models.IntegerField(
        verbose_name='ID активировшего',
        null=True
    )
    end_dt = models.DateTimeField(
        verbose_name='Время активации',
        null=True
    )

    btc_balance_was_creator = models.DecimalField(
        verbose_name='Баланс BTC был у создателя кода',
        null=True,
        max_digits=24,
        decimal_places=8
    )
    rub_balance_was_creator = models.DecimalField(
        verbose_name='Баланс RUB был у создателя кода',
        null=True,
        max_digits=16,
        decimal_places=2
    )
    btc_balance_was_activator = models.DecimalField(
        verbose_name='Баланс BTC был у активировшего код',
        null=True,
        max_digits=24,
        decimal_places=8
    )
    rub_balance_was_activator = models.DecimalField(
        verbose_name='Баланс RUB был у активировшего код',
        null=True,
        max_digits=16,
        decimal_places=2
    )

    btc_balance_creator = models.DecimalField(
        verbose_name='Баланс BTC стал у создателя кода',
        null=True,
        max_digits=24,
        decimal_places=8
    )
    rub_balance_creator = models.DecimalField(
        verbose_name='Баланс RUB стал у создателя кода',
        null=True,
        max_digits=16,
        decimal_places=2
    )
    btc_balance_activator = models.DecimalField(
        verbose_name='Баланс BTC стал у активировшего код',
        null=True,
        max_digits=24,
        decimal_places=8
    )
    rub_balance_activator = models.DecimalField(
        verbose_name='Баланс RUB стал у активировшего код',
        null=True,
        max_digits=16,
        decimal_places=2
    )

    def __str__(self):
        return f'Коды №{self.id}'

    class Meta:
        verbose_name = 'код'
        verbose_name_plural = 'коды'
        db_table = 'codes'


class support(models.Model):
    time = models.DateTimeField(
        verbose_name='Время сообщения',
        null=True
    )
    t_id = models.IntegerField(
        verbose_name='ID пользователя',
        null=True
    )
    admin_id = models.IntegerField(
        verbose_name='ID администратора',
        null=True
    )
    message = models.TextField(
        verbose_name='Текст',
        null=True
    )
    from_who = models.TextField(
        verbose_name='Кто написал',
        null=True
    )
    connect_id = models.IntegerField(
        verbose_name='connect_id',
        null=True
    )

    def __str__(self):
        return f'№{self.id}'

    class Meta:
        verbose_name = 'support'
        verbose_name_plural = 'support'
        db_table = 'support'


class wallets(models.Model):
    wallet = models.TextField(
        verbose_name='Кошелек',
        null=True
    )
    currency = models.TextField(
        verbose_name='Валюта',
        null=True
    )

    def __str__(self):
        return f'Кошелек №{self.id}'

    class Meta:
        verbose_name = 'кошелек'
        verbose_name_plural = 'кошельки'
        db_table = 'wallets'


class transactions(models.Model):
    t_id = models.IntegerField(
        verbose_name='ID пользователя',
        null=True
    )
    dt = models.DateTimeField(
        verbose_name='Время транзакции',
        null=True
    )
    got = models.TextField(
        verbose_name='Получил',
        null=True
    )
    sent = models.TextField(
        verbose_name='Отправил',
        null=True
    )
    balance_was = models.TextField(
        verbose_name='Баланс был',
        null=True
    )
    balance = models.TextField(
        verbose_name='Баланс стал',
        null=True
    )
    type = models.TextField(
        verbose_name='Тип',
        null=True
    )
    commission = models.TextField(
        verbose_name='Коммиссия',
        null=True
    )
    info = models.TextField(
        verbose_name='Информация',
        null=True
    )
    status = models.TextField(
        verbose_name='Статус',
        null=True
    )
    end_dt = models.DateTimeField(
        verbose_name='Время окончания',
        null=True
    )
    answer = models.TextField(
        verbose_name='Причина отказа',
        null=True
    )
    to_address = models.TextField(
        verbose_name='На адрес',
        null=True
    )
    txid = models.TextField(
        verbose_name='Txid',
        null=True
    )

    def __str__(self):
        return f'Транзакция №{self.id}'

    class Meta:
        verbose_name = 'транзакция'
        verbose_name_plural = 'транзакции'
        db_table = 'transactions'


class commission(models.Model):
    replenish = models.PositiveIntegerField(
        verbose_name='Комиссия ввода в %'
    )
    exchange = models.PositiveIntegerField(
        verbose_name='Комиссия обмена в %'
    )
    withdraw_sber = models.PositiveIntegerField(
        verbose_name='Комиссия вывода на сбер в %'
    )
    withdraw_tink = models.PositiveIntegerField(
        verbose_name='Комиссия вывода на тинькофф в %'
    )
    withdraw_btc = models.DecimalField(
        max_digits=24,
        decimal_places=8,
        verbose_name='Комиссия вывода BTC в btc'
    )
    min_rub = models.DecimalField(
        decimal_places=2,
        max_digits=24,
        verbose_name='Мин. сумма обмена в ₽',
        null=True
    )
    min_btc = models.DecimalField(
        decimal_places=8,
        max_digits=24,
        verbose_name='Мин. сумма обмена в ₿',
        null=True
    )

    class Meta:
        verbose_name = 'комиссия'
        verbose_name_plural = 'комиссия'
        db_table = 'commission'


class email_codes(models.Model):
    t_id = models.IntegerField(
        verbose_name='ID пользователя'
    )
    create_dt = models.DateTimeField(
        verbose_name='Время создания'
    )
    status = models.TextField(
        verbose_name='Статус'
    )
    code = models.IntegerField(
        verbose_name='Код'
    )
    email = models.TextField(
        verbose_name='email'
    )
    end_dt = models.DateTimeField(
        verbose_name='Время подтверждения',
        null=True
    )

    class Meta:
        verbose_name = 'код email'
        verbose_name_plural = 'коды email'
        db_table = 'email_codes'
