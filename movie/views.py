from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from movie.models import *
from django.http import HttpResponse, JsonResponse
import json
import math
import random
from movie.initializer import search_cache, search_index
#import sort value for dict
import operator
from django.contrib.auth.decorators import login_required
from user.models import Activity, Notification, UserSeenNotifycation
from django.views import View

#add average for rate 
from django.db.models import Avg

# ML, DL python 
import pandas as pd
import numpy as np
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from django.utils import timezone
import humanize
import datetime as dt
from datetime import timedelta

class V_WatchedMovie(View):
    # function handling seen object
    def add_seen(self, request, movie_id):
        if request.is_ajax():
            # check seen object already exists
            history = Seen.objects.filter(movieid_id=movie_id, username=request.user.get_username())
            # create seen object
            if len(history) == 0:
                movie = Popularity.objects.get(movieid_id=movie_id)
                weight = movie.weight
                movie.delete()
                # if user seen movie , popularity + 3
                new_record = Popularity(movieid_id=movie_id, weight=weight + 2)
                new_record.save()
                new_record = Seen(movieid_id=movie_id, username=request.user.get_username())
                new_record.save()
                return HttpResponse('1')
            else:
                # delete seen object
                history.delete()
                return HttpResponse('0')

    def seen(self, request):
        if request.POST:
            try:
                d = Seen.objects.get(username=request.user.get_username(), movieid_id=movie_id)
                d.delete()
            except:
                return render(self, request, '404.html')
        movie_dict = search_index.data_in_memory['movie_dict']
        records = Seen.objects.filter(username=request.user.get_username())
        movies = []
        watched_movies = set([movie_dict[movie.movieid_id] for movie in records ] +
                            [movie_dict[movie.movieid_id] for movie in Expect.objects.filter(username=request.user.username)])
        unwatched_movies = set(search_index.data_in_memory['movie_list']) - watched_movies
        
        data = {}
        recommend = V_Recommend()
        # add you may also like movie - recommend here 

        data['top_movie'] = top_movie(self, request)
        data['action_movie'] = action_movie(self, request)
        data['comedy_movie'] = comedy_movie(self, request)
        list_movie_id = []
        #id movie
        recommend_movie = []
        recommend = []
        recommend_for_seen_movie = []
        for record in records:
            movie_id = str(record).split('|')[1]
            movies.append(Movie.objects.get(movieid=movie_id))
            list_movie_id.append(movie_id)
        if len(list_movie_id) >= 2:
            recommend_movie = get_recommend_by_cosine(list_movie_id)
            for movieid in recommend_movie:
                recommend.append(Movie.objects.get(movieid=movieid))
            for movie in recommend:
                if movie not in watched_movies:
                    recommend_for_seen_movie.append({'movieid': movie.movieid, 'poster': movie.poster})
        if len(list_movie_id) == 1:
            recommend_movie = recommend.get_recommend_by_jaccard(list_movie_id[0])
            for movieid in recommend_movie:
                recommend.append(Movie.objects.get(movieid=movieid))
            for movie in recommend:
                if movie not in watched_movies:
                    recommend_for_seen_movie.append({'movieid': movie.movieid, 'poster': movie.poster})
        if len(list_movie_id) == 0:
            for movie in unwatched_movies:
                    recommend_for_seen_movie.append({'movieid': movie.movieid, 'poster': movie.poster})
                    if len(recommend_for_seen_movie) == 11:
                        break
        if len(recommend_for_seen_movie) > 11:
            recommend_for_seen_movie = [recommend_for_seen_movie[i] for i in random.sample(range(len(recommend_for_seen_movie)), 11)]

        data['recommend_movies'] = recommend_for_seen_movie
        data['items'] = movies
        data['number_seen_movie'] = len(movies)
        return render(self, request, 'seen.html', data)


