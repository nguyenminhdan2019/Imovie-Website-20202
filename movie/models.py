from django.db import models
from django.contrib.auth.models import User

#add timezones
from django.utils import timezone
import datetime as dt
from django.db.models.signals import post_save
from django.dispatch import receiver
import user.models 

from django.contrib.humanize.templatetags import humanize

class Movie(models.Model):
    movieid = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=30)
    year = models.CharField(max_length=4)
    length = models.CharField(max_length=10)
    genres = models.CharField(max_length=100)
    rate = models.IntegerField(default=0)
    poster = models.URLField(default='')
    plot = models.CharField(max_length=1000)
    trailer = models.URLField(default='')
    #addd
    movielenid = models.CharField(max_length=20)
    youtubeid = models.CharField(max_length=500)

    def __str__(self):
        return self.movieid + '|' + self.title

    def get_absolute_url(self):
        return "/movie/movie_detail/{}".format(self.movie.movieid)


class Actor(models.Model):
    actorid = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=30)
    photo = models.URLField()

    def __str__(self):
        return self.actorid + '|' + self.name

    @staticmethod
    def get_name():
        return 'actor'
    
    def get_simple_name(self):
        if len(self.name) >= 12:
            if len(self.name.split()[0]) < len(self.name.split()[1]):
                return self.name.split()[1]
            return self.name.split()[0]
        else:
            return self.name


class Act(models.Model):
    movieid = models.ForeignKey('Movie', default=1, on_delete=models.CASCADE)
    actorid = models.ForeignKey('Actor', default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.actorid.actorid + '|' + self.movieid.movieid


class Seen(models.Model):
    username = models.CharField(max_length=150)
    movieid = models.ForeignKey('Movie', default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.username + '|' + self.movieid.movieid


class Expect(models.Model):
    username = models.CharField(max_length=150)
    movieid = models.ForeignKey('Movie', default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.username + '|' + self.movieid.movieid


class Popularity(models.Model):
    movieid = models.ForeignKey('Movie', default=' ', on_delete=models.CASCADE)
    weight = models.IntegerField(default=0)


class Rate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rate = models.IntegerField(default=0)
    reviewContent = models.CharField(max_length=500, null=True)
    datePosted = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='review_likes', blank=True)

    def __str__(self):
        return self.movie.movieid + '|' + str(self.user.username) + '|' + str(self.rate) + '|' + str(self.review)    
    def get_date(self):
        return humanize.naturaltime(self.datePosted)


class ReplyReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Rate, on_delete=models.CASCADE)
    content = models.CharField(max_length=500, null=True)
    datePosted = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='reply_likes', blank=True)

    def countReply(self):
        return self.review.objects.all().count()

    def __str__(self):
        return self.user.username + '|' + str(self.review) + '|' + str(self.content)

    def get_date(self):
        return humanize.naturaltime(self.datePosted)
    


# create notification if user reply reivew
@receiver(post_save, sender=ReplyReview)
def create_notification_by_reply_review(sender, instance, created, **kwargs):
    if created:
        if instance.user != instance.review.user:
            user.models.Notification.objects.create(reply_to_review = instance, user = instance.review.user, user2=instance.user ,type=4)


class Tag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, default=1, on_delete=models.CASCADE)
    tag =  models.CharField(max_length=150)


    def __str__(self):
        return str(self.user.username) + '|' +  str(self.movie) + '|' + str(self.tags)
    def count_tag(self):
        return Tag.objects.filter(movie=self.movie, tags=self.tags).count()



class Search(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datePosted = models.DateTimeField(default=timezone.now)
    content = models.CharField(max_length=500)