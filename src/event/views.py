import json
from django.db import connection
from django.shortcuts import render
from django.http import HttpResponse
from .models import Event, Schedule


def index(request):
    with connection.cursor() as cursor:

        cursor.execute("""select *
                        from event_event
                        left join event_schedule on event_event.id = event_schedule.event_id_id
                        order by event_event.start_date asc, event_event.id asc
                        """)
        rows = cursor.fetchall()

        list = [{
                'title': data[1],
                'start': str(data[2]),
                'date': str(data[8]),
                'start_time': str(data[6]),
                'schedule_title': str(data[5]),
                'end': str(data[3])
                } for data in rows]
        print(list)


    return render(request,'index.html',{"list":json.dumps(list)})



def index2(request):
    with connection.cursor() as cursor:

        cursor.execute("""select *
                        from event_event
                        left join event_schedule on event_event.id = event_schedule.event_id_id
                        order by event_event.start_date asc, event_event.id asc
                        """)
        rows = cursor.fetchall()
    print(rows)

    # list_events = Event.objects.order_by('start_date')[:5]
    list_events = Event.objects.raw('SELECT * FROM event_event order by start_date limit 5')
    list_events = Event.objects.raw('SELECT * FROM event_event order by start_date limit 5')
    ids = ", ".join(str(event.id) for event in list_events)
    list_schedules = Schedule.objects.raw('select * from event_schedule where event_id_id in (%s)' % ids)
    list = []
    for data in list_events:
        list.append( {
            'title': data.title,
            'start': str(data.start_date),
            'end': str(data.end_date)
            })
        # schedules = data.schedule_set.all()
        # print(schedules)

        for schedule in list_schedules:
            if data.id == schedule.event_id_id:
                list.append({
                    'start':f'{schedule.event_date} {schedule.start_time}',
                    'end':f'{schedule.event_date} {schedule.end_time}',
                    'title':schedule.title

                    })



    print(list)
    return render(request,'index.html',{"list":json.dumps(list)})
