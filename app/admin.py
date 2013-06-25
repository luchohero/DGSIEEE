from django.contrib import admin
from models import *
#Datos.objects.order_by('id',)
class Clases_CrecimientoAdmin(admin.ModelAdmin):
		list_display = 'nivel',
		list_filter = 'nivel',
		search_fields = ['nivel']

#class DatosAdmin(admin.ModelAdmin):
	


	#Trabajo
    #TitulosTeologicos
    #Titulos
    #Vivienda
    
admin.site.register(Calendario)
admin.site.register(Datos)
admin.site.register(Flet)
admin.site.register(Clases_Crecimiento, Clases_CrecimientoAdmin)


#admin.site.register(Algo, AlgoAdmin)
#admin.site.register(Datos, DatosAdmin)
admin.site.register(Estado)
#admin.site.register(Trabajo)
#admin.site.register(TitulosTeologico)
#admin.site.register(Titulo)
#admin.site.register(Vivienda)



