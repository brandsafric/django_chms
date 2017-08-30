from django.conf.urls import url

from . import views


urlpatterns = [
        url(r'(?P<year>\d{4})-(?P<month>(0[1-9])|(1[0-2]))-(?P<day>(0[1-9])|([12][0-9])|(3[01]))/$', views.EventDailyListView.as_view(), name='event_daily'),
        url(r'(?P<year>\d{4})-(?P<week>(0[1-9])|([1-4][0-9])(5[0-2]))w/$', views.EventWeeklyListView.as_view(), name='event_weekly'),
        url(r'(?P<year>\d{4})-(?P<month>0[1-9]|1[0-2])/$', views.EventMonthlyListView.as_view(), name='event_monthly'),
        url(r'(?P<year>\d{4})/$', views.EventYearlyListView.as_view(), name='event_yearly'),
        url(r'(?P<pk>\d+)/$', views.EventDetailView.as_view(), name='event_detail'),
        ]
