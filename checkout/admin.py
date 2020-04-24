from django.contrib import admin
from checkout.models import DeviceDB, ExecuteStrategy, CaseSet, StrategyRecord, TestCase, StrategyData, InitData, Basics


@admin.register(Basics)
class DeviceDBAdmin(admin.ModelAdmin):
    module = Basics
    list_per_page = 50
    model_column_list = []
    params = [f for f in module._meta.fields]
    for msg in params:
        model_column_list.append(msg.name)
    list_display = tuple(model_column_list)


@admin.register(InitData)
class DeviceDBAdmin(admin.ModelAdmin):
    module = InitData
    list_per_page = 50
    model_column_list = []
    params = [f for f in module._meta.fields]
    for msg in params:
        model_column_list.append(msg.name)
    list_display = tuple(model_column_list)


@admin.register(StrategyData)
class DeviceDBAdmin(admin.ModelAdmin):
    module = StrategyData
    list_per_page = 50
    model_column_list = []
    params = [f for f in module._meta.fields]
    for msg in params:
        model_column_list.append(msg.name)
    list_display = tuple(model_column_list)


@admin.register(TestCase)
class DeviceDBAdmin(admin.ModelAdmin):
    module = TestCase
    list_per_page = 50
    model_column_list = []
    params = [f for f in module._meta.fields]
    for msg in params:
        model_column_list.append(msg.name)
    list_display = tuple(model_column_list)


@admin.register(StrategyRecord)
class DeviceDBAdmin(admin.ModelAdmin):
    module = StrategyRecord
    list_per_page = 50
    model_column_list = []
    params = [f for f in module._meta.fields]
    for msg in params:
        model_column_list.append(msg.name)
    list_display = tuple(model_column_list)


@admin.register(ExecuteStrategy)
class DeviceDBAdmin(admin.ModelAdmin):
    module = ExecuteStrategy
    list_per_page = 50
    model_column_list = []
    params = [f for f in module._meta.fields]
    for msg in params:
        model_column_list.append(msg.name)
    list_display = tuple(model_column_list)


@admin.register(CaseSet)
class DeviceDBAdmin(admin.ModelAdmin):
    module = CaseSet
    list_per_page = 50
    model_column_list = []
    params = [f for f in module._meta.fields]
    for msg in params:
        model_column_list.append(msg.name)
    list_display = tuple(model_column_list)


@admin.register(DeviceDB)
class DeviceDBAdmin(admin.ModelAdmin):
    module = DeviceDB
    list_per_page = 50
    model_column_list = []
    params = [f for f in module._meta.fields]
    for msg in params:
        model_column_list.append(msg.name)
    list_display = tuple(model_column_list)