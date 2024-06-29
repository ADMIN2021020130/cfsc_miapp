def classify_meal_time_for_datetime(input_datetime):
    lunch_start = input_datetime.replace(hour=10, minute=30, second=0, microsecond=0)
    lunch_end = input_datetime.replace(hour=14, minute=0, second=0, microsecond=0)
    dinner_start = input_datetime.replace(hour=16, minute=30, second=0, microsecond=0)
    dinner_end = input_datetime.replace(hour=21, minute=0, second=0, microsecond=0)

    date_str = input_datetime.strftime("%Y-%m-%d")
    use_food_time = ""
    if lunch_start <= input_datetime <= lunch_end:
        use_food_time = f"午餐 {input_datetime.strftime('%H:%M')}"
    elif dinner_start <= input_datetime <= dinner_end:
        use_food_time = f"晚餐 {input_datetime.strftime('%H:%M')}"
    return date_str, use_food_time