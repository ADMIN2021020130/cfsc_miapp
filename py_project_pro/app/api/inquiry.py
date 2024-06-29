from fastapi import APIRouter, HTTPException
from app.models.booking import QueryInfo
from app.services.booking_service import BookingService
from app.utils.logger import get_logger

router = APIRouter()
booking_service = BookingService()
logger = get_logger(__name__)

@router.post("/inquire_invester_info_api")
async def check_sql(query_key: QueryInfo):
    logger.info(f"收到查询请求: {query_key}")
    result = booking_service.get_booking_info(query_key.id)
    if isinstance(result, dict) and result.get('message'):
        logger.error(f"查询预定失败: {result.get('message')}")
        raise HTTPException(status_code=500, detail=result.get('message'))
    if not result:
        logger.warning(f"未找到预定信息: {query_key}")
        raise HTTPException(status_code=404, detail="找不到预定信息")
    logger.info(f"成功查询预定: {result}")
    return result