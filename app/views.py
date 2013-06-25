# -*- encoding: utf-8 -*-
from django.shortcuts import render_to_response
from django.db.models import Q
from django.template import RequestContext
from django.template import loader, Context
from models import *
from app.forms import *
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.views.decorators import staff_member_required
import csv
from django.http import HttpResponse
from datetime import datetime, date
from excel_response import ExcelResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required(login_url='/')
def calendario(request):
  usuario = request.user
  calendario = Calendario.objects.all() 
  return render_to_response('calendario/inicio.html',{'calendario':calendario, 'usuario':usuario},context_instance=RequestContext(request))
  


def ingresar(request):

  if not request.user.is_anonymous():
        return HttpResponseRedirect('/manage/')
  if request.method == 'POST':
    formulario_ing = AuthenticationForm(request.POST)
    if formulario_ing.is_valid:
      usuario = request.POST['username']
      clave = request.POST['password']
      acceso = authenticate(username=usuario, password=clave)
      if acceso is not None:
        if acceso.is_active:
          login(request, acceso)
          return HttpResponseRedirect('/agenda/')
        else:
          mensaje = 'error'
          return HttpResponseRedirect('')
      else:
        mensaje = 'error1'
        return HttpResponseRedirect('')
  else:
    formulario_ing = AuthenticationForm()
  return render_to_response('acceso.html',{'formulario_ing':formulario_ing}, context_instance=RequestContext(request))


#login
# agragar a la tabla nativa
@login_required(login_url='/')
def usuario(request):

  if request.method == 'POST':
    formulario_user = UserCreationForm(request.POST)
      
    if formulario_user.is_valid:
      formulario_user.save()
      d=request.POST['username']
      return HttpResponseRedirect('/add/us/?p=%s' % d)
    
  else:
    formulario_user = UserCreationForm()
  return render_to_response('nuevousuario.html',{'formulario_user':formulario_user}, context_instance=RequestContext(request))

@login_required(login_url='/')
def usuario_names(request):
  d = request.GET['p']
  usuario = User.objects.get(username=d)
  if request.method == 'POST':
    formulario_user = UserForm(request.POST,instance=usuario)
    
    if formulario_user.is_valid:
      formulario_user.save()
      return HttpResponseRedirect('/add/?p=%s' % d)

  else:
    formulario_user = UserForm(instance=usuario)
  return render_to_response('nuevousuario1.html',{'formulario_user':formulario_user}, context_instance=RequestContext(request))


@login_required(login_url='/')
def nuevo(request):  

  dm = request.GET['p']
  
  if request.method == "POST":

      formulario = DatosForm(request.POST)
      if formulario.is_valid():
        formulario.save()
        return HttpResponseRedirect("/manage/")
  else:
      formulario = DatosForm()
  return render_to_response('agregar.html',{'formulario':formulario, 'dm':dm},context_instance=RequestContext(request))

@login_required(login_url='/')
def estado_f(request):
  if request.method == "POST":
      formularioestado = EstadoForm(request.POST)
      if formularioestado.is_valid():
        formularioestado.save()
        return HttpResponseRedirect("../../add")
  else:
      formularioestado = EstadoForm()
  return render_to_response('estado.html',{'formularioestado':formularioestado},context_instance=RequestContext(request))  


@login_required(login_url='/')
def perfil(request,num1):
    
    n = int(num1)
    perfil = Datos.objects.filter(Usuario__username=num1)
    
    return render_to_response('perfil.html',{'perfil':perfil})

##########################################################
def exportar(request):
  query = request.GET.get('q', '')
  if query:
    qset = (
            Q(Telefono__icontains=query) |
            Q(Usuario__first_name__icontains=query) |
            Q(Usuario__last_name__icontains=query) |
            Q(Usuario__username__icontains=query) |
            Q(Celular__icontains=query) |
            Q(Usuario__email__icontains=query) |
            Q(Fletn__nivel__icontains=query)
        )
    usuarios = Datos.objects.filter(qset).distinct()

    #return render_to_response('inicio.html',{'usuarios':usuarios, 'usuario':usuario},context_instance=RequestContext(request))

  else:
    usuarios = Datos.objects.all()
  
  response = HttpResponse(content_type='text/xls')
  response['Content-Disposition'] = 'attachment; filename="somefilename.xls"'
  #usuarios = Datos.objects.all()

  t = loader.get_template('xlst.html')
  c = Context({
        'usuarios': usuarios,
  })
  response.write(t.render(c))
  return response

@login_required(login_url='/')
def cerrar(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url='/')
def eliminar(request):
    if request.method == 'GET':
      p = request.GET['p']
      us = User.objects.get(username=p)
      us.delete()
    return HttpResponseRedirect('../')


#########################



