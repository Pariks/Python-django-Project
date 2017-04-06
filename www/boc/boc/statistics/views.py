from django.shortcuts import render
from statistics.models import Statistic, StatisticsContent
from predictions.models import PredictionArticle, Prediction
from django.db.models import Sum, Case, Value, When, Count, IntegerField, Q

from datetime import datetime, timedelta
import decimal
import json
import pytz

def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError

def index(request):
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
    c = {'yearly_statistics':yearly_statistics, 
         'total_statistics': [total_statistics], 
         'monthly_statistics': monthly_statistics, 
         'rate_of_return_statistics': rate_of_return_statistics,
         'dog_fave_profit': dog_fave_profit,
         'yearly_statistics_graph': json.dumps(yearly_statistics, default=decimal_default),
         'monthly_statistics_graph': json.dumps(monthly_statistics, default=decimal_default),
         'rate_of_return_statistics_graph': json.dumps(rate_of_return_statistics, default=decimal_default),
         'dog_fave_profit_graph': json.dumps(dog_fave_profit, default=decimal_default),
         'content':content[0].content}
    return render(request, 'statistics/statistics.html', c)
