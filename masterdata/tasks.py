import requests
from celery import shared_task
from django.core.mail import EmailMessage

from masterdata.model_implementation.translation import Translation
from masterdata.model_implementation.user import User
from masterdata.model_implementation.user_assessment import UserAssessment
from masterrisk import settings


@shared_task
def send_final_report(**kwargs):
    assessment: UserAssessment = UserAssessment.objects.get(
        id=kwargs["assessment_id"],
        secret_token=kwargs["secret_token"],
    )
    all_internal_mail_addresses = [
        user.email.lower() for user in User.objects.filter(ew_status="intern")
    ]

    all_receivers = [
        r.address.lower() for r in assessment.email_recipients.all()
    ]

    external_receivers = []
    internal_receivers = []

    for receiver in all_receivers:
        if receiver in all_internal_mail_addresses:
            internal_receivers.append(receiver)
        else:
            external_receivers.append(receiver)

    message = Translation.objects.get(id="MAIL_REPORT").translation
    subject = Translation.objects.get(id="MAIL_REPORT_SUBJECT").translation

    reports = [
        ["internal", internal_receivers],
        ["external", external_receivers],
    ]

    for report in reports:
        mail = EmailMessage(
            subject, message, settings.EMAIL_HOST_USER, report[1]
        )

        domain = f"{settings.PROTOCOL}://{settings.HOSTNAME}"

        body = {
            "url": f"{domain}/assessment/{assessment.id}/{assessment.secret_token}?forceLanguage={kwargs['lang']}&report_type={report[0]}",
            "emulateScreenMedia": False,
            "goto": {"timeout": 60000, "networkIdleInflight": 0},
        }
        receive = requests.post(
            f"http://printserver-service:9000/api/render/", json=body
        )
        mail.attach("report.pdf", receive.content, "application/pdf")

        mail.send()
        print(
            f"Sent {report[0]} report to {len(report[1])} receivers: {', '.join(report[1])}"
        )

    return True


@shared_task
def send_moving_risk_report(
    receiver_mail_address: str,
    customer_id: str,
    species_id: str,
    for_months: int,
    lang: str,
):
    message = Translation.objects.get(id="MAIL_REPORT").translation
    subject = Translation.objects.get(id="MAIL_REPORT_SUBJECT").translation
    mail = EmailMessage(
        subject, message, settings.EMAIL_HOST_USER, [receiver_mail_address]
    )

    domain = f"{settings.PROTOCOL}://{settings.HOSTNAME}"
    body = {
        "url": f"{domain}/moving-risk/{customer_id}/{species_id}/{for_months}?forceLanguage={lang}",
        "emulateScreenMedia": False,
        "goto": {"timeout": 60000},
    }
    receive = requests.post(f"http://printserver:9000/api/render/", json=body)
    mail.attach("report.pdf", receive.content, "application/pdf")
    mail.send()
