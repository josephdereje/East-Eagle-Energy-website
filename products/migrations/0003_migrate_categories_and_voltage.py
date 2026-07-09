from django.db import migrations


def migrate_categories(apps, schema_editor):
    """Migrate Commercial and Industrial products to C & I BESS"""
    Product = apps.get_model('products', 'Product')
    
    # Update all commercial products to c_and_i_bess
    Product.objects.filter(category='commercial').update(category='c_and_i_bess')
    
    # Update all industrial products to c_and_i_bess
    Product.objects.filter(category='industrial').update(category='c_and_i_bess')
    
    print("✓ Migrated Commercial and Industrial products to C & I BESS")


def set_voltage_types(apps, schema_editor):
    """Set voltage types for residential products based on their specifications"""
    Product = apps.get_model('products', 'Product')
    
    # Low voltage residential products (typically <100V DC, modular batteries, small inverters)
    low_voltage_keywords = ['5kW', '3kW', '5.12kWh', '3.5kWh', 'US3000C', 'Wall-Mount']
    for keyword in low_voltage_keywords:
        Product.objects.filter(
            category='residential',
            name__icontains=keyword
        ).update(voltage_type='low_voltage')
    
    # High voltage residential products (typically >100V DC, larger systems)
    high_voltage_keywords = ['8kW', '10kW', '12kW']
    for keyword in high_voltage_keywords:
        Product.objects.filter(
            category='residential',
            name__icontains=keyword
        ).update(voltage_type='high_voltage')
    
    print("✓ Set voltage types for residential products")


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_productsidebarsection_product_voltage_type_and_more'),
    ]

    operations = [
        migrations.RunPython(migrate_categories, migrations.RunPython.noop),
        migrations.RunPython(set_voltage_types, migrations.RunPython.noop),
    ]
