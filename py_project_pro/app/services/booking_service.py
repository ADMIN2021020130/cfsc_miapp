from datetime import datetime
from app.utils.datetime_utils import classify_meal_time_for_datetime
from pkg.mysql_handler import MysqlHandler, ServerError
from config.config import get_config


config = get_config()
mysql_handler = MysqlHandler(mysql_info=config.MYSQL_INFO)

class BookingService:
    def add_booking(self, room_booking):
        full_datetime_str = f"{room_booking.booking_time} {room_booking.use_time}"
        full_datetime = datetime.strptime(full_datetime_str, "%Y-%m-%d %H:%M")

        check_sql = "SELECT booking_id FROM room_bookings WHERE inviter=%s AND room_info=%s AND number_of_people=%s AND booking_time=%s AND tail_number=%s"
        check_data = (room_booking.inviter, room_booking.room_info, room_booking.number_of_people, full_datetime, room_booking.tail_number)
        try:
            existing_booking = mysql_handler.query_sql(check_sql, check_data)
        except ServerError as e:
            return {'id': 'error', 'message': str(e)}

        if existing_booking:
            return {'id': existing_booking[0]}

        insert_sql = "INSERT INTO room_bookings (inviter, number_of_people, booking_time, room_info, phone, tail_number) VALUES (%s, %s, %s, %s, %s, %s)"
        insert_data = (room_booking.inviter, room_booking.number_of_people, full_datetime, room_booking.room_info, room_booking.phone, room_booking.tail_number)
        try:
            mysql_handler.excute_sql(insert_sql, insert_data)
        except ServerError as e:
            return {'id': 'error', 'message': str(e)}

        search_sql = "SELECT booking_id FROM room_bookings WHERE inviter=%s AND number_of_people=%s AND room_info=%s AND booking_time=%s AND tail_number=%s"
        search_data = (room_booking.inviter, room_booking.number_of_people, room_booking.room_info, full_datetime, room_booking.tail_number)
        try:
            new_booking = mysql_handler.query_sql(search_sql, search_data)
        except ServerError as e:
            return {'id': 'error', 'message': str(e)}

        if new_booking:
            return {'id': new_booking[0]}
        else:
            return {'id': 'error', 'message': '添加预定信息失败'}

    def get_booking_info(self, booking_id):
        sql = "SELECT * FROM room_bookings WHERE booking_id=%s"
        try:
            res = mysql_handler.query_sql_all(sql, (booking_id,))
        except ServerError as e:
            return {'message': str(e)}

        if not res:
            return []

        res_lst = [
            res[0][1],  # 预定人信息
            res[0][2],  # 预定人数
            classify_meal_time_for_datetime(res[0][3])[0],  # 预定日期
            classify_meal_time_for_datetime(res[0][3])[1],  # 预定时间段
            res[0][4],  # 包间号
            res[0][5],  # 联系电话
            res[0][6],  # 手机尾号
        ]

        return res_lst