class V_ExpectedMovie(View):
    # function handling expect object
    def add_expect(self, request, movie_id):
        if request.is_ajax():
            history = Expect.objects.filter(movieid_id=movie_id, username=request.user.get_username())
            if len(history) == 0:
                movie = Popularity.objects.get(movieid_id=movie_id)
                weight = movie.weight
                movie.delete()
                # add want to see movie , populartity +2
                new_record = Popularity(movieid_id=movie_id, weight=weight + 2)
                new_record.save()
                new_record = Expect(movieid_id=movie_id, username=request.user.get_username())
                new_record.save()
                return HttpResponse('2')
            else:
                history.delete()
                return HttpResponse('0')

    def expect(self, request):
        if request.POST:
            try:
                d = Expect.objects.get(username=request.user.get_username(), movieid_id=movie_id)
                d.delete()
            except:
                return render(self, request, '404.html')
        movie_dict = search_index.data_in_memory['movie_dict']
        records = Expect.objects.filter(username=request.user.get_username())
        movies = []
        watched_movies = set([movie_dict[movie.movieid_id] for movie in records ] +
                            [movie_dict[movie.movieid_id] for movie in Expect.objects.filter(username=request.user.username)])
        unwatched_movies = set(search_index.data_in_memory['movie_list']) - watched_movies
        
        data = {}
        recommend = V_Recommend()
        # add you may also like movie - recommend here 

        data['top_movie'] = top_movie(self, request)
        data['action_movie'] = action_movie(self, request)
        data['comedy_movie'] = comedy_movie(self, request)
        list_movie_id = []
        #id movie
        recommend_movie = []
        recommend = []
        recommend_for_expect_movie = []
        for record in records:
            movie_id = str(record).split('|')[1]
            movies.append(Movie.objects.get(movieid=movie_id))
            list_movie_id.append(movie_id)
        if len(list_movie_id) >= 2:
            recommend_movie = get_recommend_by_cosine(list_movie_id)
            for movieid in recommend_movie:
                recommend.append(Movie.objects.get(movieid=movieid))
            for movie in recommend:
                if movie not in watched_movies:
                    recommend_for_expect_movie.append({'movieid': movie.movieid, 'poster': movie.poster})
        if len(list_movie_id) == 1:
            recommend_movie = recommend.get_recommend_by_jaccard(list_movie_id[0])
            for movieid in recommend_movie:
                recommend.append(Movie.objects.get(movieid=movieid))
            for movie in recommend:
                if movie not in watched_movies:
                    recommend_for_expect_movie.append({'movieid': movie.movieid, 'poster': movie.poster})
        if len(list_movie_id) == 0:
            for movie in unwatched_movies:
                    recommend_for_expect_movie.append({'movieid': movie.movieid, 'poster': movie.poster})
                    if len(recommend_for_expect_movie) == 11:
                        break
        if len(recommend_for_expect_movie) > 11:
            recommend_for_expect_movie = [recommend_for_expect_movie[i] for i in random.sample(range(len(recommend_for_expect_movie)), 11)]

        
        data['recommend_movies'] = recommend_for_expect_movie
        data['items'] = movies
        data['number_expect_movie'] = len(movies)
        
        
        return render(self, request, 'expect.html', data)



