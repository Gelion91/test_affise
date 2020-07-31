from flask import Blueprint, render_template, current_app
from requests import Timeout, TooManyRedirects, Session

blueprint = Blueprint('main', __name__)


@blueprint.route('/')
@blueprint.route('/getoffer')
def get_offer():
    url = 'http://api.cpanomer1.affise.com/3.0/partner/offers'
    params = {
        'API-Key' : current_app.config['API_KEY']
    }
    session_offer = Session().get(url, params=params)

    url_conversion = 'http://api.cpanomer1.affise.com/3.0/stats/conversions'
    params = {
        'API-Key': current_app.config['API_KEY'],
        'date_from': ''
    }
    session_conv = Session().get(url_conversion, params=params)
    try:
        offer = session_offer.json()
        offer = offer['offers'][0]
        countries = set()
        for i in offer['payments']:
            countries.update(i['countries'])

        conversion = session_conv.json()
        conversion = conversion['conversions'][0]
        return render_template('offer/get_offer.html', result=offer, countries=list(countries), conversion=conversion)

    except (ConnectionError, Timeout, TooManyRedirects, AttributeError) as e:
        print(e)



