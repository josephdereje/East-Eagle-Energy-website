from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand

from products.models import (
    EssSubType,
    Product,
    ProductCategory,
    ProductImage,
    ProductType,
    VoltageType,
)

SEED_ASSET_DIR = Path(__file__).resolve().parents[2] / 'seed_assets'
MEDIA_KEYS = ('image_file', 'gallery_files')


SAMPLE_PRODUCTS = [
    # ── RESIDENTIAL ESS (Energy Storage) ──
    {
        'name': 'Deye LiFePO4 Battery 5.12kWh (Wall-Mount)',
        'slug': 'deye-lifepo4-battery-512kwh-wall-mount',
        'product_type': ProductType.ENERGY_STORAGE,
        'category': ProductCategory.RESIDENTIAL,
        'voltage_type': VoltageType.LOW_VOLTAGE,
        'ess_sub_type': EssSubType.LOW_VOLTAGE_ESS,
        'short_description': '5.12 kWh / Wall-Mount LiFePO4 Energy Storage',
        'description': '5.12kWh wall-mounted lithium iron phosphate battery with 6000+ cycle life. Modular design allows expansion up to 30.72kWh. Compatible with Deye and other hybrid inverters.',
        'price': 65000.00,
        'is_featured': True,
    },
    {
        'name': 'Pylontech US3000C LiFePO4 Battery 3.5kWh',
        'slug': 'pylontech-us3000c-lifepo4-battery-35kwh',
        'product_type': ProductType.ENERGY_STORAGE,
        'category': ProductCategory.RESIDENTIAL,
        'voltage_type': VoltageType.LOW_VOLTAGE,
        'ess_sub_type': EssSubType.LOW_VOLTAGE_ESS,
        'short_description': '3.5 kWh / Stackable Modular Battery Module',
        'description': 'Pylontech US3000C 3.5kWh lithium battery module. Stackable up to 16 units (56kWh). Industry-leading safety with integrated BMS.',
        'price': 52000.00,
        'is_featured': False,
    },
    {
        'name': 'BYD Battery-Box Premium HVS 5.1kWh',
        'slug': 'byd-battery-box-premium-hvs-51kwh',
        'product_type': ProductType.ENERGY_STORAGE,
        'category': ProductCategory.RESIDENTIAL,
        'voltage_type': VoltageType.HIGH_VOLTAGE,
        'ess_sub_type': EssSubType.HIGH_VOLTAGE_ESS,
        'short_description': '5.1 kWh / High Voltage Residential ESS',
        'description': 'BYD Battery-Box Premium HVS high-voltage residential energy storage. Scalable up to 66.3kWh. German engineering with automotive-grade cells.',
        'price': 78000.00,
        'is_featured': True,
    },

    # ── RESIDENTIAL INVERTERS ──
    {
        'name': 'Deye Hybrid Inverter 5kW SUN-5K-SG04LP3',
        'slug': 'deye-hybrid-inverter-5kw-sun5k-sg04lp3',
        'product_type': ProductType.INVERTER,
        'category': ProductCategory.RESIDENTIAL,
        'voltage_type': VoltageType.LOW_VOLTAGE,
        'short_description': '5 kW / Hybrid Solar Inverter with Battery Backup',
        'description': 'Deye 5kW hybrid inverter with MPPT, battery storage support, and smart energy management. WiFi monitoring, 97.6% efficiency.',
        'price': 45000.00,
        'is_featured': True,
    },
    {
        'name': 'Growatt MIN 3000-6000 TL-XH Hybrid Inverter',
        'slug': 'growatt-min-3000-6000-tl-xh-hybrid',
        'product_type': ProductType.INVERTER,
        'category': ProductCategory.RESIDENTIAL,
        'voltage_type': VoltageType.LOW_VOLTAGE,
        'short_description': '3–6 kW / Residential Hybrid Inverter',
        'description': 'Growatt residential hybrid inverter series with flexible power range 3-6kW. Dual MPPT, battery compatibility, backup power support.',
        'price': 38000.00,
        'is_featured': False,
    },
    {
        'name': 'Deye SUN-8K-SG01LP1 Hybrid Inverter 8kW',
        'slug': 'deye-sun-8k-sg01lp1-hybrid-inverter-8kw',
        'product_type': ProductType.INVERTER,
        'category': ProductCategory.RESIDENTIAL,
        'voltage_type': VoltageType.HIGH_VOLTAGE,
        'short_description': '8 kW / High-Power Residential Hybrid Inverter',
        'description': 'Deye 8kW single-phase hybrid inverter for larger homes. Supports up to 16kW PV input, 200A battery current, seamless backup switching.',
        'price': 72000.00,
        'is_featured': True,
    },

    # ── C & I BESS (Energy Storage) ──
    {
        'name': 'BYD Battery-Box Premium LVL 15.4kWh',
        'slug': 'byd-battery-box-premium-lvl-154kwh',
        'product_type': ProductType.ENERGY_STORAGE,
        'category': ProductCategory.C_AND_I_BESS,
        'ess_sub_type': EssSubType.STACKED_ESS,
        'short_description': '15.4 kWh~983 kWh / Stacked Commercial ESS',
        'description': 'BYD Battery-Box Premium LVL 15.4kWh modular energy storage. Expandable up to 983kWh. Ideal for offices, shops, and commercial buildings.',
        'price': 185000.00,
        'is_featured': False,
    },
    {
        'name': 'Sungrow ST2236UX Liquid-Cooled ESS 2.5MWh',
        'slug': 'sungrow-st2236ux-liquid-cooled-ess-25mwh',
        'product_type': ProductType.ENERGY_STORAGE,
        'category': ProductCategory.C_AND_I_BESS,
        'ess_sub_type': EssSubType.STACKED_ESS,
        'short_description': '2.5 MWh / Utility-Scale Liquid-Cooled ESS',
        'description': 'Sungrow 2.5MWh liquid-cooled battery container. Integrated PCS, battery, HVAC, and fire suppression for utility-scale applications.',
        'price': 18500000.00,
        'is_featured': False,
    },
    {
        'name': 'Tesla Powerpack 2 Industrial Energy Storage',
        'slug': 'tesla-powerpack-2-industrial-energy-storage',
        'product_type': ProductType.ENERGY_STORAGE,
        'category': ProductCategory.C_AND_I_BESS,
        'ess_sub_type': EssSubType.ALL_IN_ONE_ESS,
        'short_description': '210 kWh / All-in-One Industrial ESS',
        'description': 'Tesla Powerpack 2 with 210kWh usable capacity. Scalable battery system for peak shaving, load shifting, and backup power.',
        'price': 2850000.00,
        'is_featured': False,
    },
    {
        'name': 'Deye C&I Storage & Charging Cabinet 100kWh',
        'slug': 'deye-ci-storage-charging-cabinet-100kwh',
        'product_type': ProductType.ENERGY_STORAGE,
        'category': ProductCategory.C_AND_I_BESS,
        'ess_sub_type': EssSubType.STORAGE_CHARGING,
        'short_description': '100 kWh / Storage & EV Charging System',
        'description': 'Deye commercial storage and charging cabinet combining 100kWh LiFePO4 battery with integrated PCS and EV charging capability.',
        'price': 950000.00,
        'is_featured': True,
    },

    # ── C & I INVERTERS ──
    {
        'name': 'Deye Three-Phase Hybrid Inverter 12kW',
        'slug': 'deye-three-phase-hybrid-inverter-12kw',
        'product_type': ProductType.INVERTER,
        'category': ProductCategory.C_AND_I_BESS,
        'short_description': '12 kW / Three-Phase Commercial Hybrid Inverter',
        'description': 'Deye SUN-12K-SG04LP3 12kW three-phase hybrid inverter. Ideal for shops, offices, and small businesses.',
        'price': 125000.00,
        'is_featured': True,
    },
    {
        'name': 'Deye SUN-50K-SG01HP3 Commercial Inverter 50kW',
        'slug': 'deye-sun-50k-sg01hp3-commercial-50kw',
        'product_type': ProductType.INVERTER,
        'category': ProductCategory.C_AND_I_BESS,
        'short_description': '50 kW / Three-Phase Commercial String Inverter',
        'description': '50kW three-phase string inverter for commercial solar projects. 6 MPPT inputs, IP65 protection, 99% efficiency.',
        'price': 285000.00,
        'is_featured': True,
    },
    {
        'name': 'Growatt SPF 5000-12000 ES Plus Off-Grid Inverter',
        'slug': 'growatt-spf-5000-12000-es-plus-off-grid',
        'product_type': ProductType.INVERTER,
        'category': ProductCategory.C_AND_I_BESS,
        'short_description': '5–12 kW / Off-Grid Commercial Inverter',
        'description': 'Growatt SPF series 5-12kW off-grid inverter with pure sine wave output. Built-in MPPT controller and generator input support.',
        'price': 95000.00,
        'is_featured': True,
    },
    {
        'name': 'Solis S6 Series Three-Phase Inverter 30kW',
        'slug': 'solis-s6-series-three-phase-30kw',
        'product_type': ProductType.INVERTER,
        'category': ProductCategory.C_AND_I_BESS,
        'short_description': '30 kW / Three-Phase Commercial Inverter',
        'description': 'Solis S6-EH3P30K three-phase string inverter. Wide MPPT voltage range, dual MPPT trackers, integrated WiFi monitoring.',
        'price': 195000.00,
        'is_featured': False,
    },
    {
        'name': 'Deye SUN-100K-SG01HP3 Industrial Inverter 100kW',
        'slug': 'deye-sun-100k-sg01hp3-industrial-100kw',
        'product_type': ProductType.INVERTER,
        'category': ProductCategory.C_AND_I_BESS,
        'short_description': '100 kW / Industrial Three-Phase Inverter',
        'description': 'Deye 100kW three-phase string inverter for large-scale industrial solar. 10 MPPT inputs, active and reactive power control.',
        'price': 485000.00,
        'is_featured': True,
    },
    {
        'name': 'Growatt MAX 100-125KTL3-X LV Three-Phase Inverter',
        'slug': 'growatt-max-100-125ktl3-x-lv-three-phase',
        'product_type': ProductType.INVERTER,
        'category': ProductCategory.C_AND_I_BESS,
        'short_description': '100–125 kW / Industrial-Grade Inverter',
        'description': 'Growatt MAX series 100-125kW low-voltage three-phase inverter. Type II DC&AC SPD, 98.5% efficiency, IP66 protection.',
        'price': 520000.00,
        'is_featured': True,
    },

    # ── ESS SOLUTIONS (All-in-One Systems) ──
    {
        'name': 'Deye All-in-One ESS 10.24kWh Hybrid System',
        'slug': 'deye-all-in-one-ess-1024kwh-hybrid-system',
        'product_type': ProductType.ENERGY_STORAGE,
        'category': ProductCategory.ESS_SOLUTION,
        'ess_sub_type': EssSubType.ALL_IN_ONE_ESS,
        'short_description': '10.24 kWh / All-in-One Hybrid ESS System',
        'description': 'Deye all-in-one ESS combining 5kW hybrid inverter and 10.24kWh LiFePO4 battery in single cabinet. Plug-and-play installation.',
        'price': 145000.00,
        'is_featured': True,
    },
    {
        'name': 'Growatt AXE All-in-One ESS 5kW/10kWh',
        'slug': 'growatt-axe-all-in-one-ess-5kw-10kwh',
        'product_type': ProductType.ENERGY_STORAGE,
        'category': ProductCategory.ESS_SOLUTION,
        'ess_sub_type': EssSubType.ALL_IN_ONE_ESS,
        'short_description': '10 kWh / Modular All-in-One ESS',
        'description': 'Growatt AXE integrated ESS with 5kW inverter and 10kWh battery. Modular design, easy expansion, smart energy management.',
        'price': 138000.00,
        'is_featured': True,
    },
    {
        'name': 'Sonnen Eco ESS 10kWh Complete System',
        'slug': 'sonnen-eco-ess-10kwh-complete-system',
        'product_type': ProductType.ENERGY_STORAGE,
        'category': ProductCategory.ESS_SOLUTION,
        'ess_sub_type': EssSubType.ALL_IN_ONE_ESS,
        'short_description': '10 kWh / Premium German-Engineered ESS',
        'description': 'Sonnen Eco 10kWh all-in-one energy storage system. Premium German engineering with integrated inverter, battery, and energy manager.',
        'price': 285000.00,
        'is_featured': True,
    },
    {
        'name': 'Victron Energy ESS Package with MultiPlus-II 5kW',
        'slug': 'victron-energy-ess-package-multiplus-ii-5kw',
        'product_type': ProductType.ENERGY_STORAGE,
        'category': ProductCategory.ESS_SOLUTION,
        'ess_sub_type': EssSubType.ALL_IN_ONE_ESS,
        'short_description': '5 kW / Flexible Victron ESS Package',
        'description': 'Complete Victron ESS package: MultiPlus-II 5kW inverter/charger, Cerbo GX controller, and compatible battery system.',
        'price': 165000.00,
        'is_featured': False,
    },
    # SOLAR PANELS
    {
        'name': 'Jinko Solar Tiger Neo 555W Monocrystalline Panel',
        'slug': 'jinko-solar-tiger-neo-555w',
        'product_type': ProductType.SOLAR_PANEL,
        'category': ProductCategory.RESIDENTIAL,
        'short_description': '555W / High-Efficiency Monocrystalline Solar Panel',
        'description': 'Jinko Tiger Neo 555W N-type TOPCon module with 22.3% efficiency. Ideal for residential and commercial rooftop installations.',
        'price': 18500.00,
        'is_featured': True,
    },
    {
        'name': 'Jinko Solar Tiger Pro 540W Commercial Panel',
        'slug': 'jinko-solar-tiger-pro-540w',
        'product_type': ProductType.SOLAR_PANEL,
        'category': ProductCategory.C_AND_I_BESS,
        'short_description': '540W / Commercial-Grade Solar Module',
        'description': 'Jinko Tiger Pro 540W panel for C&I installations. High power output, excellent low-light performance, 25-year warranty.',
        'price': 17200.00,
        'is_featured': False,
    },
    # EV CHARGERS
    {
        'name': 'East Eagle 7kW Wall-Mount GB/T EV Charger',
        'slug': 'east-eagle-7kw-wall-mount-gbt-ev-charger',
        'product_type': ProductType.EV_CHARGER,
        'category': ProductCategory.RESIDENTIAL,
        'short_description': '7 kW / Wall-mount AC charger with GBT (GB/T) connector',
        'description': (
            'East Eagle 7 kW wall-mounted AC EV charger with a hardwired GBT (GB/T) connector '
            'for home and small-site charging.\n\n'
            'Rated output is 7.0 kW at 230 VAC ±15%, with current adjustable from 6 A to 32 A. '
            'Supply is single-phase 1P+N+PE, 230 VAC ±15%, 32 A.\n\n'
            'The wall-mount unit has an LED power display, RGB status ring, and RFID reader. '
            'Charging can start by RFID card, plug-and-play, or the optional app and Wi-Fi. '
            'The tethered cable is 5 m, with custom lengths available. Housing is PC + ABS V0 '
            'and the cable jacket is TPU.\n\n'
            'Cooling is natural. The operating range is −25°C to +50°C, 5%–95% humidity, '
            'and altitudes up to 2,000 m.\n\n'
            'Protection includes Type B leakage detection (AC 30 mA + DC 6 mA), IP55, IK10, '
            'over-current, over- and under-voltage, RCD, ground fault, surge, and over-temperature. '
            'Power measurement accuracy is ±1.0% from 1% to full scale. Warranty is 2 years. '
            'Certifications include CE and FCC, with RFID and mobile remote operation.'
        ),
        'is_featured': False,
        'image_file': 'ev-chargers/wall-mount-7kw-gbt.jpg',
    },
    {
        'name': 'East Eagle DC Mini EV Charger 20–40kW',
        'slug': 'east-eagle-dc-mini-ev-charger-20-40kw',
        'product_type': ProductType.EV_CHARGER,
        'category': ProductCategory.C_AND_I_BESS,
        'short_description': '20 / 30 / 40 kW / Compact DC fast charger',
        'description': (
            'East Eagle DC Mini is a compact wall-mounted DC fast charger for commercial '
            'and fleet sites. It is offered in 20 kW, 30 kW, and 40 kW ratings.\n\n'
            'The cabinet includes an LCD screen, status indicator lamp, RFID reader, '
            'emergency stop button, and a side-mounted charging connector with a tethered cable.\n\n'
            'Connectivity covers Wi-Fi, 4G, Modbus, and OCPP 1.6 JSON. '
            'The enclosure is rated IP55 and carries CE marking.'
        ),
        'is_featured': False,
        'image_file': 'ev-chargers/dc-mini-main.jpg',
        'gallery_files': [
            {'file': 'ev-chargers/dc-mini-range.png', 'label': '20–40 kW range'},
            {'file': 'ev-chargers/dc-mini-features.png', 'label': 'Features'},
        ],
    },
    # SMART ENERGY MANAGEMENT
    {
        'name': 'Deye Smart Energy Management System',
        'slug': 'deye-smart-energy-management-system',
        'product_type': ProductType.ENERGY_STORAGE,
        'category': ProductCategory.ESS_SOLUTION,
        'ess_sub_type': EssSubType.SMART_ENERGY_MANAGEMENT,
        'short_description': 'Integrated EMS / Smart Energy Management Platform',
        'description': 'Deye smart energy management system for monitoring and optimizing solar, storage, and grid power flows.',
        'price': 95000.00,
        'is_featured': True,
    },
    {
        'name': 'Deye Cloud Monitoring Platform',
        'slug': 'deye-cloud-monitoring-platform',
        'product_type': ProductType.ENERGY_STORAGE,
        'category': ProductCategory.ESS_SOLUTION,
        'ess_sub_type': EssSubType.CLOUD_MONITORING,
        'short_description': 'Cloud Monitoring / Real-Time Energy Dashboard',
        'description': 'Deye cloud monitoring platform with real-time dashboards, alerts, remote diagnostics, and fleet management for ESS installations.',
        'price': 35000.00,
        'is_featured': True,
    },
]


