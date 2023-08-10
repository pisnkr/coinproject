import requests

def get_krw_market_coins_with_names():
    try:
        url = "https://api.upbit.com/v1/market/all"

        # 모든 마켓 정보 요청
        response = requests.get(url)
        markets = response.json()
        
        # 원화 시장에 있는 코인 정보 추출
        krw_market_coins = [{'market': market['market'], 'name': market['korean_name']} for market in markets if market['market'].startswith('KRW-')]

        return krw_market_coins

    except Exception as e:
        print("Error:", e)
        return []

def get_market_data():
    krw_coins_with_names = get_krw_market_coins_with_names()
    market_data = []

    for coin in krw_coins_with_names:
        market_name = f"{coin['market']}, {coin['name']}"
        market_code = market_name.split(",")[0]
        market_korean_name = market_name.split(",")[1]

        url = f'https://api.upbit.com/v1/ticker?markets={market_code}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if len(data) > 0:
                result = {
                    'name': market_korean_name.strip(),
                    'ticker': market_code,
                    'trade_price': data[0]['trade_price'],
                    'acc_trade_volume': data[0]['acc_trade_volume'],
                    'acc_trade_price': data[0]['acc_trade_price'],
                }
                market_data.append(result)

    return market_data

