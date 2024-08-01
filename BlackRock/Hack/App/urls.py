from django.urls import path,include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns=[
    path('login/', views.login_page, name='login_page'),
    path('register/', views.register, name='register'),
    path('homepage/', views.homepage, name='homepage'),
    path('resetpass/',views.resetpass,name='resetpass'),
    path('financials/', views.viewvalues, name='financials'),
    path('mockstock/', views.mockstock, name='mockstock'),
    path('get_stock_price/', views.get_stock_price, name='get_stock_price'),
    path('module/', views.module, name='module'),
    path('contactus/', views.contactus, name='contactus'),
    path('homepage1/', views.homepage1, name='homepage1'),
    path('streamlit/', views.streamlit_view, name='streamlit'),
    # path('historical/', views.historical_data_view, name='historical_data'),
]
