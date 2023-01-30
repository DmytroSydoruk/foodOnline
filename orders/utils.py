from datetime import datetime

def generate_order_number(pk: int) -> str:
    """generate unique order number based on date and time"""

    current_datetime:str = datetime.now().strftime('%Y%m%d%H%M')
    return current_datetime+str(pk)


