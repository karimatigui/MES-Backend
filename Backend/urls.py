from django.contrib import admin  # type: ignore
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static  
# Modular view imports
from .views.get_operations import get_operations
from .views.get_token import get_token
from .views.get_dispatch_data import get_dispatch_data
from .views.get_nc_data import get_nc_data
from .views.post_nc import post_nc
from .views.complete_order import complete_order
from .views.get_inventory import get_inventory
from .views.get_items import get_items
from .views.report_operation import report_operation
from .views.get_operation_data import get_operation_data
from .views.post_initiate_materials import post_initiate_materials
from .views.get_materials import get_materials
from .views.get_related_nc_data import get_related_nc_data
from .views.post_nc_attachment import post_nc_attachment
from .views.create_ionapi_credentials import create_ionapi_credentials
from .views.get_ionapi_credential import get_ionapi_credential
from .views.create_user import create_user
from .views.get_users import get_users
from .views.get_user_data import get_user_data
from .views.delete_user import delete_user
from .views.update_user import update_user
from .views.login_user import login_user



urlpatterns = [
    path('admin/', admin.site.urls),

    # Core APIs
    path('api/operations/', get_operations),
    path('api/get-token/', get_token),
    path('api/dispatch-data/', get_dispatch_data), 
    path('api/nc-data/', get_nc_data), 
    path('api/post_nc/', post_nc), 
    path('api/completeorder/', complete_order), 
    path('api/get_inventory/', get_inventory), 
    path('api/get_items/', get_items), 

    # Operations
    path('api/report_operation/', report_operation), 
    path('api/get_operation_data/', get_operation_data), 
    path('api/post_initiate_materials/', post_initiate_materials), 
    path('api/get_materials/', get_materials), 
    path('api/get_related_nc_data/', get_related_nc_data), 
    path('api/post_nc_attachment/', post_nc_attachment), 

    # # ION API
    path('api/create_ionapi_credentials/', create_ionapi_credentials), 
    path('api/get_ionapi_credential/', get_ionapi_credential),

    # Users
    path('api/create_user/', create_user),
    path('api/get_users/', get_users),
    path('api/delete_user/<int:user_id>/', delete_user),
    path('api/update_user/<int:user_id>/', update_user),
    path('api/get_user_data/<int:user_id>/', get_user_data),
    path('api/login/', login_user, name='login_user'),
    

    # Auth app
    path('api/', include('auth_app.urls')),
]
# Only for development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)