class V_Review(View):

    def addRate(self, request):
        print('rate movie here ')
        if request.method == 'POST':
            print('rate movie here 2')
            if request.is_ajax():
                movie_id =request.POST.get('movieid')
                username = request.POST.get('username')
                print(movie_id)
                print(username)

                rate_score = request.POST.get('rate_score')
                movie = Movie.objects.get(movieid=movie_id)
                user = User.objects.get(username=username)
                try:
                    rate_movie = User_Rate.objects.get(user=user, movie=movie)
                    rate_movie.rate = int(rate_score)
                    rate_movie.save()
                    data = {'type': 'rated', 'rate_score':rate_score }
                    return JsonResponse(data)
                except:
                    rate_movie = User_Rate(movie=movie, user=user, rate=rate_score)
                    rate_movie.save()
                    data = {'type': 'rated' , 'rate_score':rate_score}
                    return JsonResponse(data)

        return JsonResponse({'type':'error'})

    def addReview(self, request):
        if request.method == 'POST':
            if request.is_ajax():
                movie_id = request.POST.get('movieid')
                username = request.POST.get('username')
                content = request.POST.get('content')
                type = request.POST.get('type')

                if type =='review':
                    try:
                        movie = Movie.objects.get(movieid=movie_id)
                        user = User.objects.get(username=username)

                        rate_movie = User_Rate.objects.get(user=user, movie=movie)
                        rate_movie.review = content
                        print(rate_movie)
                        rate_movie.save()
                        # add activity
                        Activity.objects.create(review = rate_movie, user = request.user, type = 3)

                    except:
                        rate_movie = User_Rate(movie=movie, user=user, review=content)
                        rate_movie.save()
                        # every one create 1 review => create activity  here !!!
                        # add activity
                        Activity.objects.create(review = rate_movie, user = request.user, type = 3)

                    return JsonResponse({'mess':'success'})
                else:
                    return JsonResponse({'mess':'error'})
        return JsonResponse({'mess':'error'})

    def replyReview(self, request):
        if request.method == 'POST':
            if request.is_ajax():
                data = {}
                review_id = request.POST.get('postID')
                content = request.POST.get('content')
                type = request.POST.get('type')
                print(review_id)
                print(content)

                if type == 'reply':
                    try:
                        rate_movie = User_Rate.objects.get(id=int(review_id))
                        reply = ReplyToReview(user=request.user, review=rate_movie, content=content)
                        reply.save()
                        data['mess'] = 'succsess'
                        data['send_user'] = request.user.username
                        data['content'] = content
                        data['review_id'] = review_id

                        data['send_user_url'] = request.user.profile.get_absolute_url()
                        data['send_user_avatar']= request.user.profile.profile_picture.url
                        data['date_posted']  = 'just now'
                        data['count_reply'] = rate_movie.total_reply()
                        print('data here', data)

                        return JsonResponse(data)
                    except:
                        return JsonResponse({'mess':'error'})
        return JsonResponse({'mess':'error'})

    def likeReview(self, request):
        if request.method == 'POST':
            if request.is_ajax():
                postID = request.POST.get('postID')
                type = request.POST.get('type')
                if type == 'like':
                    post = get_object_or_404(User_Rate, pk=int(postID))
                    request_user = request.user
                    if request_user in post.likes.all():
                        #dislike
                        post.likes.remove(self, request_user)
                        count_likes = post.likes.count()
                        return JsonResponse({'count_likes': count_likes, 'type':'dislike'})
                    else:
                        post.likes.add(self, request.user)
                        # add notification
                        if request.user.id != post.user.id:
                            if post.user != request.user:
                                Notification.objects.create(user=post.user, user2=request.user, review = post, type = 6)
                        count_likes = post.likes.count()
                        return JsonResponse({'count_likes': count_likes, 'type':'like'})
        return JsonResponse({'count_likes': 0, 'type': -1})

    def getBreakRate(self, request):
        if request.method == 'POST':
            if request.is_ajax():
                data = {}
                movieid = request.POST.get('movieid')
                try:
                    # send data rating to client 
                    movie = Movie.objects.get(movieid=movieid)
                    count_all = User_Rate.objects.filter(movie=movie, rate__gte = 1).count()
                    print(count_all)
                    count_rate_5 = User_Rate.objects.filter(movie=movie, rate =5).count()
                    count_rate_5_percent = int(count_rate_5/count_all*100)
                    count_rate_4 = User_Rate.objects.filter(movie=movie, rate =4).count()
                    count_rate_4_percent = int(count_rate_4/count_all*100)
                    count_rate_3 = User_Rate.objects.filter(movie=movie, rate =3).count()
                    count_rate_3_percent = int(count_rate_3/count_all*100)
                    count_rate_2 = User_Rate.objects.filter(movie=movie, rate =2).count()
                    count_rate_2_percent = int(count_rate_2/count_all*100)
                    count_rate_1 = User_Rate.objects.filter(movie=movie, rate =1).count()
                    count_rate_1_percent = int(count_rate_1/count_all*100)
                    data['count_rate_5'] = count_rate_5
                    data['count_rate_5_percent'] = count_rate_5_percent
                    data['count_rate_4'] = count_rate_4
                    data['count_rate_4_percent'] = count_rate_4_percent
                    data['count_rate_3'] = count_rate_3
                    data['count_rate_3_percent'] = count_rate_3_percent
                    data['count_rate_2'] = count_rate_2
                    data['count_rate_2_percent'] = count_rate_2_percent
                    data['count_rate_1'] = count_rate_1
                    data['count_rate_1_percent'] = count_rate_1_percent
                    data['mess'] = 'oke'
                    avg =  User_Rate.objects.filter(movie=movie, rate__gte=1).aggregate(Avg('rate'))
                    data['rate_all_for_movie'] = round(avg['rate__avg'], 2)

                    return JsonResponse(data)


                except:
                    return JsonResponse({'mess':'error'})
        return JsonResponse({'mess':'error'})

