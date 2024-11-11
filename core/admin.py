from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Classe, Eleve, Periode, Matiere, Notation

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'profile_pic', 'is_active',
                    'is_staff', 'is_superuser', 'last_login',)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2", "profile_pic"),
            },
        ),
    )
    
admin.site.register(CustomUser, CustomUserAdmin)



@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    # Ajouter 'prof' à 'list_display' pour qu'il soit visible dans la liste des matières
    list_display = ('nom', 'classe', 'prof')  # Affichage de la matière, de la classe et du professeur
    
    # Permet de filtrer par classe et professeur dans l'administration
    list_filter = ('classe', 'prof')  # Ajout de 'prof' dans la liste des filtres

    # Vous pouvez également ajouter d'autres options si nécessaire
    search_fields = ('nom',)  # Permet de rechercher par nom de la matière

    # Si vous voulez que les champs apparaissent lors de l'édition, vous pouvez personnaliser les 'fieldsets'
    fieldsets = (
        (None, {'fields': ('nom', 'classe', 'prof')}),
    )



class EleveInline(admin.TabularInline):
    model = Eleve
    extra = 1

class MatiereInline(admin.TabularInline):
    model = Matiere
    extra = 1

class NotationInline(admin.TabularInline):
    model = Notation
    extra = 1

@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    inlines = [EleveInline, MatiereInline]

@admin.register(Eleve)
class EleveAdmin(admin.ModelAdmin):
    list_display = ('nom', 'classe')
    list_filter = ('classe',)

@admin.register(Periode)
class PeriodeAdmin(admin.ModelAdmin):
    list_display = ('nom',)


@admin.register(Notation)
class NotationAdmin(admin.ModelAdmin):
    list_display = ('eleve', 'matiere', 'periode', 'note_attendue', 'note_obtenue')
    list_filter = ('matiere', 'periode')

    def __init__(self, *args, **kwargs):
        classe_id = kwargs.pop('classe_id', None)
        super().__init__(*args, **kwargs)
        if classe_id:
            self.fields['eleve'].queryset = Eleve.objects.filter(classe_id=classe_id)
            self.fields['matiere'].queryset = Matiere.objects.filter(classe_id=classe_id)