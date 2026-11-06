from django. urls import path
from.import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[

    path('',views.Home,name='Home'),
    path('Register',views.Register,name='register'),
    path('login', views.login, name='login'),
    path('account',views.account,name='account'),
    path('logout_view', views.logout_view, name='logout_view'),
    path('addproduct', views.addproduct, name='addproduct'),
    path('view_product',views.view_product,name='view_product'),
    path('addtocart/<int:id>/', views.addtocart, name='addtocart'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
    path('confirmorder', views.confirmorder, name='confirmorder'),
    path('myorders',views.myorders,name='myorders'),

]
urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)