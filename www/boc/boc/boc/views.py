from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from userprofile.forms import PhoneForm
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from userprofile.models import UserExtraInfo
from predictions.models import PredictionArticle
from news.models import Article
from carousel.models import CarouselItem, FundsUnderManagement
from opportunity.models import OpportunityItem
from testimonial.models import TestimonialItem
from advisory.models import AdvisoryBoard
from boc.forms import ContactForm
from django.contrib.flatpages.models import FlatPage
from django.core.mail import send_mail
from django.template import RequestContext
#from decimal import *
import stripe
import json
from django.core.serializers.json import DjangoJSONEncoder
from statistics.models import Statistic, StatisticsContent
from predictions.models import PredictionArticle, Prediction
from django.db.models import Sum, Case, Value, When, Count, IntegerField, Q
from datetime import datetime, timedelta
import decimal
import pytz
import decimal

def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError

def home(request):
    next_prediction = PredictionArticle.next_prediction()
    last_prediction = PredictionArticle.last_prediction()
    phone_form = PhoneForm()

    predictions = []


    if next_prediction:
        for prediction in next_prediction:
            predictions.append(prediction)
    if last_prediction:
        for prediction in last_prediction:
            predictions.append(prediction)

    #past_predictions = Prediction.objects.filter(open=True).order_by('-event__date')[:1]
    #upcoming_predictions = Prediction.objects.filter(open=False).order_by('-event__date')[:1]

    #setting the vairable carouselitems
    carouselitems = CarouselItem.objects.filter().order_by('order')
    testimonialitems = TestimonialItem.objects.filter().order_by('order')
    testimonials = testimonialitems.values_list('content')
    testimonials_names = testimonialitems.values_list('name')
    testimonial_json = json.dumps(list(testimonials), cls=DjangoJSONEncoder)
    testimonial_name_json = json.dumps(list(testimonials_names), cls=DjangoJSONEncoder)

    funds = FundsUnderManagement.objects.filter()[0]

    articles = Article.objects.filter(published=True).order_by('-date_published')[:4]
    c = {'articles': articles, 'predictions': predictions, 'phone_form': phone_form,'carouselitems':carouselitems,
        'testimonialitems':testimonialitems, 'testimonials': testimonials, 'testimonial_json': testimonial_json,
        'testimonial_name_json': testimonial_name_json,'funds':funds}
    return render(request, 'boc/home.html', c)

def login(request):
    form = AuthenticationForm(auto_id='id_%s-L')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST, auto_id='id_%s-L')
        if form.is_valid():
            auth.login(request, form.get_user())
            return HttpResponseRedirect(request.POST.get('next'))

    c = {'form': form, 'next':  '/'}
    return render(request, 'boc/login.html', c)


def join(request):

    form = ExtendedUserCreationForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            cd = form.cleaned_data
            user = auth.authenticate(username=cd['username'], password=cd['password1'])
            auth.login(request, user)
            UserExtraInfo.objects.create(user=user)
            return HttpResponseRedirect(request.POST.get('next'))
    c = {'form': form, 'next': '/'}
    return render(request, 'boc/join.html', c)

def logout(request):
    if request.method == 'GET':
        auth.logout(request)
        return HttpResponseRedirect( '/')

def settings(request):
    if request.user.is_authenticated():
        c = {}
        return render(request, 'boc/settings.html', c)
    return HttpResponseRedirect( '/login/')


def contact(request):
    contact_flatpage = get_object_or_404(FlatPage, url='/contact/')
    form = ContactForm()
    sent = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']
            recipients = ['info@betoncombat.com']
            send_mail(subject, name+"\n"+message, email, recipients)                                                                                                                                           
            form = ContactForm()
            sent = True
    c = {'form': form, 'flatpage': contact_flatpage, 'sent':sent}
    return render(request, 'flatpages/contact.html',  c)


def _ajax_response(request, template, **kwargs):
    response = {
        "html": render_to_string(
            template,
            RequestContext(request, kwargs)
        )
    }
    if "location" in kwargs:
        response.update({"location": kwargs["location"]})
    return HttpResponse(json.dumps(response), content_type="application/json")

