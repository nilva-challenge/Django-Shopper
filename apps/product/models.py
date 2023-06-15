from django.db import models

from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    name = models.CharField(_("product"), max_length=200)
    is_exists = models.BooleanField(_("is_exists"), default=True)
    insert_datetime = models.DateTimeField(_('insert_date'), auto_now_add=True)
    update_datetime = models.DateTimeField(_('update_date'), auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _("products")
        verbose_name = _("product")
        db_table = "product"