class V_Tag(View):
    def addTag(self, request):
        if request.method == 'POST':
            if request.is_ajax():
                data = {}
                movieid = request.POST.get('movieid')
                username = request.POST.get('username')
                tags = request.POST.get('tag')
                type = request.POST.get('type')
                print(movieid)
                print(username)
                print(tags)

                movie = Movie.objects.get(movieid=movieid)
                user = User.objects.get(username=username)
                data = {}
                try:
                    tag = MovieTags.objects.filter(movie=movie,user=user,tags=tags)
                    if len(tag) > 0:
                        data['mess'] = 'error'
                        return JsonResponse(data)
                    else:
                        tag = MovieTags(movie=movie, user=user, tags=tags)
                        comunity_tags = MovieTags.objects.filter(movie=movie)
                        if len(comunity_tags) >0:
                            data['showComunity'] = 1
                        else:
                            data['showComunity'] = 0
                        dict_comunity = {}
                        for historyTag in comunity_tags:
                            if historyTag.tags in dict_comunity.keys():
                                dict_comunity[historyTag.tags] +=1
                            else:
                                dict_comunity[historyTag.tags] = 1
                        if tags in dict_comunity.keys():
                            dict_comunity[tags] +=1
                            data['newTag'] = 0 # false
                            data['new_count'] = dict_comunity[tags]
                        else:
                            dict_comunity[tags] =1
                            data['newTag'] = 1 # true
                            data['new_count'] = 1
                        tag.save()
                        data['id'] = tag.id
                        data['mess'] = 'success'
                        data['tags'] = tags
                        data['count'] = MovieTags.objects.filter(movie=movie, tags=tags).count()
                        print(data)
                        return JsonResponse(data)
                except:
                    return JsonResponse({'mess':'ERROR!!!'})

    def deleteTag(self, request):
        if request.method == 'POST':
            if request.is_ajax():
                tagID = request.POST.get('tagID')
                print(tagID)
                data = {}
                try:
                    tag = MovieTags.objects.get(id=tagID)
                    # print(tag)
                    comunity_tags = MovieTags.objects.filter(movie=tag.movie)
                    # tinh toan de xoa khoi comunity
                    dict_comunity = {}
                    for historyTag in comunity_tags:
                        if historyTag.tags in dict_comunity.keys():
                            dict_comunity[historyTag.tags] +=1
                        else:
                            dict_comunity[historyTag.tags] = 1
                    # neu chi co 1 tag cua user do trong comunity
                    if dict_comunity[tag.tags] == 1:
                        # xoa luon ca o comunity
                        data['deleteComunity'] = 1 # true
                        data['id_group'] = '#tag' + tag.tags
                        data['name_group'] = tag.tags
                    else:
                        data['deleteComunity'] = 0 # False
                        data['id_count'] = 'x' + tag.tags
                        data['name_group'] = tag.tags
                        data['count'] = 'x' + str(dict_comunity[tag.tags] - 1)

                    data['mess'] = 'succsess'
                    data['tagName'] = tag.tags
                    # delete ta
                    tag.delete()
                    # print(data)
                    return JsonResponse(data)
                except:
                    return JsonResponse({'mess':'error'})
        return JsonResponse({'mess':'error'})