def about(request):
    #/about/advisory-board/
    #/about/philosophy/
    #/about/the-brand/
    #/about/the-fund/
    #/about/word-from-the-founder/
    #/about/faq/
    is_active_flag = 1
    advisory = get_object_or_404(FlatPage, url='/about/advisory-board/')
    philosophy = get_object_or_404(FlatPage, url='/about/philosophy/')
    brand = get_object_or_404(FlatPage, url='/about/the-brand/')
    fund = get_object_or_404(FlatPage, url='/about/the-fund/')
    founder = get_object_or_404(FlatPage, url='/about/word-from-the-founder/')
    faq = get_object_or_404(FlatPage, url='/about/faq/')
    advisors = AdvisoryBoard.objects.filter().order_by('order')

    past_predictions = PredictionArticle.objects.filter(open=True).order_by('timestamp')
    current_year = past_predictions[0].timestamp.year
    current_date = datetime.now(pytz.timezone('US/Pacific')) - timedelta(days=365)
    start_month = datetime(current_date.year, current_date.month, 1, 0, 0, 0, 0, pytz.UTC)  
    #year, win, loss, accuracy, total risk, profit, roi, fund
    total_statistics = {'category':'Life-to-date', 'win':0, 'loss':0, 'accuracy':0, 'total_risk': 0, 'profit':0, 'roi':0 , 'fund':0}

    yearly_statistics = []
    yearly_statistics.append({'category':current_year, 'win':0, 'loss':0, 'accuracy':0, 'total_risk': 0, 'profit':0, 'roi':0 , 'fund':0})

    rate_of_return_statistics = []
    dow_return = {2008: -38.2, 2009: 18.8, 2010: 10.4, 2011: 5.5, 2012: 7.3, 2013: 26.5, 2014: 7.5}
    sp_return = {2008: -44.8, 2009: 23.5, 2010: 12.0, 2011: 0.01, 2012: 13.4, 2013: 29.6, 2014: 11.4}

    index = 0
    month_fund = 0
    total_fund = 0
    for prediction_article in past_predictions:

        #get start fund for month table
        if prediction_article.timestamp >= start_month and month_fund == 0:
            month_fund = total_fund

        if prediction_article.timestamp.year > current_year:
            if index == 0:
                total_statistics['fund'] = total_statistics['fund'] + yearly_statistics[index]['total_risk']

            yearly_statistics[index]['accuracy'] = int((float(yearly_statistics[index]['win']) / ( float(yearly_statistics[index]['win']) +  float(yearly_statistics[index]['loss'])))*100)
            yearly_statistics[index]['roi'] = int((float(yearly_statistics[index]['profit']) /  float(yearly_statistics[index]['total_risk']))*100)
            total_statistics['fund'] = total_statistics['fund'] + yearly_statistics[index]['profit']
            yearly_statistics[index]['fund'] = total_statistics['fund']

            total_statistics['win'] = total_statistics['win'] + yearly_statistics[index]['win']
            total_statistics['loss'] = total_statistics['loss'] + yearly_statistics[index]['loss']
            total_statistics['total_risk'] = total_statistics['total_risk']+ yearly_statistics[index]['total_risk']
            total_statistics['profit'] = total_statistics['profit']+ yearly_statistics[index]['profit']

            if current_year >= 2008 and current_year < 2015:
                rate_of_return_statistics.append({'year': current_year, 'boc': yearly_statistics[index]['roi'], 'dow': dow_return[current_year], 'sp': sp_return[current_year]})


            current_year = prediction_article.timestamp.year
            yearly_statistics.append({'category': current_year, 'win':0, 'loss':0, 'accuracy':0, 'total_risk': 0, 'profit':0, 'roi':0 , 'fund':0})
            index = index + 1


        predictions = prediction_article.prediction_set.all()
        for prediction in predictions:
            yearly_statistics[index]['total_risk'] = yearly_statistics[index]['total_risk'] + prediction.risk
            if prediction.result == 'Win':
                yearly_statistics[index]['win'] = yearly_statistics[index]['win'] + 1
                yearly_statistics[index]['profit'] = yearly_statistics[index]['profit'] + prediction.win
                total_fund = total_fund + prediction.win
            elif prediction.result == 'Loss':
                yearly_statistics[index]['loss'] = yearly_statistics[index]['loss'] + 1
                yearly_statistics[index]['profit'] = yearly_statistics[index]['profit'] - prediction.risk
                total_fund = total_fund - prediction.risk


    yearly_statistics[index]['accuracy'] = int((float(yearly_statistics[index]['win']) / ( float(yearly_statistics[index]['win']) +  float(yearly_statistics[index]['loss'])))*100)
    yearly_statistics[index]['roi'] = int((float(yearly_statistics[index]['profit']) /  float(yearly_statistics[index]['total_risk']))*100)
    total_statistics['fund'] = total_statistics['fund'] + yearly_statistics[index]['profit']
    yearly_statistics[index]['fund'] =  total_statistics['fund']

    total_statistics['accuracy'] =  int((float(total_statistics['win']) / ( float(total_statistics['win']) +  float(total_statistics['loss'])))*100)
    total_statistics['roi'] = int((float(total_statistics['profit']) /  float(total_statistics['total_risk']))*100)
    total_statistics['win'] = total_statistics['win'] + yearly_statistics[index]['win']
    total_statistics['loss'] = total_statistics['loss'] + yearly_statistics[index]['loss']

    yearly_statistics.reverse()

    #Monthly Statistics
    past_predictions = PredictionArticle.objects.filter(open=True, timestamp__gte=start_month).order_by('timestamp')
    monthly_statistics = []
    monthly_statistics.append({'category':start_month.strftime('%b %Y'), 'win':0, 'loss':0, 'accuracy':0, 'total_risk': 0, 'profit':0, 'roi':0 , 'fund':month_fund})
    current_month = start_month

    index = 0

    for prediction_article in past_predictions:
        compare_date = datetime(prediction_article.timestamp.year, prediction_article.timestamp.month, 1, 0, 0, 0, 0, pytz.UTC)
        if compare_date > current_month:
            if monthly_statistics[index]['total_risk'] > 0:
                monthly_statistics[index]['accuracy'] = int((float(monthly_statistics[index]['win']) / ( float(monthly_statistics[index]['win']) +  float(monthly_statistics[index]['loss'])))*100)
                monthly_statistics[index]['roi'] = int((float(monthly_statistics[index]['profit']) /  float(monthly_statistics[index]['total_risk']))*100)
                monthly_statistics[index]['fund'] = monthly_statistics[index]['fund'] + monthly_statistics[index]['profit']

            current_month = compare_date
            index = index + 1
            monthly_statistics.append({'category': current_month.strftime('%b %Y'), 'win':0, 'loss':0, 'accuracy':0, 'total_risk': 0, 'profit':0, 'roi':0 , 'fund':monthly_statistics[index-1]['fund']})

        predictions = prediction_article.prediction_set.all()
        for prediction in predictions:
            monthly_statistics[index]['total_risk'] = monthly_statistics[index]['total_risk'] + prediction.risk
            if prediction.result == 'Win':
                monthly_statistics[index]['win'] = monthly_statistics[index]['win'] + 1
                monthly_statistics[index]['profit'] = monthly_statistics[index]['profit'] + prediction.win
            elif prediction.result == 'Loss':
                monthly_statistics[index]['loss'] = monthly_statistics[index]['loss'] + 1
                monthly_statistics[index]['profit'] = monthly_statistics[index]['profit'] - prediction.risk


    if monthly_statistics[index]['total_risk'] > 0:
        monthly_statistics[index]['accuracy'] = int((float(monthly_statistics[index]['win']) / ( float(monthly_statistics[index]['win']) +  float(monthly_statistics[index]['loss'])))*100)
        monthly_statistics[index]['roi'] = int((float(monthly_statistics[index]['profit']) /  float(monthly_statistics[index]['total_risk']))*100)
        monthly_statistics[index]['fund'] = monthly_statistics[index-1]['fund'] + monthly_statistics[index]['profit']

    monthly_statistics.reverse()


    #underdog profit (odds > 0 + win add profit, loss subtract risk)
    dog_fave_statistics = Prediction.objects.filter(bet_type='ST').aggregate(underdog_win=Sum(Case(
                                                                                             When(Q(result='Win') & Q(odds__gt=0), then='win'),
                                                                                             output_field=IntegerField())),
                                                                           underdog_lose=Sum(Case(
                                                                                             When(Q(result='Loss') & Q(odds__gt=0), then='risk'),
                                                                                             output_field=IntegerField())),
                                                                           fave_win=Sum(Case(
                                                                                             When(Q(result='Win') & Q(odds__lt=0), then='win'),
                                                                                             output_field=IntegerField())),
                                                                           fave_lose=Sum(Case(
                                                                                             When(Q(result='Loss') & Q(odds__lt=0), then='risk'),
                                                                                             output_field=IntegerField())),)

    dog_fave_profit = {
                       'underdog': {'profit': (dog_fave_statistics['underdog_win'] - dog_fave_statistics['underdog_lose'])},
                       'favourite': {'profit': (dog_fave_statistics['fave_win'] - dog_fave_statistics['fave_lose'])},
                       'total': {}
                       }

    dog_fave_profit['total']['profit'] = dog_fave_profit['underdog']['profit'] + dog_fave_profit['favourite']['profit']
    dog_fave_profit['underdog']['percentage'] = int((float(dog_fave_profit['underdog']['profit'])/float(dog_fave_profit['total']['profit']))*100)
    dog_fave_profit['favourite']['percentage'] = int((float(dog_fave_profit['favourite']['profit'])/float(dog_fave_profit['total']['profit']))*100)

    content = StatisticsContent.objects.all()

    c = {'advisory': advisory, 'philosophy': philosophy, 'brand': brand,'fund':fund, 'founder':founder,
         'faq' : faq, 'is_active_flag': is_active_flag, 'advisors': advisors,
         'yearly_statistics':yearly_statistics,
         'total_statistics': [total_statistics],
         'monthly_statistics': monthly_statistics,
         'rate_of_return_statistics': rate_of_return_statistics,
         'dog_fave_profit': dog_fave_profit,
         'yearly_statistics_graph': json.dumps(yearly_statistics, default=decimal_default),
         'monthly_statistics_graph': json.dumps(monthly_statistics, default=decimal_default),
         'rate_of_return_statistics_graph': json.dumps(rate_of_return_statistics, default=decimal_default),
         'dog_fave_profit_graph': json.dumps(dog_fave_profit, default=decimal_default),
         'content':content[0].content }

    return render(request, 'flatpages/about.html',  c)

