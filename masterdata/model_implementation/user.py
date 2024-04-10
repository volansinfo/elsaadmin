from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    UserManager as BaseUserManager,
)
from masterdata.model_implementation.contact_person import ContactPerson
import typing


class UserManager(BaseUserManager):

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        if password is None:
            raise ValueError('The password must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Set the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if password is None:
            raise ValueError('The password must be set')
        return self.create_user(email, password, **extra_fields)
    def create_staffuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        return self._create_user(email, password, **extra_fields)

    def update_user_from_csv(
        self,
        user,
        name: str,
        country_access: typing.List[str],
        product_acces: typing.List[str],
        status: typing.Literal["intern", "extern"],
        company_id: str,
        contact_person_id: str,
        backend_user: str,
    ):
        from masterdata.model_implementation.company import Company
        from masterdata.model_implementation.contact_person import (
            ContactPerson,
        )

        try:
            company = Company.objects.get(name=company_id)
        except Company.DoesNotExist:
            print(f"No company '{company_id}' was found")
            company = None
        try:
            contact_person = ContactPerson.objects.get(name=contact_person_id)
        except ContactPerson.DoesNotExist:
            print(f"No contactperson '{contact_person_id}' was found")
            contact_person = None

        user.name = name
        user.ew_status = status
        user.company = company
        user.contact_person = contact_person
        user.is_staff = True if str(backend_user) == "1" else False
        user.is_superuser = True if str(backend_user) == "1" else False

        user.products.clear()
        user.countries.clear()
        for product_id in product_acces:
            user.products.add(product_id)
        for country_id in country_access:
            user.countries.add(country_id)
        user.save()
        return user

    def import_user_from_csv(
        self,
        email: str,
        name: str,
        country_access: typing.List[str],
        product_acces: typing.List[str],
        status: typing.Literal["intern", "extern"],
        company_id: str,
        contact_person_id: str,
        backend_user: str,
    ):
        from masterdata.model_implementation.company import Company
        from masterdata.model_implementation.contact_person import (
            ContactPerson,
        )

        password = self.make_random_password()

        try:
            company = Company.objects.get(name=company_id)
        except Company.DoesNotExist:
            print(f"No company '{company_id}' was found")
            company = None
        try:
            contact_person = ContactPerson.objects.get(name=contact_person_id)
        except ContactPerson.DoesNotExist:
            print(f"No contactperson '{contact_person_id}' was found")
            contact_person = None

        user = self.create_user(
            email=email,
            name=name,
            ew_status=status,
            company=company,
            contact_person=contact_person,
            password=password,
            is_staff=True if str(backend_user) == "1" else False,
            is_superuser=True if str(backend_user) == "1" else False,
        )
        for product_id in product_acces:
            user.products.add(product_id)
        for country_id in country_access:
            user.countries.add(country_id)

        return user


class User(AbstractUser):
    EW_USER_STATUS = (("intern", "Intern"), ("extern", "Extern"))
    DATABASE_ACCESS_TYPES = (
        ("none", "No Database access"),
        ("own", "Access to all own database entries"),
        (
            "countries",
            "Access to all database entries of the countries the user has access to",
        ),
        ("all", "Access to all database entries"),
    )

    username = None
    email = models.EmailField(
        verbose_name="email address", max_length=255, unique=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # Email & Password are required by default.

    name = models.CharField(max_length=255, blank=True, default="")
    countries = models.ManyToManyField("masterdata.country", blank=True)
    products = models.ManyToManyField("masterdata.product", blank=True)
    ew_status = models.CharField(
        max_length=255, choices=EW_USER_STATUS, default="intern", blank=False
    )
    notify_on_registrations = models.BooleanField(default=False)

    company = models.ForeignKey(
        "masterdata.company",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=None,
    )
    contact_person = models.ForeignKey(
        ContactPerson,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=None,
    )

    database_access = models.CharField(
        max_length=255,
        choices=DATABASE_ACCESS_TYPES,
        blank=False,
        default="none",
        verbose_name="Access to sample database",
    )
    customer_database_access = models.BooleanField(
        default=False, verbose_name="Access to customer database"
    )

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def get_assessment_database(self):
        from masterdata.model_implementation.user_assessment import (
            UserAssessmentSample,
        )

        if self.database_access == "none":
            return []
        elif self.database_access == "own":
            return UserAssessmentSample.objects.all().filter(
                assessment__author_id=self.id
            )
        elif self.database_access == "countries":
            return UserAssessmentSample.objects.all().filter(
                assessment__country__in=self.countries.all()
            )
        elif self.database_access == "all":
            return UserAssessmentSample.objects.all()

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    objects = UserManager()
