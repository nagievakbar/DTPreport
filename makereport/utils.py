from .models import Report


def get_last_report_id(request):
    last_report = Report.objects.last()
    last_report_id = last_report.report_id
    return last_report_id

