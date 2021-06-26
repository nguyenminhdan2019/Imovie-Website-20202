from django.conf.urls import url
from .views import V_ExpectedMovie, V_Movie, V_Recommend, V_Tag, V_WatchedMovie, V_Statistical, V_Search
from . import models
from django.urls import include, path

urlpatterns = [

    # render data on the page
    url(r'^movie_all/(?P<page>\d*)', views.movie_whole_list, {'model': models.Movie}, name='movie_whole_list'),
    url(r'^actor_all/(?P<page>\d*)', views.actor_whole_list, {'model': models.Actor}, name='actor_whole_list'),
    url(r'^movie_detail/(?P<id>.*)', V_Movie.detailMovie, {'model': models.Movie}, name='movie_detail'),
    url(r'^actor_detail/(?P<id>.*)', V_Actor.detailActor, {'model': models.Actor}, name='actor_detail'),
    url(r'^search/(?P<item>.*)/(?P<query_string>.*)/(?P<page>\d*).*', V_Search.search, name='search'),
    url(r'^seen/(?P<movie_id>.*)', V_WatchedMovie.seen, name='seen'),
    url(r'^expect/(?P<movie_id>.*)', views.expect, name='expect'),
    url(r'^add_expect/(?P<movie_id>.*)', views.add_expect, name='expect', name='add_expect'),
    url(r'^search_suggest/(?P<query_string>.*)', V_Search.search_suggest, name='search_suggest'),

    # API  ajax send, get data for REVIEW
    path('API/like_review/', V_Review.likeReview, name='like-review'),
    path('API/review_movie/', V_Review.reviewMovie, name='review-movie'),
    path('API/reply_review/', V_Review.replyReview, name='reply-review'),
    path('API/rate_movie/', V_Review.addRate, name='rate-movie'),
    path('API/get_data_rate/', V_Review.getBreakRate, name='get_data_rate'),


    # API ajax send data for TAG
    path('API/add_tag/', V_Tag.addTag, name='add-tag'),
    path('API/delete_tag/', V_Tag.deleteTag, name='delete-tag'),

    #API send data from search bar and get Recommend search
    path('API/get_search_value/', V_Search.recommendSearch, name='get-search-value'),

    # API get data for chart Admin
    path('API/get_chart_movie_rate/', V_Statistical.getTopMovie, name='get_chart_movie'),

]
