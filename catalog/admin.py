from django.contrib import admin
from .models import Book,Author,Language,BookInstance,Genre


# Register your models here.

#admin.site.register(Book)
#admin.site.register(BookInstance)
#admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Language)

class BookInline(admin.TabularInline):
    model=Book
    extra=0

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    fields = ['first_name','last_name',('date_of_birth','date_of_death')]
    list_display = ['first_name','last_name','date_of_birth','date_of_death']
    inlines=[BookInline]

class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra=0

class BookAdmin(admin.ModelAdmin):
    list_display = ['title','author','display_genre']
    inlines = [BookInstanceInline]

admin.site.register(Book,BookAdmin)

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ['book','id','borrower','status','due_back',]
    list_filter = ['status','due_back']
    fieldsets = (
        (
            None, {'fields':('book','imprint','id')}
        ),('Availability',{'fields':('status','due_back','borrower')}))