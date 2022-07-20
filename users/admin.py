from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ContactUsQuery, User, ProfessionalUser, Service, SubService, ProfessionalUserService, \
    UserRequirement, FlaggedProfessionalUserReport, FavouriteUser  # HireProfessionalRequest

# Register your models here.
# admin.site.unregister(User)

admin.site.register(ContactUsQuery)
admin.site.register(User)
admin.site.register(ProfessionalUser)
admin.site.register(Service)
admin.site.register(SubService)
admin.site.register(ProfessionalUserService)
# admin.site.register(HireProfessionalRequest)
admin.site.register(UserRequirement)
admin.site.register(FlaggedProfessionalUserReport)
admin.site.register(FavouriteUser)