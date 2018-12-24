import sys
import base64
import json
import asyncio
import websockets
import time
from datetime import datetime
import psycopg2
from dbconfig import read_postgres_db_config

db_config = read_postgres_db_config()
conn = psycopg2.connect(**db_config)
cursor = conn.cursor()

async def copart(param):
    nirvanalv = param.split('-')[1]
    param = param.split('-')[0]
    async with websockets.connect('wss://nirvanalv' + nirvanalv + '.copart.com/sv/ws') as websocket:
        param_1st = 'F=1&Connection-Type=JC&Y=10&V=Netscape&P=nws&W=81457-81457&X=February-12 2016&Z=Linux&S=ANONYMOUS&A=VB3&G=T&D=F&B=&R={}&1Date={}&'.format
        await websocket.send(param_1st(2, str(int(time.time() * 1000))))
        await websocket.recv()

        param_2nd = 'F=5&R={}&E=1&N=/COPART{}/outbound,0,,F'.format
        await websocket.send(param_2nd(3, param))
        await websocket.recv()

        keep_alive = 'F=3&R={}&'.format
        r = 4

        old = datetime.now()
        while True:
            greeting = await websocket.recv()
            try:
                decoded = base64.b64decode(json.loads(greeting)[0]['d'][1]['Data'])
                data = json.loads(decoded.decode())
                if 'ATTRIBUTE' in data:
                    # print(','.join([param, data['LOTNO'], data['BID']]))
                    # auction_file = open('auction_history.txt', 'a')
                    # auction_file.write(','.join([param, data['LOTNO'], data['BID'], '\n']))
                    # auction_file.close()

                    query = "select exists(select 1 from product_vehicle where lot = {})".format
                    cursor.execute(query(data['LOTNO']))
                    if cursor.fetchone()[0]:
                        query = "UPDATE product_vehicle SET sold_price = {}, sale_status = 'SOLD' WHERE lot = {}".format
                        cursor.execute(query(data['BID'], data['LOTNO']))
                        conn.commit()
                        print(','.join([param, data['LOTNO'], data['BID'], 'updated']))
                    else:
                        # query = "INSERT INTO product_vehicle(lot, sold_price, sale_status) VALUES ({}, {}, 'SOLD')".format
                        # cursor.execute(query(data['LOTNO'], data['BID']))
                        # conn.commit()
                        print(','.join([param, data['LOTNO'], data['BID'], 'not exist on db']))

                if 'TEXT' in data:
                    cursor.close()
                    conn.close()
                    break
            except:
                pass
            now = datetime.now()
            if (now - old).seconds > 28:
                await websocket.send(keep_alive(3, r))
                r += 1
                old = datetime.now()


def get_copart_auction(param):
    asyncio.get_event_loop().run_until_complete(copart(param))

if __name__ == '__main__':
    arg = sys.argv[1:]

    if len(arg) == 1:
        print('started - https://www.copart.com/auctionDashboard?auctionDetails=' + arg[0][:-1].lstrip('0') + '-' + arg[0][-1])
        get_copart_auction(arg[0])
    else:
        print('Please input the correct command')