def about_fund(request):
    #/about/advisory-board/
    #/about/philosophy/
    #/about/the-brand/
    #/about/the-fund/
    #/about/word-from-the-founder/
    #/about/faq/
    is_active_flag = 2
    advisory = get_object_or_404(FlatPage, url='/about/advisory-board/')
    philosophy = get_object_or_404(FlatPage, url='/about/philosophy/')
    brand = get_object_or_404(FlatPage, url='/about/the-brand/')
    fund = get_object_or_404(FlatPage, url='/about/the-fund/')
    founder = get_object_or_404(FlatPage, url='/about/word-from-the-founder/')
    faq = get_object_or_404(FlatPage, url='/about/faq/')
    advisors = AdvisoryBoard.objects.filter().order_by('order')

    past_predictions = PredictionArticle.objects.filter(open=True).order_by('timestamp')
    current_year = past_predictions[0].timestamp.year
    current_date = datetime.now(pytz.timezone('US/Pacific')) - timedelta(days=365)
    start_month = datetime(current_date.year, current_date.month + 1, 1, 0, 0, 0, 0, pytz.UTC)

    #year, win, loss, accuracy, total risk, profit, roi, fund
    total_statistics = {'category':'Life-to-date', 'win':0, 'loss':0, 'accuracy':0, 'total_risk': 0, 'profit':0, 'roi':0 , 'fund':0}

    yearly_statistics = []
    yearly_statistics.append({'category':current_year, 'win':0, 'loss':0, 'accuracy':0, 'total_risk': 0, 'profit':0, 'roi':0 , 'fund':0})

    rate_of_return_statistics = []
    dow_return = {2008: -38.2, 2009: 18.8, 2010: 10.4, 2011: 5.5, 2012: 7.3, 2013: 26.5, 2014: 7.5}
    sp_return = {2008: -44.8, 2009: 23.5, 2010: 12.0, 2011: 0.01, 2012: 13.4, 2013: 29.6, 2014: 11.4}

    index = 0
    month_fund = 0
    total_fund = 0
    for prediction_article in past_predictions:

        #get start fund for month table
        if prediction_article.timestamp >= start_month and month_fund == 0:
            month_fund = total_fund

        if prediction_article.timestamp.year > current_year:
            if index == 0:
                total_statistics['fund'] = total_statistics['fund'] + yearly_statistics[index]['total_risk']

            yearly_statistics[index]['accuracy'] = int((float(yearly_statistics[index]['win']) / ( float(yearly_statistics[index]['win']) +  float(yearly_statistics[index]['loss'])))*100)
            yearly_statistics[index]['roi'] = int((float(yearly_statistics[index]['profit']) /  float(yearly_statistics[index]['total_risk']))*100)
            total_statistics['fund'] = total_statistics['fund'] + yearly_statistics[index]['profit']
            yearly_statistics[index]['fund'] = total_statistics['fund']

            total_statistics['win'] = total_statistics['win'] + yearly_statistics[index]['win']
            total_statistics['loss'] = total_statistics['loss'] + yearly_statistics[index]['loss']
            total_statistics['total_risk'] = total_statistics['total_risk']+ yearly_statistics[index]['total_risk']
            total_statistics['profit'] = total_statistics['profit']+ yearly_statistics[index]['profit']

            if current_year >= 2008 and current_year < 2015:
                rate_of_return_statistics.append({'year': current_year, 'boc': yearly_statistics[index]['roi'], 'dow': dow_return[current_year], 'sp': sp_return[current_year]})


            current_year = prediction_article.timestamp.year
            yearly_statistics.append({'category': current_year, 'win':0, 'loss':0, 'accuracy':0, 'total_risk': 0, 'profit':0, 'roi':0 , 'fund':0})
            index = index + 1


        predictions = prediction_article.prediction_set.all()
        for prediction in predictions:
            yearly_statistics[index]['total_risk'] = yearly_statistics[index]['total_risk'] + prediction.risk
            if prediction.result == 'Win':
                yearly_statistics[index]['win'] = yearly_statistics[index]['win'] + 1
                yearly_statistics[index]['profit'] = yearly_statistics[index]['profit'] + prediction.win
                total_fund = total_fund + prediction.win
            elif prediction.result == 'Loss':
                yearly_statistics[index]['loss'] = yearly_statistics[index]['loss'] + 1
                yearly_statistics[index]['profit'] = yearly_statistics[index]['profit'] - prediction.risk
                total_fund = total_fund - prediction.risk


    yearly_statistics[index]['accuracy'] = int((float(yearly_statistics[index]['win']) / ( float(yearly_statistics[index]['win']) +  float(yearly_statistics[index]['loss'])))*100)
    yearly_statistics[index]['roi'] = int((float(yearly_statistics[index]['profit']) /  float(yearly_statistics[index]['total_risk']))*100)
    total_statistics['fund'] = total_statistics['fund'] + yearly_statistics[index]['profit']
    yearly_statistics[index]['fund'] =  total_statistics['fund']

    total_statistics['accuracy'] =  int((float(total_statistics['win']) / ( float(total_statistics['win']) +  float(total_statistics['loss'])))*100)
    total_statistics['roi'] = int((float(total_statistics['profit']) /  float(total_statistics['total_risk']))*100)
    total_statistics['win'] = total_statistics['win'] + yearly_statistics[index]['win']
    total_statistics['loss'] = total_statistics['loss'] + yearly_statistics[index]['loss']

    yearly_statistics.reverse()

    #Monthly Statistics
    past_predictions = PredictionArticle.objects.filter(open=True, timestamp__gte=start_month).order_by('timestamp')
    monthly_statistics = []
    monthly_statistics.append({'category':start_month.strftime('%b %Y'), 'win':0, 'loss':0, 'accuracy':0, 'total_risk': 0, 'profit':0, 'roi':0 , 'fund':month_fund})
    current_month = start_month

    index = 0

    for prediction_article in past_predictions:
        compare_date = datetime(prediction_article.timestamp.year, prediction_article.timestamp.month, 1, 0, 0, 0, 0, pytz.UTC)
        if compare_date > current_month:
            if monthly_statistics[index]['total_risk'] > 0:
                monthly_statistics[index]['accuracy'] = int((float(monthly_statistics[index]['win']) / ( float(monthly_statistics[index]['win']) +  float(monthly_statistics[index]['loss'])))*100)
                monthly_statistics[index]['roi'] = int((float(monthly_statistics[index]['profit']) /  float(monthly_statistics[index]['total_risk']))*100)
                monthly_statistics[index]['fund'] = monthly_statistics[index]['fund'] + monthly_statistics[index]['profit']

            current_month = compare_date
            index = index + 1
            monthly_statistics.append({'category': current_month.strftime('%b %Y'), 'win':0, 'loss':0, 'accuracy':0, 'total_risk': 0, 'profit':0, 'roi':0 , 'fund':monthly_statistics[index-1]['fund']})

        predictions = prediction_article.prediction_set.all()
        for prediction in predictions:
            monthly_statistics[index]['total_risk'] = monthly_statistics[index]['total_risk'] + prediction.risk
            if prediction.result == 'Win':
                monthly_statistics[index]['win'] = monthly_statistics[index]['win'] + 1
                monthly_statistics[index]['profit'] = monthly_statistics[index]['profit'] + prediction.win
            elif prediction.result == 'Loss':
                monthly_statistics[index]['loss'] = monthly_statistics[index]['loss'] + 1
                monthly_statistics[index]['profit'] = monthly_statistics[index]['profit'] - prediction.risk


    if monthly_statistics[index]['total_risk'] > 0:
        monthly_statistics[index]['accuracy'] = int((float(monthly_statistics[index]['win']) / ( float(monthly_statistics[index]['win']) +  float(monthly_statistics[index]['loss'])))*100)
        monthly_statistics[index]['roi'] = int((float(monthly_statistics[index]['profit']) /  float(monthly_statistics[index]['total_risk']))*100)
        monthly_statistics[index]['fund'] = monthly_statistics[index-1]['fund'] + monthly_statistics[index]['profit']

    monthly_statistics.reverse()


    #underdog profit (odds > 0 + win add profit, loss subtract risk)
    dog_fave_statistics = Prediction.objects.filter(bet_type='ST').aggregate(underdog_win=Sum(Case(
                                                                                             When(Q(result='Win') & Q(odds__gt=0), then='win'),
                                                                                             output_field=IntegerField())),
                                                                           underdog_lose=Sum(Case(
                                                                                             When(Q(result='Loss') & Q(odds__gt=0), then='risk'),
                                                                                             output_field=IntegerField())),
                                                                           fave_win=Sum(Case(
                                                                                             When(Q(result='Win') & Q(odds__lt=0), then='win'),
                                                                                             output_field=IntegerField())),
                                                                           fave_lose=Sum(Case(
                                                                                             When(Q(result='Loss') & Q(odds__lt=0), then='risk'),
                                                                                             output_field=IntegerField())),)

    dog_fave_profit = {
                       'underdog': {'profit': (dog_fave_statistics['underdog_win'] - dog_fave_statistics['underdog_lose'])},
                       'favourite': {'profit': (dog_fave_statistics['fave_win'] - dog_fave_statistics['fave_lose'])},
                       'total': {}
                       }

    dog_fave_profit['total']['profit'] = dog_fave_profit['underdog']['profit'] + dog_fave_profit['favourite']['profit']
    dog_fave_profit['underdog']['percentage'] = int((float(dog_fave_profit['underdog']['profit'])/float(dog_fave_profit['total']['profit']))*100)
    dog_fave_profit['favourite']['percentage'] = int((float(dog_fave_profit['favourite']['profit'])/float(dog_fave_profit['total']['profit']))*100)

    content = StatisticsContent.objects.all()

    c = {'advisory': advisory, 'philosophy': philosophy, 'brand': brand,'fund':fund, 'founder':founder,
         'faq' : faq, 'is_active_flag': is_active_flag, 'advisors': advisors,
         'yearly_statistics':yearly_statistics,
         'total_statistics': [total_statistics],
         'monthly_statistics': monthly_statistics,
         'rate_of_return_statistics': rate_of_return_statistics,
         'dog_fave_profit': dog_fave_profit,
         'yearly_statistics_graph': json.dumps(yearly_statistics, default=decimal_default),
         'monthly_statistics_graph': json.dumps(monthly_statistics, default=decimal_default),
         'rate_of_return_statistics_graph': json.dumps(rate_of_return_statistics, default=decimal_default),
         'dog_fave_profit_graph': json.dumps(dog_fave_profit, default=decimal_default),
         'content':content[0].content }

    return render(request, 'flatpages/about.html',  c)

