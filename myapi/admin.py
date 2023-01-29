from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.shortcuts import render

from .models import *


def check_time(start, finish):
    if start < timezone.now() < finish:
        return True
    else:
        return False


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'token')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username',)


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = []

    def has_delete_permission(self, request, obj=None):
        # Disable delete
        return False

    actions = []


def get_result(modeladmin, request, queryset):
    results_list = []
    for v in queryset:
        print(v)
        if not check_time(v.start, v.finish):
            candidates = Candidates.objects.filter(faculty=v.faculty).values()
            print(candidates)
            cand_list = []
            for c in candidates:
                print(c['candidate_name'])
                result = Goals.objects.get(candidate_name=c['id']).candidate_goals
                print(result)
                cand_list.append({"candidate_name": c['candidate_name'], "result": result})
            results_list.append({"voting": v.name, "candidates": cand_list})
    context = {
        "result": results_list
    }
    print(context)
    return render(request, 'results.html', context=context)


def delete_voting(modeladmin, request, queryset):
    for v in queryset:
        if v.start > timezone.now():
            print(v.faculty)
            Candidates.objects.filter(faculty=v.faculty).delete()
            v.delete()


def delete_candidates(modeladmin, request, queryset):
    for c in queryset:
        if Votings.objects.get(faculty=c.faculty).start > timezone.now():
            c.delete()


class VotingsAdmin(admin.ModelAdmin):
    list_display = ['name']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if request.user.username[0].upper() != 'J':
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        # Disable delete
        return False

    actions = [get_result, delete_voting]


class CandidatesAdmin(admin.ModelAdmin):
    ordering = ('-faculty',)
    def has_delete_permission(self, request, obj=None):
        # Disable delete
        return False
    actions = [delete_candidates]



admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Votings, VotingsAdmin)
admin.site.register(Candidates, CandidatesAdmin)
admin.site.register(Faculty)
