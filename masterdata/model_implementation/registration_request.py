# # from django.core.mail import send_mail
# # from django.db import models
# # from django.db.models.signals import post_save

# # from masterdata.model_implementation.user import User
# from django.core.mail import send_mail
# from django.db import models
# from django.db.models.signals import post_save
# import logging

# from masterdata.model_implementation.user import User

# logger = logging.getLogger(__name__)  # Define the logger at the beginning


# class RegistrationRequest(models.Model):
#     name = models.CharField(max_length=255)
#     email = models.CharField(max_length=255)
#     country = models.CharField(max_length=255)
#     company_name = models.CharField(max_length=255)
#     company_address = models.TextField()


# # def save_registration_request(sender, instance: RegistrationRequest, **kwargs):

# #     send_mail(
# #         subject="New RiskCloud registration",
# #         message=f"""Dear RiskCloud administrator,
        
# # There is a new registration request for the RiskCloud by:

# # ##############################################################

# # Name: {instance.name}
# # Mail: {instance.email}
# # From: {instance.country}
# # Company: 
# # {instance.company_name}
# # {instance.company_address}
        
# # ##############################################################

# # You can create an account for this person in the RiskCloud administrator interface. 
# # Keep in mind that you have to inform new users about their account by ether sending a mail after creation or by using the "lost password" function of the RiskCloud.

# # If you don't want to create an account for this person you can simply ignore this email.

# # ----
# # You received this mail because the "Notify on registrations" option was activated for your account in the RiskCloud admin. 
# #         """,
# #         recipient_list=User.objects.filter(
# #             notify_on_registrations=True
# #         ).values_list("email", flat=True),
# #         from_email=None,
# #         fail_silently=True,
# #     )


# # post_save.connect(save_registration_request, sender=RegistrationRequest)


# def save_registration_request(sender, instance: RegistrationRequest, **kwargs):
#     try:
#         logger.info("save_registration_request function triggered")  # Log that the function is triggered

#         send_mail(
#             subject="New RiskCloud registration",
#             message=f"""Dear RiskCloud administrator,
#          Name: {instance.name}
#  Mail: {instance.email}
#  From: {instance.country}
#  Company: 
#  {instance.company_name}
#  {instance.company_address}
#                         # ... (email content)
#                     """,
#             recipient_list=User.objects.filter(notify_on_registrations=True).values_list("email", flat=True),
#             logger.info(f"Recipient List: {recipient_list}")
#             from_email=None,
#             fail_silently=False,
#         )
#         logger.info("Before sending email")
#         logger.info("Email sent successfully")

#     except Exception as e:
#         logger.error(f"Error sending email: {e}")
#         # Optionally, raise the exception again if you want to see the traceback in the Django logs.
#         raise e
 
# post_save.connect(save_registration_request, sender=RegistrationRequest)
# registration_request.py
# registration_request.py
# from django.core.mail import send_mail
# from django.db import models
# from django.db.models.signals import post_save
# import logging

# from masterdata.model_implementation.user import User

# logger = logging.getLogger(__name__)  # Define the logger at the beginning


# class RegistrationRequest(models.Model):
#     name = models.CharField(max_length=255)
#     email = models.EmailField()  # Use EmailField for email addresses
#     password = models.TextField()

# def save_registration_request(sender, instance: RegistrationRequest, **kwargs):
#     try:
#         print("save_registration_request function triggered")
#         logger.info("save_registration_request function triggered")  # Log that the function is triggered

#         # Get the list of users to notify
#         recipient_list = User.objects.filter(notify_on_registrations=True).values_list("email", flat=True)
#         logger.info(f"Recipient List: {recipient_list}")
#         print("Before sending email")
#         # Send email
#         send_mail(
#             subject="New RiskCloud registration",
#             message=f"""Dear RiskCloud administrator,
#                   Name: {instance.name}
#                   Mail: {instance.email}
#                   From: {instance.country}
#                   Company: 
#                   {instance.company_name}
#                   {instance.company_address}
#                   # ... (email content)
#                 """,
#             recipient_list=recipient_list,
#             from_email=None,
#             fail_silently=False,
#         )
#         print("Email sent successfully")
#         logger.info("Before sending email")
#         logger.info("Email sent successfully")

#     except Exception as e:
#         logger.error(f"Error sending email: {e}")
#         # Optionally, raise the exception again if you want to see the traceback in the Django logs.
#         raise e

# # Connect the signal to the model
# post_save.connect(save_registration_request, sender=RegistrationRequest)
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.hashers import make_password
from masterdata.model_implementation.user import User
import logging

logger = logging.getLogger(__name__)  # Define the logger at the beginning


class RegistrationRequest(models.Model):
    name = models.CharField(max_length=255)
    emaial = models.EmailField()  # Use EmailField for email addresses
    password = models.TextField()

def save_registration_request(sender, instance: RegistrationRequest, **kwargs):
    try:
        logger.info("save_registration_request function triggered")  # Log that the function is triggered

        # Hash the password before saving
        instance.password = make_password(instance.password)

        # Get the list of users to notify
        recipient_list = User.objects.filter(notify_on_registrations=True).values_list("email", flat=True)
        logger.info(f"Recipient List: {recipient_list}")

        # Send email
        send_mail(
            subject="New RiskCloud registration",
            message=f"""Dear RiskCloud administrator,
                  Name: {instance.name}
                  Mail: {instance.email}
                  From: {instance.country}
                  Company: 
                  {instance.company_name}
                  {instance.company_address}
                  # ... (email content)
                """,
            recipient_list=recipient_list,
            from_email=None,
            fail_silently=False,
        )

        logger.info("Email sent successfully")

    except Exception as e:
        logger.error(f"Error hashing password or sending email: {e}")
        # Optionally, raise the exception again if you want to see the traceback in the Django logs.
        raise e

# Connect the signal to the model
post_save.connect(save_registration_request, sender=RegistrationRequest)
