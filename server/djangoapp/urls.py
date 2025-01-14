from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    # path for about view
    path(route='about', view=views.about, name='about'),
    # path for contact us view
    path(route='contact', view=views.contact, name='contact'),
    # path for registration
    path(route='registration', view=views.registration_request, name="registration"),
    # path for login
    path(route='login', view=views.login_request, name='login'),
    # path for logout
    path(route='logout', view=views.logout_request, name='logout'),
    # path for home/index
    path(route='', view=views.get_dealerships, name='index'),
    # path for get_dealer_by_id_view
    path(route='<int:id>', view=views.get_dealer_by_id_view, name='by_id'),
    # path for get_dealer_by_state_view
    #path(route='<str:st>', view=views.get_dealer_by_state_view, name='by_state'),
    # path for dealer reviews view
    path(route='dealer/<int:dealer_id>/', view=views.get_dealer_details, name='dealer_details'),
    # path for add a review view
    path(route='dealer/<int:dealerId>/add_review', view=views.add_review, name='add_review'),
    # path for import cars view
    path(route='import', view=views.import_cars, name='import_cars'),
    #path for add new vehicle view
    path(route='dealer/<int:dealerId>/add_vehicle', view=views.add_new_vehicle, name='add_vehicle'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)