def V_Movie(View):
    template_name = 'movie_detail.html'

    def detailMovie(self, request, model, id):
        #set rate score
        items = []
        rate_score = 0
        try:
            if model.get_name() == 'movie' and id != 'None':
                try:
                    d = Popularity.objects.get(movieid_id=id)
                    weight = d.weight
                    d.delete()
                    new_record = Popularity(movieid_id=id, weight=weight + 1)
                    new_record.save()
                except:
                    new_record = Popularity(movieid_id=id, weight=1)
                    new_record.save()
                label = 'actor'
                object = model.objects.get(movieid=id)
                records = Act.objects.filter(movieid_id=id)
                if request.user.get_username() != '':
                    seen_list = [str(x).split('|')[1] for x in
                                Seen.objects.filter(username=request.user.get_username())]
                    expect_list = [str(y).split('|')[1] for y in
                                Expect.objects.filter(username=request.user.get_username())]
                    if id in seen_list:
                        object.flag = 1
                    if id in expect_list:
                        object.flag = 2
                for query in records:
                    for actor in Actor.objects.filter(actorid=query.actorid_id):
                        print(actor)
                        items.append(actor)
                # add rated movie for user -  if form_flag =1 =>> user can review , -1 can not review
                review_form_flag = 1

                try:
                    rate_movie = User_Rate.objects.get(movie=object, user=request.user)
                    rate_score = rate_movie.rate
                    if rate_movie.review != None:
                        review_form_flag = -1
                    reviews = User_Rate.objects.filter(movie=object, review__isnull = False).order_by('-date_posted')

                except:
                    rate_score = 0
                    reviews = User_Rate.objects.filter(movie=object, review__isnull = False).order_by('-date_posted')
                    print(rate_score)

                # get tags from movie
                users_tags = []
                all_tags = []
                dict_tag_users = {}
                dict_all_tag = {}
                try:
                    users_tags = MovieTags.objects.filter(movie=object, user = request.user)
                    all_tags = MovieTags.objects.filter(movie=object)
                    
                    # must build tag by dict 
                    # comunity's tag
                    for tag in all_tags:
                        if tag.tags in dict_all_tag.keys():
                            dict_all_tag[tag.tags] +=1
                        else:
                            dict_all_tag[tag.tags] =1
                except:
                    dict_tag_users = []
                    dict_all_tag = []
                    users_tags = []
        except:
            return render(self, request, '404.html')


        if request.user.is_authenticated :
            notifications = Notification.objects.filter(user = request.user).order_by('-date_posted')[:10]
            count_noti = UserSeenNotifycation.objects.filter(user = request.user, is_seen = False).count()
            return render(self, request, template_name, {'users_tags': users_tags, 'comunity_tags':dict_all_tag,
            'items': items,'notifications' : notifications, 'count_noti':count_noti, 'review_form_flag':review_form_flag  ,'number': len(items), 'object': object , 'rate_score' : rate_score,'user':request.user, 'reviews':reviews})


        return render(self, request, template_name, {
        'items': items  ,'number': len(items), 'object': object , 'rate_score' : rate_score,'user':request.user, 'reviews':reviews})


class V_Actor(View):
    template_name = 'movie_list_all.html'
    def detailActor(self, request, model, id):
        items = []
        if model.get_name() == 'actor':
            label = 'movie'
            object = model.objects.get(actorid=id)
            records = Act.objects.filter(actorid_id=id)
            for query in records:
                for movie in Movie.objects.filter(movieid=query.movieid_id):
                    items.append(movie)

        return render(self, request, template_name, {'items': items, 'number': len(items), 'object': object})


# function handle pagination - list all movie
def movie_whole_list(self, request, model, page):
    if page is None:
        return render(self, request, '404.html')
    page = int(page)
    #movie
    objects = model.objects.all()
    total_page = int(math.ceil(len(objects) / 10))
    if page > total_page:
        return render(self, request, '404.html')
    last_item_index = 10 * page if page != total_page else len(objects)
    pages = []
    end_distance = total_page - page
    start_page_num = page - 5 if end_distance >= 5 else page - 10 + end_distance
    end_page_num = page + 5 if page > 5 else 10
    for i in range(start_page_num, end_page_num + 1):
        if 1 <= i <= total_page:
            pages.append(i)
    # print(objects)
    objects =  objects[ 2:]
    data = {'items': objects[10 * (page - 1):last_item_index], 'current_page': page, 'page_number': total_page,
            'pages': pages}
    return render(self, request, 'movie_list_all.html'.format(model.get_name()), data)


