from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

class Product(models.Model):
    SIZE = (
        (0,'Small'),
        (1, 'Medium'),
        (2, 'Large')
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
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, default=0)
    image = models.ImageField(upload_to='', null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    inventory = models.IntegerField(null=True, blank=False, default=0)

    def save(self, *args, **kwargs):
            super().save(*args, **kwargs)
            if self.image:
                # Update image_url with the full URL to the S3 image
                if self.image_url != self.image.url:
                    self.image_url = self.image.url
                    # Save again to update image_url field
                    super().save(update_fields=['image_url'])

    def __str__(self):
        return self.name


class Color(models.Model):
    COLOR_CHOICES = [
        # Pinks & Reds
        ('pink', 'Pink'),
        ('light_pink', 'Light Pink'),
        ('rose_red', 'Rose Red'),
        ('red', 'Red'),

        # Yellows & Oranges
        ('yellow', 'Yellow'),
        ('light_yellow', 'Light Yellow'),
        ('orange', 'Orange'),
        ('gold_black', 'Gold & Black'),
        ('yellow_black', 'Yellow & Black'),

        # Greens
        ('green', 'Green'),
        ('dark_green', 'Dark Green'),
        ('seafoam', 'Seafoam'),
        ('seafoam_blue', 'Seafoam Blue'),
        ('teal', 'Teal'),

        # Blues & Purples
        ('blue', 'Blue'),
        ('light_blue', 'Light Blue'),
        ('dark_blue', 'Dark Blue'),
        ('medium_blue', 'Medium Blue'),
        ('purple', 'Purple'),
        ('grape', 'Grape'),

        # Greys & Black
        ('gray', 'Gray'),
        ('light_grey', 'Light Grey'),
        ('dark_grey', 'Dark Grey'),
        ('black', 'Black'),

        # Neutrals & Others
        ('white', 'White'),
        ('peach', 'Peach'),
        ('mixed', 'Mixed'),
        ('rainbow', 'Rainbow'),
    ]

    name = models.CharField(max_length=20, choices=COLOR_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_product_rating()

    def delete(self, *args, **kwargs):
        product = self.product
        super().delete(*args, **kwargs)
        self.update_product_rating(product)

    def update_product_rating(self, product=None):
        product = product or self.product
        avg_rating = product.reviews.aggregate(avg=Avg('rating'))['avg'] or 0
        product.rating = round(avg_rating, 2)
        product.save()

    def __str__(self):
        return f"{self.product.name} review by {self.user.username} ({self.rating}★)"