def career(request):

    job_offer = get_object_or_404(FlatPage, url='/career/')
    pages = OpportunityItem.objects.filter().order_by('order')


    c = {'job_offer': job_offer, 'pages': pages }

    return render(request, 'flatpages/career.html',  c)

def advisory_board(request):
    is_active_flag = 3
    advisory = get_object_or_404(FlatPage, url='/about/advisory-board/')
    philosophy = get_object_or_404(FlatPage, url='/about/philosophy/')
    brand = get_object_or_404(FlatPage, url='/about/the-brand/')
    fund = get_object_or_404(FlatPage, url='/about/the-fund/')
    founder = get_object_or_404(FlatPage, url='/about/word-from-the-founder/')
    faq = get_object_or_404(FlatPage, url='/about/faq/')
    advisors = AdvisoryBoard.objects.filter().order_by('order')

    past_predictions = PredictionArticle.objects.filter(open=True).order_by('timestamp')
    current_year = past_predictions[0].timestamp.year
    current_date = datetime.now(pytz.timezone('US/Pacific')) - timedelta(days=365)
    start_month = datetime(current_date.year, current_date.month + 1, 1, 0, 0, 0, 0, pytz.UTC)

    #year, win, loss, accuracy, total risk, profit, roi, fund
    total_statistics = {'category':'Life-to-date', 'win':0, 'loss':0, 'accuracy':0, 'total_risk': 0, 'profit':0, 'roi':0 , 'fund':0}

    yearly_statistics = []
    yearly_statistics.append({'category':current_year, 'win':0, 'loss':0, 'accuracy':0, 'total_risk': 0, 'profit':0, 'roi':0 , 'fund':0})

    rate_of_return_statistics = []
    dow_return = {2008: -38.2, 2009: 18.8, 2010: 10.4, 2011: 5.5, 2012: 7.3, 2013: 26.5, 2014: 7.5}
    sp_return = {2008: -44.8, 2009: 23.5, 2010: 12.0, 2011: 0.01, 2012: 13.4, 2013: 29.6, 2014: 11.4}

    index = 0
    month_fund = 0
    total_fund = 0
    for prediction_article in past_predictions:

        #get start fund for month table
        if prediction_article.timestamp >= start_month and month_fund == 0:
            month_fund = total_fund

        if prediction_article.timestamp.year > current_year:
            if index == 0:
                total_statistics['fund'] = total_statistics['fund'] + yearly_statistics[index]['total_risk']

            yearly_statistics[index]['accuracy'] = int((float(yearly_statistics[index]['win']) / ( float(yearly_statistics[index]['win']) +  float(yearly_statistics[index]['loss'])))*100)
            yearly_statistics[index]['roi'] = int((float(yearly_statistics[index]['profit']) /  float(yearly_statistics[index]['total_risk']))*100)
            total_statistics['fund'] = total_statistics['fund'] + yearly_statistics[index]['profit']
            yearly_statistics[index]['fund'] = total_statistics['fund']

            total_statistics['win'] = total_statistics['win'] + yearly_statistics[index]['win']
            total_statistics['loss'] = total_statistics['loss'] + yearly_statistics[index]['loss']
            total_statistics['total_risk'] = total_statistics['total_risk']+ yearly_statistics[index]['total_risk']
            total_statistics['profit'] = total_statistics['profit']+ yearly_statistics[index]['profit']

            if current_year >= 2008 and current_year < 2015:
                rate_of_return_statistics.append({'year': current_year, 'boc': yearly_statistics[index]['roi'], 'dow': dow_return[current_year], 'sp': sp_return[current_year]})


            current_year = prediction_article.timestamp.year
            yearly_statistics.append({'category': current_year, 'win':0, 'loss':0, 'accuracy':0, 'total_risk': 0, 'profit':0, 'roi':0 , 'fund':0})
            index = index + 1


        predictions = prediction_article.prediction_set.all()
        for prediction in predictions:
            yearly_statistics[index]['total_risk'] = yearly_statistics[index]['total_risk'] + prediction.risk
            if prediction.result == 'Win':
                yearly_statistics[index]['win'] = yearly_statistics[index]['win'] + 1
                yearly_statistics[index]['profit'] = yearly_statistics[index]['profit'] + prediction.win
                total_fund = total_fund + prediction.win
            elif prediction.result == 'Loss':
                yearly_statistics[index]['loss'] = yearly_statistics[index]['loss'] + 1
                yearly_statistics[index]['profit'] = yearly_statistics[index]['profit'] - prediction.risk
                total_fund = total_fund - prediction.risk


    yearly_statistics[index]['accuracy'] = int((float(yearly_statistics[index]['win']) / ( float(yearly_statistics[index]['win']) +  float(yearly_statistics[index]['loss'])))*100)
    yearly_statistics[index]['roi'] = int((float(yearly_statistics[index]['profit']) /  float(yearly_statistics[index]['total_risk']))*100)
    total_statistics['fund'] = total_statistics['fund'] + yearly_statistics[index]['profit']
    yearly_statistics[index]['fund'] =  total_statistics['fund']

    total_statistics['accuracy'] =  int((float(total_statistics['win']) / ( float(total_statistics['win']) +  float(total_statistics['loss'])))*100)
    total_statistics['roi'] = int((float(total_statistics['profit']) /  float(total_statistics['total_risk']))*100)
    total_statistics['win'] = total_statistics['win'] + yearly_statistics[index]['win']
    total_statistics['loss'] = total_statistics['loss'] + yearly_statistics[index]['loss']

    yearly_statistics.reverse()

    #Monthly Statistics
    past_predictions = PredictionArticle.objects.filter(open=True, timestamp__gte=start_month).order_by('timestamp')
    monthly_statistics = []
    monthly_statistics.append({'category':start_month.strftime('%b %Y'), 'win':0, 'loss':0, 'accuracy':0, 'total_risk': 0, 'profit':0, 'roi':0 , 'fund':month_fund})
    current_month = start_month

    index = 0

    for prediction_article in past_predictions:
        compare_date = datetime(prediction_article.timestamp.year, prediction_article.timestamp.month, 1, 0, 0, 0, 0, pytz.UTC)
        if compare_date > current_month:
            if monthly_statistics[index]['total_risk'] > 0:
                monthly_statistics[index]['accuracy'] = int((float(monthly_statistics[index]['win']) / ( float(monthly_statistics[index]['win']) +  float(monthly_statistics[index]['loss'])))*100)
                monthly_statistics[index]['roi'] = int((float(monthly_statistics[index]['profit']) /  float(monthly_statistics[index]['total_risk']))*100)
                monthly_statistics[index]['fund'] = monthly_statistics[index]['fund'] + monthly_statistics[index]['profit']

            current_month = compare_date
            index = index + 1
            monthly_statistics.append({'category': current_month.strftime('%b %Y'), 'win':0, 'loss':0, 'accuracy':0, 'total_risk': 0, 'profit':0, 'roi':0 , 'fund':monthly_statistics[index-1]['fund']})

        predictions = prediction_article.prediction_set.all()
        for prediction in predictions:
            monthly_statistics[index]['total_risk'] = monthly_statistics[index]['total_risk'] + prediction.risk
            if prediction.result == 'Win':
                monthly_statistics[index]['win'] = monthly_statistics[index]['win'] + 1
                monthly_statistics[index]['profit'] = monthly_statistics[index]['profit'] + prediction.win
            elif prediction.result == 'Loss':
                monthly_statistics[index]['loss'] = monthly_statistics[index]['loss'] + 1
                monthly_statistics[index]['profit'] = monthly_statistics[index]['profit'] - prediction.risk


    if monthly_statistics[index]['total_risk'] > 0:
        monthly_statistics[index]['accuracy'] = int((float(monthly_statistics[index]['win']) / ( float(monthly_statistics[index]['win']) +  float(monthly_statistics[index]['loss'])))*100)
        monthly_statistics[index]['roi'] = int((float(monthly_statistics[index]['profit']) /  float(monthly_statistics[index]['total_risk']))*100)
        monthly_statistics[index]['fund'] = monthly_statistics[index-1]['fund'] + monthly_statistics[index]['profit']

    monthly_statistics.reverse()


    #underdog profit (odds > 0 + win add profit, loss subtract risk)
    dog_fave_statistics = Prediction.objects.filter(bet_type='ST').aggregate(underdog_win=Sum(Case(
                                                                                             When(Q(result='Win') & Q(odds__gt=0), then='win'),
                                                                                             output_field=IntegerField())),
                                                                           underdog_lose=Sum(Case(
                                                                                             When(Q(result='Loss') & Q(odds__gt=0), then='risk'),
                                                                                             output_field=IntegerField())),
                                                                           fave_win=Sum(Case(
                                                                                             When(Q(result='Win') & Q(odds__lt=0), then='win'),
                                                                                             output_field=IntegerField())),
                                                                           fave_lose=Sum(Case(
                                                                                             When(Q(result='Loss') & Q(odds__lt=0), then='risk'),
                                                                                             output_field=IntegerField())),)

    dog_fave_profit = {
                       'underdog': {'profit': (dog_fave_statistics['underdog_win'] - dog_fave_statistics['underdog_lose'])},
                       'favourite': {'profit': (dog_fave_statistics['fave_win'] - dog_fave_statistics['fave_lose'])},
                       'total': {}
                       }

    dog_fave_profit['total']['profit'] = dog_fave_profit['underdog']['profit'] + dog_fave_profit['favourite']['profit']
    dog_fave_profit['underdog']['percentage'] = int((float(dog_fave_profit['underdog']['profit'])/float(dog_fave_profit['total']['profit']))*100)
    dog_fave_profit['favourite']['percentage'] = int((float(dog_fave_profit['favourite']['profit'])/float(dog_fave_profit['total']['profit']))*100)

    content = StatisticsContent.objects.all()

    c = {'advisory': advisory, 'philosophy': philosophy, 'brand': brand,'fund':fund, 'founder':founder,
         'faq' : faq, 'is_active_flag': is_active_flag,'advisors': advisors,
         'yearly_statistics':yearly_statistics,
         'total_statistics': [total_statistics],
         'monthly_statistics': monthly_statistics,
         'rate_of_return_statistics': rate_of_return_statistics,
         'dog_fave_profit': dog_fave_profit,
         'yearly_statistics_graph': json.dumps(yearly_statistics, default=decimal_default),
         'monthly_statistics_graph': json.dumps(monthly_statistics, default=decimal_default),
         'rate_of_return_statistics_graph': json.dumps(rate_of_return_statistics, default=decimal_default),
         'dog_fave_profit_graph': json.dumps(dog_fave_profit, default=decimal_default),
         'content':content[0].content }
    return render(request, 'flatpages/about.html',  c)


