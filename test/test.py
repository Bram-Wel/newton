#!/usr/bin/python3
"""Test."""


from deriv_api import DerivAPI
from rx import Observable

import asyncio

# api = DerivAPI(endpoint='wss://ws.binaryws.com/websockets/v3', app_id=1089)


async def sample_calls():
    """Test."""
    api = DerivAPI(app_id=1089)
    # wait_tick = api.expect_response('tick')
    last_data = {}
    source_tick_50: Observable = await api.subscribe({'ticks': 'R_50'})

    def create_subs_cb(symbol):
        count = 0

        def cb(data):
            nonlocal count
            count = count + 1
            print(data)
            last_data[symbol] = data
            # print('last_data', last_data)
            print(f"get symbol {symbol} {count}")
        return cb

    a_sub = source_tick_50.subscribe(create_subs_cb('R_50'))
    # b_sub = source_tick_50.subscribe(create_subs_cb('R_50'))
    # source_tick_100: Observable = await api.subscribe({'ticks': 'R_100'})
    # source_tick_100.subscribe(create_subs_cb('R_100'))
    # first_tick = await wait_tick
    # print(f"first tick is {first_tick}")
    print(a_sub)
    await asyncio.sleep(5)
    # print("now will forget")
    # await api.forget(last_data['R_50']['subscription']['id'])
    # await api.forget(last_data['R_100']['subscription']['id'])
    # await api.forget_all('ticks')
    # a_sub.dispose()
    # await asyncio.sleep(5)
    # print("disposing the last one will call forget")
    # b_sub.dispose()
    # await asyncio.sleep(5)
    # await api.clear()

asyncio.run(sample_calls())
