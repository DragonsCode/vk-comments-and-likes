from vkbottle import API, BuiltinStateDispenser, User
from vkbottle.bot import BotLabeler


token = 'vk1.a.PdBxBthx3qG98nynYuoZb1fs0ns80iF_KAOfQDpAgIBQMD1zuC6iBheqpWH0YdoiwGkBeTzCoaiQS_xZmCcw5M_e7R7eiFdhquoceizjJdOYC7JzJaeZEn5Xn5ZgiRJnUht__phyFcRVViif9bDAbt9Q1YBKRZTi6CiWMPAg-EkY0FyD8qGV73ZRnvdkT3_N'
user_token = 'vk1.a.gcSKluVuVTJrMj9iDufKswZmrpFBuDSleTehyZRH8EDCrZZjMEvVdRgCDqQOi9jTOiF-96PnnXpOWI7sRr4EDRQA1ENqE0vl-str10CuNzOm1r6AyOv36bAszD7bPJA-EQQUp9cHGj4hrw7qeNH9IRcqlcE0cOxTo-Yp3AcAXLZAcG6PO8P2IaK4JZAjtVJtv_GeCl5Oie_JjtlilcbL2g'

api = API(token)
vk_user = User(token=user_token)
labeler = BotLabeler()
state_dispenser = BuiltinStateDispenser()