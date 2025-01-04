from . import jalali, gregorian
from django.utils import timezone
from datetime import datetime

def persian_numbers_converter(mystr):
  numbers = {
    "0": "۰",
    "1": "۱",
    "2": "۲",
    "3": "۳",
    "4": "۴",
    "5": "۵",
    "6": "۶",
    "7": "۷",
    "8": "۸",
    "9": "۹",
  }

  for e, p in numbers.items():
    mystr = mystr.replace(e, p)

  return mystr  

def jalali_converter(time):

  if timezone.is_aware(time):
    time = timezone.localtime(time)

  jmonths = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]

  time_to_str = '{},{},{}'.format(time.year, time.month, time.day)
  time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
  time_to_list = list(time_to_tuple)

  for index, month in enumerate(jmonths):
    if time_to_list[1] == index + 1:
      time_to_list[1] = month
      break

  formatted_time = '{}:{}'.format(str(time.hour).zfill(2), str(time.minute).zfill(2))

  output = '{} {} {}, ساعت {}'.format(
    time_to_list[2],
    time_to_list[1],
    time_to_list[0],
    formatted_time,
  )

  return persian_numbers_converter(output)


def age(birthyear, birthmonth, birthday):
  if not all([birthyear, birthmonth, birthday]):
    return None

  jmonths = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]

  if birthmonth not in jmonths:
    return None

  birth_month_index = jmonths.index(birthmonth) + 1
  jalali_date_str = f"{birthyear},{birth_month_index},{birthday}"
  try:
    gregorian_date = jalali.Persian(jalali_date_str).gregorian_datetime()
  except Exception as e:
    return None

  today = datetime.now()
  age = today.year - gregorian_date.year - (
    (today.month, today.day) < (gregorian_date.month, gregorian_date.day)
  )
  return age

  
def birth_day(birthyear, birthmonth, birthday):
    if not all([birthyear, birthmonth, birthday]):
        return None

    jmonths = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]

    if birthmonth not in jmonths:
        return None

    birth_month_index = jmonths.index(birthmonth) + 1
    jalali_date_str = f"{birthyear},{birth_month_index},{birthday - 1}"
    try:
        gregorian_date = jalali.Persian(jalali_date_str).gregorian_datetime()
    except Exception as e:
        return None

    today = datetime.now()
    if (today.month, today.day) == (gregorian_date.month, gregorian_date.day):
        return True  # It is the user's birthday today
    return False  # Not the user's birthday
  
