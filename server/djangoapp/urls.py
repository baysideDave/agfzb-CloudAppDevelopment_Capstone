from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL
    
    # path for index view
    # path(route='', view=views.index, name='index'),
 
    path(route='', view=views.get_dealerships, name='index'),
    
    # path for about view
    path(route='about/', view=views.about, name='about'),

    # path for contact us view
    path(route='contact/', view=views.contact, name='contact'),

    # path for registration
    path('registration/', views.registration_request, name='registration'),

    # path for login
    path(route='login/', view=views.login_request, name='login'),

    # path for logout
    path('logout/', view=views.logout_request, name='logout'),
    
    #path(route='', view=views.get_dealerships, name='index'),

    # path for dealer reviews view
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),

    # path for add a review view

    #path(route='add_review/<int:dealer_id>/', view=views.add_review, name="add_review"),

    re_path(r'^add_review/',   view=views.add_review, name="dgxyz"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)