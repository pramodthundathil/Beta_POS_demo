from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Home import views  # Make sure Home is an installed app and views.py exists

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include('Home.urls')),
    path("inventory/", include('Inventory.urls')),
    path("pos/", include('POS.urls')),
    path("finance/", include('Finance.urls')),
   
]
   


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





# Define error handlers
handler404 = 'Home.views.custom_404'
handler500 = 'Home.views.custom_500'