# function handle pagination - list all actor
def actor_whole_list(self, request, model, page):
    if page is None:
        return render(self, request, '404.html')
    page = int(page)
    #actor
    objects = model.objects.all()
    print(objects)
    total_page = int(math.ceil(len(objects) / 10))
    if page > total_page:
        return render(self, request, '404.html')
    last_item_index = 10 * page if page != total_page else len(objects)
    pages = []
    end_distance = total_page - page
    start_page_num = page - 5 if end_distance >= 5 else page - 10 + end_distance
    end_page_num = page + 5 if page > 5 else 10
    for i in range(start_page_num, end_page_num + 1):
        if 1 <= i <= total_page:
            pages.append(i)
    # print(objects)
    # objects =  objects[ 2:]

    # for actor in objects[10 * (page - 1):last_item_index]:
    #     print(actor.photo)

    data = {'items': objects[10 * (page - 1):last_item_index], 'current_page': page, 'page_number': total_page,
            'pages': pages}
    return render(self, request, 'actor_list_all.html', data)


class V_Search(View):

    def search(self, request, item, query_string, page):
        if item is None or query_string is None or page is None:
            return render(self, request, '404.html')
        query_string = query_string.replace("%20", " ")
        if item == 'movie':
            result = [search_index.data_in_memory['movie_dict'][movie_id] for movie_id in
                    search_index.search_movie(query_string)]
        elif item == 'actor':
            result = [search_index.data_in_memory['actor_dict'][actor_id] for actor_id in
                    search_index.search_actor(query_string)]
        else:
            return render(self, request, '404.html')
        page = int(page)
        total_page = int(math.ceil(len(result) / 10))
        if page > total_page and total_page != 0:
            return render(self, request, '404.html')
        last_item_index = 10 * page if page != total_page else len(result)
        pages = []
        end_distance = total_page - page
        start_page_num = page - 5 if end_distance >= 5 else page - 10 + end_distance
        end_page_num = page + 5 if page > 5 else 10
        for i in range(start_page_num, end_page_num + 1):
            if 1 <= i <= total_page:
                pages.append(i)
        return render(self, request, item + '_search.html',
                    {'items': result[10 * (page - 1):last_item_index], 'length': len(result),
                    'query_string': query_string, 'current_page': page, 'page_number': total_page, 'pages': pages})

    def search_suggest(self, request, query_string):
        result = search_cache.get(query_string)
        print(query_string)


        if result is not None:
            return HttpResponse(json.dumps(result, ensure_ascii=False))
        movie_list, actor_list = [], []
        search_result = search_index.search_suggest(query_string)
        for i, movie_id in enumerate(search_result[0]):
            movie = search_index.data_in_memory['movie_dict'].get(movie_id)
            movie_list.append({'movieid': movie.movieid, 'poster': movie.poster, 'title': movie.title})
            if i == 2:
                break
        for i, actor_id in enumerate(search_result[1]):
            actor = search_index.data_in_memory['actor_dict'].get(actor_id)
            actor_list.append({'actorid': actor.actorid, 'photo': actor.photo, 'name': actor.name})
            if i == 2:
                break
        result = {'movie': movie_list, 'actor': actor_list, 'text': query_string}
        search_cache.set(query_string, result)
        return HttpResponse(json.dumps(result, ensure_ascii=False))

    def recommendSearch(self, request):
        data = {}
        if request.method == 'POST':
            if request.is_ajax():
                user_id = request.POST.get('user_id')
                content = request.POST.get('content')
                keyup_now = request.POST.get('keyup_now')

                user = User.objects.get(id=user_id)
                
                try:
                    all_sessions = User_Search.objects.all()
                    user_search_sessions = User_Search.objects.filter(user=request.user)
                    recommend_sessions = []
                    for search_session in all_sessions:
                        if search_session not in user_search_sessions:
                            recommend_sessions.append(search_session)
                    print(search_session)

                    all_search_value = [session.content for  session in  recommend_sessions]

                    #search in all_search_value , which the best similarity 
                    sort_search_value = sorted(all_search_value , key = lambda value: jaccard_similarity(content, value)[0])
                    print('content giong nhau nhat',sort_search_value[-1])
                    # content giong nhau nhat 
                    content_best_similarity = sort_search_value[-1]
                    print(content_best_similarity.split(","))
                    key_recommend = content_best_similarity.split(",")[-1]
                    print('tu khoa goi y',key_recommend)
                    jaccard_value = jaccard_similarity(content, content_best_similarity)[0]
                    print(jaccard_value)
                    # print('key recommend here', key_recommend)
                    # if jaccard similarity > 0.5 
                    # print(keyup_now)
                    if jaccard_value > 0.75 :
                        if key_recommend.find(keyup_now) != -1 and len(key_recommend) > len(keyup_now):
                            print('Exactly recommend key :', key_recommend)
                            data['mess'] = 'success'
                            data['check_recommend'] = 'true'
                            data['key_recommend'] = key_recommend
                    else:
                        data['mess'] = 'success'
                        data['check_recommend'] = 'false'
                        data['key_recommend'] = 'false'
                except:
                    data['mess'] = 'false'
                    data['check_recommend'] = 'false'
                    data['key_recommend'] = 'false'
                
                
                #save search value to database 
                
                try:
                    now_user_session = User_Search.objects.filter(user=user).latest('date_posted')
                    if content.find(now_user_session.content) != -1:
                        now_user_session.content = content
                        # after search , save... now dont save
                        now_user_session.save()
                    else:
                        new_user_session = User_Search(user=user, content=content)
                        new_user_session.save()
                except:
                    # first user create session 
                    new_user_session = User_Search(user=user, content=content)
                    new_user_session.save()
        return JsonResponse(data)



