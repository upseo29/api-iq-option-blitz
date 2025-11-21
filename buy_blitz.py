# buy_blitz.py
from iqoptionapi.ws.objects.base import Base
from iqoptionapi.global_value import global_value
# import datetime
# import time
# from iqoptionapi.ws.chanels.base import Base
# import logging
# import iqoptionapi.global_value as global_value
# from iqoptionapi.expiration import get_expiration_time
import time
import logging
from random import randint
import json
class Buyv3_blizt(Base):


    def __call__(self, price, active_id, direction, duration, request_id, value=None, profit_percent=88):
        now = int(self.api.timesync.server_timestamp)
        expired = now + duration

        # 🔥 Use real 'value' from browser capture, or test with known one
        if value is None:
            value = 1057685  # ← Replace with latest from browser!

        data = {
            "name": "binary-options.open-option",
            "version": "2.0",
            "body": {
                "user_balance_id": int(self.api.profile.balance_id),
                "active_id": int(active_id),
                "option_type_id": 12,
                "direction": direction.lower(),
                "expired": int(expired),
                "price": float(price),
                "refund_value": 0,
                "value": int(value),
                "profit_percent": int(profit_percent),
                "expiration_size": int(duration)
            }
        }

        print(f"[BlitzV2] ➡️ Sending: {json.dumps(data, separators=(',',':'))}")
        self.api.send_websocket_request("sendMessage", data, request_id)
