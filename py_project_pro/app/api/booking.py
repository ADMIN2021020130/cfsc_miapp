from fastapi import APIRouter, HTTPException
from app.models.booking import RoomBooking
from app.services.booking_service import BookingService
from app.utils.logger import get_logger

router = APIRouter()
booking_service = BookingService()
logger = get_logger(__name__)

@router.post('/insert_booking_info_api')
async def add_booking_info(room_booking: RoomBooking):
    logger.info(f"收到预定请求: {room_booking.dict()}")
    result = booking_service.add_booking(room_booking)
    if result.get('id') == 'error':
        logger.error(f"添加预定失败: {result.get('message', '未知错误')}")
        raise HTTPException(status_code=500, detail=result.get('message', '添加预定信息失败'))
    logger.info(f"成功添加预定: {result}")
    return result