WELCOME_MESSAGE = (
    "Hello! I'm the East Eagle Energy service bot. "
    "Ask me about inverters, batteries, ESS, solar panels, quotes, or installation — "
    "I'm here to help right away."
)


def bot_reply_for_message(text):
    """Simple keyword replies for common technical questions."""
    q = (text or '').lower()

    if any(word in q for word in ('price', 'quote', 'cost', 'pricing', 'how much')):
        return (
            "Pricing depends on your system size and products. Our technical team can "
            "prepare a custom quote — I've notified them and they usually reply within "
            "one business day. Call China +86 137 1072 7747 or Ethiopia +251 93 321 9802."
        )

    if any(word in q for word in ('inverter', 'deye', 'growatt', 'hybrid')):
        return (
            "We supply residential and C&I inverters from trusted brands like Deye. "
            "Browse inverters at /products/inverters/ or tell us your kW needs and "
            "our team will recommend a match."
        )

    if any(word in q for word in ('battery', 'ess', 'storage', 'lifepo4', 'bess')):
        return (
            "We offer LiFePO4 battery and ESS solutions for homes and businesses. "
            "See Energy Storage at /products/ess/ or share your backup/runtime goals "
            "and our team will advise."
        )

    if any(word in q for word in ('solar panel', 'solar', 'pv', 'panel')):
        return (
            "We carry solar panels for residential and commercial projects. "
            "View options at /products/solar-panels/ or describe your roof/site "
            "and our team can help size a system."
        )

    if any(word in q for word in ('install', 'installation', 'setup', 'warranty')):
        return (
            "We support installation planning and after-sales service. Share your "
            "location and project type — our technical team will follow up with "
            "next steps and warranty details."
        )

    if any(word in q for word in ('contact', 'phone', 'call', 'email', 'hours')):
        return (
            "Main office: Room 1133, Garden Building, No. 368 Huanshi East Road, "
            "Yuexiu District, Guangzhou, China — +86 137 1072 7747. "
            "Ethiopia branch: Century Executive Tower, Addis Ababa — +251 93 321 9802. "
            "A Tanzania office is opening soon. Email info@easteagleenergy.com."
        )

    if any(word in q for word in ('hello', 'hi', 'hey', 'help')):
        return (
            "Hello! Ask me about products, system sizing, quotes, or installation. "
            "For urgent matters, call China +86 137 1072 7747 or Ethiopia +251 93 321 9802."
        )

    return (
        "Thanks for your message! I've sent it to our technical team — they'll "
        "reply to your email soon. For faster help, call China +86 137 1072 7747 "
        "or Ethiopia +251 93 321 9802."
    )
