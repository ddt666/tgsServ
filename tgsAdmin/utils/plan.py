from tgsAdmin.models import Plan


def update_plan_status(plan_id):
    print(f"执行plan{plan_id}")
    Plan.objects.filter(id=plan_id).update(status=1)
