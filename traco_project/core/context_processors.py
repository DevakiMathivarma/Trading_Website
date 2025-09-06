from .models import FooterSettings, SocialLink, FooterLink

def footer_context(request):
    settings = FooterSettings.objects.first()
    social_links = SocialLink.objects.all()
    footer_links = FooterLink.objects.all()
    # group links into columns 1..5
    columns = {i: [] for i in range(1,6)}
    for l in footer_links:
        columns.get(l.column, []).append(l)
    return {
        "traco_footer_settings": settings,
        "traco_social_links": social_links,
        "traco_footer_columns": columns,
    }
