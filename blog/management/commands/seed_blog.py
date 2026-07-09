from django.core.management.base import BaseCommand
from django.utils import timezone

from blog.models import BlogPost, HomepageAd


BLOG_POSTS = [
    {
        'title': 'East Eagle Energy Launches New Line of Deye Hybrid Inverters',
        'slug': 'east-eagle-energy-launches-deye-hybrid-inverters',
        'excerpt': 'We are excited to announce the availability of Deye\'s latest hybrid inverter series, bringing cutting-edge solar technology to Ethiopian homes and businesses.',
        'content': '''We are thrilled to announce that East Eagle Energy is now offering Deye's latest generation of hybrid inverters, bringing world-class solar technology to Ethiopia.

**What Makes Deye Inverters Special?**

Deye has established itself as a global leader in solar energy solutions, and their new hybrid inverter series represents a significant leap forward in reliability and efficiency. These inverters combine grid-tie and off-grid capabilities, allowing users to maximize their solar investment while maintaining backup power during outages.

**Key Features:**
- 97.6% peak efficiency for maximum energy harvest
- Dual MPPT trackers for optimal panel configuration
- Battery storage compatibility with multiple brands
- WiFi monitoring and smart energy management
- Seamless backup switching during power failures
- IP65 weatherproof protection

**Perfect for Ethiopian Conditions**

Ethiopia's power infrastructure is evolving, and these hybrid inverters are designed to work seamlessly in both grid-connected and off-grid scenarios. Whether you're in Addis Ababa with intermittent grid power or in a rural area with no grid access, these systems adapt to your needs.

**Available Models:**
- Residential: 3kW to 12kW single-phase
- Commercial: 12kW to 50kW three-phase
- Industrial: 50kW to 100kW+ systems

**Installation and Support**

East Eagle Energy provides complete installation services, including site assessment, system design, professional installation, and ongoing maintenance. Our team is trained and certified on all Deye products.

Contact us today at +251 93 321 9802 to learn more about how Deye hybrid inverters can power your home or business.''',
        'author': 'East Eagle Energy Team',
        'is_featured': True,
        'is_published': True,
    },
    {
        'title': 'Understanding LiFePO4 Battery Technology: Why It Matters',
        'slug': 'understanding-lifepo4-battery-technology',
        'excerpt': 'LiFePO4 (Lithium Iron Phosphate) batteries are revolutionizing energy storage. Learn why this technology is the future of solar battery systems.',
        'content': '''When it comes to solar energy storage, not all batteries are created equal. LiFePO4 (Lithium Iron Phosphate) batteries have emerged as the gold standard for residential and commercial solar installations, and for good reason.

**What is LiFePO4?**

LiFePO4 is a type of lithium-ion battery that uses iron phosphate as the cathode material. This chemistry offers significant advantages over traditional lead-acid batteries and other lithium-ion variants.

**Key Advantages:**

1. **Longevity**: LiFePO4 batteries typically last 6000+ charge cycles, compared to 500-1000 cycles for lead-acid batteries. This means 10-15 years of reliable service.

2. **Safety**: Iron phosphate chemistry is inherently stable and doesn't suffer from thermal runaway like some other lithium batteries. They're extremely safe for home use.

3. **Depth of Discharge**: You can safely use 80-90% of a LiFePO4 battery's capacity, compared to only 50% for lead-acid. This means you get more usable energy from the same rated capacity.

4. **Temperature Performance**: These batteries perform well in Ethiopia's climate, maintaining efficiency in both hot and moderate conditions.

5. **Low Maintenance**: Unlike lead-acid batteries, LiFePO4 requires no watering, equalizing, or regular maintenance.

**Environmental Benefits**

LiFePO4 batteries contain no toxic heavy metals like lead or cadmium. They're more environmentally friendly and easier to recycle at end-of-life.

**Cost Consideration**

While LiFePO4 batteries have a higher upfront cost, their longer lifespan and higher efficiency make them more economical over the system's lifetime. When you calculate cost per cycle, LiFePO4 is actually cheaper than lead-acid.

**Brands We Trust**

At East Eagle Energy, we work with leading LiFePO4 manufacturers:
- Deye (5.12kWh modular systems)
- Pylontech (US3000C and US5000 series)
- BYD (Battery-Box Premium)

**Is LiFePO4 Right for You?**

For most solar installations in Ethiopia, the answer is yes. Whether you're building a new system or upgrading an existing one, LiFePO4 batteries offer the best combination of performance, safety, and value.

Contact East Eagle Energy to discuss the right battery solution for your needs.''',
        'author': 'Technical Team',
        'is_featured': True,
        'is_published': True,
    },
    {
        'title': 'Solar Energy Incentives and Opportunities in Ethiopia 2026',
        'slug': 'solar-energy-incentives-ethiopia-2026',
        'excerpt': 'Ethiopia is rapidly expanding its renewable energy sector. Discover the latest incentives, programs, and opportunities for solar adoption.',
        'content': '''Ethiopia's commitment to renewable energy is creating unprecedented opportunities for businesses and homeowners to adopt solar power. Here's what you need to know about the current landscape.

**Government Initiatives**

The Ethiopian government has set ambitious targets for renewable energy expansion as part of its Climate Resilient Green Economy strategy. Several programs are making solar more accessible:

1. **Tax Incentives**: Import duty exemptions on solar equipment continue to reduce upfront costs.

2. **Net Metering Pilots**: Select regions are testing net metering programs that allow solar system owners to sell excess power back to the grid.

3. **Rural Electrification**: Off-grid solar programs are expanding to underserved communities.

**Industrial and Commercial Benefits**

Businesses can significantly reduce operating costs through solar adoption:

- **Reduced Energy Bills**: Lock in predictable energy costs and reduce grid dependency
- **Backup Power**: Eliminate productivity losses during outages
- **Corporate Sustainability**: Meet environmental goals and improve corporate image
- **Fast ROI**: Most commercial systems pay for themselves in 3-5 years

**Residential Advantages**

For homeowners, solar power means:

- **Energy Independence**: Reduce or eliminate grid dependency
- **Reliable Power**: Keep essential appliances running during outages
- **Property Value**: Solar-equipped homes command premium prices
- **Long-term Savings**: 25+ year system lifespan provides decades of savings

**Financing Options**

While upfront costs can be significant, several financing models are emerging:

- Traditional bank loans
- Equipment financing through suppliers
- Group buying programs for reduced costs
- Corporate PPAs (Power Purchase Agreements) for businesses

**Technology Improvements**

Solar technology continues to improve while costs decline:

- Panel efficiency has increased 15-20% in recent years
- Battery costs have dropped by 50% since 2020
- Smart inverters optimize energy usage automatically
- Monitoring systems provide real-time performance data

**Getting Started**

East Eagle Energy offers free site assessments and system design consultations. We'll evaluate your property, estimate your energy savings, and design a system that meets your needs and budget.

The solar opportunity in Ethiopia is stronger than ever. Don't wait—start your renewable energy journey today.

Contact: +251 93 321 9802 | info@easteagleenergy.com''',
        'author': 'East Eagle Energy',
        'is_featured': True,
        'is_published': True,
    },
    {
        'title': 'Choosing the Right Inverter Size for Your Home',
        'slug': 'choosing-right-inverter-size-home',
        'excerpt': 'Selecting the correct inverter size is crucial for system performance and longevity. This guide helps you determine the right capacity.',
        'content': '''One of the most common questions we receive is: "What size inverter do I need?" The answer depends on several factors, and getting it right is essential for optimal system performance.

**Understanding Power Requirements**

First, you need to assess your power consumption:

1. **List Your Appliances**: Make a list of everything you want to power
2. **Check Wattage**: Find the wattage rating on each appliance
3. **Calculate Total Load**: Add up the wattages to get your peak demand
4. **Consider Startup Surge**: Some appliances (motors, pumps) require 2-3x their running wattage to start

**Typical Ethiopian Home Loads**

Here's what a typical home might use:

- Refrigerator: 150-300W running, 600-900W startup
- Lights (LED): 10-20W each
- TV: 50-150W
- Fan: 50-75W
- Washing Machine: 500-1000W
- Water Pump: 750-1500W startup surge
- Air Conditioner: 1000-2000W

**Sizing Guidelines**

**Small Home (3-5kW Inverter)**
- 2-3 bedroom home
- Basic appliances: lights, TV, fans, refrigerator
- No AC or heavy appliances
- Typical homes in urban areas

**Medium Home (5-8kW Inverter)**
- 3-4 bedroom home
- Standard appliances plus occasional AC use
- Small water pump
- Most suburban homes

**Large Home (8-12kW Inverter)**
- 4+ bedroom home
- Multiple ACs, large refrigerators
- Heavy appliances (large pumps, workshop equipment)
- Villas and larger properties

**Safety Margin**

Always add a 20-30% safety margin to your calculations. This accounts for:
- Future load growth
- Simultaneous appliance operation
- Startup surges
- System efficiency losses

**Battery Considerations**

Your battery bank should be sized to match your inverter and provide adequate backup time:

- Minimum backup: 2-4 hours (5-10kWh for a 3kW load)
- Half-day backup: 6-8 hours (15-20kWh for a 3kW load)
- Full-day backup: 24 hours (requires substantial battery investment)

**Professional Assessment**

While these guidelines help, every home is unique. East Eagle Energy provides free load assessments where we:

1. Analyze your electricity bills
2. Measure your current consumption patterns
3. Plan for future growth
4. Recommend the optimal system configuration
5. Provide detailed cost estimates

**Popular Systems We Install**

- **Deye 5kW Hybrid**: Perfect for average homes, expandable battery
- **Deye 8kW Hybrid**: Ideal for larger homes with AC
- **Deye 12kW Three-Phase**: Commercial and large residential properties

Don't guess—get it right the first time. Contact us for a professional assessment: +251 93 321 9802''',
        'author': 'Technical Team',
        'is_featured': False,
        'is_published': True,
    },
    {
        'title': 'Maintenance Tips for Your Solar Power System',
        'slug': 'maintenance-tips-solar-power-system',
        'excerpt': 'Proper maintenance ensures your solar system operates at peak efficiency for decades. Follow these essential maintenance guidelines.',
        'content': '''Solar power systems are remarkably low-maintenance, but regular care ensures optimal performance and longevity. Here's your comprehensive maintenance guide.

**Monthly Checks**

**1. Visual Inspection**
- Check panels for visible dirt, bird droppings, or debris
- Look for any physical damage or cracks
- Ensure mounting brackets are secure
- Check for shading from growing trees or new structures

**2. Monitor Performance**
- Review your monitoring app/system regularly
- Compare output to expected values
- Note any significant drops in production
- Check battery state of charge and health indicators

**Quarterly Maintenance**

**1. Panel Cleaning**
Ethiopia's dry season creates dust buildup that can reduce efficiency by 10-20%. Clean panels quarterly or more often if needed:

- Use soft cloth or sponge with clean water
- Avoid harsh chemicals or abrasive materials
- Clean early morning or evening (avoid hot panels)
- For tall installations, hire professional cleaners

**2. Connection Check**
- Inspect all visible wire connections
- Look for corrosion or loose connections
- Check junction boxes are properly sealed
- Ensure inverter ventilation isn't blocked

**Annual Professional Service**

We recommend annual professional maintenance including:

- Comprehensive system testing
- Inverter diagnostic check
- Battery health assessment
- Connection tightening and cleaning
- Performance optimization
- Firmware updates (if available)

**Battery Maintenance**

**LiFePO4 Batteries** (minimal maintenance):
- Check for error codes on BMS
- Ensure proper ventilation
- Keep batteries cool and dry
- Monitor cell balance through monitoring system

**Lead-Acid Batteries** (if you have them):
- Check electrolyte levels monthly
- Top up with distilled water as needed
- Check for sulfation or corrosion on terminals
- Perform equalization charge quarterly

**Inverter Care**

- Keep inverter area well-ventilated
- Don't block cooling vents
- Keep installation area clean and dust-free
- Listen for unusual sounds (may indicate fan issues)
- Check display regularly for error messages

**Warning Signs to Watch For**

Contact us immediately if you notice:
- Significant drop in power production (>15%)
- Error messages on inverter display
- Strange noises from inverter or batteries
- Physical damage to panels or equipment
- Frequent system shutdowns
- Battery not holding charge

**Warranty Considerations**

Most equipment comes with warranties:
- Solar panels: 25-year performance warranty
- Inverters: 5-10 year warranty
- Batteries: 5-10 year warranty

Proper maintenance and documentation helps ensure warranty coverage if issues arise.

**East Eagle Energy Maintenance Plans**

We offer annual maintenance contracts that include:
- 4 quarterly service visits
- Professional panel cleaning
- Comprehensive system testing
- Priority emergency response
- Performance reporting
- Discounted repairs and parts

**DIY vs. Professional**

Basic cleaning and monitoring can be done yourself, but we recommend professional annual service. Our technicians have specialized training and equipment to fully diagnose and optimize your system.

**Cost of Neglect**

Poor maintenance can cost you:
- 20-30% reduced energy production from dirty panels
- Premature equipment failure
- Voided warranties
- Expensive emergency repairs

Regular maintenance is a small investment that protects your much larger solar investment.

Schedule your annual maintenance today: +251 93 321 9802''',
        'author': 'Service Department',
        'is_featured': False,
        'is_published': True,
    },
    {
        'title': 'Commercial Solar: Reducing Business Operating Costs',
        'slug': 'commercial-solar-reducing-business-costs',
        'excerpt': 'Ethiopian businesses are discovering that solar power dramatically reduces overhead costs while providing reliable energy. Learn how.',
        'content': '''For businesses operating in Ethiopia, energy costs and reliability are major concerns. Commercial solar power offers a compelling solution that improves both your bottom line and operational reliability.

**The Business Case for Solar**

**1. Dramatic Cost Savings**
Typical commercial electricity rates in Ethiopia range from 2-4 Birr/kWh depending on usage tier. Solar power, once installed, produces electricity for virtually free:

- Average payback period: 3-5 years
- 25+ year system lifespan
- 20+ years of free electricity after payback
- Protection from future rate increases

**2. Improved Reliability**
Grid power interruptions cost businesses thousands in:
- Lost productivity
- Spoiled inventory
- Damaged equipment
- Customer dissatisfaction

Solar with battery backup provides uninterrupted power during outages.

**3. Environmental Credentials**
Modern consumers and partners increasingly value sustainability:
- Reduce your carbon footprint
- Meet corporate sustainability goals
- Improve brand image
- Qualify for green certifications

**Industries Benefiting Most**

**Manufacturing**
- 24/7 power for production lines
- Reduce operating costs
- Improve profit margins
- Power-intensive processes become viable

**Hospitality**
- Hotels and restaurants need reliable power
- Keep refrigeration running
- Maintain guest comfort (lighting, AC)
- Protect reservations systems and POS

**Retail**
- Keep stores open during outages
- Protect refrigerated goods
- Maintain security systems
- Process transactions without interruption

**Agriculture**
- Power irrigation pumps
- Cold storage for produce
- Processing equipment
- Greenhouses and controlled environments

**Healthcare**
- Critical equipment must never fail
- Vaccine refrigeration
- Diagnostic equipment
- Emergency backup for clinics

**Real-World Example**

A mid-size hotel in Addis Ababa installed a 50kW solar system with 100kWh battery backup:

**Investment**: 4.2 million Birr
**Monthly Savings**: 85,000 Birr (reduced grid electricity costs)
**Annual Savings**: 1,020,000 Birr
**Payback Period**: 4.1 years
**25-Year Savings**: 21+ million Birr (accounting for energy inflation)

**System Components for Businesses**

**Small Business (10-20kW)**
- Shops, small offices, restaurants
- 20-40kWh battery backup
- Investment: 800,000 - 1.6M Birr

**Medium Business (30-60kW)**
- Hotels, supermarkets, clinics
- 60-120kWh battery backup
- Investment: 2.5M - 5M Birr

**Large Business (100kW+)**
- Factories, large hotels, warehouses
- Customized battery systems
- Investment: 8M+ Birr

**Financing Options**

Several approaches make commercial solar accessible:

1. **Cash Purchase**: Best ROI, own system immediately
2. **Bank Loans**: Leverage business credit
3. **Equipment Financing**: Spread cost over 3-5 years
4. **Power Purchase Agreements**: No upfront cost, pay per kWh

**Tax and Accounting Benefits**

- Solar equipment qualifies as capital investment
- Accelerated depreciation possible in some cases
- Import duty exemptions on solar equipment
- Reduces ongoing operating expenses

**Getting Started**

East Eagle Energy specializes in commercial installations:

1. **Free Site Assessment**: We visit your facility and analyze energy usage
2. **Custom Design**: System tailored to your needs and budget
3. **ROI Analysis**: Detailed financial projections
4. **Professional Installation**: Minimal business disruption
5. **Training**: We train your staff on system operation
6. **Ongoing Support**: Maintenance and monitoring services

**Success Stories**

We've installed systems for:
- 20+ hotels across Ethiopia
- 15+ manufacturing facilities
- 30+ retail and office buildings
- 10+ agricultural operations
- 5+ healthcare facilities

**Take Action Now**

Energy costs will only increase. Lock in low electricity costs today and protect your business from future uncertainty.

Schedule a free commercial assessment: +251 93 321 9802 | info@easteagleenergy.com

**East Eagle Energy** - Powering Ethiopian businesses since 2022.''',
        'author': 'Commercial Sales Team',
        'is_featured': False,
        'is_published': True,
    },
]


