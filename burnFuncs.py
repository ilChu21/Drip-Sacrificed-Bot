import json, requests, os
from datetime import datetime
from web3 import Web3

bsc = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc))

def getTotalBurns(address):
    address = web3.toChecksumAddress(address)
    METHOD_ID = "0xa9059cbb"
    TO_DRIP = "0x20f663cea80face82acdfa3aae6862d246ce0333"
    TAX_VAULT = "bff8a1f9b5165b787a00659216d7313354d25472"
    burnTxs = []
    totalBurned = 0
    burnCount = 0

    transactions = json.loads(requests.get(f'https://api.bscscan.com/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=desc&apikey={os.environ["BSCSCAN_API_KEY"]}').text)
    for transaction in transactions['result']:
        if transaction['methodId'] == METHOD_ID and transaction['to'] == TO_DRIP and TAX_VAULT in transaction['input'] and transaction['txreceipt_status'] == '1':
            txDate = datetime.utcfromtimestamp(int(transaction['timeStamp'])).strftime('%Y/%m/%d')
            hashLink = f"https://bscscan.com/tx/{transaction['hash']}"
            input = transaction['input']
            inputAmount = web3.fromWei(web3.toInt(hexstr=input[-64:]), 'ether')
            burnTx = f"[{txDate}]({hashLink}) - {round(inputAmount, 3):,}"
            burnTxs.append(burnTx)
            totalBurned += inputAmount
            burnCount += 1

    return {'burnTxs': burnTxs, 'totalBurned': totalBurned, 'burnCount': burnCount}