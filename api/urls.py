from django.urls import path, include

urlpatterns = [
    path('v1/', include('api.v1.urls')),
    #path('admin/', include('')),
    #path('manager/', include('')),
    #path('', include('')),
]
