from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

import os
from pathlib import Path


import shutil
import sys
import uvicorn
from pkg.mysql_handler import MysqlHandler
from config.config import get_config

rootPath = os.path.abspath(os.path.dirname(__file__))
sys.path.append(rootPath)
config = get_config()
from datetime import datetime
mysql_handler = MysqlHandler(mysql_info=config.MYSQL_INFO)




app = FastAPI()










@app.get("/")
def read_root():
    return {"Hello": "World"}


from datetime import datetime




def classify_meal_time_for_datetime(input_datetime):


    # 定义午餐和晚餐的时间段
    lunch_start = input_datetime.replace(hour=10, minute=30, second=0, microsecond=0)
    lunch_end = input_datetime.replace(hour=14, minute=0, second=0, microsecond=0)
    dinner_start = input_datetime.replace(hour=16, minute=30, second=0, microsecond=0)
    dinner_end = input_datetime.replace(hour=21, minute=0, second=0, microsecond=0)

    # 判断并返回包含日期、实际时间点和星期几的字符串
    date_str = input_datetime.strftime("%Y-%m-%d")
    use_food_time = ""
    if lunch_start <= input_datetime <= lunch_end:
        use_food_time =  f"午餐 {input_datetime.strftime('%H:%M')}"
    elif dinner_start <= input_datetime <= dinner_end:
        use_food_time = f"晚餐 {input_datetime.strftime('%H:%M')}"
    return date_str, use_food_time








# 定义接口传入的字段信息
class RoomBooking(BaseModel):
    # 预定人
    inviter: str

    # 房间信息
    room_info: str

    # 预定人数
    number_of_people: int
    # 预定时间
    booking_time: str
    # 用餐时间
    use_time: str
    # 联系人的电话话
    phone: str
    # 预约手机尾号
    tail_number: str





@app.post('/insert_booking_info_api')
async def add_booking_info(room_booking: RoomBooking):
    full_datetime_str = f"{room_booking.booking_time} {room_booking.use_time}"
    full_datetime = datetime.strptime(full_datetime_str, "%Y-%m-%d %H:%M")

    # 检查是否有重复预定
    check_sql = "SELECT booking_id FROM room_bookings WHERE inviter=%s AND room_info=%s AND number_of_people=%s AND booking_time=%s AND tail_number=%s"
    check_data = (room_booking.inviter, room_booking.room_info, room_booking.number_of_people, full_datetime,room_booking.tail_number)
    existing_booking = mysql_handler.query_sql(check_sql, check_data)

    if existing_booking:
        print('用户已存在，返回其id',existing_booking[0])
        print(f"插入预定信息: {room_booking.inviter}用户已在表中")
        return {'id': existing_booking[0]}

    # 插入数据
    insert_sql = "INSERT INTO room_bookings (inviter, number_of_people, booking_time, room_info, phone, tail_number) VALUES (%s, %s, %s, %s, %s,%s)"
    insert_data = (room_booking.inviter, room_booking.number_of_people, full_datetime, room_booking.room_info, room_booking.phone, room_booking.tail_number)
    mysql_handler.excute_sql(insert_sql, insert_data)
    print(f"插入预定信息: {room_booking.dict()}")

    search_sql = "SELECT booking_id FROM room_bookings WHERE inviter=%s AND number_of_people=%s AND room_info=%s AND booking_time=%s AND tail_number=%s"
    search_data = (room_booking.inviter, room_booking.number_of_people, room_booking.room_info, full_datetime,room_booking.tail_number)
    new_booking = mysql_handler.query_sql(search_sql, search_data)

    if new_booking:
        print('用户不存在,已成功注册',new_booking[0])
        print(f"插入预定信息: {room_booking.inviter}注册成功")
        return {'id': new_booking[0]}
    else:
        return {'id': 'error'}





class Query_info(BaseModel):
    # 查询id
    id : int


@app.post("/inquire_invester_info_api")
async def check_sql(query_key: Query_info):
    sql = "SELECT * FROM room_bookings WHERE booking_id=%s"
    res = mysql_handler.query_sql_all(sql, (query_key.id,))

    if not res:
        return []

    res_lst = [
        res[0][1],  # 预定人信息
        res[0][2],  # 预定人数
        classify_meal_time_for_datetime(res[0][3])[0],  # 预定日期
        classify_meal_time_for_datetime(res[0][3])[1],  # 预定时间段
        res[0][4],  # 包间号
        res[0][5] ,  # 联系电话
        res[0][6],
    ]

    return res_lst


if __name__ == "__main__":


    uvicorn.run(app='main:app', host="0.0.0.0",  port=8080,reload=True)