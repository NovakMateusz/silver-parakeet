from enum import Enum

__all__ = ['CODE_NAME_MAPPING', 'NAME_CODE_MAPPING', 'ExternalServiceResponseFieldsName']

CODE_NAME_MAPPING = {
    'BTC': 'Bitcoin',
    'ETH': 'Ethereum',
    'USDT': 'Tether',
    'BNB': 'BNB',
    'USDC': 'USDCoin',
    'SOL': 'Solana',
    'LUNA': 'Terra',
    'XRP': 'XRP',
    'ADA': 'Cardano',
    'AVAX': 'Avalanche',
    'DOT': 'Polkadot',
    'DOGE': 'Dogecoin',
    'BUSD': 'BinanceUSD',
    'UST': 'TerraUSD',
    'SHIB': 'ShibaInu'
}

NAME_CODE_MAPPING = {
    'Bitcoin': 'BTC',
    'Ethereum': 'ETH',
    'Tether': 'USDT',
    'BNB': 'BNB',
    'USDCoin': 'USDC',
    'Solana': 'SOL',
    'Terra': 'LUNA',
    'XRP': 'XRP',
    'Cardano': 'ADA',
    'Avalanche': 'AVAX',
    'Polkadot': 'DOT',
    'Dogecoin': 'DOGE',
    'BinanceUSD': 'BUSD',
    'TerraUSD': 'UST',
    'ShibaInu': 'SHIB'
}


class ExternalServiceResponseFieldsName(Enum):
    from_currency_code = '1. From_Currency Code'
    from_currency_name = '2. From_Currency Name'
    to_currency_code = '3. To_Currency Code'
    to_currency_name = '4. To_Currency Name'
    exchange_rate = '5. Exchange Rate'
    last_refreshed = '6. Last Refreshed'
    time_zone = '7. Time Zone'
    bid_price = '8. Bid Price'
    ask_price = '9. Ask Price'
