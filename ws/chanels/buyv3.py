import datetime
import time
from iqoptionapi.ws.chanels.base import Base
import logging
import iqoptionapi.global_value as global_value
from iqoptionapi.expiration import get_expiration_time 
from iqoptionapi.expiration import get_expiration_second
import json

# class BuyBlitz(Base):
#     name = "sendMessage"

#     def __call__(self, price, act, direction, request_id):
#         """
#         Send a Blitz option purchase request.

#         :param price: int, amount to invest (e.g., 100 for $100)
#         :param act: int, asset identifier (from devtools, e.g., 2301)
#         :param direction: str, "call" or "put"
#         :param exp_value: int, internal expiry code (e.g., 335795 for 30s)
#         :param request_id: str, unique ID for tracking
#         """
#         server_timestamp = int(self.api.timesync.server_timestamp)
#         exp = server_timestamp + 30  # Blitz มักใช้ duration สั้น เช่น 30 วินาที
#         data = {
#             "name": "option",
#             "version": "1.0",
#             "body": {
#                 "type": "blitz",
#                 "price": int(price),
#                 "act": (act),
#                 "direction": direction.lower(),
#                 "exp_value":exp,
#                 "user_balance_id": int(global_value.balance_id),
#                 # "client_platform_id": 9  # From your capture
#             }
#         }
#         print(f"[Blitz] Sending: request_id={request_id}, data={data}")
#         self.send_websocket_request(self.name, data, request_id)

class Buyv3_blizt(Base):

    name = "sendMessage"

    # def __call__(self, price, active, direction, duration, request_id):

    #     # thank Darth-Carrotpie's code
    #     # https://github.com/Lu-Yi-Hsun/iqoptionapi/issues/6
    #     exp, idx = get_expiration_second(
    #         int(self.api.timesync.server_timestamp), duration)
    #     # if idx < 1:
    #     #     option = 12  # "turbo"
    #     #     print("show exp idx ",idx)
    #     # else:
    #     #     option = 1  # "binary"
    #     data = {
    #         "body": {"price": price,
    #                  "active_id": active,
    #                  "expired": int(exp),
    #                  "direction": direction.lower(),
    #                  "option_type_id": 12,
    #                  "user_balance_id": int(global_value.balance_id)
    #                  },
    #         "name": "binary-options.open-option",
    #         "version": "2.0"
    #     }
    #     self.send_websocket_request(self.name, data, str(request_id))
   
    def __call__(self, price, active_id, direction, duration, request_id,profit_percent=88):   
        now = int(self.api.timesync.server_timestamp)
        expired = now + duration

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
                # "value": int(value),
                "profit_percent": int(profit_percent),
                "expiration_size": int(duration)
            }
        }

        print(f"[BlitzV2] ➡️ Sending: {json.dumps(data, separators=(',',':'))}")
        self.api.send_websocket_request("sendMessage", data, request_id)



class Buyv3(Base):

    name = "sendMessage"

    def __call__(self, price, active, direction, duration, request_id):

        # thank Darth-Carrotpie's code
        # https://github.com/Lu-Yi-Hsun/iqoptionapi/issues/6
        exp, idx = get_expiration_time(
            int(self.api.timesync.server_timestamp), duration)
        if idx < 5:
            option = 3  # "turbo"
        else:
            option = 1  # "binary"
        data = {
            "body": {"price": price,
                     "active_id": active,
                     "expired": int(exp),
                     "direction": direction.lower(),
                     "option_type_id": option,
                     "user_balance_id": int(global_value.balance_id)
                     },
            "name": "binary-options.open-option",
            "version": "1.0"
        }
        self.send_websocket_request(self.name, data, str(request_id))


class Buyv3_by_raw_expired(Base):

    name = "sendMessage"

    def __call__(self, price, active, direction, option, expired, request_id):

        # thank Darth-Carrotpie's code
        # https://github.com/Lu-Yi-Hsun/iqoptionapi/issues/6

        if option == "turbo":
            option_id = 3  # "turbo"
        elif option == "binary":
            option_id = 1  # "binary"
        data = {
            "body": {"price": price,
                     "active_id": active,
                     "expired": int(expired),
                     "direction": direction.lower(),
                     "option_type_id": option_id,
                     "user_balance_id": int(global_value.balance_id)
                     },
            "name": "binary-options.open-option",
            "version": "1.0"
        }
        self.send_websocket_request(self.name, data, str(request_id))


"""
    # thank Darth-Carrotpie's code
    # https://github.com/Lu-Yi-Hsun/iqoptionapi/issues/6
    def get_expiration_time(self, duration):
        exp = time.time()
        if duration >= 1 and duration <= 5:
            option = 3#"turbo"
            # Round to next full minute
            # datetime.datetime.now().second>30
            if (exp % 60) > 30:
                exp = exp - (exp % 60) + 60*(duration+1)
            else:
                exp = exp - (exp % 60)+60*(duration)
        elif duration > 5:
            option = 1#"binary"
            period = int(round(duration / 15))
            tmp_exp = exp - (exp % 60)  # nuima sekundes
            tmp_exp = tmp_exp - (tmp_exp % 3600)  # nuimam minutes
            j = 0
            while exp > tmp_exp + (j)*15*60:  # find quarter
                j = j+1
            if exp - tmp_exp > 5 * 60:
                quarter = tmp_exp + (j)*15*60
                exp = quarter + period*15*60
            else:
                quarter = tmp_exp + (j+1)*15*60
                exp = quarter + period*15*60
        else:
            logging.error("ERROR get_expiration_time DO NOT LESS 1")
            exit(1)
        return exp, option
"""