class V_Recommend(View):
    def getTopMovie(self, request):
        top_movie = Movie.objects.order_by('-rate')[:30]
        result = list(top_movie)
        top_movie = [result[i] for i in random.sample(range(len(result)), 11 )]
        return top_movie

    @staticmethod
    def checkGenres(movie, genre):
        if movie.genres.find(genre)!=-1:
            return True
        return False

    def getActionMovie(self, request):
        all_action_movie = Movie.objects.order_by('-rate')[:200]
        results = []
        for movie in all_action_movie:
            if V_Recommend.checkGenres(movie, 'Action'):
                results.append(movie)
        return [results[i] for i in random.sample(range(len(results)), 11 )]
        
    def getComedyMovie(self, request):
        all_action_movie = Movie.objects.order_by('-rate')[:200]
        results = []
        for movie in all_action_movie:
            if V_Recommend.checkGenres(movie, 'Comedy'):
                results.append(movie)
        return [results[i] for i in random.sample(range(len(results)), 11 )]

    def getFavouriteMovie(self, user):
        try:
            # filter with source code https://stackoverflow.com/questions/10040143/how-to-do-a-less-than-or-equal-to-filter-in-django-queryset
            # list_movie = User_Rate.objects.filter(user=request.user, rate_gte=4)
            # print(user)
            # tinh trung binh luot rate
            user_rate = User_Rate.objects.filter(user=user)
            count = User_Rate.objects.filter(user=user).count()
            sum_rate = 0
            for rate in user_rate:
                sum_rate += rate.rate
            medium = sum_rate/count
            print('medium',medium)
            if medium >=3:
                list_rate_good = User_Rate.objects.filter(user=user, rate__gte=medium)
            else:
                list_rate_good = User_Rate.objects.filter(user=user, rate__gte=3)
            list_movie = [rate.movie.movieid for rate in list_rate_good]
        except:
            list_movie = []
        return list_movie
    

    def get_recommend_by_jaccard(self, movieid):
        # get data file
        mv_genres = pd.read_csv('data/data_movie.csv')
        mv_tags = pd.read_csv('data/genome_scores_data.csv')
        mv_tags_desc = pd.read_csv('data/genome-tags.csv')

        print(mv_tags.head())
        print(mv_genres.head())
        print(mv_tags_desc.head())

        movie = {}
        movie = pd.DataFrame(data=movie)

        movie['imdbId'] = mv_genres['movieid']
        movie['movieId'] = mv_genres['movielenid']

        #prepare
        mv_tags_denorm = mv_tags.merge(mv_tags_desc, on='tagId').merge(movie, on='movieId')
        mv_tags_denorm['relevance_rank'] = mv_tags_denorm.groupby("movieId")["relevance"].\
            rank(method="first",ascending=False).astype('int64')

        mv_tags_list = mv_tags_denorm[mv_tags_denorm.relevance_rank <= 50].groupby(['movieId', 'imdbId'])['tag'].apply(lambda x: ','.join(x)).reset_index()
        mv_tags_list['tag_list'] = mv_tags_list.tag.map(lambda x: x.split(','))

        target_movie_id = movieid

        target_tag_list = mv_tags_list[mv_tags_list.imdbId == target_movie_id].tag_list.values[0]
        mv_tags_list_sim = mv_tags_list[['movieId', 'imdbId', 'tag_list', 'tag']]
        mv_tags_list_sim['jaccard_sim'] = mv_tags_list_sim.tag_list.map(
            lambda x: len(set(x).intersection(set(target_tag_list))) / len(set(x).union(set(target_tag_list))))
        # print(f'Movies most similar to {target_movie_id} based on tags:')
        recommend_movie = mv_tags_list_sim.sort_values(by='jaccard_sim', ascending=False).head(12)['imdbId']
        recommend_movie = recommend_movie[1:]
        return list(recommend_movie)


    def get_recommend_by_cosine(list_movie_id):
        mv_genres = pd.read_csv('data/data_movie.csv')
        mv_tags = pd.read_csv('data/genome_scores_data.csv')
        mv_tags_desc = pd.read_csv('data/genome-tags.csv')

        movie = {}
        movie = pd.DataFrame(data=movie)

        movie['imdbId'] = mv_genres['movieid']
        movie['movieId'] = mv_genres['movielenid']

        # prepare
        mv_tags_denorm = mv_tags.merge(mv_tags_desc, on='tagId').merge(movie, on='movieId')
        mv_tags_denorm['relevance_rank'] = mv_tags_denorm.groupby("movieId")["relevance"]. \
            rank(method="first", ascending=False).astype('int64')

        mv_tags_list = mv_tags_denorm[mv_tags_denorm.relevance_rank <= 50].groupby(['movieId', 'imdbId'])['tag'].apply(
            lambda x: ','.join(x)).reset_index()
        mv_tags_list['tag_list'] = mv_tags_list.tag.map(lambda x: x.split(','))

        #model
        model = Doc2Vec.load('model/model_version1')
        mv_tags_vectors = model.dv.vectors

        #generate movie recommendation for user
        # compute user vector as an average of movie vectors seen by that user
        user_movie_vector = np.zeros(shape=mv_tags_vectors.shape[1])

        # remove data with not tag in data
        for movieid in list_movie_id:
            if mv_tags_list[mv_tags_list["imdbId"] == movieid].empty:
                # print(movieid)
                list_movie_id.remove(movieid)

        # print(list_movie_id)

        for movie_id in list_movie_id:

            mv_index = mv_tags_list[mv_tags_list["imdbId"] == movie_id].index.values[0]
            user_movie_vector += mv_tags_vectors[mv_index]

        user_movie_vector /= len(list_movie_id)

        #  find movies similar to user vector to generate movie recommendations

        print('Movie Recommendations:')

        sims = model.docvecs.most_similar(positive=[user_movie_vector], topn=30)
        results = []
        for i, j in sims:
            movie_sim = mv_tags_list.loc[int(i), "imdbId"].strip()
            if movie_sim not in list_movie_id:
                # print(movie_sim)
                results.append(movie_sim)

        return results

    def jaccard_similarity(text1, text2):
        list1 = text1.split(',')
        list2 = text2.split(',')
        return (len(set(list1).intersection(set(list2))) / len(set(list1).union(set(list2))), set(list2) - set(list1))

class V_Statistical(View):

    @staticmethod
    def getAllRates(movie):
        return User_Rate.objects.filter(movie=movie).count()
    
    def getTopMovie(self, request):
        if request.is_ajax():
            all_movies = Movie.objects.all()
            top_movie = sorted(all_movies, key= lambda t: V_Statistical.getAllRates(t))[-10:]
            labels = []
            data = []
            for movie in top_movie[-5:]:
                labels.append(movie.title)
                data.append( V_Statistical.getAllRates(movie))
            total_rates = User_Rate.objects.all().count()
            print(total_rates)
            return JsonResponse({'mess':'success', 'labels': labels, 'data': data, 'total_rates':total_rates})
        return JsonResponse({'mess':'error'})

