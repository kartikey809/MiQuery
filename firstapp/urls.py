from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('explore',views.explore,name='explore'),
    path('dna/',views.dna,name='dna'),
    path('tech/',views.tech,name='tech'),
    path('eng/',views.eng,name='eng'),
    path('uploadcode/',views.uploadcode,name='uploadcode'),
    path('updatecode/<int:id>/',views.updatecode,name='updatecode'),
    path('viewcode/<int:id>/',views.viewcode,name='viewcode'),
    path('upvote/<int:id>/',views.upvote,name='upvote'),
    path('copycount/<int:id>/',views.copycount,name='copycount'),
    path('newcode',views.newcode,name='newcode'),
    path('advsearch',views.advsearch,name='advsearch'),
    path('adv_searcher',views.adv_searcher,name='adv_searcher'),
    path('simsearch',views.simsearch,name='simsearch'),
    path('sim_search',views.sim_search,name='sim_search'),
    path('gpt_explain_page',views.gpt_explain_page,name='gpt_explain_page'),
    path('gpt_explain',views.gpt_explain,name='gpt_explain'),
    path('ppt_explain_page',views.ppt_explain_page,name='ppt_explain_page'),
    path('ppt_explain',views.ppt_explain,name='ppt_explain'),
    path('browseusecase',views.browseusecase,name='browseusecase'),
    path('scoreboard',views.scoreboard,name='scoreboard'),
]
