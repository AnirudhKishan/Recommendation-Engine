from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url (r'^userUserCollab/', include ('UserUserCollab.Urls', namespace="UserUserCollab")),
    url (r'^itemItemCollab/', include ('ItemItemCollab.Urls', namespace="ItemItemCollab")),
    
    url (r'^contentBased/', include ('ContentBased.Urls', namespace="ContentBased")),
    url (r'^hybrid/', include ('Hybrid.Urls', namespace="Hybrid")),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