def _attach_media(product, item):
    image_file = item.get('image_file')
    if image_file:
        path = SEED_ASSET_DIR / image_file
        if path.exists():
            with path.open('rb') as handle:
                product.image.save(path.name, File(handle), save=True)

    gallery = item.get('gallery_files') or []
    if not gallery:
        return

    product.gallery_images.all().delete()
    for order, entry in enumerate(gallery, start=1):
        path = SEED_ASSET_DIR / entry['file']
        if not path.exists():
            continue
        gallery_image = ProductImage(
            product=product,
            label=entry.get('label', ''),
            display_order=order,
            is_active=True,
        )
        with path.open('rb') as handle:
            gallery_image.image.save(path.name, File(handle), save=False)
        gallery_image.save()


class Command(BaseCommand):
    help = 'Seed sample products for ESS, inverters, solar panels, and EV chargers'

    def handle(self, *args, **options):
        created = 0
        updated = 0
        for item in SAMPLE_PRODUCTS:
            defaults = {k: v for k, v in item.items() if k != 'slug' and k not in MEDIA_KEYS}
            product, was_created = Product.objects.update_or_create(
                slug=item['slug'],
                defaults=defaults,
            )
            _attach_media(product, item)
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(self.style.SUCCESS(
            f'Seed complete. {created} new, {updated} updated. '
            f'Total: {Product.objects.count()} products'
        ))