def learn(request):
    is_active_flag = 1
    betting_guide = get_object_or_404(FlatPage, url='/learn/guide/')
    money_management = get_object_or_404(FlatPage, url='/learn/money-management/')
    roi = get_object_or_404(FlatPage, url='/learn/roi/')
    become_a_student = get_object_or_404(FlatPage, url='/learn/become-a-student/')

    c = {'is_active_flag': is_active_flag, 'betting_guide': betting_guide, 'money_management': money_management,
         'roi': roi, 'become_a_student' : become_a_student}

    return render(request, 'flatpages/learn.html',  c)

def roi(request):
    is_active_flag = 3
    betting_guide = get_object_or_404(FlatPage, url='/learn/guide/')
    money_management = get_object_or_404(FlatPage, url='/learn/money-management/')
    roi = get_object_or_404(FlatPage, url='/learn/roi/')
    become_a_student = get_object_or_404(FlatPage, url='/learn/become-a-student/')

    c = {'is_active_flag': is_active_flag, 'betting_guide': betting_guide, 'money_management': money_management,
         'roi': roi, 'become_a_student' : become_a_student}

    return render(request, 'flatpages/learn.html',  c)

def become_a_student(request):
    is_active_flag = 5
    betting_guide = get_object_or_404(FlatPage, url='/learn/guide/')
    money_management = get_object_or_404(FlatPage, url='/learn/money-management/')
    roi = get_object_or_404(FlatPage, url='/learn/roi/')
    become_a_student = get_object_or_404(FlatPage, url='/learn/become-a-student/')

    c = {'is_active_flag': is_active_flag, 'betting_guide': betting_guide, 'money_management': money_management,
         'roi': roi, 'become_a_student' : become_a_student}

    return render(request, 'flatpages/learn.html',  c)


