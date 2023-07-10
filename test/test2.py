from deriv_api import DerivAPI
from rx import Observable

import asyncio


async def deriv():
    """Doc."""
    api = DerivAPI(app_id=1089)
    count = 1
    # wait_tick = api.expect_response('tick')

    source_tick_50 = await api.subscribe({'ticks': 'R_50'})
    # subscribe the rxpy sequence with a callback function,
    # when the data received , the call back function will be called
    # first_tick = await wait_tick
    seq_sub1 = source_tick_50.subscribe(lambda tick: print(f"get tick from sub1 {tick}"))
    # seq_sub2 = source_tick_50.subscribe(lambda tick: print(f"get tick from sub2 {tick}"))
    # print('First tick', first_tick)

    while True:
        await asyncio.sleep(1)


asyncio.run(deriv())
