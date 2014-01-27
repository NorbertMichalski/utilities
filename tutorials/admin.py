from django.contrib import admin
from django.contrib.contenttypes import generic
from models import Category, Tutorial, Step, CategoryView, TutorialView, StepView

class StepInline(admin.TabularInline):
    model = Step
    extra = 1
    fields = ('caption', 'notes', 'image_url')

class StepViewInline(admin.TabularInline):
    model = StepView
    extra = 0
    fields = ('caption', 'image_url', 'notes',)
    template = 'admin/tutorials/stepview/edit_inline/tabular.html'

class TutorialInline(admin.StackedInline):
    model = Tutorial
    extra = 1
    inlines = [StepInline]

class TutorialLinkInline(admin.TabularInline):
    model = Tutorial
    extra = 0
    readonly_fields = ('changeform_link', )

class TutorialViewLinkInline(admin.TabularInline):
    model = TutorialView
    extra = 0
    readonly_fields = ('changeform_link', )

class TutorialViewInline(admin.StackedInline):
    model = TutorialView
    extra = 0

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'tutorials_contained', 'number_tutorials',)
    fieldsets = [
        ('Name',               {'fields': ['category_name',]}),
        #('Tutorials', {'fields': ['title']}),
    ]
    inlines = [TutorialLinkInline]

class CategoryViewAdmin(admin.ModelAdmin):
    list_display = ('category', 'tutorials_contained')
    fieldsets = [
        ('Name',               {'fields': ['category_name',]}),
        #('Tutorials', {'fields': ['title']}),
    ]
    inlines = [TutorialViewLinkInline]
    actions = None
    readonly_fields = ('category_name', )
    change_list_template = 'admin/tutorials/categoryview/change_list.html' 
    
    def __init__(self, *args, **kwargs):
        super(CategoryViewAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = (None, )
    
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        #Return nothing to make sure user can't update any data
        pass
    
    def changelist_view(self, request, extra_context=None):
        return super(CategoryViewAdmin, self).changelist_view(request, extra_context)
    

class TutorialAdmin(admin.ModelAdmin):
    list_display = ('tutorial_title', 'category', 'number_steps')
    fieldsets = [
        ('Details',               {'fields': ['category', 'tutorial_title']}),
        #('Tutorials', {'fields': ['title']}),
    ]
    inlines = [StepInline]
    
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

class StepAdmin(admin.ModelAdmin):
    list_display = ('image', 'caption', 'notes')
    list_filter = ('tutorial__tutorial_title', 'tutorial__category__category_name')
    search_fields = ['tutorial__tutorial_title', 'tutorial__category__category_name', 'caption', 'notes']

class TutorialViewAdmin(admin.ModelAdmin):
    list_display = ('tutorial_title', 'category', 'number_steps')
    fieldsets = [
        ('Details',               {'fields': ['category', 'tutorial_title']}),
        #('Tutorials', {'fields': ['title']}),
    ]
    inlines = [StepViewInline]
    actions = None
    readonly_fields = ('tutorial_title', 'category' )
    change_list_template = 'admin/tutorials/tutorialview/change_list.html' 
    
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        #Return nothing to make sure user can't update any data
        pass
    
    def changelist_view(self, request, extra_context=None):
        return super(TutorialViewAdmin, self).changelist_view(request, extra_context)
    
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

admin.site.register(Tutorial, TutorialAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CategoryView, CategoryViewAdmin)
#admin.site.register(StepView, StepAdmin)

admin.site.register(TutorialView, TutorialViewAdmin)