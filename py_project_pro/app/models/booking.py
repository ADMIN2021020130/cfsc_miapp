from pydantic import BaseModel

class RoomBooking(BaseModel):
    inviter: str
    room_info: str
    number_of_people: int
    booking_time: str
    use_time: str
    phone: str
    tail_number: str

class QueryInfo(BaseModel):
    id: int