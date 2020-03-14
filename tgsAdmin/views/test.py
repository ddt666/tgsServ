from rest_framework.response import Response
from rest_framework.views import APIView

# from django_celery_beat.models import PeriodicTask, IntervalSchedule
from tgsAdmin.tasks import time_task, time_task1
from tgsAdmin.utils.my_scheduler import scheduler

class TestView(APIView):
    authentication_classes = []

    def get(self, request):
        # schedule, created = IntervalSchedule.objects.get_or_create(
        #
        #     every=10,
        #
        #     period=IntervalSchedule.SECONDS,
        # )
        # PeriodicTask.objects.create(
        #
        #     interval=schedule,  # we created this above.
        #
        #     name='Importing contacts',  # simply describes this periodic task.
        #
        #     task='tgsAdmin.tasks.time_task',  # name of task.
        # )
        # res = time_task.delay()
        # print(res)
        import datetime
        for i in range(10):
            scheduler.add_job(time_task1, 'date',
                              run_date=datetime.datetime.now() + datetime.timedelta(seconds=20),
                              args=[str(i)])

        return Response("ok")