def betting_guide(request):
    is_active_flag = 1
    betting_guide = get_object_or_404(FlatPage, url='/learn/guide/')
    money_management = get_object_or_404(FlatPage, url='/learn/money-management/')
    roi = get_object_or_404(FlatPage, url='/learn/roi/')
    become_a_student = get_object_or_404(FlatPage, url='/learn/become-a-student/')

    c = {'is_active_flag': is_active_flag, 'betting_guide': betting_guide, 'money_management': money_management,
         'roi': roi, 'become_a_student' : become_a_student}

    return render(request, 'flatpages/learn.html',  c)

def legal(request):
    privacy = get_object_or_404(FlatPage, url='/legal/privacy-policy/')
    terms = get_object_or_404(FlatPage, url='/legal/terms-and-conditions/')
    member_agreement = get_object_or_404(FlatPage, url='/legal/member-agreement/')

    c = {'privacy': privacy, 'terms': terms, 'member_agreement' : member_agreement}

    return render(request, 'flatpages/legal.html',  c)

def testimonial(request):
    order_now = request.GET['order']
    testimonialitem = TestimonialItem.objects.get(order = order_now)
    contents = getattr(testimonialitem,'content')

    c = {'contents': contents}

    return render(request, 'flatpages/testimonial_sub.html',c)




