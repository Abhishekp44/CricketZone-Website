from django.urls import path
from cricketapp import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('home', views.home),
    path('login',views.user_login),
    path('logout',views.user_logout),
    path('register',views.register),
    path('dashboard',views.dashboard),
    path('search',views.search),
    path('teams',views.teams),
    path('league',views.league),
    path('teams/<tid>',views.players),
    path('matches',views.matches),
    path('rank_m',views.rank_m),
    path('rank_w',views.rank_w),
    path('scorecard/<sid>',views.scorecard),
    path('tickets',views.tickets),
    path('contact',views.contact_us),
    path('thankyou',views.thankyou),
    path('addtocart/<pid>',views.add),
    path('viewcart',views.view),
    path('updateqty/<x>/<cid>',views.updateqty),
    path('pay',views.   pay),
    path('makepayment',views.makepayment),
    path('paymentsuccess',views.paymentsuccess),
    path('updateseats',views.updateseats),
    path('contact',views.contact),
    path('about',views.about),
]

urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)