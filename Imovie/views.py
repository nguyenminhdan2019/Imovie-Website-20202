from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from movie.models import *
import operator
import random
from movie.initializer import search_index
from movie.views import V_Recommend
from django.http import HttpResponse, JsonResponse
from user.models import *
from django.contrib.auth.models import User
from movie.models import *

def index(request):
    data = {}
    recommend = V_Recommend()
    movie_dict = search_index.data_in_memory['movie_dict']
    if request.user.is_authenticated:
        data = {'username': request.user.get_username()}
        notifications = Notification.objects.filter(user = request.user).order_by('-date_posted')[:10]
        data['notifications'] = notifications
        # not seen 
        count_noti = UserSeenNotifycation.objects.filter(user = request.user, is_seen = False).count()
        data['count_noti'] = count_noti
    popular_movies = Popularity.objects.all().order_by('-weight')
    popular = []
    for movie in popular_movies[:11]:
        try:
            popular.append({'movieid': movie.movieid_id, 'poster': movie_dict[movie.movieid_id].poster})
        except:
            continue
    data['popular'] = popular
    popular_movie_list = [movie_dict[movie.movieid_id] for movie in popular_movies[:5]]
    data['recommendation'] = get_recommendation(request, popular_movie_list)
    data['top_movie'] = recommend.getTopMovie(request)
    data['action_movie'] = recommend.getActionMovie(request)
    data['comedy_movie'] = recommend.getComedyMovie(request)
    return render(request, 'base.html', data)

def get_recommendation(request, popular_movie_list):
    result = []
    movie_dict = search_index.data_in_memory['movie_dict']
    added_movie_list = []
    if request.user.is_authenticated:
        username = request.user.get_username()
        watched_movies = set([movie_dict[movie.movieid_id] for movie in Seen.objects.filter(username=username)] +
                             [movie_dict[movie.movieid_id] for movie in Expect.objects.filter(username=username)])
        unwatched_movies = set(search_index.data_in_memory['movie_list']) - watched_movies - set(popular_movie_list)
        # ecpect is add favourite movie
        user = request.user
        liked_movie = favourite_movie(user)
        # print(unwatched_movies())
        if len(liked_movie) == 0:
            for movie in unwatched_movies:
                result.append({'movieid': movie.movieid, 'poster': movie.poster})
                if len(result) == 11:
                    break
        else:
            if len(liked_movie) == 1:
                # use Jaccard Index
                recommend_movie = get_recommend_by_jaccard(liked_movie[0])
                movie_object_list = []
                for movieid in recommend_movie:
                    movie_object_list.append(Movie.objects.get(movieid=movieid))
                for movie in movie_object_list:
                    result.append({'movieid': movie.movieid, 'poster': movie.poster})
                return result
            elif len(liked_movie) >=2 :
                print(liked_movie)
                # user cosine similarity
                recommend_movie = get_recommend_by_cosine(liked_movie)
                movie_object_list = []
                print(recommend_movie[:5])
                if len(recommend_movie) >=20:
                    for movieid in recommend_movie:
                        movie_object_list.append(Movie.objects.get(movieid=movieid))
                    for movie in movie_object_list:
                        if movie in unwatched_movies:
                            result.append({'movieid': movie.movieid, 'poster': movie.poster})
                    return [result[i] for i in random.sample(range(len(result)), 11)]
    return result

