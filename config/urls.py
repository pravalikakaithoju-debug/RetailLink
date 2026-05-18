from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from .views import home

from products.views import product_list

from orders.views import (
    cart_view,
    add_to_cart,
    place_order,
    my_orders,
    order_detail,
    dashboard
)


from users.views import (
    register_view,
    login_view,
    logout_view
)

urlpatterns = [

    path('admin/', admin.site.urls),

    path('', home, name='home'),

    path('products/', product_list, name='products'),

    path('cart/', cart_view, name='cart'),

    path('add-to-cart/', add_to_cart, name='add_to_cart'),

    path('place-order/', place_order, name='place_order'),

    path('register/', register_view, name='register'),

    path('login/', login_view, name='login'),

    path('logout/', logout_view, name='logout'),
    path('my-orders/', my_orders, name='my_orders'),
    path('order/<int:order_id>/',order_detail,name='order_detail'),
    path('dashboard/',dashboard,name='dashboard'),


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)