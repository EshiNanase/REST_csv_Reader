from django.db import models


class Customer(models.Model):

    username = models.CharField(
        max_length=255,
        verbose_name='Логин клиента'
    )
    spent_money = models.PositiveBigIntegerField(
        default=0,
        verbose_name='Количество потраченных денег'
    )

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'

    def __str__(self):
        return self.username


class Stone(models.Model):

    name = models.CharField(
        max_length=255,
        verbose_name='Название камня'
    )

    class Meta:
        verbose_name = 'Камень'
        verbose_name_plural = 'Камни'

    def __str__(self):
        return self.name


class StoneItem(models.Model):

    customer = models.ForeignKey(
        to=Customer,
        on_delete=models.CASCADE,
        related_name='stones',
        verbose_name='Покупатель'
    )
    stone = models.ForeignKey(
        to=Stone,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Камень'
    )
    quantity = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Купленный камень'
        verbose_name_plural = 'Купленные камни'

    def __str__(self):
        return f'{self.stone.name} - {self.customer.username} - {self.quantity}'
