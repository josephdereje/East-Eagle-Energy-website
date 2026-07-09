from django.db import models
from django.urls import reverse


class ProductCategory(models.TextChoices):
    RESIDENTIAL = 'residential', 'Residential'
    C_AND_I_BESS = 'c_and_i_bess', 'C & I BESS'
    ESS_SOLUTION = 'ess_solution', 'ESS Solution'


class VoltageType(models.TextChoices):
    LOW_VOLTAGE = 'low_voltage', 'Low Voltage'
    HIGH_VOLTAGE = 'high_voltage', 'High Voltage'
    NOT_APPLICABLE = 'not_applicable', 'N/A'


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    category = models.CharField(max_length=20, choices=ProductCategory.choices)
    voltage_type = models.CharField(
        max_length=20, 
        choices=VoltageType.choices, 
        default=VoltageType.NOT_APPLICABLE,
        help_text='For Residential products: Low Voltage or High Voltage'
    )
    short_description = models.CharField(max_length=300, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug': self.slug})

    @property
    def category_label(self):
        return ProductCategory(self.category).label
    
    @property
    def voltage_label(self):
        return VoltageType(self.voltage_type).label


class ProductSidebarSection(models.Model):
    """Editable sidebar content for product pages"""
    category = models.CharField(
        max_length=20, 
        choices=ProductCategory.choices,
        unique=True,
        help_text='Which product category this sidebar is for'
    )
    title = models.CharField(max_length=100, default='Product Categories')
    description = models.TextField(
        blank=True,
        help_text='Optional description text shown at top of sidebar'
    )
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['display_order']
        verbose_name = 'Product Sidebar Section'
        verbose_name_plural = 'Product Sidebar Sections'
    
    def __str__(self):
        return f'{self.get_category_display()} Sidebar'


class ProductSidebarImage(models.Model):
    """Sliding/rotating images for product sidebar"""
    sidebar_section = models.ForeignKey(
        ProductSidebarSection, 
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='sidebar/')
    title = models.CharField(max_length=100, blank=True)
    caption = models.CharField(max_length=200, blank=True)
    link_url = models.CharField(max_length=200, blank=True, help_text='Optional link URL')
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['display_order', 'id']
        verbose_name = 'Sidebar Image'
        verbose_name_plural = 'Sidebar Images'
    
    def __str__(self):
        return f'{self.title or "Image"} - {self.sidebar_section}'
