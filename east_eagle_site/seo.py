"""Shared SEO schema and helpers for Google site name + sitelink signals."""

import json

SITE_URL = 'https://www.easteagleenergy.com'
ORG_ID = f'{SITE_URL}/#organization'
WEBSITE_ID = f'{SITE_URL}/#website'

MAIN_NAV = [
    {'name': 'Products', 'path': '/products/'},
    {'name': 'Blog', 'path': '/blog/'},
    {'name': 'About Us', 'path': '/about/'},
    {'name': 'Contact', 'path': '/contact/'},
]


def organization_node():
    return {
        '@type': 'Organization',
        '@id': ORG_ID,
        'name': 'East Eagle Energy',
        'alternateName': ['East Eagle Energy PLC', 'EEE'],
        'url': SITE_URL,
        'logo': {
            '@type': 'ImageObject',
            'url': f'{SITE_URL}/images/favicon-512.png',
            'width': 512,
            'height': 512,
        },
        'description': (
            'East Eagle Energy specializes in solar inverters, LiFePO4 batteries, '
            'and energy storage systems for homes and businesses worldwide.'
        ),
        'foundingDate': '2022',
        'address': {
            '@type': 'PostalAddress',
            'streetAddress': 'Century Executive Tower, 12-Room Number F12/06',
            'addressLocality': 'Addis Ababa',
            'addressCountry': 'ET',
        },
        'telephone': '+251933219802',
        'sameAs': [
            'https://www.facebook.com/easteagleenergy',
            'https://www.linkedin.com/company/easteagleenergy',
        ],
    }


def website_node():
    return {
        '@type': 'WebSite',
        '@id': WEBSITE_ID,
        'url': SITE_URL,
        'name': 'East Eagle Energy',
        'alternateName': ['East Eagle Energy PLC', 'easteagleenergy.com'],
        'description': 'Global provider of solar energy solutions',
        'publisher': {'@id': ORG_ID},
        'inLanguage': 'en',
        'potentialAction': {
            '@type': 'SearchAction',
            'target': f'{SITE_URL}/products/search/?q={{search_term_string}}',
            'query-input': 'required name=search_term_string',
        },
    }


def main_navigation_node():
    return {
        '@type': 'ItemList',
        '@id': f'{SITE_URL}/#main-navigation',
        'name': 'East Eagle Energy main navigation',
        'itemListElement': [
            {
                '@type': 'SiteNavigationElement',
                'position': index,
                'name': item['name'],
                'url': f"{SITE_URL}{item['path']}",
            }
            for index, item in enumerate(MAIN_NAV, start=1)
        ],
    }


def webpage_node(url, name, description=None):
    page = {
        '@type': 'WebPage',
        '@id': f'{url}#webpage',
        'url': url,
        'name': name,
        'isPartOf': {'@id': WEBSITE_ID},
        'about': {'@id': ORG_ID},
        'publisher': {'@id': ORG_ID},
        'inLanguage': 'en',
    }
    if description:
        page['description'] = description
    return page


def breadcrumb_node(items):
    return {
        '@type': 'BreadcrumbList',
        'itemListElement': [
            {
                '@type': 'ListItem',
                'position': index,
                'name': item['name'],
                'item': item['url'],
            }
            for index, item in enumerate(items, start=1)
        ],
    }


def build_schema_graph(*extra_nodes, include_navigation=False):
    graph = [organization_node(), website_node()]
    if include_navigation:
        graph.append(main_navigation_node())
    graph.extend(extra_nodes)
    return {'@context': 'https://schema.org', '@graph': graph}


def build_page_schema(*extra_nodes):
    """Page-only structured data; site Organization/WebSite come from context processor."""
    if not extra_nodes:
        return ''
    return json.dumps({'@context': 'https://schema.org', '@graph': list(extra_nodes)})


def dumps_schema(*extra_nodes, include_navigation=False):
    return json.dumps(build_schema_graph(*extra_nodes, include_navigation=include_navigation))


def site_schema_json():
    """Organization + WebSite on every page for consistent Google site name signals."""
    return dumps_schema()


def home_schema_json():
    return build_page_schema(
        webpage_node(
            SITE_URL + '/',
            'East Eagle Energy | Energy Solutions',
            (
                'East Eagle Energy - Global provider of solar inverters, LiFePO4 batteries, '
                'and energy storage systems.'
            ),
        ),
        main_navigation_node(),
    )


def about_schema_json():
    url = f'{SITE_URL}/about/'
    return build_page_schema(
        webpage_node(url, 'About East Eagle Energy', 'About East Eagle Energy'),
        breadcrumb_node([
            {'name': 'East Eagle Energy', 'url': SITE_URL + '/'},
            {'name': 'About Us', 'url': url},
        ]),
    )


def contact_schema_json():
    url = f'{SITE_URL}/contact/'
    return build_page_schema(
        webpage_node(url, 'Contact East Eagle Energy', 'Contact East Eagle Energy for solar quotes and support.'),
        breadcrumb_node([
            {'name': 'East Eagle Energy', 'url': SITE_URL + '/'},
            {'name': 'Contact', 'url': url},
        ]),
    )
