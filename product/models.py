from django.db import models


class Product(models.Model):
    SIZE = (
        (0,'S'),
        (1, 'M'),
        (2, 'L')
        )
    code = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    size = models.IntegerField(choices=SIZE, null=False, blank=False, default=0)
    has_colors = models.BooleanField(default=False, null=True, blank=True)

    color = models.ForeignKey(
        'Color',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='products_by_color'
    )

    available_colors = models.ManyToManyField(
        'Color',
        blank=True,
        related_name='products_available_colors'
    )
    
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    care_details = models.CharField(max_length=254, null=True, blank=True)
    inventory = models.IntegerField(null=True, blank=False, default=0)

    def __str__(self):
        return self.name


class Color(models.Model):
    COLOR_CHOICES = [
        ('pink', 'Pink'),
        ('blue', 'Blue'),
        ('light_blue', 'Light Blue'),
        ('white', 'White'),
        ('gray', 'Gray'),
        ('rainbow', 'Rainbow'),
    ]

    name = models.CharField(max_length=20, choices=COLOR_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()
