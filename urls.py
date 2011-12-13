from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'glitch.views.home', name='home'),
    # url(r'^glitch/', include('glitch.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'^$', 'ecurnomics.views.list_items'),
    (r'^auctions/', 'ecurnomics.views.list_items'),
    (r'^prices_for_item/(?P<class_tsid>[^/]+)', 'ecurnomics.views.prices_for_item'),
)
