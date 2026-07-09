from django.core.management.base import BaseCommand

from products.models import Product, ProductCategory


SAMPLE_PRODUCTS = [
    # RESIDENTIAL PRODUCTS
    {
        'name': 'Deye Hybrid Inverter 5kW SUN-5K-SG04LP3',
        'slug': 'deye-hybrid-inverter-5kw-sun5k-sg04lp3',
        'category': ProductCategory.RESIDENTIAL,
        'short_description': 'Premium hybrid solar inverter with battery backup for homes.',
        'description': 'Deye 5kW hybrid inverter with MPPT, battery storage support, and smart energy management. Perfect for residential solar installations with grid-tie and off-grid capabilities. Features WiFi monitoring, multiple battery compatibility, and high efficiency up to 97.6%.',
        'price': 45000.00,
        'is_featured': True,
    },
    {
        'name': 'Deye LiFePO4 Battery 5.12kWh (Wall-Mount)',
        'slug': 'deye-lifepo4-battery-512kwh-wall-mount',
        'category': ProductCategory.RESIDENTIAL,
        'short_description': 'Compact lithium battery for home energy storage.',
        'description': '5.12kWh wall-mounted lithium iron phosphate battery with 6000+ cycle life. Modular design allows expansion up to 30.72kWh. Compatible with Deye and other hybrid inverters. Built-in BMS for safety and longevity.',
        'price': 65000.00,
        'is_featured': True,
    },
    {
        'name': 'Growatt MIN 3000-6000 TL-XH Hybrid Inverter',
        'slug': 'growatt-min-3000-6000-tl-xh-hybrid',
        'category': ProductCategory.RESIDENTIAL,
        'short_description': 'Versatile residential hybrid inverter (3-6kW range).',
        'description': 'Growatt residential hybrid inverter series with flexible power range 3-6kW. Features dual MPPT, battery compatibility, backup power support, and smart monitoring via WiFi/4G.',
        'price': 38000.00,
        'is_featured': False,
    },
    {
        'name': 'Pylontech US3000C LiFePO4 Battery 3.5kWh',
        'slug': 'pylontech-us3000c-lifepo4-battery-35kwh',
        'category': ProductCategory.RESIDENTIAL,
        'short_description': 'Stackable modular battery for residential use.',
        'description': 'Pylontech US3000C 3.5kWh lithium battery module. Stackable up to 16 units (56kWh). Industry-leading safety with integrated BMS, compatible with most hybrid inverters. 15-year design life.',
        'price': 52000.00,
        'is_featured': False,
    },
    {
        'name': 'Deye SUN-8K-SG01LP1 Hybrid Inverter 8kW',
        'slug': 'deye-sun-8k-sg01lp1-hybrid-inverter-8kw',
        'category': ProductCategory.RESIDENTIAL,
        'short_description': 'High-power residential hybrid inverter 8kW.',
        'description': 'Deye 8kW single-phase hybrid inverter for larger homes. Supports up to 16kW PV input, 200A battery current, and seamless backup switching. Dual MPPT trackers and comprehensive protection features.',
        'price': 72000.00,
        'is_featured': True,
    },
    
    # COMMERCIAL PRODUCTS
    {
        'name': 'Deye Three-Phase Hybrid Inverter 12kW',
        'slug': 'deye-three-phase-hybrid-inverter-12kw',
        'category': ProductCategory.COMMERCIAL,
        'short_description': 'Three-phase commercial hybrid inverter for businesses.',
        'description': 'Deye SUN-12K-SG04LP3 12kW three-phase hybrid inverter. Ideal for shops, offices, and small businesses. Features battery backup, grid-tie capability, remote monitoring, and high efficiency. Compatible with high-voltage battery systems.',
        'price': 125000.00,
        'is_featured': True,
    },
    {
        'name': 'Growatt SPF 5000-12000 ES Plus Off-Grid Inverter',
        'slug': 'growatt-spf-5000-12000-es-plus-off-grid',
        'category': ProductCategory.COMMERCIAL,
        'short_description': 'Reliable off-grid inverter for commercial use.',
        'description': 'Growatt SPF series 5-12kW off-grid inverter with pure sine wave output. Perfect for commercial sites without grid access. Built-in MPPT controller, battery charging, and generator input support.',
        'price': 95000.00,
        'is_featured': True,
    },
    {
        'name': 'BYD Battery-Box Premium LVL 15.4kWh',
        'slug': 'byd-battery-box-premium-lvl-154kwh',
        'category': ProductCategory.COMMERCIAL,
        'short_description': 'Premium lithium battery system for commercial applications.',
        'description': 'BYD Battery-Box Premium LVL 15.4kWh modular energy storage. Expandable up to 983kWh. German engineering with BYD automotive-grade cells. 10-year warranty. Ideal for offices, shops, and commercial buildings.',
        'price': 185000.00,
        'is_featured': False,
    },
    {
        'name': 'Deye SUN-50K-SG01HP3 Commercial Inverter 50kW',
        'slug': 'deye-sun-50k-sg01hp3-commercial-50kw',
        'category': ProductCategory.COMMERCIAL,
        'short_description': 'High-power three-phase commercial inverter.',
        'description': '50kW three-phase string inverter for commercial solar projects. Features 6 MPPT inputs, IP65 protection, smart monitoring, and 99% efficiency. Suitable for supermarkets, warehouses, and large offices.',
        'price': 285000.00,
        'is_featured': True,
    },
    {
        'name': 'Solis S6 Series Three-Phase Inverter 30kW',
        'slug': 'solis-s6-series-three-phase-30kw',
        'category': ProductCategory.COMMERCIAL,
        'short_description': 'Reliable commercial solar inverter 30kW.',
        'description': 'Solis S6-EH3P30K three-phase string inverter. Wide MPPT voltage range, dual MPPT trackers, integrated WiFi monitoring. Proven reliability for commercial solar installations.',
        'price': 195000.00,
        'is_featured': False,
    },
    
    # INDUSTRIAL PRODUCTS
    {
        'name': 'Deye SUN-100K-SG01HP3 Industrial Inverter 100kW',
        'slug': 'deye-sun-100k-sg01hp3-industrial-100kw',
        'category': ProductCategory.INDUSTRIAL,
        'short_description': 'Heavy-duty 100kW inverter for industrial facilities.',
        'description': 'Deye 100kW three-phase string inverter for large-scale industrial solar. Features 10 MPPT inputs, active and reactive power control, remote monitoring, and robust protection. Designed for factories, plants, and large facilities.',
        'price': 485000.00,
        'is_featured': True,
    },
    {
        'name': 'Growatt MAX 100-125KTL3-X LV Three-Phase Inverter',
        'slug': 'growatt-max-100-125ktl3-x-lv-three-phase',
        'category': ProductCategory.INDUSTRIAL,
        'short_description': 'Industrial-grade inverter 100-125kW range.',
        'description': 'Growatt MAX series 100-125kW low-voltage three-phase inverter. Type II DC&AC SPD, 98.5% efficiency, IP66 protection. Ideal for industrial rooftop and ground-mount installations.',
        'price': 520000.00,
        'is_featured': True,
    },
    {
        'name': 'Tesla Powerpack 2 Industrial Energy Storage',
        'slug': 'tesla-powerpack-2-industrial-energy-storage',
        'category': ProductCategory.INDUSTRIAL,
        'short_description': 'Large-scale industrial battery storage system.',
        'description': 'Tesla Powerpack 2 with 210kWh usable capacity. Scalable battery system for peak shaving, load shifting, and backup power in industrial applications. Includes integrated inverter and thermal management.',
        'price': 2850000.00,
        'is_featured': False,
    },
    {
        'name': 'Sungrow ST2236UX Liquid-Cooled ESS 2.5MWh',
        'slug': 'sungrow-st2236ux-liquid-cooled-ess-25mwh',
        'category': ProductCategory.INDUSTRIAL,
        'short_description': 'Utility-scale liquid-cooled energy storage.',
        'description': 'Sungrow 2.5MWh liquid-cooled battery container. Integrated PCS, battery, HVAC, and fire suppression. Designed for utility-scale solar plants, microgrids, and large industrial facilities. 20-year design life.',
        'price': 18500000.00,
        'is_featured': False,
    },
    
    # ESS SOLUTION PRODUCTS
    {
        'name': 'Deye All-in-One ESS 10.24kWh Hybrid System',
        'slug': 'deye-all-in-one-ess-1024kwh-hybrid-system',
        'category': ProductCategory.ESS_SOLUTION,
        'short_description': 'Complete integrated home energy storage solution.',
        'description': 'Deye all-in-one ESS combining 5kW hybrid inverter and 10.24kWh LiFePO4 battery in single cabinet. Plug-and-play installation, WiFi monitoring, backup power support. Perfect turnkey solution for residential solar-plus-storage.',
        'price': 145000.00,
        'is_featured': True,
    },
    {
        'name': 'Growatt AXE All-in-One ESS 5kW/10kWh',
        'slug': 'growatt-axe-all-in-one-ess-5kw-10kwh',
        'category': ProductCategory.ESS_SOLUTION,
        'short_description': 'Modular all-in-one energy storage system.',
        'description': 'Growatt AXE integrated ESS with 5kW inverter and 10kWh battery. Modular design, easy expansion, smart energy management, and seamless backup switching. Includes mobile app control.',
        'price': 138000.00,
        'is_featured': True,
    },
    {
        'name': 'Sonnen Eco ESS 10kWh Complete System',
        'slug': 'sonnen-eco-ess-10kwh-complete-system',
        'category': ProductCategory.ESS_SOLUTION,
        'short_description': 'German-engineered premium home ESS.',
        'description': 'Sonnen Eco 10kWh all-in-one energy storage system. Premium German engineering with integrated inverter, battery, and energy manager. Smart grid-ready, 10-year warranty. Weather-resistant for indoor/outdoor installation.',
        'price': 285000.00,
        'is_featured': True,
    },
    {
        'name': 'Victron Energy ESS Package with MultiPlus-II 5kW',
        'slug': 'victron-energy-ess-package-multiplus-ii-5kw',
        'category': ProductCategory.ESS_SOLUTION,
        'short_description': 'Flexible ESS solution with Victron components.',
        'description': 'Complete Victron ESS package: MultiPlus-II 5kW inverter/charger, Cerbo GX controller, and compatible battery system. Highly configurable for off-grid, grid-tie, or hybrid installations. Remote monitoring via VRM portal.',
        'price': 165000.00,
        'is_featured': False,
    },
]


class Command(BaseCommand):
    help = 'Seed sample products for all categories'

    def handle(self, *args, **options):
        created = 0
        for item in SAMPLE_PRODUCTS:
            _, was_created = Product.objects.update_or_create(
                slug=item['slug'],
                defaults=item,
            )
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(
            f'Seed complete. {created} new products added. Total: {Product.objects.count()}'
        ))