HOMEPAGE_ADS = [
    {
        'title': 'Deye Hybrid Inverters Now Available',
        'subtitle': 'Latest generation solar inverters with battery storage - Professional installation included',
        'button_text': 'View Products',
        'link_url': '/products/category/residential/',
        'display_order': 1,
        'is_active': True,
    },
    {
        'title': 'Free Solar System Assessment',
        'subtitle': 'Get expert consultation and custom system design for your home or business',
        'button_text': 'Get Free Quote',
        'link_url': '/#quote',
        'display_order': 2,
        'is_active': True,
    },
    {
        'title': 'Commercial Solar Solutions',
        'subtitle': 'Reduce operating costs by up to 70% with professional solar installations',
        'button_text': 'Learn More',
        'link_url': '/products/category/commercial/',
        'display_order': 3,
        'is_active': True,
    },
]


class Command(BaseCommand):
    help = 'Seed blog posts and homepage ads'

    def handle(self, *args, **options):
        # Seed blog posts
        blog_created = 0
        for item in BLOG_POSTS:
            _, was_created = BlogPost.objects.update_or_create(
                slug=item['slug'],
                defaults=item,
            )
            if was_created:
                blog_created += 1

        # Seed homepage ads
        ad_created = 0
        for item in HOMEPAGE_ADS:
            _, was_created = HomepageAd.objects.update_or_create(
                title=item['title'],
                defaults=item,
            )
            if was_created:
                ad_created += 1

        self.stdout.write(self.style.SUCCESS(
            f'Seed complete!\n'
            f'Blog Posts: {blog_created} new, {BlogPost.objects.count()} total\n'
            f'Homepage Ads: {ad_created} new, {HomepageAd.objects.count()} total'
        ))