@login_required(login_url='/')
@staff_member_required
def index(request):
  
  

  query = request.GET.get('q','')
  if query:
      qset = (
            Q(Telefono__icontains=query) |
            Q(Usuario__first_name__icontains=query) |
            Q(Usuario__last_name__icontains=query) |
            Q(Usuario__username__icontains=query) |
            Q(Celular__icontains=query) |
            Q(Usuario__email__icontains=query) |
            Q(Fletn__nivel__icontains=query)
        )
      #usuarios = Datos.objects.filter(qset).distinct()
      
      q = request.GET['q']
      d = '?q=%s&' % q
      usuario_list = Datos.objects.filter(qset).distinct()
      paginator = Paginator(usuario_list, 20) # Show 25 contacts per page

      page = request.GET.get('page')
      try:
        usuarios = paginator.page(page)
      except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        usuarios = paginator.page(1)
      except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        usuarios = paginator.page(paginator.num_pages)
    #return render_to_response('inicio.html',{'usuarios':usuarios, 'usuario':usuario, 'q':q},context_instance=RequestContext(request))
    #return render_to_response('inicio.html',{'usuarios':usuarios, 'usuario':usuario},context_instance=RequestContext(request))
      return render_to_response('inicio.html',{'usuarios':usuarios,'q':q, 'd':d},context_instance=RequestContext(request))
  
  else:
    d = '?'
    usuario_list = Datos.objects.all()
    paginator = Paginator(usuario_list, 20) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
      usuarios = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
      usuarios = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
      usuarios = paginator.page(paginator.num_pages)
    f = usuarios.paginator.num_pages
    return render_to_response('inicio.html',{'usuarios':usuarios,'d':d},context_instance=RequestContext(request))
  

  

def listing(request):
    contact_list = Datos.objects.all()
    paginator = Paginator(contact_list, 5) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return render_to_response('list.html', {"contacts": contacts})

@login_required(login_url='/')
@staff_member_required
def buscar(request):

  usuario_list = Datos.objects.all()
  paginator = Paginator(usuario_list, 2) # Show 25 contacts per page

  page = request.GET.get('page')
  try:
    usuarios = paginator.page(page)
  except PageNotAnInteger:
        # If page is not an integer, deliver first page.
    usuarios = paginator.page(1)
  except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
    usuarios = paginator.page(paginator.num_pages)

  return render_to_response('inicio.html', {"usuarios": usuarios})


def suma(request,num1,num2):
      op1 = int(num1)
      op2 = int(num2)
      html = "<html><body>La suma de los numeros es: %s </body></html>" % (op1-op2)
      return HttpResponse(html)

@login_required(login_url='/')
@staff_member_required
def manage(request,num1):
  
  if num1 == '100':
      n = 'Nuevo Inicio'
  if num1 == '101':
      n = 'Clase 101'
  if num1 == '201':
      n = 'Clase 201'
  if num1 == '301':
      n = 'Clase 301'
  if num1 == '401':
      n = 'Clase 401'
  if num1 == '501':
      n = 'Clase 501'

  
  query = request.GET.get('q','')
  if query:
      qset = (
            Q(Telefono__icontains=query) |
            Q(Usuario__first_name__icontains=query) |
            Q(Usuario__last_name__icontains=query) |
            Q(Usuario__username__icontains=query) |
            Q(Celular__icontains=query) |
            Q(Usuario__email__icontains=query) |
            Q(Fletn__nivel__icontains=query)
        )
      #usuarios = Datos.objects.filter(qset).distinct()
      
      q = request.GET['q']
      d = '?q=%s&' % q
      usuario_list = Datos.objects.filter(qset,CC__nivel=n).distinct()
      paginator = Paginator(usuario_list, 20) # Show 25 contacts per page

      page = request.GET.get('page')
      try:
        usuarios = paginator.page(page)
      except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        usuarios = paginator.page(1)
      except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        usuarios = paginator.page(paginator.num_pages)
    #return render_to_response('inicio.html',{'usuarios':usuarios, 'usuario':usuario, 'q':q},context_instance=RequestContext(request))
    #return render_to_response('inicio.html',{'usuarios':usuarios, 'usuario':usuario},context_instance=RequestContext(request))
      return render_to_response('inicio.html',{'usuarios':usuarios,'q':q, 'd':d},context_instance=RequestContext(request))
  
  else:
    d = '?'
    usuario_list = Datos.objects.filter(CC__nivel=n)
    paginator = Paginator(usuario_list, 20) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
      usuarios = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
      usuarios = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
      usuarios = paginator.page(paginator.num_pages)
    f = usuarios.paginator.num_pages
    return render_to_response('inicio.html',{'usuarios':usuarios,'d':d},context_instance=RequestContext(request))
  


