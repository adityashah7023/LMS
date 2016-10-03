from django.contrib import admin
from libapp.models import Book, Dvd, Libuser, Libitem, Suggestion
import datetime


def renew(modeladmin, request, queryset):
    for item in queryset:
        if item.checked_out == True:
            item.duedate= datetime.datetime.now()+datetime.timedelta(days=21)
            item.save()


class BookInline(admin.StackedInline):
    model = Book  # This shows all fields of Book.
    fields = [('title', 'author'), 'duedate',]   #  Customizes to show only certain fields
    extra = 0

class DvdInline(admin.TabularInline):
    model = Dvd
    exclude = ['last_chkout', 'date_acquired']
    extra = 0

class LibuserAdmin(admin.ModelAdmin):
    fields = [('username'), ('first_name', 'last_name'),('profile_image')]
    inlines = [BookInline,DvdInline]


class BookAdmin(admin.ModelAdmin):
    fields = [('title', 'author', 'pubyr'), ('checked_out', 'itemtype', 'user', 'duedate'),'category']
    list_display = ('title', 'borrower','overdue','category','get_author')
    list_filter = ('category','author',)
    search_fields = ('author',)
    actions = [renew]

    def borrower(self, obj=None):
        if obj.checked_out == True:
            return obj.user     #Returns the user who has borrowed this book
        else:
            return ''

    def get_author(self, obj):
        return obj.author

    get_author.short_description = 'Author'
    get_author.admin_order_field = 'author'

class DvdAdmin(admin.ModelAdmin):
    fields = [('title','maker','pubyr'),('checked_out','itemtype','user','duedate'),'rating']
    list_display = ('title','rating','borrower','checked_out','overdue')
    list_filter = ('rating',)
    search_fields = ('title',)
    actions = [renew]

    def borrower(self, obj=None):
        if obj.checked_out == True:
            return obj.user  # Returns the user who has borrowed this book
        else:
            return ''


# Register your models here.
admin.site.register(Book,BookAdmin)
admin.site.register(Dvd,DvdAdmin)
admin.site.register(Libuser,LibuserAdmin)
admin.site.register(Suggestion)
