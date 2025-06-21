from datetime import timedelta, datetime
import calendar
from copy import deepcopy
from dateutil import rrule
from dateutil.relativedelta import relativedelta


def today_zero(day=None):
    """
    获取今天零点时间
    :param day: 今天
    :return:今天零点时间
    """
    now = day or datetime.now()
    return datetime(now.year, now.month, now.day, 0, 0, 0)


def tomorrow_zero(day=None):
    """
    获取明天零点时间
    :param day: 今天
    :return:明天零点时间
    """
    now = day or datetime.now()
    return datetime(now.year, now.month, now.day, 0, 0, 0) + timedelta(days=1)


def tomorrow_date(day=None):
    """
    :param day:
    :return:
    """
    now_day = day or datetime.now().date()
    return now_day + timedelta(days=1)


def this_week_start(base_date=None):
    """
    本周第一天
    :param base_date:
    :return:
    """
    today = base_date or datetime.now().date()
    return today - timedelta(days=today.weekday())


def this_week_start_zero():
    """
    本周第一天零点
    :return:
    """
    day = this_week_start()
    return today_zero(day=day)


def this_week_end(base_date=None):
    """
    本周最后一天
    :param base_date:
    :return:
    """
    today = base_date or datetime.now().date()
    return today + timedelta(days=6 - today.weekday())


def this_week_friday(base_date=None):
    """
    本周周五
    :param base_date:
    :return:
    """
    today = base_date or datetime.now().date()
    return today + timedelta(days=4 - today.weekday())


def last_week_start(base_date=None):
    """
    上周第一天
    :param base_date:
    :return:
    """
    today = base_date or datetime.now().date()
    return today - timedelta(days=today.weekday() + 7)


def last_week_end(base_date=None):
    """
    上周最后一天
    :param base_date:
    :return:
    """
    today = base_date or datetime.now().date()
    return today - timedelta(days=today.weekday() + 1)


def next_week_start(base_date=None):
    """
    下周第一天
    :param base_date:
    :return:
    """
    today = base_date or datetime.now().date()
    return today + timedelta(days=7 - today.weekday())


def next_week_end(base_date=None):
    """
    下周最后一天
    :param base_date:
    :return:
    """
    today = base_date or datetime.now().date()
    return today + timedelta(days=13 - today.weekday())


def this_month_start(this_month=None):
    """
    本月第一天
    :param this_month:
    :return:
    """
    now = this_month or datetime.now()
    return datetime(now.year, now.month, 1)


def this_month_end(this_month=None):
    """
    本月最后一天
    :param this_month:
    :return:
    """
    now = this_month or datetime.now()
    return datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1])


def get_current_day_prev_week_workday_end(current_day):
    """
    :param current_day:
    :return:
    """
    prev_week_workday_end = current_day - timedelta(days=current_day.weekday() + 3)
    return prev_week_workday_end


def get_current_day_next_week_start(current_day):
    next_week_start = (current_day + timedelta(days=7 - current_day.weekday()))
    return next_week_start


def get_current_day_current_week_end(current_day):
    current_week_end = (current_day + timedelta(days=6 - current_day.weekday()))
    return current_week_end


def get_first_day_of_last_month():
    """
    获取上个月第一天的日期
    :return: 返回日期
    """
    today = datetime.today()
    year = today.year
    month = today.month
    if month == 1:
        month = 12
        year -= 1
    else:
        month -= 1
    res = datetime(year, month, 1)
    return res


def get_1st_of_next_month(today):
    """
    获取下个月的1号的日期
    :return: 返回日期
    """
    year = today.year
    month = today.month
    if month == 12:
        month = 1
        year += 1
    else:
        month += 1
    res = datetime(year, month, 1).date()
    return res


def next_workday(start_date, include_start_date=False):
    """
    下一个工作日
    :param start_date:
    :param include_start_date:
    :return:
    """
    if include_start_date and is_workday(start_date):
        return start_date
    return get_date_by_timedelta_days(start_date, 1, only_workday=True)



def get_date_by_timedelta_days(start_date, days_count, only_workday=False):
    """
    获取一个日期 延期后的日期
    :param start_date:
    :param days_count:
    :param only_workday:
    :return:
    """
    if only_workday:
        business_days_to_add = days_count
        current_date = start_date
        while business_days_to_add > 0:
            current_date += timedelta(days=1)
            weekday = current_date.weekday()
            if weekday >= 5:  # sunday = 6
                continue
            business_days_to_add -= 1
        return current_date
    else:
        result_date = start_date + timedelta(days=days_count)
    return result_date



def get_days_count_between_date(start_date, end_date, only_workday=False):
    """
    获取两个日期之前的天数   包含起始结束日期。
    :param start_date:
    :param end_date:
    :param only_workday: 是否只统计工作日
    :return:
    """
    if only_workday:
        days_count = workday_count(start_date, end_date)
    else:
        days_count = (end_date - start_date).days + 1
    return days_count


def is_workday(date):
    if date.weekday() in [5, 6]:
        return False
    return True


def workday_count(start, end, holidays=0, days_off=None):
    """
    工作日天数。默认周六、周日为非工作日。
    :param start:
    :param end:
    :param holidays:
    :param days_off:
    :return:
    """
    if days_off is None:
        days_off = (5, 6)
    workday_list = [x for x in range(7) if x not in days_off]
    days = rrule.rrule(rrule.DAILY, dtstart=start, until=end, byweekday=workday_list)
    return days.count() - holidays


def get_date_list(start_date, end_date):
    """
    获取开始日期到结束日期之间的日期列表
    :param start_date: 开始日期
    :param end_date: 结束日期
    :return:
    """
    data = []
    current_date = start_date
    while current_date <= end_date:
        data.append(deepcopy(current_date))
        current_date = current_date + timedelta(days=1)
    return data


def get_date_str_list(start_date, end_date, date_format="'%Y-%m-%d'"):
    """
    获取开始日期到结束日期之间的日期字符串列表
    :param start_date: 开始日期
    :param end_date: 结束日期
    :param date_format:'%Y-%m-%d'
    :return:
    """
    data = []
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime(date_format)
        data.append(date_str)
        current_date = current_date + timedelta(days=1)
    return data


def get_month_str_list(start_date, end_date, date_format="%Y-%m"):
    """
    获取开始日期到结束日期之间的年月字符串列表
    :param start_date: 开始日期
    :param end_date: 结束日期
    :param date_format:'%Y-%m'
    :return:
    """
    data = []
    current_date = start_date
    end_date_format = end_date.strftime(date_format)
    while current_date.strftime(date_format) <= end_date_format:
        date_str = current_date.strftime(date_format)
        data.append(date_str)
        current_date = current_date + relativedelta(months=1)
    return data
