from django.conf.urls import url
from django.urls import include, path
from .views import V_Actor, V_User, V_Profile, V_NewFeed, V_Post, V_Follow, V_Statistical
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Logout, Register, LoginFacebbok
    url(r'^logout/', views.user_logout, name='logout'),
    url(r'^register/', views.user_register, name='register'),
    url(r'^facebook/', views.facebook, name='facebook'),
    # API Login
    path('API/login', V_User.login, name='send-login'),
    # DJANGO AUTH CLASS
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html') ,name='password_reset_done'),
    path('password_reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html') ,name='password_reset_confirm'),
    path('password_reset/complete', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html') ,name='password_reset_complete'),
    path('activate/<uidb64>/', V_User.activate, name='activate'),
    path('API/change_password', V_User.changePassword, name='change-password'),
    
    #detail user, edit profile
    path('detail/edit_profile', V_Profile.changeProfile, name='detail-edit-profile'),
    path('social/', V_Profile.changeSocialLink, name='connect_social'),
    path('detail/<int:profile_id>/', V_Profile.detailUser, name='detail'),

    # newfeed
    path('comunity/', views.comunity, name='comunity'),
    path('API/post_now/', V_NewFeed.createPostNow, name='post-now'),

    # API POST
    path('API/like_post/', V_Post.likePost, name='like-post'),
    path('API/report_post/', V_Post.reportPost, name='report-post'),

    # API Follow
    path('API/follow/', V_Follow.follow, name='follow'),
    path('API/follow_now/', V_NewFeed.followNow, name='follow-now'),

    # API seen noti
    path('API/seen-noti/', V_Notification.seenNoti, name='seen-noti'),

    # API get data to show CHART - ADMIN
    path('API/get_data_chart_user_register/', V_Statistical.getDataUserRegister, name='get_data_user_register'),
    path('API/get_data_chart_user_activity/', V_Statistical.getTopUserActivity, name='get_chart_user_activity'),
    path('API/get_data_chart_post/', V_Statistical.getQualityPost, name='get_chart_post'),

]
