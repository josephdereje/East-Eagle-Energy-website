from django.db import migrations


def classify_existing_products(apps, schema_editor):
    Product = apps.get_model('products', 'Product')

    inverter_keywords = ['inverter', 'Inverter', 'MultiPlus', 'MIN ', 'SPF', 'MAX ', 'S6 ']
    for keyword in inverter_keywords:
        Product.objects.filter(name__icontains=keyword).update(product_type='inverter')

    # ESS Solution products
    Product.objects.filter(category='ess_solution').update(
        product_type='energy_storage',
        ess_sub_type='all_in_one_ess',
    )

    # C&I BESS batteries -> stacked
    battery_keywords = ['Battery', 'Powerpack', 'ESS 2.5', 'Liquid-Cooled']
    for keyword in battery_keywords:
        Product.objects.filter(
            category='c_and_i_bess',
            name__icontains=keyword,
        ).update(
            product_type='energy_storage',
            ess_sub_type='stacked_ess',
        )

    # Residential batteries
    Product.objects.filter(
        category='residential',
        name__icontains='Battery',
    ).update(
        product_type='energy_storage',
        ess_sub_type='low_voltage_ess',
    )

    Product.objects.filter(
        category='residential',
        name__icontains='HVS',
    ).update(
        product_type='energy_storage',
        ess_sub_type='high_voltage_ess',
        voltage_type='high_voltage',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_add_product_type_and_ess_sub_type'),
    ]

    operations = [
        migrations.RunPython(classify_existing_products, migrations.RunPython.noop),
    ]
