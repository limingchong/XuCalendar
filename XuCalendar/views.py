import datetime

from django.http import HttpResponseRedirect
from datetime import date

from django.views.generic import ListView

from XuCalendar.models import dates

sayings = [
    ["我不知道将去何方，但我已在路上。", "《千与千寻》"],
    ["我与我周旋久，宁作我。", "《世说新语》"],
    ["胆小鬼连幸福都会害怕，碰到棉花都会受伤，有时还被幸福所伤。", "《人间失格》"],
    ["希望是美好的，也许是人间至善，而美好的事物永不消逝。", "斯蒂芬・金 《肖申克的救赎》"],
    ["死亡不是生命的终点，遗忘才是。", "《寻梦环游记》"],
    ["没有人规定一朵花，必须长成向日葵或玫瑰。", ""],
    ["命中注定的人，无论中间经过多少曲折，终会相遇。", ""],
    ["当你年轻时，以为什么都有答案，可是老了的时候，你可能又觉得其实人生并没有所谓的答案。", "王家卫 《堕落天使》"],
    ["第一下掌声可能要等很久，只要你尽了力，一定会有人欣赏。", "吴宇森 《英雄本色》"],
    ["这节目没有剧本、没有提示卡。未必是杰作，但如假包换。是一个人一生的真实记录。", "楚门的世界"]
]


class index(ListView):
    model = dates
    template_name = "Index.html"

    def get(self, request, *args, **kwargs):
        return super(index, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        now = datetime.datetime.now() + datetime.timedelta(hours=8)
        if 'id' in self.kwargs:
            base_day = date.fromordinal(self.kwargs["id"])
        else:
            base_day = date(year=now.year, month=now.month, day=now.day)

        first_month_day = date(year=base_day.year, month=base_day.month, day=1)
        sub_days = first_month_day.weekday()
        first_day_time = datetime.datetime.combine(first_month_day, datetime.datetime.min.time()) - datetime.timedelta(
            days=sub_days)
        first_day = first_day_time.date()

        if base_day.month != 12:
            next_month_day = date(year=base_day.year, month=base_day.month + 1, day=1)
        else:
            next_month_day = date(year=base_day.year + 1, month=1, day=1)
        add_days = (7 - next_month_day.weekday()) % 7
        last_day_time = datetime.datetime.combine(next_month_day, datetime.datetime.min.time()) + datetime.timedelta(
            days=add_days - 1)
        last_day = last_day_time.date()

        context = super().get_context_data(**kwargs)
        context['today'] = now.strftime("%Y.%m.%d").replace('.0', '.')
        context['month'] = base_day.strftime("%B")
        context['year'] = base_day.strftime("%Y")
        context['first_day'] = first_day.toordinal()
        context['this_day'] = now.toordinal()
        context['last_day'] = last_day.toordinal()
        context['saying'] = sayings[now.toordinal() % len(sayings)][0]
        context['author'] = sayings[now.toordinal() % len(sayings)][1]
        return context


class manage(ListView):
    model = dates
    template_name = "Manager.html"

    def post(self, request, *args, **kwargs):
        for date in dates.objects.all():
            if date.year == 2000:
                new_special = request.POST.get('special_' + str(date.id))
                dates.objects.filter(month=date.month, day=date.day).update(special=new_special)

        return HttpResponseRedirect("manage")


def color(request, color_id):
    now = datetime.datetime.now() + datetime.timedelta(hours=8)
    today_ordinal = now.toordinal()
    dates.objects.filter(ordinal=today_ordinal).update(color='#' + color_id)
    return HttpResponseRedirect("/")


def reset(request, *args, **kwargs):
    dates.objects.all().delete()

    today = datetime.datetime(year=2000, month=1, day=1)

    while today.year <= 2030:
        new_day = {
            'ordinal': today.toordinal(),
            'year': today.year,
            'month': today.month,
            'day': today.day,
            'week_day': today.weekday() + 1,
            'color': "white",
            'special': ""
        }
        dates.objects.create(**new_day)
        today += datetime.timedelta(days=1)

    print("reset finished.")
    return HttpResponseRedirect("manage")
