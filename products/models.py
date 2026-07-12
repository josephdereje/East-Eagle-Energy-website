from django.db import models
from django.urls import reverse


class ProductCategory(models.TextChoices):
    RESIDENTIAL = 'residential', 'Residential'
    C_AND_I_BESS = 'c_and_i_bess', 'C & I Energy Storage Systems'
    ESS_SOLUTION = 'ess_solution', 'ESS Solution'


class ProductType(models.TextChoices):
    ENERGY_STORAGE = 'energy_storage', 'Energy Storage System'
    INVERTER = 'inverter', 'Inverter'
    SOLAR_PANEL = 'solar_panel', 'Solar Panel'
    EV_CHARGER = 'ev_charger', 'EV Charger'


class VoltageType(models.TextChoices):
    LOW_VOLTAGE = 'low_voltage', 'Low Voltage'
    HIGH_VOLTAGE = 'high_voltage', 'High Voltage'
    NOT_APPLICABLE = 'not_applicable', 'N/A'


class EssSubType(models.TextChoices):
    LOW_VOLTAGE_ESS = 'low_voltage_ess', 'Low Voltage ESS'
    HIGH_VOLTAGE_ESS = 'high_voltage_ess', 'High Voltage ESS'
    STACKED_ESS = 'stacked_ess', 'Stacked ESS'
    ALL_IN_ONE_ESS = 'all_in_one_ess', 'All-in-One ESS'
    STORAGE_CHARGING = 'storage_charging', 'Storage & Charging'
    SMART_ENERGY_MANAGEMENT = 'smart_energy_management', 'Smart Energy Management System'
    CLOUD_MONITORING = 'cloud_monitoring', 'Cloud Monitoring'
    NOT_APPLICABLE = 'not_applicable', 'N/A'


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    product_type = models.CharField(
        max_length=30,
        choices=ProductType.choices,
        default=ProductType.ENERGY_STORAGE,
        help_text='Energy Storage System or Inverter',
    )
    category = models.CharField(max_length=20, choices=ProductCategory.choices)
    voltage_type = models.CharField(
        max_length=20, 
        choices=VoltageType.choices, 
        default=VoltageType.NOT_APPLICABLE,
        help_text='For Residential products: Low Voltage or High Voltage'
    )
    ess_sub_type = models.CharField(
        max_length=30,
        choices=EssSubType.choices,
        default=EssSubType.NOT_APPLICABLE,
        help_text='ESS sub-category for sidebar navigation (C&I BESS, ESS Solution)',
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

    def get_gallery_items(self):
        """Main product image plus additional gallery angles for the detail page."""
        items = []
        if self.image:
            items.append({
                'url': self.image.url,
                'alt': self.name,
                'label': 'Main view',
            })
        for index, gallery_image in enumerate(
            self.gallery_images.filter(is_active=True),
            start=len(items) + 1,
        ):
            items.append({
                'url': gallery_image.image.url,
                'alt': gallery_image.label or f'{self.name} — view {index}',
                'label': gallery_image.label or f'View {index}',
            })
        return items

    @property
    def category_label(self):
        return ProductCategory(self.category).label
    
    @property
    def product_type_label(self):
        return ProductType(self.product_type).label

    @property
    def voltage_label(self):
        return VoltageType(self.voltage_type).label

    @property
    def ess_sub_type_label(self):
        return EssSubType(self.ess_sub_type).label


class ProductImage(models.Model):
    """Additional product photos (side, back, detail angles) for the detail gallery."""

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='gallery_images',
    )
    image = models.ImageField(upload_to='products/gallery/')
    label = models.CharField(
        max_length=100,
        blank=True,
        help_text='Optional label, e.g. Side view, Back view',
    )
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order', 'id']
        verbose_name = 'Product Gallery Image'
        verbose_name_plural = 'Product Gallery Images'

    def __str__(self):
        return self.label or f'Gallery image for {self.product.name}'


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


class RecommendedProduct(models.Model):
    """
    Featured / best-seller promo slides on the product list page.
    Ad-style cards managed in admin — link to a catalog product or a custom URL.
    """

    class Badge(models.TextChoices):
        BEST_SELLER = 'best_seller', 'Best Seller'
        FEATURED = 'featured', 'Featured'
        HOT_DEAL = 'hot_deal', 'Hot Deal'
        NEW = 'new', 'New Arrival'
        POPULAR = 'popular', 'Popular'
        PROMO = 'promo', 'Promo'

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='recommendations',
        help_text='Optional: link to a catalog product',
    )
    title = models.CharField(
        max_length=150,
        blank=True,
        help_text='Leave blank to use the product name',
    )
    subtitle = models.CharField(
        max_length=250,
        blank=True,
        help_text='Short promo line under the title',
    )
    badge = models.CharField(
        max_length=20,
        choices=Badge.choices,
        default=Badge.BEST_SELLER,
    )
    image = models.ImageField(
        upload_to='recommended/',
        blank=True,
        null=True,
        help_text='Promo image (uses product image if empty)',
    )
    link_url = models.CharField(
        max_length=300,
        blank=True,
        help_text='Optional custom link. Blank = product page URL',
    )
    button_text = models.CharField(max_length=50, default='View Product')
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', '-created_at']
        verbose_name = 'Recommended Product'
        verbose_name_plural = 'Recommended Products'

    def __str__(self):
        return self.display_title

    @property
    def display_title(self):
        if self.title:
            return self.title
        if self.product_id:
            return self.product.name
        return 'Recommended Product'

    @property
    def display_subtitle(self):
        if self.subtitle:
            return self.subtitle
        if self.product_id and self.product.short_description:
            return self.product.short_description
        return ''

    @property
    def display_image_url(self):
        if self.image:
            return self.image.url
        if self.product_id and self.product.image:
            return self.product.image.url
        return ''

    @property
    def display_url(self):
        if self.link_url:
            return self.link_url
        if self.product_id:
            return self.product.get_absolute_url()
        return '/products/'

    @property
    def badge_label(self):
        return self.get_badge_display()
