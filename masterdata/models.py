from django.core.mail import send_mail
from django.dispatch import receiver
from django.template import Template, Context
from django_rest_passwordreset.signals import reset_password_token_created
from django.db import models

from .model_implementation import (
    registration_request,
    species,
    comment,
    level,
    mycotoxin,
    company,
    component,
    contact_person,
    country,
    factor,
    interaction,
    product,
    sample_type,
    species,
    species_comment,
    species_level,
    species_sample_type_component,
    mycotoxin_levels,
    product_recommendation,
    recommendation,
    laboratory,
    user,
    translation,
)
from .model_implementation.translation import Translation


class masterdata_axxess(models.Model):
    species = models.CharField(max_length=100)
    ingredients = models.CharField(max_length=100)
    sol_ax = models.CharField(max_length=100, blank=True, null=True, default='0.0')
    insol_ax = models.CharField(max_length=100, blank=True, null=True, default='0.0')
    me_kcal = models.CharField(max_length=100, blank=True, null=True, default='0.0')
    inclusion_percentage = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'masterdata_axxess'

    def __str__(self):
        return f"{self.species} - {self.ingredients}"


class masterdata_formulation(models.Model):
    species = models.CharField(max_length=100)
    formulation_Sol_AX = models.CharField(max_length=100)
    formulation_Insol_AX = models.CharField(max_length=100)

    class Meta:
        db_table = 'masterdata_formulation'

    def __str__(self):
        return self.species


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        "user": reset_password_token.user.name,
        "token": reset_password_token.key,
    }

    t = Template(Translation.objects.get(id="MAIL_LOST_PASSWORD").translation)
    c = Context(context)
    message = t.render(c)

    send_mail(
        recipient_list=[reset_password_token.user.email],
        subject=Translation.objects.get(id="MAIL_LOST_PASSWORD_SUBJECT").translation,
        message=message,
        from_email=None,
    )



# from django.db import models

# class masterdata_User(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=100)
#     country = models.CharField(max_length=100)
#     company = models.CharField(max_length=100)
#     address_of_company = models.CharField(max_length=200)

#     class Meta:
#         db_table = 'masterdata_user'

#     def __str__(self):
#         return self.name






# from django.contrib.auth.models import AbstractUser
# from django.db import models

# class CustomUserUser(AbstractUser):
#     # Custom fields
#     company = models.CharField(max_length=255)
#     country = models.CharField(max_length=255)
#     address = models.CharField(max_length=255)
#     name = models.CharField(max_length=150)
#     email = models.EmailField(max_length=255, unique=True)  # Assuming email should be unique
#     password = models.CharField(max_length=255)  # You might want to use a more secure field like PasswordField

#     # Specify unique related_name arguments for conflicting fields
#     groups = models.ManyToManyField(
#         'auth.Group',
#         related_name='custom_user_user_groups',  # Unique related_name for groups
#         blank=True,
#         verbose_name='groups',
#         help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
#     )
#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         related_name='custom_user_user_permissions',  # Unique related_name for user_permissions
#         blank=True,
#         verbose_name='user permissions',
#         help_text='Specific permissions for this user.',
#     )

#     def __str__(self):
#         return self.username


# ## models.py

# from django.contrib.auth.models import AbstractUser
# from django.db import models

# class CustomUser(AbstractUser):
#     name = models.CharField(max_length=150)
#     company_name = models.CharField(max_length=150)
#     country_name = models.CharField(max_length=150)
#     address = models.CharField(max_length=255)

#     def __str__(self):
#         return self.username
