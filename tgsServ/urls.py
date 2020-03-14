"""tgsServ URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings

from tgsAdmin.views.test import TestView
from tgsAdmin.views.login import LoginView
from tgsAdmin.views.login import LogoutView
from tgsAdmin.views.userInfo import UserInfoView
from tgsAdmin.views.media import MediaView, MediaSort
from tgsAdmin.views.option import OptionView, LocationView, PortView, ChargeSortView
from tgsAdmin.views.advert import AdvertiserView
from tgsAdmin.views.plan import PlanView, export_as_excel, export_advert_statement, PlanBatchView
from tgsAdmin.views.settlment import SettlementEditView, SettlementView, StatementView, MediaStatementsView
from tgsAdmin.views.plan import PlanEditView
from tgsAdmin.views.checkout import AdvertCheckoutView
from tgsAdmin.views.statement import AdvertStatementsView

# from tgs.views.service import AdServiceView,ServiceEditView
# from tgs.views.mediadata import MediaDataView
# from tgs.views.adData import AdDataView

urlpatterns = [

    path('admin/', admin.site.urls),
    path('test', TestView.as_view()),



    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('userInfo', UserInfoView.as_view()),

    path('options', OptionView.as_view()),
    path('locations', LocationView.as_view()),
    path('ports', PortView.as_view()),
    path('chargeSorts', ChargeSortView.as_view()),

    path('media', MediaView.as_view()),
    path('advertisers', AdvertiserView.as_view()),

    path('plans', PlanView.as_view()),
    path('plans/batch', PlanBatchView.as_view()),

    re_path('plans/(?P<id>\d+)', PlanEditView.as_view()),

    path('settlements', SettlementView.as_view()),

    path('statements', StatementView.as_view()),

    path('advertCheckout', AdvertCheckoutView.as_view()),

    path('mediaStatements', MediaStatementsView.as_view()),
    path('advertStatements', AdvertStatementsView.as_view()),

    re_path('settlements/(?P<id>\d+)', SettlementEditView.as_view()),

    # path('planSettlement', PlanView.as_view()),

    # re_path('media/(?P<id>\d+)', MediaEditView.as_view()),
    path('media_sorts/', MediaSort.as_view()),

    path("export", export_as_excel),
    path("exportAdvertStatement", export_advert_statement)
    #
    # path('service', AdServiceView.as_view()),
    # re_path('service/(?P<serv_id>\d+)', ServiceEditView.as_view()),
    #
    # path('mediaData',MediaDataView.as_view()),
    # path('adData',AdDataView.as_view()),
    # # media路径配置
    # re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})

]
