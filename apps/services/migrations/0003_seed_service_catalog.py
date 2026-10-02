from django.db import migrations


SERVICES = [
    {
        "title": "Website Development",
        "slug": "website-development",
        "short_description": "Responsive, accessible websites built around your customers and business goals.",
        "description": "We plan and build fast, maintainable websites with clear navigation, accessible patterns and a content structure your team can grow. The work starts with your audience and ends with a site that is ready to be measured and improved.",
        "icon": "code",
    },
    {
        "title": "Web Design",
        "slug": "web-design",
        "short_description": "Distinctive digital experiences that make the next step easy to find.",
        "description": "From information architecture to responsive interface design, we create considered digital experiences for real people. Each design decision supports a clear journey, strong accessibility and a consistent brand expression.",
        "icon": "layout",
    },
    {
        "title": "E-commerce Development",
        "slug": "ecommerce-development",
        "short_description": "E-commerce experiences designed to make browsing and buying feel straightforward.",
        "description": "We develop online storefronts with useful product discovery, clear checkout steps and practical tools for managing content and catalogues. Integrations and platform choices are scoped around the way your team operates.",
        "icon": "shopping-bag",
    },
    {
        "title": "Custom Software Development",
        "slug": "custom-software-development",
        "short_description": "Purpose-built web software for processes that off-the-shelf tools do not fit.",
        "description": "We help define, design and develop custom web applications around the workflows your business depends on. Work can include discovery, data modelling, integrations, secure access and ongoing maintenance.",
        "icon": "settings",
    },
    {
        "title": "Django Development",
        "slug": "django-development",
        "short_description": "Secure, maintainable Django applications for content-rich sites and business workflows.",
        "description": "We build and improve Django websites and applications using the framework's ORM, templates, authentication and admin tools. Projects focus on clear architecture, secure defaults, automated checks and maintainable delivery.",
        "icon": "layers",
    },
    {
        "title": "Python Development",
        "slug": "python-development",
        "short_description": "Python development for integrations, automation and data-backed web products.",
        "description": "We use Python to connect systems, automate repeatable work and build dependable application services. Each solution is designed around clear inputs, useful error handling, security and the team's ability to maintain it.",
        "icon": "terminal",
    },
    {
        "title": "SEO Services",
        "slug": "seo-services",
        "short_description": "A practical search strategy that connects technical health, useful content and intent.",
        "description": "Our SEO work combines site structure, technical reviews, on-page improvements and content planning. We focus on making pages understandable to people and search engines, then track progress against agreed objectives.",
        "icon": "search",
    },
    {
        "title": "Local SEO",
        "slug": "local-seo",
        "short_description": "Help nearby customers find accurate, useful information about your business.",
        "description": "Local SEO work improves how your business appears for location-based searches through consistent business details, location pages, structured data and review workflows. Recommendations are based on your service area and available evidence.",
        "icon": "map-pin",
    },
    {
        "title": "Technical SEO",
        "slug": "technical-seo",
        "short_description": "Improve crawlability, indexation, structured data and page experience foundations.",
        "description": "Technical SEO reviews examine crawl paths, indexation, metadata, canonical signals, sitemaps, structured data, performance and mobile usability. We prioritise issues by their likely impact and provide implementation guidance.",
        "icon": "scan-search",
    },
    {
        "title": "Digital Marketing",
        "slug": "digital-marketing",
        "short_description": "Connected digital campaigns shaped around your audience, offer and business objectives.",
        "description": "We help plan and coordinate digital marketing across search, content and social channels. The approach begins with a clear audience and objective, then uses useful measurement to inform ongoing improvements.",
        "icon": "trending-up",
    },
    {
        "title": "Google Ads",
        "slug": "google-ads",
        "short_description": "Search and paid campaigns with deliberate targeting, clear landing pages and measured learning.",
        "description": "Google Ads work can include campaign planning, account structure, keyword research, ad creative, conversion tracking and ongoing optimisation. Budgets and success measures are agreed before campaigns are launched.",
        "icon": "mouse-pointer-click",
    },
    {
        "title": "Social Media Marketing",
        "slug": "social-media-marketing",
        "short_description": "Consistent social content and campaigns that give your audience a reason to engage.",
        "description": "We help define channel roles, plan content themes and create campaign assets that fit your brand and audience. Publishing and paid activity are guided by a practical calendar and clear review process.",
        "icon": "share-2",
    },
    {
        "title": "Content Marketing",
        "slug": "content-marketing",
        "short_description": "Useful content that answers real questions and supports the customer journey.",
        "description": "Content marketing starts with audience questions and the decisions they need to make. We support topic research, editorial planning, on-page content and measurement so the work remains relevant and discoverable.",
        "icon": "file-text",
    },
    {
        "title": "Branding",
        "slug": "branding",
        "short_description": "A clear visual and verbal identity that carries consistently across digital touchpoints.",
        "description": "Branding work clarifies how your business should look, sound and feel to the people it serves. The resulting direction can inform identity assets, messaging and practical guidelines for consistent use.",
        "icon": "shapes",
    },
]


def seed_services(apps, schema_editor):
    service_model = apps.get_model("services", "Service")
    service_model.objects.using(schema_editor.connection.alias).bulk_create(
        service_model(**service) for service in SERVICES
    )


def remove_services(apps, schema_editor):
    service_model = apps.get_model("services", "Service")
    slugs = [service["slug"] for service in SERVICES]
    service_model.objects.using(schema_editor.connection.alias).filter(slug__in=slugs).delete()


class Migration(migrations.Migration):
    dependencies = [("services", "0002_service_canonical_url")]

    operations = [migrations.RunPython(seed_services, remove_services)]