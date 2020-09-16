from django.db import models


class ProductManager(models.Manager):
    def availables(self):
        """
        This helper returns product that are available which means its count is more than zero!

        Returns:
            QuerySet: products that their count is more than zero
        """
        return self.filter(count__gt=0)
