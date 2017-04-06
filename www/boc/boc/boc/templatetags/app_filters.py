from django import template
from django.contrib.humanize.templatetags.humanize import intcomma
from django.template.loader import get_template
from django.template import Context

register = template.Library()

@register.filter(name='format_odds')
def format_odds(odds):
    
    if odds and int(odds) > 0:
        return '+'+str(odds)
    return odds

@register.filter(name='implied_prob')
def implied_prob(odds):
    if type(odds) is long:
        odds = float(odds)
    if odds > 0:
        decimal_odds = ((odds/100) + 1)
    elif odds < 0:
        decimal_odds = ((100/-odds) + 1)
    
    return round((1/decimal_odds)*100,1)


@register.filter(name='inefficiency')
def inefficency(odds, boc_percent):
    prob = implied_prob(odds)
    inefficiency = float(boc_percent) - prob
    if inefficiency > 0:
        inefficiency = "+"+str(inefficiency)
    return inefficiency


@register.filter(name='prediction_record')
def prediction_record(predictions):
    return str(predictions.filter(result='Win').count()) +'-'+str(predictions.filter(result='Loss').count())

@register.filter(name='prediction_profit')
def prediction_profit(predictions):
    sum = 0
    for prediction in predictions:
        if prediction.result == 'Win':
            sum = sum + prediction.win
        elif prediction.result == 'Loss':
            sum = sum - prediction.risk
            
    return sum       
   
@register.filter(name='prediction_overall_result')
def prediction_overall_result(predictions):
    return str(predictions.filter(result='Win').count()) +'-'+str(predictions.filter(result='Loss').count())
        
@register.filter(name='material')
def material(value):
    template = get_template("materialforms/field.html")
    context = Context({'field': value})
    return template.render(context)

@register.filter(name='material_radio')
def material_radio(value):
    template = get_template("materialforms/radio.html")
    context = Context({'field': value})
    return template.render(context)

@register.filter(name='material_input')
def material_input(value):
    return value.as_widget(attrs={'class': 'mdl-textfield__input', 'placeholder':''})

@register.filter(name='material_select')
def material_select(value):
    template = get_template("materialforms/select.html")
    context = Context({'field': value})
    return template.render(context)


@register.filter(name='material_checkbox')
def material_checkbox(value):
    print value.value
    template = get_template("materialforms/checkbox.html")
    context = Context({'field': value})
    return template.render(context)


@register.filter(name='material_select_input')
def material_select_input(value):
    return value.as_widget(attrs={'class': 'mdl-selectfield__select', 'placeholder':''})


@register.filter(name='tweet_button')
def tweet_button(value):
    template = get_template("socialshare/tweet.html")
    return template.render()


    
