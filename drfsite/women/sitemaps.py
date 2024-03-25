from django.contrib.sitemaps import Sitemap

from women.models import Women


class PostSiteMap(Sitemap):
    changefreq = 'monthly'
    priority = 0.9

    def items(self):
        return Women.published.all()

    def lastmod(self, obj):
        return obj.time_update