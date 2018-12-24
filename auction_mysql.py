import sys
import base64
import json
import asyncio
import websockets
import time
from datetime import datetime
from mysql.connector import MySQLConnection
from dbconfig import read_mysql_db_config

db_config = read_mysql_db_config()
conn = MySQLConnection(**db_config)
cursor = conn.cursor()

async def copart(param):
    nirvanalv = param.split('-')[1]
    param = param.split('-')[0]
    async with websockets.connect('wss://nirvanalv' + nirvanalv + '.copart.com/sv/ws') as websocket:
        param_1st = 'F=1&Connection-Type=JC&Y=10&V=Netscape&P=nws&W=81457-81457&X=February-12 2016&Z=Linux&S=ANONYMOUS&A=VB3&G=T&D=F&B=&R={}&1Date={}&'.format
        await websocket.send(param_1st(2, str(int(time.time() * 1000))))
        greeting = await websocket.recv()
        print("{}".format(greeting))

        param_2nd = 'F=5&R={}&E=1&N=/COPART{}/outbound,0,,F'.format
        await websocket.send(param_2nd(3, param))
        greeting = await websocket.recv()
        print("{}".format(greeting))

        keep_alive = 'F=3&R={}&'.format
        r = 4

        old = datetime.now()
        while True:
            greeting = await websocket.recv()
            try:
                decoded = base64.b64decode(json.loads(greeting)[0]['d'][1]['Data'])
                data = json.loads(decoded.decode())
                if 'ATTRIBUTE' in data:
                    print(','.join([param, data['LOTNO'], data['BID']]))

                    try:
                        query = "UPDATE product_vehicle SET sold_price = {} WHERE lot = {}".format
                        cursor.execute(query(data['BID'], data['LOTNO']))
                        conn.commit()
                    except Exception as e:
                        print(e)

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
        get_copart_auction(arg[0])
    else:
        print('Please input the correct command')
