"""LIMS views."""
# Django module
from django.urls import reverse
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from django.db.models import Q

from . import models
from datetime import datetime
from workdays import workday
from math import ceil

# Pandas module
import pandas as pd

# Bokeh module
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.palettes import Spectral
from bokeh.models import ColumnDataSource
# Create your views here.

def is_lab(user):
    return user.groups.filter(name='laboratorio').exists()

def is_manager(user):
    return user.groups.filter(name='manager').exists()

def is_commercial(user):
    return user.groups.filter(name='comercial').exists()

def is_income(user):
    return user.groups.filter(name='ingreso').exists()

def is_income_or_coordinador(user):
    return user.groups.filter(name='ingreso').exists() or user.groups.filter(name='coordinador').exists()

def is_commercial_or_income(user):
    return user.groups.filter(name='comercial').exists() or user.groups.filter(name='ingreso').exists() or user.groups.filter(name='coordinador').exists()

def is_analyst(user):
    return user.groups.filter(name='analista').exists()

def is_coordinador(user):
    return user.groups.filter(name='coordinador').exists()

def add_workdays(start_date, num_workdays):
    end_date = workday(start_date, num_workdays)
    return end_date

def title_fix(texto):
    texto = texto.lower().title()
    texto = " ".join(texto.split())
    if texto[-1] == " ": texto = texto[:-1]
    if texto[0] == " ": texto = texto[1:]
    return texto

def cap_fix(texto):
    texto = texto.lower().capitalize()
    texto = " ".join(texto.split())
    if texto[-1] == " ": texto = texto[:-1]
    if texto[0] == " ": texto = texto[1:]
    return texto

def rut_fix(rut):
    rut = rut.replace('.','').replace(',','').replace('-','')
    rut = " ".join(rut.split())
    if rut[-1] == " ": rut = rut[:-1]
    if rut[0] == " ": rut = rut[1:]
    return rut

def list_to_string(lista):
    if len(lista)==2:
        return ' y '.join(lista)
    else:
        return ', '.join(lista)


def render_view(request, template, context):
    """Render views"""
    return render(request, template, context)


def calc_param_cot_etfa(parameters):

    """Esta función es para completar parametros faltantes en los servicio ETFA"""
    parameters_f = []
    for p in parameters:
        parametro = models.ParametroEspecifico.objects.get(pk= p).codigo
        if 'HCT' in parametro:
            if 'AFI-HCT'==parametro:
                HCF = models.ParametroEspecifico.objects.get(codigo='AFI-HCF-GRV')
                HCV = models.ParametroEspecifico.objects.get(codigo='AFI-HCV')
                if HCF.codigo_etfa=='nan' or HCF.codigo_etfa==None or HCV.codigo_etfa=='nan' or HCV.codigo_etfa==None:
                    parameters_f.append(p)
                
            
            elif 'AP-HCT'==parametro:
                HCF = models.ParametroEspecifico.objects.get(codigo='AP-HCF-GRV')
                HCV = models.ParametroEspecifico.objects.get(codigo='AP-HCV')
                if HCF.codigo_etfa=='nan' or HCF.codigo_etfa==None or HCV.codigo_etfa=='nan' or HCV.codigo_etfa==None:
                    parameters_f.append(p)
            
            elif 'AR-HCT' == parametro:
                HCF = models.ParametroEspecifico.objects.get(codigo='AR-HCF-GRV')
                HCV = models.ParametroEspecifico.objects.get(codigo='AR-HCV')
                if HCF.codigo_etfa=='nan' or HCF.codigo_etfa==None or HCV.codigo_etfa=='nan' or HCV.codigo_etfa==None:
                    parameters_f.append(p)
            
            elif 'SUB-HCT' == parametro:
                HCF = models.ParametroEspecifico.objects.get(codigo='SUB-HCF-GRV')
                HCV = models.ParametroEspecifico.objects.get(codigo='SUB-HCV')
                if HCF.codigo_etfa=='nan' or HCF.codigo_etfa==None or HCV.codigo_etfa=='nan' or HCV.codigo_etfa==None:
                    parameters_f.append(p)
            
            elif 'SUP-HCT' == parametro:
                HCF = models.ParametroEspecifico.objects.get(codigo='SUP-HCF-GRV')
                HCV = models.ParametroEspecifico.objects.get(codigo='SUP-HCV')
                if HCF.codigo_etfa=='nan' or HCF.codigo_etfa==None or HCV.codigo_etfa=='nan' or HCV.codigo_etfa==None:
                    parameters_f.append(p)                
            
            elif 'L-HCT' == parametro:
                HCF = models.ParametroEspecifico.objects.get(codigo='L-HCF-GRV')
                HCV = models.ParametroEspecifico.objects.get(codigo='L-HCV')
                if HCF.codigo_etfa=='nan' or HCF.codigo_etfa==None or HCV.codigo_etfa=='nan' or HCV.codigo_etfa==None:
                    parameters_f.append(p)
            
            elif 'SD-HCT' == parametro:
                HCF = models.ParametroEspecifico.objects.get(codigo='SD-HCF-GRV')
                HCV = models.ParametroEspecifico.objects.get(codigo='SD-HCV')
                if HCF.codigo_etfa=='nan' or HCF.codigo_etfa==None or HCV.codigo_etfa=='nan' or HCV.codigo_etfa==None:
                    parameters_f.append(p)
            
            elif 'S-HCT' == parametro:
                HCF = models.ParametroEspecifico.objects.get(codigo='S-HCF-GRV')
                HCV = models.ParametroEspecifico.objects.get(codigo='S-HCV')
                if HCF.codigo_etfa=='nan' or HCF.codigo_etfa==None or HCV.codigo_etfa=='nan' or HCV.codigo_etfa==None:
                    parameters_f.append(p)
        
        elif 'DDD+DDE+DDT' in parametro:
            if 'AP-DDD+DDE+DDT'==parametro:
                DDD = models.ParametroEspecifico.objects.get(codigo='AP-DDD-ME')
                DDE = models.ParametroEspecifico.objects.get(codigo='AP-DDE-ME')
                DDT = models.ParametroEspecifico.objects.get(codigo='AP-DDT-ME')
                if DDD.codigo_etfa=='nan' or DDD.codigo_etfa==None or DDE.codigo_etfa=='nan' or DDE.codigo_etfa==None or DDT.codigo_etfa=='nan' or DDT.codigo_etfa==None:
                    parameters_f.append(p)
            
            elif 'FC-DDD+DDE+DDT'==parametro:
                DDD = models.ParametroEspecifico.objects.get(codigo='FC-DDD-ME')
                DDE = models.ParametroEspecifico.objects.get(codigo='FC-DDE-ME')
                DDT = models.ParametroEspecifico.objects.get(codigo='FC-DDT-ME')
                if DDD.codigo_etfa=='nan' or DDD.codigo_etfa==None or DDE.codigo_etfa=='nan' or DDE.codigo_etfa==None or DDT.codigo_etfa=='nan' or DDT.codigo_etfa==None:
                    parameters_f.append(p)
            
        elif 'THM' in parametro:
            if 'AFI-THM-SM'==parametro:
                BROMODICL = models.ParametroEspecifico.objects.get(codigo='AFI-BROMODICL-SM')
                DIBROMOCL = models.ParametroEspecifico.objects.get(codigo='AFI-DIBROMOCL-SM')
                TRIBROM = models.ParametroEspecifico.objects.get(codigo='AFI-TRIBROM-SM')
                TRICLOR = models.ParametroEspecifico.objects.get(codigo='AFI-TRICLOR-SM')
                if BROMODICL.codigo_etfa=='nan' or BROMODICL.codigo_etfa==None or DIBROMOCL.codigo_etfa=='nan' or DIBROMOCL.codigo_etfa==None or TRIBROM.codigo_etfa=='nan' or TRIBROM.codigo_etfa==None or TRICLOR.codigo_etfa=='nan' or TRICLOR.codigo_etfa==None:
                    parameters_f.append(p)
            
            elif 'AP-THM-ME'==parametro:
                BROMODICL = models.ParametroEspecifico.objects.get(codigo='AP-BROMODICL-ME')
                DIBROMOCL = models.ParametroEspecifico.objects.get(codigo='AP-DIBROMOCL-ME')
                TRIBROM = models.ParametroEspecifico.objects.get(codigo='AP-TRIBROM-ME')
                TRICLOR = models.ParametroEspecifico.objects.get(codigo='AP-TRICLOR-ME')
                if BROMODICL.codigo_etfa=='nan' or BROMODICL.codigo_etfa==None or DIBROMOCL.codigo_etfa=='nan' or DIBROMOCL.codigo_etfa==None or TRIBROM.codigo_etfa=='nan' or TRIBROM.codigo_etfa==None or TRICLOR.codigo_etfa=='nan' or TRICLOR.codigo_etfa==None:
                    parameters_f.append(p)
            
            elif 'AP-THM-SM'==parametro:
                BROMODICL = models.ParametroEspecifico.objects.get(codigo='AP-BROMODICL-SM')
                DIBROMOCL = models.ParametroEspecifico.objects.get(codigo='AP-DIBROMOCL-SM')
                TRIBROM = models.ParametroEspecifico.objects.get(codigo='AP-TRIBROM-SM')
                TRICLOR = models.ParametroEspecifico.objects.get(codigo='AP-TRICLOR-SM')
                if BROMODICL.codigo_etfa=='nan' or BROMODICL.codigo_etfa==None or DIBROMOCL.codigo_etfa=='nan' or DIBROMOCL.codigo_etfa==None or TRIBROM.codigo_etfa=='nan' or TRIBROM.codigo_etfa==None or TRICLOR.codigo_etfa=='nan' or TRICLOR.codigo_etfa==None:
                    parameters_f.append(p)
            
            elif 'AR-THM-SM'==parametro:
                BROMODICL_NCH = models.ParametroEspecifico.objects.get(codigo='AR-BROMODICL-NCH')
                BROMODICL_SM = models.ParametroEspecifico.objects.get(codigo='AR-BROMODICL-SM')
                DIBROMOCL_NCH = models.ParametroEspecifico.objects.get(codigo='AR-DIBROMOCL-NCH')
                DIBROMOCL_SM = models.ParametroEspecifico.objects.get(codigo='AR-DIBROMOCL-SM')
                TRIBROM_NCH = models.ParametroEspecifico.objects.get(codigo='AR-TRIBROM-NCH')
                TRIBROM_SM = models.ParametroEspecifico.objects.get(codigo='AR-TRIBROM-SM')
                TRICLOR = models.ParametroEspecifico.objects.get(codigo='AR-TRICLOR-SM')
                if BROMODICL_NCH.codigo_etfa=='nan' or BROMODICL_NCH.codigo_etfa==None or BROMODICL_SM.codigo_etfa=='nan' or BROMODICL_SM.codigo_etfa==None or DIBROMOCL_NCH.codigo_etfa=='nan' or DIBROMOCL_NCH.codigo_etfa==None or DIBROMOCL_SM.codigo_etfa=='nan' or DIBROMOCL_SM.codigo_etfa==None or TRIBROM_NCH.codigo_etfa=='nan' or TRIBROM_NCH.codigo_etfa==None or TRIBROM_SM.codigo_etfa=='nan' or TRIBROM_SM.codigo_etfa==None or TRICLOR.codigo_etfa=='nan' or TRICLOR.codigo_etfa==None:
                    parameters_f.append(p)
            
            elif 'SUB-THM-SM'==parametro:
                BROMODICL = models.ParametroEspecifico.objects.get(codigo='SUB-BROMODICL-SM')
                DIBROMOCL = models.ParametroEspecifico.objects.get(codigo='SUB-DIBROMOCL-SM')
                TRIBROM = models.ParametroEspecifico.objects.get(codigo='SUB-TRIBROM-SM')
                TRICLOR = models.ParametroEspecifico.objects.get(codigo='SUB-TRICLOR-SM')
                if BROMODICL.codigo_etfa=='nan' or BROMODICL.codigo_etfa==None or DIBROMOCL.codigo_etfa=='nan' or DIBROMOCL.codigo_etfa==None or TRIBROM.codigo_etfa=='nan' or TRIBROM.codigo_etfa==None or TRICLOR.codigo_etfa=='nan' or TRICLOR.codigo_etfa==None:
                    parameters_f.append(p)
            
            elif 'SUP-THM-SM'==parametro:
                BROMODICL = models.ParametroEspecifico.objects.get(codigo='SUP-BROMODICL-SM')
                DIBROMOCL = models.ParametroEspecifico.objects.get(codigo='SUP-DIBROMOCL-SM')
                TRIBROM = models.ParametroEspecifico.objects.get(codigo='SUP-TRIBROM-SM')
                TRICLOR = models.ParametroEspecifico.objects.get(codigo='SUP-TRICLOR-SM')
                if BROMODICL.codigo_etfa=='nan' or BROMODICL.codigo_etfa==None or DIBROMOCL.codigo_etfa=='nan' or DIBROMOCL.codigo_etfa==None or TRIBROM.codigo_etfa=='nan' or TRIBROM.codigo_etfa==None or TRICLOR.codigo_etfa=='nan' or TRICLOR.codigo_etfa==None:
                    parameters_f.append(p)
            
            elif 'FC-THM-ME'==parametro:
                BROMODICL = models.ParametroEspecifico.objects.get(codigo='FC-BROMODICL-ME')
                DIBROMOCL = models.ParametroEspecifico.objects.get(codigo='FC-DIBROMOCL-ME')
                TRIBROM = models.ParametroEspecifico.objects.get(codigo='FC-TRIBROM-ME')
                TRICLOR = models.ParametroEspecifico.objects.get(codigo='FC-TRICLOR-ME')
                if BROMODICL.codigo_etfa=='nan' or BROMODICL.codigo_etfa==None or DIBROMOCL.codigo_etfa=='nan' or DIBROMOCL.codigo_etfa==None or TRIBROM.codigo_etfa=='nan' or TRIBROM.codigo_etfa==None or TRICLOR.codigo_etfa=='nan' or TRICLOR.codigo_etfa==None:
                    parameters_f.append(p)
        
        elif 'LANGELIER' in parametro:
            if 'SUP-LANGELIER'==parametro:
                CA = models.ParametroEspecifico.objects.get(codigo='SUP-CA-ICP1')
                ALCAL = models.ParametroEspecifico.objects.get(codigo='SUP-ALCAL-T')
                DUREZA = models.ParametroEspecifico.objects.get(codigo='SUP-DUREZA-CA')
                PH = models.ParametroEspecifico.objects.get(codigo='SUP-PH-SM')                
                SDT = models.ParametroEspecifico.objects.get(codigo='SUP-SDT-GRV')
                if CA.codigo_etfa=='nan' or CA.codigo_etfa==None or ALCAL.codigo_etfa=='nan' or ALCAL.codigo_etfa==None or DUREZA.codigo_etfa=='nan' or DUREZA.codigo_etfa==None or PH.codigo_etfa=='nan' or PH.codigo_etfa==None or DUREZA.codigo_etfa==None or SDT.codigo_etfa=='nan' or SDT.codigo_etfa==None:
                    parameters_f.append(p)

            
            elif 'SUB-LANGELIER'==parametro:
                CA = models.ParametroEspecifico.objects.get(codigo='SUB-CA-ICP1')
                ALCAL = models.ParametroEspecifico.objects.get(codigo='SUB-ALCAL-T')
                DUREZA = models.ParametroEspecifico.objects.get(codigo='SUB-DUREZA-CA')
                PH = models.ParametroEspecifico.objects.get(codigo='SUB-PH-SM')
                SDT = models.ParametroEspecifico.objects.get(codigo='SUB-SDT-GRV')
                if CA.codigo_etfa=='nan' or CA.codigo_etfa==None or ALCAL.codigo_etfa=='nan' or ALCAL.codigo_etfa==None or DUREZA.codigo_etfa=='nan' or DUREZA.codigo_etfa==None or PH.codigo_etfa=='nan' or PH.codigo_etfa==None or DUREZA.codigo_etfa==None or SDT.codigo_etfa=='nan' or SDT.codigo_etfa==None:
                    parameters_f.append(p)
            
            elif 'AR-LANGELIER'==parametro:
                CA = models.ParametroEspecifico.objects.get(codigo='AR-CA-ICP1')
                ALCAL = models.ParametroEspecifico.objects.get(codigo='AR-ALCAL-T')
                DUREZA = models.ParametroEspecifico.objects.get(codigo='AR-DUREZA-CA')
                PH = models.ParametroEspecifico.objects.get(codigo='AR-PH-SM')
                PH2 = models.ParametroEspecifico.objects.get(codigo='AR-PH-NCH')
                SDT = models.ParametroEspecifico.objects.get(codigo='AR-SDT-GRV')
                if CA.codigo_etfa=='nan' or CA.codigo_etfa==None or ALCAL.codigo_etfa=='nan' or ALCAL.codigo_etfa==None or DUREZA.codigo_etfa=='nan' or DUREZA.codigo_etfa==None or PH.codigo_etfa=='nan' or PH.codigo_etfa==None or PH2.codigo_etfa=='nan' or PH2.codigo_etfa==None or DUREZA.codigo_etfa==None or SDT.codigo_etfa=='nan' or SDT.codigo_etfa==None:
                    parameters_f.append(p)


            elif 'AP-LANGELIER'==parametro:
                CA = models.ParametroEspecifico.objects.get(codigo='AP-CA-ICP1')
                ALCAL = models.ParametroEspecifico.objects.get(codigo='AP-ALCAL-T')
                DUREZA = models.ParametroEspecifico.objects.get(codigo='AP-DUREZA-CA')
                PH = models.ParametroEspecifico.objects.get(codigo='AP-PH-SM')
                SDT = models.ParametroEspecifico.objects.get(codigo='AP-SDT-GRV')
                if CA.codigo_etfa=='nan' or CA.codigo_etfa==None or ALCAL.codigo_etfa=='nan' or ALCAL.codigo_etfa==None or DUREZA.codigo_etfa=='nan' or DUREZA.codigo_etfa==None or PH.codigo_etfa=='nan' or PH.codigo_etfa==None or DUREZA.codigo_etfa==None or SDT.codigo_etfa=='nan' or SDT.codigo_etfa==None:
                    parameters_f.append(p)

            elif 'AFI-LANGELIER'==parametro:
                CA = models.ParametroEspecifico.objects.get(codigo='AFI-CA-AAS')
                ALCAL = models.ParametroEspecifico.objects.get(codigo='AFI-ALCAL-T')
                DUREZA = models.ParametroEspecifico.objects.get(codigo='AFI-DUREZA-CA')
                PH = models.ParametroEspecifico.objects.get(codigo='AFI-PH-SM')
                SDT = models.ParametroEspecifico.objects.get(codigo='AFI-SDT-GRV')
                if CA.codigo_etfa=='nan' or CA.codigo_etfa==None or ALCAL.codigo_etfa=='nan' or ALCAL.codigo_etfa==None or DUREZA.codigo_etfa=='nan' or DUREZA.codigo_etfa==None or PH.codigo_etfa=='nan' or PH.codigo_etfa==None or DUREZA.codigo_etfa==None or SDT.codigo_etfa=='nan' or SDT.codigo_etfa==None:
                    parameters_f.append(p)

        elif 'NT' in parametro:
            if 'AFI-NT'==parametro:
                NO3 = models.ParametroEspecifico.objects.get(codigo='AFI-NO3-CI')
                NO2 = models.ParametroEspecifico.objects.get(codigo='AFI-NO2-CI')
                NKT = models.ParametroEspecifico.objects.get(codigo='AFI-NKT')  
                if NO3.codigo_etfa=='nan' or NO3.codigo_etfa==None or NO2.codigo_etfa=='nan' or NO2.codigo_etfa==None or NKT.codigo_etfa=='nan' or NKT.codigo_etfa==None:
                    parameters_f.append(p)
            
            elif 'AP-NT'==parametro:
                NO3 = models.ParametroEspecifico.objects.get(codigo='AP-NO3-CI')
                NO2 = models.ParametroEspecifico.objects.get(codigo='AP-NO2-CI')
                NKT = models.ParametroEspecifico.objects.get(codigo='AP-NKT')                       
                if NO3.codigo_etfa=='nan' or NO3.codigo_etfa==None or NO2.codigo_etfa=='nan' or NO2.codigo_etfa==None or NKT.codigo_etfa=='nan' or NKT.codigo_etfa==None:
                    parameters_f.append(p)
            
            elif 'AR-NT'==parametro:
                NO3 = models.ParametroEspecifico.objects.get(codigo='AR-NO3-CI')
                NO2 = models.ParametroEspecifico.objects.get(codigo='AR-NO2-CI')
                NKT = models.ParametroEspecifico.objects.get(codigo='AR-NKT-SM')                       
                if NO3.codigo_etfa=='nan' or NO3.codigo_etfa==None or NO2.codigo_etfa=='nan' or NO2.codigo_etfa==None or NKT.codigo_etfa=='nan' or NKT.codigo_etfa==None:
                    parameters_f.append(p)
            
            elif 'SUB-NT'==parametro:
                NO3 = models.ParametroEspecifico.objects.get(codigo='SUB-NO3-CI')
                NO2 = models.ParametroEspecifico.objects.get(codigo='SUB-NO2-CI')
                NKT = models.ParametroEspecifico.objects.get(codigo='SUB-NKT')                       
                if NO3.codigo_etfa=='nan' or NO3.codigo_etfa==None or NO2.codigo_etfa=='nan' or NO2.codigo_etfa==None or NKT.codigo_etfa=='nan' or NKT.codigo_etfa==None:
                    parameters_f.append(p)

            elif 'SUP-NT'==parametro:
                NO3 = models.ParametroEspecifico.objects.get(codigo='SUP-NO3-CI')
                NO2 = models.ParametroEspecifico.objects.get(codigo='SUP-NO2-CI')
                NKT = models.ParametroEspecifico.objects.get(codigo='SUP-NKT')                       
                if NO3.codigo_etfa=='nan' or NO3.codigo_etfa==None or NO2.codigo_etfa=='nan' or NO2.codigo_etfa==None or NKT.codigo_etfa=='nan' or NKT.codigo_etfa==None:
                    parameters_f.append(p)

            elif 'S-NT'==parametro:
                NO3 = models.ParametroEspecifico.objects.get(codigo='S-NO3-CI')
                NO2 = models.ParametroEspecifico.objects.get(codigo='S-NO2-CI')
                NKT = models.ParametroEspecifico.objects.get(codigo='S-NKT')                       
                if NO3.codigo_etfa=='nan' or NO3.codigo_etfa==None or NO2.codigo_etfa=='nan' or NO2.codigo_etfa==None or NKT.codigo_etfa=='nan' or NKT.codigo_etfa==None:
                    parameters_f.append(p)

            elif 'L-NT'==parametro:
                NO3 = models.ParametroEspecifico.objects.get(codigo='L-NO3-CI')
                NO2 = models.ParametroEspecifico.objects.get(codigo='L-NO2-CI')
                NKT = models.ParametroEspecifico.objects.get(codigo='L-NKT')                       
                if NO3.codigo_etfa=='nan' or NO3.codigo_etfa==None or NO2.codigo_etfa=='nan' or NO2.codigo_etfa==None or NKT.codigo_etfa=='nan' or NKT.codigo_etfa==None:
                    parameters_f.append(p)

            elif 'SD-NT'==parametro:
                NO3 = models.ParametroEspecifico.objects.get(codigo='SD-NO3-CI')
                NO2 = models.ParametroEspecifico.objects.get(codigo='SD-NO2-CI')
                NKT = models.ParametroEspecifico.objects.get(codigo='SD-NKT')                       
                if NO3.codigo_etfa=='nan' or NO3.codigo_etfa==None or NO2.codigo_etfa=='nan' or NO2.codigo_etfa==None or NKT.codigo_etfa=='nan' or NKT.codigo_etfa==None:
                    parameters_f.append(p)
        
        elif 'RAS' in parametro:
            if 'AP-RAS'==parametro:
                CA = models.ParametroEspecifico.objects.get(codigo='AP-CA-ICP1')
                MG = models.ParametroEspecifico.objects.get(codigo='AP-MG-ICP1')
                NA = models.ParametroEspecifico.objects.get(codigo='AP-NA-ICP1')                       
                if CA.codigo_etfa=='nan' or CA.codigo_etfa==None or MG.codigo_etfa=='nan' or MG.codigo_etfa==None or NA.codigo_etfa=='nan' or NA.codigo_etfa==None:
                    parameters_f.append(p)

            elif 'AR-RAS'==parametro:
                CA = models.ParametroEspecifico.objects.get(codigo='AR-CA-ICP1')
                MG = models.ParametroEspecifico.objects.get(codigo='AR-MG-ICP1')
                NA = models.ParametroEspecifico.objects.get(codigo='AR-NA-ICP1')                       
                if CA.codigo_etfa=='nan' or CA.codigo_etfa==None or MG.codigo_etfa=='nan' or MG.codigo_etfa==None or NA.codigo_etfa=='nan' or NA.codigo_etfa==None:
                    parameters_f.append(p)

            elif 'SUB-RAS'==parametro:
                CA = models.ParametroEspecifico.objects.get(codigo='SUB-CA-ICP1')
                MG = models.ParametroEspecifico.objects.get(codigo='SUB-MG-ICP1')
                NA = models.ParametroEspecifico.objects.get(codigo='SUB-NA-ICP1')                       
                if CA.codigo_etfa=='nan' or CA.codigo_etfa==None or MG.codigo_etfa=='nan' or MG.codigo_etfa==None or NA.codigo_etfa=='nan' or NA.codigo_etfa==None:
                    parameters_f.append(p)

            elif 'SUP-RAS'==parametro:
                CA = models.ParametroEspecifico.objects.get(codigo='SUP-CA-ICP1')
                MG = models.ParametroEspecifico.objects.get(codigo='SUP-MG-ICP1')
                NA = models.ParametroEspecifico.objects.get(codigo='SUP-NA-ICP1')                       
                if CA.codigo_etfa=='nan' or CA.codigo_etfa==None or MG.codigo_etfa=='nan' or MG.codigo_etfa==None or NA.codigo_etfa=='nan' or NA.codigo_etfa==None:
                    parameters_f.append(p)

        elif 'NA100' in parametro:
            if 'AP-NA100'==parametro:
                CA = models.ParametroEspecifico.objects.get(codigo='AP-CA-ICP1')
                MG = models.ParametroEspecifico.objects.get(codigo='AP-MG-ICP1')
                NA = models.ParametroEspecifico.objects.get(codigo='AP-NA-ICP1')
                K = models.ParametroEspecifico.objects.get(codigo='AP-K-ICP1')                       
                if CA.codigo_etfa=='nan' or CA.codigo_etfa==None or MG.codigo_etfa=='nan' or MG.codigo_etfa==None or NA.codigo_etfa=='nan' or NA.codigo_etfa==None or K.codigo_etfa=='nan' or K.codigo_etfa==None:
                    parameters_f.append(p)

            elif 'AR-NA100'==parametro:
                CA = models.ParametroEspecifico.objects.get(codigo='AR-CA-ICP1')
                MG = models.ParametroEspecifico.objects.get(codigo='AR-MG-ICP1')
                NA = models.ParametroEspecifico.objects.get(codigo='AR-NA-ICP1') 
                K = models.ParametroEspecifico.objects.get(codigo='AR-K-ICP1')                      
                if CA.codigo_etfa=='nan' or CA.codigo_etfa==None or MG.codigo_etfa=='nan' or MG.codigo_etfa==None or NA.codigo_etfa=='nan' or NA.codigo_etfa==None or K.codigo_etfa=='nan' or K.codigo_etfa==None:
                    parameters_f.append(p)

            elif 'SUB-NA100'==parametro:
                CA = models.ParametroEspecifico.objects.get(codigo='SUB-CA-ICP1')
                MG = models.ParametroEspecifico.objects.get(codigo='SUB-MG-ICP1')
                NA = models.ParametroEspecifico.objects.get(codigo='SUB-NA-ICP1')
                K = models.ParametroEspecifico.objects.get(codigo='SUB-K-ICP1')                       
                if CA.codigo_etfa=='nan' or CA.codigo_etfa==None or MG.codigo_etfa=='nan' or MG.codigo_etfa==None or NA.codigo_etfa=='nan' or NA.codigo_etfa==None or K.codigo_etfa=='nan' or K.codigo_etfa==None:
                    parameters_f.append(p)

            elif 'SUP-NA100'==parametro:
                CA = models.ParametroEspecifico.objects.get(codigo='SUP-CA-ICP1')
                MG = models.ParametroEspecifico.objects.get(codigo='SUP-MG-ICP1')
                NA = models.ParametroEspecifico.objects.get(codigo='SUP-NA-ICP1') 
                K = models.ParametroEspecifico.objects.get(codigo='SUP-K-ICP1')                      
                if CA.codigo_etfa=='nan' or CA.codigo_etfa==None or MG.codigo_etfa=='nan' or MG.codigo_etfa==None or NA.codigo_etfa=='nan' or NA.codigo_etfa==None or K.codigo_etfa=='nan' or K.codigo_etfa==None:
                    parameters_f.append(p)

        elif 'DUREZA-T' in parametro:
            if 'AFI-DUREZA-T'==parametro:
                CA = models.ParametroEspecifico.objects.get(codigo='AFI-CA-AAS')
                DCA = models.ParametroEspecifico.objects.get(codigo='AFI-DUREZA-CA')
                MG = models.ParametroEspecifico.objects.get(codigo='AFI-MG-AAS')
                DMG = models.ParametroEspecifico.objects.get(codigo='AFI-DUREZA-MG')                      
                if CA.codigo_etfa=='nan' or CA.codigo_etfa==None or MG.codigo_etfa=='nan' or MG.codigo_etfa==None or DCA.codigo_etfa=='nan' or DCA.codigo_etfa==None or DMG.codigo_etfa=='nan' or DMG.codigo_etfa==None:
                    parameters_f.append(p)
            
            elif 'AP-DUREZA-T'==parametro:
                CA = models.ParametroEspecifico.objects.get(codigo='AP-CA-ICP1')
                DCA = models.ParametroEspecifico.objects.get(codigo='AP-DUREZA-CA')
                MG = models.ParametroEspecifico.objects.get(codigo='AP-MG-ICP1')
                DMG = models.ParametroEspecifico.objects.get(codigo='AP-DUREZA-MG')                      
                if CA.codigo_etfa=='nan' or CA.codigo_etfa==None or MG.codigo_etfa=='nan' or MG.codigo_etfa==None or DCA.codigo_etfa=='nan' or DCA.codigo_etfa==None or DMG.codigo_etfa=='nan' or DMG.codigo_etfa==None:
                    parameters_f.append(p)

            elif 'AR-DUREZA-T'==parametro:
                CA = models.ParametroEspecifico.objects.get(codigo='AR-CA-ICP1')
                DCA = models.ParametroEspecifico.objects.get(codigo='AR-DUREZA-CA')
                MG = models.ParametroEspecifico.objects.get(codigo='AR-MG-ICP1')
                DMG = models.ParametroEspecifico.objects.get(codigo='AR-DUREZA-MG')                      
                if CA.codigo_etfa=='nan' or CA.codigo_etfa==None or MG.codigo_etfa=='nan' or MG.codigo_etfa==None or DCA.codigo_etfa=='nan' or DCA.codigo_etfa==None or DMG.codigo_etfa=='nan' or DMG.codigo_etfa==None:
                    parameters_f.append(p)
            
            elif 'SUB-DUREZA-T'==parametro:
                CA = models.ParametroEspecifico.objects.get(codigo='SUB-CA-ICP1')
                DCA = models.ParametroEspecifico.objects.get(codigo='SUB-DUREZA-CA')
                MG = models.ParametroEspecifico.objects.get(codigo='SUB-MG-ICP1')
                DMG = models.ParametroEspecifico.objects.get(codigo='SUB-DUREZA-MG')                      
                if CA.codigo_etfa=='nan' or CA.codigo_etfa==None or MG.codigo_etfa=='nan' or MG.codigo_etfa==None or DCA.codigo_etfa=='nan' or DCA.codigo_etfa==None or DMG.codigo_etfa=='nan' or DMG.codigo_etfa==None:
                    parameters_f.append(p)

            elif 'SUP-DUREZA-T'==parametro:
                CA = models.ParametroEspecifico.objects.get(codigo='SUP-CA-ICP1')
                DCA = models.ParametroEspecifico.objects.get(codigo='SUP-DUREZA-CA')
                MG = models.ParametroEspecifico.objects.get(codigo='SUP-MG-ICP1')
                DMG = models.ParametroEspecifico.objects.get(codigo='SUP-DUREZA-MG')                      
                if CA.codigo_etfa=='nan' or CA.codigo_etfa==None or MG.codigo_etfa=='nan' or MG.codigo_etfa==None or DCA.codigo_etfa=='nan' or DCA.codigo_etfa==None or DMG.codigo_etfa=='nan' or DMG.codigo_etfa==None:
                    parameters_f.append(p)
    
    return parameters_f


def calc_param_etfa(parameters, parameters_analisis_externos):

    """Esta función es para completar parametros faltantes en los servicio ETFA"""
    
    def anex_param(p):
        """Esta función es para agregar a la lista parameters los parametros que no se encuentren en esta ni en la lista de parametros de analisis externos"""
        if p not in parameters and p not in parameters_analisis_externos:
            parameters.append(p)
        return parameters
    
    def anex_param_ext(p):
        """Esta función es para agregar a la lista parameters de analisis externos los parametros que no se encuentren en esta ni en la lista de parametros"""
        if p not in parameters and p not in parameters_analisis_externos:
            parameters_analisis_externos.append(p)
        return parameters_analisis_externos
    
    def anex_param2(p, p2):
        """Esta función es para agregar a la lista parameters los parametros que no se encuentren en esta ni en la lista de parametros de analisis externos"""
        if p not in parameters and p2 not in parameters and p not in parameters_analisis_externos and p2 not in parameters_analisis_externos:
                    parameters.append(p)
    for p in parameters:
        parametro = models.ParametroEspecifico.objects.get(pk= p).codigo
        if 'HCT' in parametro:
            if 'AFI-HCT'==parametro:
                HCF = models.ParametroEspecifico.objects.get(codigo='AFI-HCF-GRV')
                HCV = models.ParametroEspecifico.objects.get(codigo='AFI-HCV')
                if HCF.codigo_etfa!='nan' and HCF.codigo_etfa!=None:
                    anex_param(str(HCF.id))
                else: anex_param_ext(str(HCF.id))
                if HCV.codigo_etfa!='nan' and HCV.codigo_etfa!=None:
                    anex_param(str(HCV.id))
                else: anex_param_ext(str(HCV.id))
                
            
            elif 'AP-HCT'==parametro:
                HCF = models.ParametroEspecifico.objects.get(codigo='AP-HCF-GRV')
                HCV = models.ParametroEspecifico.objects.get(codigo='AP-HCV')
                if HCF.codigo_etfa!='nan' and HCF.codigo_etfa!=None:
                    anex_param(str(HCF.id))
                else: anex_param_ext(str(HCF.id))
                if HCV.codigo_etfa!='nan' and HCV.codigo_etfa!=None:
                    anex_param(str(HCV.id))
                else: anex_param_ext(str(HCV.id))
            
            elif 'AR-HCT' == parametro:
                HCF2 = str(models.ParametroEspecifico.objects.get(codigo='AR-HCF-NCH-GRV').id)
                HCF = str(models.ParametroEspecifico.objects.get(codigo='AR-HCF-GRV').id)
                HCV = models.ParametroEspecifico.objects.get(codigo='AR-HCV')
                anex_param2(p=HCF, p2=HCF2)
                if HCV.codigo_etfa!='nan' and HCV.codigo_etfa!=None:
                    anex_param(str(HCV.id))
                else: anex_param_ext(str(HCV.id))
            
            elif 'SUB-HCT' == parametro:
                HCF = models.ParametroEspecifico.objects.get(codigo='SUB-HCF-GRV')
                HCV = models.ParametroEspecifico.objects.get(codigo='SUB-HCV')
                if HCF.codigo_etfa!='nan' and HCF.codigo_etfa!=None:
                    anex_param(str(HCF.id))
                else: anex_param_ext(str(HCF.id))
                if HCV.codigo_etfa!='nan' and HCV.codigo_etfa!=None:
                    anex_param(str(HCV.id))
                else: anex_param_ext(str(HCV.id))
            
            elif 'SUP-HCT' == parametro:
                HCF = models.ParametroEspecifico.objects.get(codigo='SUP-HCF-GRV')
                HCV = models.ParametroEspecifico.objects.get(codigo='SUP-HCV')
                if HCF.codigo_etfa!='nan' and HCF.codigo_etfa!=None:
                    anex_param(str(HCF.id))
                else: anex_param_ext(str(HCF.id))
                if HCV.codigo_etfa!='nan' and HCV.codigo_etfa!=None:
                    anex_param(str(HCV.id))
                else: 
                    anex_param_ext(str(HCV.id))                
            
            elif 'L-HCT' == parametro:
                HCF = models.ParametroEspecifico.objects.get(codigo='L-HCF-GRV')
                HCV = models.ParametroEspecifico.objects.get(codigo='L-HCV')
                if HCF.codigo_etfa!='nan' and HCF.codigo_etfa!=None:
                    anex_param(str(HCF.id))
                else: anex_param_ext(str(HCF.id))
                if HCV.codigo_etfa!='nan' and HCV.codigo_etfa!=None:
                    anex_param(str(HCV.id))
                else: anex_param_ext(str(HCV.id))
            
            elif 'SD-HCT' == parametro:
                HCF = models.ParametroEspecifico.objects.get(codigo='SD-HCF-GRV')
                HCV = models.ParametroEspecifico.objects.get(codigo='SD-HCV')
                if HCF.codigo_etfa!='nan' and HCF.codigo_etfa!=None:
                    anex_param(str(HCF.id))
                else: anex_param_ext(str(HCF.id))
                if HCV.codigo_etfa!='nan' and HCV.codigo_etfa!=None:
                    anex_param(str(HCV.id))
                else: anex_param_ext(str(HCV.id))
            
            elif 'S-HCT' == parametro:
                HCF = models.ParametroEspecifico.objects.get(codigo='S-HCF-GRV')
                HCV = models.ParametroEspecifico.objects.get(codigo='S-HCV')
                if HCF.codigo_etfa!='nan' and HCF.codigo_etfa!=None:
                    anex_param(str(HCF.id))
                else: anex_param_ext(str(HCF.id))
                if HCV.codigo_etfa!='nan' and HCV.codigo_etfa!=None:
                    anex_param(str(HCV.id))
                else: anex_param_ext(str(HCV.id))
        
        elif 'DDD+DDE+DDT' in parametro:
            if 'AP-DDD+DDE+DDT'==parametro:
                DDD = models.ParametroEspecifico.objects.get(codigo='AP-DDD-ME')
                DDE = models.ParametroEspecifico.objects.get(codigo='AP-DDE-ME')
                DDT = models.ParametroEspecifico.objects.get(codigo='AP-DDT-ME')
                if DDD.codigo_etfa!='nan' and DDD.codigo_etfa!=None:
                    anex_param(str(DDD.id))
                else: anex_param_ext(str(DDD.id))
                if DDE.codigo_etfa!='nan' and DDE.codigo_etfa!=None:
                    anex_param(str(DDE.id))
                else: anex_param_ext(str(DDE.id))
                if DDT.codigo_etfa!='nan' and DDT.codigo_etfa!=None:
                    anex_param(str(DDT.id))
                else: anex_param_ext(str(DDT.id))
            
            elif 'FC-DDD+DDE+DDT'==parametro:
                DDD = models.ParametroEspecifico.objects.get(codigo='FC-DDD-ME')
                DDE = models.ParametroEspecifico.objects.get(codigo='FC-DDE-ME')
                DDT = models.ParametroEspecifico.objects.get(codigo='FC-DDT-ME')
                if DDD.codigo_etfa!='nan' and DDD.codigo_etfa!=None:
                    anex_param(str(DDD.id))
                else: anex_param_ext(str(DDD.id))
                if DDE.codigo_etfa!='nan' and DDE.codigo_etfa!=None:
                    anex_param(str(DDE.id))
                else: anex_param_ext(str(DDE.id))
                if DDT.codigo_etfa!='nan' and DDT.codigo_etfa!=None:
                    anex_param(str(DDT.id))
                else: anex_param_ext(str(DDT.id))
            
        elif 'THM' in parametro:
            if 'AFI-THM-SM'==parametro:
                BROMODICL = models.ParametroEspecifico.objects.get(codigo='AFI-BROMODICL-SM')
                DIBROMOCL = models.ParametroEspecifico.objects.get(codigo='AFI-DIBROMOCL-SM')
                TRIBROM = models.ParametroEspecifico.objects.get(codigo='AFI-TRIBROM-SM')
                TRICLOR = models.ParametroEspecifico.objects.get(codigo='AFI-TRICLOR-SM')
                if BROMODICL.codigo_etfa!='nan' and BROMODICL.codigo_etfa!=None:
                    anex_param(str(BROMODICL.id))
                else: anex_param_ext(str(BROMODICL.id))
                if DIBROMOCL.codigo_etfa!='nan' and DIBROMOCL.codigo_etfa!=None:
                    anex_param(str(DIBROMOCL.id))
                else: anex_param_ext(str(DIBROMOCL.id))
                if TRIBROM.codigo_etfa!='nan' and TRIBROM.codigo_etfa!=None:
                    anex_param(str(TRIBROM.id))
                else: anex_param_ext(str(TRIBROM.id))
                if TRICLOR.codigo_etfa!='nan' and TRICLOR.codigo_etfa!=None:
                    anex_param(str(TRICLOR.id))
                else: anex_param_ext(str(TRICLOR.id))
            
            elif 'AP-THM-ME'==parametro:
                BROMODICL = models.ParametroEspecifico.objects.get(codigo='AP-BROMODICL-ME')
                DIBROMOCL = models.ParametroEspecifico.objects.get(codigo='AP-DIBROMOCL-ME')
                TRIBROM = models.ParametroEspecifico.objects.get(codigo='AP-TRIBROM-ME')
                TRICLOR = models.ParametroEspecifico.objects.get(codigo='AP-TRICLOR-ME')
                if BROMODICL.codigo_etfa!='nan' and BROMODICL.codigo_etfa!=None:
                    anex_param(str(BROMODICL.id))
                else: anex_param_ext(str(BROMODICL.id))
                if DIBROMOCL.codigo_etfa!='nan' and DIBROMOCL.codigo_etfa!=None:
                    anex_param(str(DIBROMOCL.id))
                else: anex_param_ext(str(DIBROMOCL.id))
                if TRIBROM.codigo_etfa!='nan' and TRIBROM.codigo_etfa!=None:
                    anex_param(str(TRIBROM.id))
                else: anex_param_ext(str(TRIBROM.id))
                if TRICLOR.codigo_etfa!='nan' and TRICLOR.codigo_etfa!=None:
                    anex_param(str(TRICLOR.id))
                else: anex_param_ext(str(TRICLOR.id))
            
            elif 'AP-THM-SM'==parametro:
                BROMODICL = models.ParametroEspecifico.objects.get(codigo='AP-BROMODICL-SM')
                DIBROMOCL = models.ParametroEspecifico.objects.get(codigo='AP-DIBROMOCL-SM')
                TRIBROM = models.ParametroEspecifico.objects.get(codigo='AP-TRIBROM-SM')
                TRICLOR = models.ParametroEspecifico.objects.get(codigo='AP-TRICLOR-SM')
                if BROMODICL.codigo_etfa!='nan' and BROMODICL.codigo_etfa!=None:
                    anex_param(str(BROMODICL.id))
                else: anex_param_ext(str(BROMODICL.id))
                if DIBROMOCL.codigo_etfa!='nan' and DIBROMOCL.codigo_etfa!=None:
                    anex_param(str(DIBROMOCL.id))
                else: anex_param_ext(str(DIBROMOCL.id))
                if TRIBROM.codigo_etfa!='nan' and TRIBROM.codigo_etfa!=None:
                    anex_param(str(TRIBROM.id))
                else: anex_param_ext(str(TRIBROM.id))
                if TRICLOR.codigo_etfa!='nan' and TRICLOR.codigo_etfa!=None:
                    anex_param(str(TRICLOR.id))
                else: anex_param_ext(str(TRICLOR.id))
            
            elif 'AR-THM-SM'==parametro:
                BROMODICL_NCH = str(models.ParametroEspecifico.objects.get(codigo='AR-BROMODICL-NCH').id)
                BROMODICL_SM = str(models.ParametroEspecifico.objects.get(codigo='AR-BROMODICL-SM').id)
                DIBROMOCL_NCH = str(models.ParametroEspecifico.objects.get(codigo='AR-DIBROMOCL-NCH').id)
                DIBROMOCL_SM = str(models.ParametroEspecifico.objects.get(codigo='AR-DIBROMOCL-SM').id)
                TRIBROM_NCH = str(models.ParametroEspecifico.objects.get(codigo='AR-TRIBROM-NCH').id)
                TRIBROM_SM = str(models.ParametroEspecifico.objects.get(codigo='AR-TRIBROM-SM').id)
                TRICLOR = models.ParametroEspecifico.objects.get(codigo='AR-TRICLOR-SM')
                anex_param2(p=BROMODICL_SM, p2=BROMODICL_NCH)
                anex_param(p=DIBROMOCL_SM, p2=DIBROMOCL_NCH)
                anex_param(p=TRIBROM_SM, p2=TRIBROM_NCH)
                if TRICLOR.codigo_etfa!='nan' and TRICLOR.codigo_etfa!=None:
                    anex_param(str(TRICLOR.id))
                else: anex_param_ext(str(TRICLOR.id))
            
            elif 'SUB-THM-SM'==parametro:
                BROMODICL = models.ParametroEspecifico.objects.get(codigo='SUB-BROMODICL-SM')
                DIBROMOCL = models.ParametroEspecifico.objects.get(codigo='SUB-DIBROMOCL-SM')
                TRIBROM = models.ParametroEspecifico.objects.get(codigo='SUB-TRIBROM-SM')
                TRICLOR = models.ParametroEspecifico.objects.get(codigo='SUB-TRICLOR-SM')
                if BROMODICL.codigo_etfa!='nan' and BROMODICL.codigo_etfa!=None:
                    anex_param(str(BROMODICL.id))
                else: anex_param_ext(str(BROMODICL.id))
                if DIBROMOCL.codigo_etfa!='nan' and DIBROMOCL.codigo_etfa!=None:
                    anex_param(str(DIBROMOCL.id))
                else: anex_param_ext(str(DIBROMOCL.id))
                if TRIBROM.codigo_etfa!='nan' and TRIBROM.codigo_etfa!=None:
                    anex_param(str(TRIBROM.id))
                else: anex_param_ext(str(TRIBROM.id))
                if TRICLOR.codigo_etfa!='nan' and TRICLOR.codigo_etfa!=None:
                    anex_param(str(TRICLOR.id))
                else: anex_param_ext(str(TRICLOR.id))
            
            elif 'SUP-THM-SM'==parametro:
                BROMODICL = models.ParametroEspecifico.objects.get(codigo='SUP-BROMODICL-SM')
                DIBROMOCL = models.ParametroEspecifico.objects.get(codigo='SUP-DIBROMOCL-SM')
                TRIBROM = models.ParametroEspecifico.objects.get(codigo='SUP-TRIBROM-SM')
                TRICLOR = models.ParametroEspecifico.objects.get(codigo='SUP-TRICLOR-SM')
                if BROMODICL.codigo_etfa!='nan' and BROMODICL.codigo_etfa!=None:
                    anex_param(str(BROMODICL.id))
                else: anex_param_ext(str(BROMODICL.id))
                if DIBROMOCL.codigo_etfa!='nan' and DIBROMOCL.codigo_etfa!=None:
                    anex_param(str(DIBROMOCL.id))
                else: anex_param_ext(str(DIBROMOCL.id))
                if TRIBROM.codigo_etfa!='nan' and TRIBROM.codigo_etfa!=None:
                    anex_param(str(TRIBROM.id))
                else: anex_param_ext(str(TRIBROM.id))
                if TRICLOR.codigo_etfa!='nan' and TRICLOR.codigo_etfa!=None:
                    anex_param(str(TRICLOR.id))
                else: anex_param_ext(str(TRICLOR.id))
            
            elif 'FC-THM-ME'==parametro:
                BROMODICL = models.ParametroEspecifico.objects.get(codigo='FC-BROMODICL-ME')
                DIBROMOCL = models.ParametroEspecifico.objects.get(codigo='FC-DIBROMOCL-ME')
                TRIBROM = models.ParametroEspecifico.objects.get(codigo='FC-TRIBROM-ME')
                TRICLOR = models.ParametroEspecifico.objects.get(codigo='FC-TRICLOR-ME')
                if BROMODICL.codigo_etfa!='nan' and BROMODICL.codigo_etfa!=None:
                    anex_param(str(BROMODICL.id))
                else: anex_param_ext(str(BROMODICL.id))
                if DIBROMOCL.codigo_etfa!='nan' and DIBROMOCL.codigo_etfa!=None:
                    anex_param(str(DIBROMOCL.id))
                else: anex_param_ext(str(DIBROMOCL.id))
                if TRIBROM.codigo_etfa!='nan' and TRIBROM.codigo_etfa!=None:
                    anex_param(str(TRIBROM.id))
                else: anex_param_ext(str(TRIBROM.id))
                if TRICLOR.codigo_etfa!='nan' and TRICLOR.codigo_etfa!=None:
                    anex_param(str(TRICLOR.id))
                else: anex_param_ext(str(TRICLOR.id))
        
        elif 'LANGELIER' in parametro:
            if 'SUP-LANGELIER'==parametro:
                CA = models.ParametroEspecifico.objects.get(codigo='SUP-CA-ICP1')
                ALCAL = models.ParametroEspecifico.objects.get(codigo='SUP-ALCAL-T')
                DUREZA = models.ParametroEspecifico.objects.get(codigo='SUP-DUREZA-CA')
                PH = models.ParametroEspecifico.objects.get(codigo='SUP-PH-SM')                
                SDT = models.ParametroEspecifico.objects.get(codigo='SUP-SDT-GRV')
                
                if CA.codigo_etfa!='nan' and CA.codigo_etfa!=None:
                    anex_param(str(CA.id))
                else: anex_param_ext(str(CA.id))
                if ALCAL.codigo_etfa!='nan' and ALCAL.codigo_etfa!=None:
                    anex_param(str(ALCAL.id))
                else: anex_param_ext(str(ALCAL.id))
                if DUREZA.codigo_etfa!='nan' and DUREZA.codigo_etfa!=None:
                    anex_param(str(DUREZA.id))
                else: anex_param_ext(str(DUREZA.id))
                if PH.codigo_etfa!='nan' and PH.codigo_etfa!=None:
                    anex_param(str(PH.id))
                else: anex_param_ext(str(PH.id))
                if SDT.codigo_etfa!='nan' and SDT.codigo_etfa!=None:
                    anex_param(str(SDT.id))
                else: anex_param_ext(str(SDT.id))

            
            elif 'SUB-LANGELIER'==parametro:
                CA = models.ParametroEspecifico.objects.get(codigo='SUB-CA-ICP1')
                ALCAL = models.ParametroEspecifico.objects.get(codigo='SUB-ALCAL-T')
                DUREZA = models.ParametroEspecifico.objects.get(codigo='SUB-DUREZA-CA')
                PH = models.ParametroEspecifico.objects.get(codigo='SUB-PH-SM')
                SDT = models.ParametroEspecifico.objects.get(codigo='SUB-SDT-GRV')
                if CA.codigo_etfa!='nan' and CA.codigo_etfa!=None:
                    anex_param(str(CA.id))
                else: anex_param_ext(str(CA.id))
                if ALCAL.codigo_etfa!='nan' and ALCAL.codigo_etfa!=None:
                    anex_param(str(ALCAL.id))
                else: anex_param_ext(str(ALCAL.id))
                if DUREZA.codigo_etfa!='nan' and DUREZA.codigo_etfa!=None:
                    anex_param(str(DUREZA.id))
                else: anex_param_ext(str(DUREZA.id))
                if PH.codigo_etfa!='nan' and PH.codigo_etfa!=None:
                    anex_param(str(PH.id))
                else: anex_param_ext(str(PH.id))
                if SDT.codigo_etfa!='nan' and SDT.codigo_etfa!=None:
                    anex_param(str(SDT.id))
                else: anex_param_ext(str(SDT.id))
            
            elif 'AR-LANGELIER'==parametro:
                CA = models.ParametroEspecifico.objects.get(codigo='AR-CA-ICP1')
                ALCAL = models.ParametroEspecifico.objects.get(codigo='AR-ALCAL-T')
                DUREZA = models.ParametroEspecifico.objects.get(codigo='AR-DUREZA-CA')
                PH = str(models.ParametroEspecifico.objects.get(codigo='AR-PH-SM').id)
                PH2 = str(models.ParametroEspecifico.objects.get(codigo='AR-PH-NCH').id)
                SDT = models.ParametroEspecifico.objects.get(codigo='AR-SDT-GRV')
                if CA.codigo_etfa!='nan' and CA.codigo_etfa!=None:
                    anex_param(str(CA.id))
                else: anex_param_ext(str(CA.id))
                if ALCAL.codigo_etfa!='nan' and ALCAL.codigo_etfa!=None:
                    anex_param(str(ALCAL.id))
                else: anex_param_ext(str(ALCAL.id))
                if DUREZA.codigo_etfa!='nan' and DUREZA.codigo_etfa!=None:
                    anex_param(str(DUREZA.id))
                else: anex_param_ext(str(DUREZA.id))
                if SDT.codigo_etfa!='nan' and SDT.codigo_etfa!=None:
                    anex_param(str(SDT.id))
                else: anex_param_ext(str(SDT.id))
                anex_param2(p=PH, p2=PH2)


            elif 'AP-LANGELIER'==parametro:
                CA = models.ParametroEspecifico.objects.get(codigo='AP-CA-ICP1')
                ALCAL = models.ParametroEspecifico.objects.get(codigo='AP-ALCAL-T')
                DUREZA = models.ParametroEspecifico.objects.get(codigo='AP-DUREZA-CA')
                PH = str(models.ParametroEspecifico.objects.get(codigo='AP-PH-SM').id)
                PH2 = str(models.ParametroEspecifico.objects.get(codigo='AP-PH-ME').id)
                SDT = str(models.ParametroEspecifico.objects.get(codigo='AP-SDT-GRV').id)
                SDT2 = str(models.ParametroEspecifico.objects.get(codigo='AP-SDT-ME-GRV').id)
                if CA.codigo_etfa!='nan' and CA.codigo_etfa!=None:
                    anex_param(str(CA.id))
                else: anex_param_ext(str(CA.id))
                if ALCAL.codigo_etfa!='nan' and ALCAL.codigo_etfa!=None:
                    anex_param(str(ALCAL.id))
                else: anex_param_ext(str(ALCAL.id))
                if DUREZA.codigo_etfa!='nan' and DUREZA.codigo_etfa!=None:
                    anex_param(str(DUREZA.id))
                else: anex_param_ext(str(DUREZA.id))
                anex_param2(p=PH, p2=PH2)
                anex_param2(p=SDT, p2=SDT2)

            elif 'AFI-LANGELIER'==parametro:
                CA = models.ParametroEspecifico.objects.get(codigo='AFI-CA-AAS')
                ALCAL = models.ParametroEspecifico.objects.get(codigo='AFI-ALCAL-T')
                DUREZA = models.ParametroEspecifico.objects.get(codigo='AFI-DUREZA-CA')
                PH = models.ParametroEspecifico.objects.get(codigo='AFI-PH-SM')
                SDT = models.ParametroEspecifico.objects.get(codigo='AFI-SDT-GRV')
                if CA.codigo_etfa!='nan' and CA.codigo_etfa!=None:
                    anex_param(str(CA.id))
                else: anex_param_ext(str(CA.id))
                if ALCAL.codigo_etfa!='nan' and ALCAL.codigo_etfa!=None:
                    anex_param(str(ALCAL.id))
                else: anex_param_ext(str(ALCAL.id))
                if DUREZA.codigo_etfa!='nan' and DUREZA.codigo_etfa!=None:
                    anex_param(str(DUREZA.id))
                else: anex_param_ext(str(DUREZA.id))
                if PH.codigo_etfa!='nan' and PH.codigo_etfa!=None:
                    anex_param(str(PH.id))
                else: anex_param_ext(str(PH.id))
                if SDT.codigo_etfa!='nan' and SDT.codigo_etfa!=None:
                    anex_param(str(SDT.id))
                else: anex_param_ext(str(SDT.id))

        elif 'NT' in parametro:
            if 'AFI-NT'==parametro:
                NO3 = models.ParametroEspecifico.objects.get(codigo='AFI-NO3-CI')
                NO2 = models.ParametroEspecifico.objects.get(codigo='AFI-NO2-CI')
                NKT = models.ParametroEspecifico.objects.get(codigo='AFI-NKT')  
                if NO3.codigo_etfa!='nan' and NO3.codigo_etfa!=None:
                    anex_param(str(NO3.id))
                else: anex_param_ext(str(NO3.id))
                if NO2.codigo_etfa!='nan' and NO2.codigo_etfa!=None:
                    anex_param(str(NO2.id))
                else: anex_param_ext(str(NO2.id))
                if NKT.codigo_etfa!='nan' and NKT.codigo_etfa!=None:
                    anex_param(str(NKT.id))
                else: anex_param_ext(str(NKT.id))
            
            elif 'AP-NT'==parametro:
                NO3 = models.ParametroEspecifico.objects.get(codigo='AP-NO3-CI')
                NO2 = models.ParametroEspecifico.objects.get(codigo='AP-NO2-CI')
                NKT = models.ParametroEspecifico.objects.get(codigo='AP-NKT')                       
                if NO3.codigo_etfa!='nan' and NO3.codigo_etfa!=None:
                    anex_param(str(NO3.id))
                else: anex_param_ext(str(NO3.id))
                if NO2.codigo_etfa!='nan' and NO2.codigo_etfa!=None:
                    anex_param(str(NO2.id))
                else: anex_param_ext(str(NO2.id))
                if NKT.codigo_etfa!='nan' and NKT.codigo_etfa!=None:
                    anex_param(str(NKT.id))
                else: anex_param_ext(str(NKT.id))
            
            elif 'AR-NT'==parametro:
                NO3 = models.ParametroEspecifico.objects.get(codigo='AR-NO3-CI')
                NO2 = models.ParametroEspecifico.objects.get(codigo='AR-NO2-CI')
                NKT = models.ParametroEspecifico.objects.get(codigo='AR-NKT-SM')                       
                if NO3.codigo_etfa!='nan' and NO3.codigo_etfa!=None:
                    anex_param(str(NO3.id))
                else: anex_param_ext(str(NO3.id))
                if NO2.codigo_etfa!='nan' and NO2.codigo_etfa!=None:
                    anex_param(str(NO2.id))
                else: anex_param_ext(str(NO2.id))
                if NKT.codigo_etfa!='nan' and NKT.codigo_etfa!=None:
                    anex_param(str(NKT.id))
                else: anex_param_ext(str(NKT.id))
            
            elif 'SUB-NT'==parametro:
                NO3 = models.ParametroEspecifico.objects.get(codigo='SUB-NO3-CI')
                NO2 = models.ParametroEspecifico.objects.get(codigo='SUB-NO2-CI')
                NKT = models.ParametroEspecifico.objects.get(codigo='SUB-NKT')                       
                if NO3.codigo_etfa!='nan' and NO3.codigo_etfa!=None:
                    anex_param(str(NO3.id))
                else: anex_param_ext(str(NO3.id))
                if NO2.codigo_etfa!='nan' and NO2.codigo_etfa!=None:
                    anex_param(str(NO2.id))
                else: anex_param_ext(str(NO2.id))
                if NKT.codigo_etfa!='nan' and NKT.codigo_etfa!=None:
                    anex_param(str(NKT.id))
                else: anex_param_ext(str(NKT.id))

            elif 'SUP-NT'==parametro:
                NO3 = models.ParametroEspecifico.objects.get(codigo='SUP-NO3-CI')
                NO2 = models.ParametroEspecifico.objects.get(codigo='SUP-NO2-CI')
                NKT = models.ParametroEspecifico.objects.get(codigo='SUP-NKT')                       
                if NO3.codigo_etfa!='nan' and NO3.codigo_etfa!=None:
                    anex_param(str(NO3.id))
                else: anex_param_ext(str(NO3.id))
                if NO2.codigo_etfa!='nan' and NO2.codigo_etfa!=None:
                    anex_param(str(NO2.id))
                else: anex_param_ext(str(NO2.id))
                if NKT.codigo_etfa!='nan' and NKT.codigo_etfa!=None:
                    anex_param(str(NKT.id))
                else: anex_param_ext(str(NKT.id))

            elif 'S-NT'==parametro:
                NO3 = models.ParametroEspecifico.objects.get(codigo='S-NO3-CI')
                NO2 = models.ParametroEspecifico.objects.get(codigo='S-NO2-CI')
                NKT = models.ParametroEspecifico.objects.get(codigo='S-NKT')                       
                if NO3.codigo_etfa!='nan' and NO3.codigo_etfa!=None:
                    anex_param(str(NO3.id))
                else: anex_param_ext(str(NO3.id))
                if NO2.codigo_etfa!='nan' and NO2.codigo_etfa!=None:
                    anex_param(str(NO2.id))
                else: anex_param_ext(str(NO2.id))
                if NKT.codigo_etfa!='nan' and NKT.codigo_etfa!=None:
                    anex_param(str(NKT.id))
                else: anex_param_ext(str(NKT.id))

            elif 'L-NT'==parametro:
                NO3 = models.ParametroEspecifico.objects.get(codigo='L-NO3-CI')
                NO2 = models.ParametroEspecifico.objects.get(codigo='L-NO2-CI')
                NKT = models.ParametroEspecifico.objects.get(codigo='L-NKT')                       
                if NO3.codigo_etfa!='nan' and NO3.codigo_etfa!=None:
                    anex_param(str(NO3.id))
                else: anex_param_ext(str(NO3.id))
                if NO2.codigo_etfa!='nan' and NO2.codigo_etfa!=None:
                    anex_param(str(NO2.id))
                else: anex_param_ext(str(NO2.id))
                if NKT.codigo_etfa!='nan' and NKT.codigo_etfa!=None:
                    anex_param(str(NKT.id))
                else: anex_param_ext(str(NKT.id))

            elif 'SD-NT'==parametro:
                NO3 = models.ParametroEspecifico.objects.get(codigo='SD-NO3-CI')
                NO2 = models.ParametroEspecifico.objects.get(codigo='SD-NO2-CI')
                NKT = models.ParametroEspecifico.objects.get(codigo='SD-NKT')                       
                if NO3.codigo_etfa!='nan' and NO3.codigo_etfa!=None:
                    anex_param(str(NO3.id))
                else: anex_param_ext(str(NO3.id))
                if NO2.codigo_etfa!='nan' and NO2.codigo_etfa!=None:
                    anex_param(str(NO2.id))
                else: anex_param_ext(str(NO2.id))
                if NKT.codigo_etfa!='nan' and NKT.codigo_etfa!=None:
                    anex_param(str(NKT.id))
                else: anex_param_ext(str(NKT.id))
        
        elif 'RAS' in parametro:
            if 'AP-RAS'==parametro:
                CA = models.ParametroEspecifico.objects.get(codigo='AP-CA-ICP1')
                MG = models.ParametroEspecifico.objects.get(codigo='AP-MG-ICP1')
                NA = models.ParametroEspecifico.objects.get(codigo='AP-NA-ICP1')                       
                if CA.codigo_etfa!='nan' and CA.codigo_etfa!=None:
                    anex_param(str(CA.id))
                else: anex_param_ext(str(CA.id))
                if MG.codigo_etfa!='nan' and MG.codigo_etfa!=None:
                    anex_param(str(MG.id))
                else: anex_param_ext(str(MG.id))
                if NA.codigo_etfa!='nan' and NA.codigo_etfa!=None:
                    anex_param(str(NA.id))
                else: anex_param_ext(str(NA.id))

            elif 'AR-RAS'==parametro:
                CA = models.ParametroEspecifico.objects.get(codigo='AR-CA-ICP1')
                MG = models.ParametroEspecifico.objects.get(codigo='AR-MG-ICP1')
                NA = models.ParametroEspecifico.objects.get(codigo='AR-NA-ICP1')                       
                if CA.codigo_etfa!='nan' and CA.codigo_etfa!=None:
                    anex_param(str(CA.id))
                else: anex_param_ext(str(CA.id))
                if MG.codigo_etfa!='nan' and MG.codigo_etfa!=None:
                    anex_param(str(MG.id))
                else: anex_param_ext(str(MG.id))
                if NA.codigo_etfa!='nan' and NA.codigo_etfa!=None:
                    anex_param(str(NA.id))
                else: anex_param_ext(str(NA.id))

            elif 'SUB-RAS'==parametro:
                CA = models.ParametroEspecifico.objects.get(codigo='SUB-CA-ICP1')
                MG = models.ParametroEspecifico.objects.get(codigo='SUB-MG-ICP1')
                NA = models.ParametroEspecifico.objects.get(codigo='SUB-NA-ICP1')                       
                if CA.codigo_etfa!='nan' and CA.codigo_etfa!=None:
                    anex_param(str(CA.id))
                else: anex_param_ext(str(CA.id))
                if MG.codigo_etfa!='nan' and MG.codigo_etfa!=None:
                    anex_param(str(MG.id))
                else: anex_param_ext(str(MG.id))
                if NA.codigo_etfa!='nan' and NA.codigo_etfa!=None:
                    anex_param(str(NA.id))
                else: anex_param_ext(str(NA.id))

            elif 'SUP-RAS'==parametro:
                CA = models.ParametroEspecifico.objects.get(codigo='SUP-CA-ICP1')
                MG = models.ParametroEspecifico.objects.get(codigo='SUP-MG-ICP1')
                NA = models.ParametroEspecifico.objects.get(codigo='SUP-NA-ICP1')                       
                if CA.codigo_etfa!='nan' and CA.codigo_etfa!=None:
                    anex_param(str(CA.id))
                else: anex_param_ext(str(CA.id))
                if MG.codigo_etfa!='nan' and MG.codigo_etfa!=None:
                    anex_param(str(MG.id))
                else: anex_param_ext(str(MG.id))
                if NA.codigo_etfa!='nan' and NA.codigo_etfa!=None:
                    anex_param(str(NA.id))
                else: anex_param_ext(str(NA.id))

        elif 'NA100' in parametro:
            if 'AP-NA100'==parametro:
                CA = models.ParametroEspecifico.objects.get(codigo='AP-CA-ICP1')
                MG = models.ParametroEspecifico.objects.get(codigo='AP-MG-ICP1')
                NA = models.ParametroEspecifico.objects.get(codigo='AP-NA-ICP1')
                K = models.ParametroEspecifico.objects.get(codigo='AP-K-ICP1')                       
                if CA.codigo_etfa!='nan' and CA.codigo_etfa!=None:
                    anex_param(str(CA.id))
                else: anex_param_ext(str(CA.id))
                if MG.codigo_etfa!='nan' and MG.codigo_etfa!=None:
                    anex_param(str(MG.id))
                else: anex_param_ext(str(MG.id))
                if NA.codigo_etfa!='nan' and NA.codigo_etfa!=None:
                    anex_param(str(NA.id))
                else: anex_param_ext(str(NA.id))
                if K.codigo_etfa!='nan' and K.codigo_etfa!=None:
                    anex_param(str(K.id))
                else: anex_param_ext(str(K.id))

            elif 'AR-NA100'==parametro:
                CA = models.ParametroEspecifico.objects.get(codigo='AR-CA-ICP1')
                MG = models.ParametroEspecifico.objects.get(codigo='AR-MG-ICP1')
                NA = models.ParametroEspecifico.objects.get(codigo='AR-NA-ICP1') 
                K = models.ParametroEspecifico.objects.get(codigo='AR-K-ICP1')                      
                if CA.codigo_etfa!='nan' and CA.codigo_etfa!=None:
                    anex_param(str(CA.id))
                else: anex_param_ext(str(CA.id))
                if MG.codigo_etfa!='nan' and MG.codigo_etfa!=None:
                    anex_param(str(MG.id))
                else: anex_param_ext(str(MG.id))
                if NA.codigo_etfa!='nan' and NA.codigo_etfa!=None:
                    anex_param(str(NA.id))
                else: anex_param_ext(str(NA.id))
                if K.codigo_etfa!='nan' and K.codigo_etfa!=None:
                    anex_param(str(K.id))
                else: anex_param_ext(str(K.id))

            elif 'SUB-NA100'==parametro:
                CA = models.ParametroEspecifico.objects.get(codigo='SUB-CA-ICP1')
                MG = models.ParametroEspecifico.objects.get(codigo='SUB-MG-ICP1')
                NA = models.ParametroEspecifico.objects.get(codigo='SUB-NA-ICP1')
                K = models.ParametroEspecifico.objects.get(codigo='SUB-K-ICP1')                       
                if CA.codigo_etfa!='nan' and CA.codigo_etfa!=None:
                    anex_param(str(CA.id))
                else: anex_param_ext(str(CA.id))
                if MG.codigo_etfa!='nan' and MG.codigo_etfa!=None:
                    anex_param(str(MG.id))
                else: anex_param_ext(str(MG.id))
                if NA.codigo_etfa!='nan' and NA.codigo_etfa!=None:
                    anex_param(str(NA.id))
                else: anex_param_ext(str(NA.id))
                if K.codigo_etfa!='nan' and K.codigo_etfa!=None:
                    anex_param(str(K.id))
                else: anex_param_ext(str(K.id))

            elif 'SUP-NA100'==parametro:
                CA = models.ParametroEspecifico.objects.get(codigo='SUP-CA-ICP1')
                MG = models.ParametroEspecifico.objects.get(codigo='SUP-MG-ICP1')
                NA = models.ParametroEspecifico.objects.get(codigo='SUP-NA-ICP1') 
                K = models.ParametroEspecifico.objects.get(codigo='SUP-K-ICP1')                      
                if CA.codigo_etfa!='nan' and CA.codigo_etfa!=None:
                    anex_param(str(CA.id))
                else: anex_param_ext(str(CA.id))
                if MG.codigo_etfa!='nan' and MG.codigo_etfa!=None:
                    anex_param(str(MG.id))
                else: anex_param_ext(str(MG.id))
                if NA.codigo_etfa!='nan' and NA.codigo_etfa!=None:
                    anex_param(str(NA.id))
                else: anex_param_ext(str(NA.id))
                if K.codigo_etfa!='nan' and K.codigo_etfa!=None:
                    anex_param(str(K.id))
                else: anex_param_ext(str(K.id))

        elif 'DUREZA-T' in parametro:
            if 'AFI-DUREZA-T'==parametro:
                CA = models.ParametroEspecifico.objects.get(codigo='AFI-CA-AAS')
                DCA = models.ParametroEspecifico.objects.get(codigo='AFI-DUREZA-CA')
                MG = models.ParametroEspecifico.objects.get(codigo='AFI-MG-AAS')
                DMG = models.ParametroEspecifico.objects.get(codigo='AFI-DUREZA-MG')                      
                if CA.codigo_etfa!='nan' and CA.codigo_etfa!=None:
                    anex_param(str(CA.id))
                else: anex_param_ext(str(CA.id))
                if MG.codigo_etfa!='nan' and MG.codigo_etfa!=None:
                    anex_param(str(MG.id))
                else: anex_param_ext(str(MG.id))
                if DCA.codigo_etfa!='nan' and DCA.codigo_etfa!=None:
                    anex_param(str(DCA.id))
                else: anex_param_ext(str(DCA.id))
                if DMG.codigo_etfa!='nan' and DMG.codigo_etfa!=None:
                    anex_param(str(DMG.id))
                else: anex_param_ext(str(DMG.id))
            
            elif 'AP-DUREZA-T'==parametro:
                CA = models.ParametroEspecifico.objects.get(codigo='AP-CA-ICP1')
                DCA = models.ParametroEspecifico.objects.get(codigo='AP-DUREZA-CA')
                MG = models.ParametroEspecifico.objects.get(codigo='AP-MG-ICP1')
                DMG = models.ParametroEspecifico.objects.get(codigo='AP-DUREZA-MG')                      
                if CA.codigo_etfa!='nan' and CA.codigo_etfa!=None:
                    anex_param(str(CA.id))
                else: anex_param_ext(str(CA.id))
                if MG.codigo_etfa!='nan' and MG.codigo_etfa!=None:
                    anex_param(str(MG.id))
                else: anex_param_ext(str(MG.id))
                if DCA.codigo_etfa!='nan' and DCA.codigo_etfa!=None:
                    anex_param(str(DCA.id))
                else: anex_param_ext(str(DCA.id))
                if DMG.codigo_etfa!='nan' and DMG.codigo_etfa!=None:
                    anex_param(str(DMG.id))
                else: anex_param_ext(str(DMG.id))

            elif 'AR-DUREZA-T'==parametro:
                CA = models.ParametroEspecifico.objects.get(codigo='AR-CA-ICP1')
                DCA = models.ParametroEspecifico.objects.get(codigo='AR-DUREZA-CA')
                MG = models.ParametroEspecifico.objects.get(codigo='AR-MG-ICP1')
                DMG = models.ParametroEspecifico.objects.get(codigo='AR-DUREZA-MG')                      
                if CA.codigo_etfa!='nan' and CA.codigo_etfa!=None:
                    anex_param(str(CA.id))
                else: anex_param_ext(str(CA.id))
                if MG.codigo_etfa!='nan' and MG.codigo_etfa!=None:
                    anex_param(str(MG.id))
                else: anex_param_ext(str(MG.id))
                if DCA.codigo_etfa!='nan' and DCA.codigo_etfa!=None:
                    anex_param(str(DCA.id))
                else: anex_param_ext(str(DCA.id))
                if DMG.codigo_etfa!='nan' and DMG.codigo_etfa!=None:
                    anex_param(str(DMG.id))
                else: anex_param_ext(str(DMG.id))
            
            elif 'SUB-DUREZA-T'==parametro:
                CA = models.ParametroEspecifico.objects.get(codigo='SUB-CA-ICP1')
                DCA = models.ParametroEspecifico.objects.get(codigo='SUB-DUREZA-CA')
                MG = models.ParametroEspecifico.objects.get(codigo='SUB-MG-ICP1')
                DMG = models.ParametroEspecifico.objects.get(codigo='SUB-DUREZA-MG')                      
                if CA.codigo_etfa!='nan' and CA.codigo_etfa!=None:
                    anex_param(str(CA.id))
                else: anex_param_ext(str(CA.id))
                if MG.codigo_etfa!='nan' and MG.codigo_etfa!=None:
                    anex_param(str(MG.id))
                else: anex_param_ext(str(MG.id))
                if DCA.codigo_etfa!='nan' and DCA.codigo_etfa!=None:
                    anex_param(str(DCA.id))
                else: anex_param_ext(str(DCA.id))
                if DMG.codigo_etfa!='nan' and DMG.codigo_etfa!=None:
                    anex_param(str(DMG.id))
                else: anex_param_ext(str(DMG.id))

            elif 'SUP-DUREZA-T'==parametro:
                CA = models.ParametroEspecifico.objects.get(codigo='SUP-CA-ICP1')
                DCA = models.ParametroEspecifico.objects.get(codigo='SUP-DUREZA-CA')
                MG = models.ParametroEspecifico.objects.get(codigo='SUP-MG-ICP1')
                DMG = models.ParametroEspecifico.objects.get(codigo='SUP-DUREZA-MG')                      
                if CA.codigo_etfa!='nan' and CA.codigo_etfa!=None:
                    anex_param(str(CA.id))
                else: anex_param_ext(str(CA.id))
                if MG.codigo_etfa!='nan' and MG.codigo_etfa!=None:
                    anex_param(str(MG.id))
                else: anex_param_ext(str(MG.id))
                if DCA.codigo_etfa!='nan' and DCA.codigo_etfa!=None:
                    anex_param(str(DCA.id))
                else: anex_param_ext(str(DCA.id))
                if DMG.codigo_etfa!='nan' and DMG.codigo_etfa!=None:
                    anex_param(str(DMG.id))
                else: anex_param_ext(str(DMG.id))
    
    return parameters


def calc_param_no_etfa(parameters):
    """Esta función es para completar parametros faltantes en los servicio NO ETFA"""
    def anex_param(p):
        """Esta función es para agregar a la lista parameters los parametros que no se encuentren en esta ni en la lista de parametros de analisis externos"""
        if p not in parameters:
            parameters.append(p)
        return parameters

    def anex_param2(p, p2):
        """Esta función es para agregar a la lista parameters los parametros que no se encuentren en esta ni en la lista de parametros de analisis externos"""
        if p not in parameters and p2 not in parameters:
                    parameters.append(p)

    for p in parameters:
        parametro = models.ParametroEspecifico.objects.get(pk= p).codigo
        if 'HCT' in parametro:
            if 'AFI-HCT'==parametro:
                HCF = models.ParametroEspecifico.objects.get(codigo='AFI-HCF-GRV')
                HCV = models.ParametroEspecifico.objects.get(codigo='AFI-HCV')
                anex_param(str(HCF.id))
                anex_param(str(HCV.id))
                
            
            elif 'AP-HCT'==parametro:
                HCF = models.ParametroEspecifico.objects.get(codigo='AP-HCF-GRV')
                HCV = models.ParametroEspecifico.objects.get(codigo='AP-HCV')
                anex_param(str(HCF.id))
                anex_param(str(HCV.id))
            
            elif 'AR-HCT' == parametro:
                HCF2 = str(models.ParametroEspecifico.objects.get(codigo='AR-HCF-NCH-GRV').id)
                HCF = str(models.ParametroEspecifico.objects.get(codigo='AR-HCF-GRV').id)
                HCV = models.ParametroEspecifico.objects.get(codigo='AR-HCV')
                anex_param2(p=HCF, p2=HCF2)
                anex_param(str(HCV.id))
            
            elif 'SUB-HCT' == parametro:
                HCF = models.ParametroEspecifico.objects.get(codigo='SUB-HCF-GRV')
                HCV = models.ParametroEspecifico.objects.get(codigo='SUB-HCV')
                anex_param(str(HCF.id))
                anex_param(str(HCV.id))
            
            elif 'SUP-HCT' == parametro:
                HCF = models.ParametroEspecifico.objects.get(codigo='SUP-HCF-GRV')
                HCV = models.ParametroEspecifico.objects.get(codigo='SUP-HCV')
                anex_param(str(HCF.id))
                anex_param(str(HCV.id))
                
            
            elif 'L-HCT' == parametro:
                HCF = models.ParametroEspecifico.objects.get(codigo='L-HCF-GRV')
                HCV = models.ParametroEspecifico.objects.get(codigo='L-HCV')
                anex_param(str(HCF.id))
                anex_param(str(HCV.id))
            
            elif 'SD-HCT' == parametro:
                HCF = models.ParametroEspecifico.objects.get(codigo='SD-HCF-GRV')
                HCV = models.ParametroEspecifico.objects.get(codigo='SD-HCV')
                anex_param(str(HCF.id))
                anex_param(str(HCV.id))
            
            elif 'S-HCT' == parametro:
                HCF = models.ParametroEspecifico.objects.get(codigo='S-HCF-GRV')
                HCV = models.ParametroEspecifico.objects.get(codigo='S-HCV')
                anex_param(str(HCF.id))
                anex_param(str(HCV.id))
        
        elif 'DDD+DDE+DDT' in parametro:
            if 'AP-DDD+DDE+DDT'==parametro:
                DDD = str(models.ParametroEspecifico.objects.get(codigo='AP-DDD-ME').id)
                DDE = str(models.ParametroEspecifico.objects.get(codigo='AP-DDE-ME').id)
                DDT = str(models.ParametroEspecifico.objects.get(codigo='AP-DDT-ME').id)
                anex_param(DDD)
                anex_param(DDE)
                anex_param(DDT)
            
            elif 'FC-DDD+DDE+DDT'==parametro:
                DDD = str(models.ParametroEspecifico.objects.get(codigo='FC-DDD-ME').id)
                DDE = str(models.ParametroEspecifico.objects.get(codigo='FC-DDE-ME').id)
                DDT = str(models.ParametroEspecifico.objects.get(codigo='FC-DDT-ME').id)
                anex_param(DDD)
                anex_param(DDE)
                anex_param(DDT)
            
        elif 'THM' in parametro:
            if 'AFI-THM-SM'==parametro:
                BROMODICL = str(models.ParametroEspecifico.objects.get(codigo='AFI-BROMODICL-SM').id)
                DIBROMOCL = str(models.ParametroEspecifico.objects.get(codigo='AFI-DIBROMOCL-SM').id)
                TRIBROM = str(models.ParametroEspecifico.objects.get(codigo='AFI-TRIBROM-SM').id)
                TRICLOR = str(models.ParametroEspecifico.objects.get(codigo='AFI-TRICLOR-SM').id)
                anex_param(BROMODICL)
                anex_param(DIBROMOCL)
                anex_param(TRIBROM)
                anex_param(TRICLOR)
            
            elif 'AP-THM-ME'==parametro:
                BROMODICL = str(models.ParametroEspecifico.objects.get(codigo='AP-BROMODICL-ME').id)
                DIBROMOCL = str(models.ParametroEspecifico.objects.get(codigo='AP-DIBROMOCL-ME').id)
                TRIBROM = str(models.ParametroEspecifico.objects.get(codigo='AP-TRIBROM-ME').id)
                TRICLOR = str(models.ParametroEspecifico.objects.get(codigo='AP-TRICLOR-ME').id)
                anex_param(BROMODICL)
                anex_param(DIBROMOCL)
                anex_param(TRIBROM)
                anex_param(TRICLOR)
            
            elif 'AP-THM-SM'==parametro:
                BROMODICL = str(models.ParametroEspecifico.objects.get(codigo='AP-BROMODICL-SM').id)
                DIBROMOCL = str(models.ParametroEspecifico.objects.get(codigo='AP-DIBROMOCL-SM').id)
                TRIBROM = str(models.ParametroEspecifico.objects.get(codigo='AP-TRIBROM-SM').id)
                TRICLOR = str(models.ParametroEspecifico.objects.get(codigo='AP-TRICLOR-SM').id)
                anex_param(BROMODICL)
                anex_param(DIBROMOCL)
                anex_param(TRIBROM)
                anex_param(TRICLOR)
            
            elif 'AR-THM-SM'==parametro:
                BROMODICL_NCH = str(models.ParametroEspecifico.objects.get(codigo='AR-BROMODICL-NCH').id)
                BROMODICL_SM = str(models.ParametroEspecifico.objects.get(codigo='AR-BROMODICL-SM').id)
                DIBROMOCL_NCH = str(models.ParametroEspecifico.objects.get(codigo='AR-DIBROMOCL-NCH').id)
                DIBROMOCL_SM = str(models.ParametroEspecifico.objects.get(codigo='AR-DIBROMOCL-SM').id)
                TRIBROM_NCH = str(models.ParametroEspecifico.objects.get(codigo='AR-TRIBROM-NCH').id)
                TRIBROM_SM = str(models.ParametroEspecifico.objects.get(codigo='AR-TRIBROM-SM').id)
                TRICLOR = str(models.ParametroEspecifico.objects.get(codigo='AR-TRICLOR-SM').id)
                anex_param2(p=BROMODICL_SM, p2=BROMODICL_NCH)
                anex_param(p=DIBROMOCL_SM, p2=DIBROMOCL_NCH)
                anex_param(p=TRIBROM_SM, p2=TRIBROM_NCH)
                anex_param(TRICLOR)
            
            elif 'SUB-THM-SM'==parametro:
                BROMODICL = str(models.ParametroEspecifico.objects.get(codigo='SUB-BROMODICL-SM').id)
                DIBROMOCL = str(models.ParametroEspecifico.objects.get(codigo='SUB-DIBROMOCL-SM').id)
                TRIBROM = str(models.ParametroEspecifico.objects.get(codigo='SUB-TRIBROM-SM').id)
                TRICLOR = str(models.ParametroEspecifico.objects.get(codigo='SUB-TRICLOR-SM').id)
                anex_param(BROMODICL)
                anex_param(DIBROMOCL)
                anex_param(TRIBROM)
                anex_param(TRICLOR)
            
            elif 'SUP-THM-SM'==parametro:
                BROMODICL = str(models.ParametroEspecifico.objects.get(codigo='SUP-BROMODICL-SM').id)
                DIBROMOCL = str(models.ParametroEspecifico.objects.get(codigo='SUP-DIBROMOCL-SM').id)
                TRIBROM = str(models.ParametroEspecifico.objects.get(codigo='SUP-TRIBROM-SM').id)
                TRICLOR = str(models.ParametroEspecifico.objects.get(codigo='SUP-TRICLOR-SM').id)
                anex_param(BROMODICL)
                anex_param(DIBROMOCL)
                anex_param(TRIBROM)
                anex_param(TRICLOR)
            
            elif 'FC-THM-ME'==parametro:
                BROMODICL = str(models.ParametroEspecifico.objects.get(codigo='FC-BROMODICL-ME').id)
                DIBROMOCL = str(models.ParametroEspecifico.objects.get(codigo='FC-DIBROMOCL-ME').id)
                TRIBROM = str(models.ParametroEspecifico.objects.get(codigo='FC-TRIBROM-ME').id)
                TRICLOR = str(models.ParametroEspecifico.objects.get(codigo='FC-TRICLOR-ME').id)
                anex_param(BROMODICL)
                anex_param(DIBROMOCL)
                anex_param(TRIBROM)
                anex_param(TRICLOR)
        
        elif 'LANGELIER' in parametro:
            if 'SUP-LANGELIER'==parametro:
                CA = str(models.ParametroEspecifico.objects.get(codigo='SUP-CA-ICP1').id)
                ALCAL = str(models.ParametroEspecifico.objects.get(codigo='SUP-ALCAL-T').id)
                DUREZA = str(models.ParametroEspecifico.objects.get(codigo='SUP-DUREZA-CA').id)
                PH = str(models.ParametroEspecifico.objects.get(codigo='SUP-PH-SM').id)                       
                SDT = str(models.ParametroEspecifico.objects.get(codigo='SUP-SDT-GRV').id)
                anex_param(CA)
                anex_param(ALCAL)
                anex_param(DUREZA)
                anex_param(PH)
                anex_param(SDT)
            
            elif 'SUB-LANGELIER'==parametro:
                CA = str(models.ParametroEspecifico.objects.get(codigo='SUB-CA-ICP1').id)
                ALCAL = str(models.ParametroEspecifico.objects.get(codigo='SUB-ALCAL-T').id)
                DUREZA = str(models.ParametroEspecifico.objects.get(codigo='SUB-DUREZA-CA').id)
                PH = str(models.ParametroEspecifico.objects.get(codigo='SUB-PH-SM').id)
                SDT = str(models.ParametroEspecifico.objects.get(codigo='SUB-SDT-GRV').id)
                anex_param(CA)
                anex_param(ALCAL)
                anex_param(DUREZA)
                anex_param(PH)
                anex_param(SDT)
            
            elif 'AR-LANGELIER'==parametro:
                CA = str(models.ParametroEspecifico.objects.get(codigo='AR-CA-ICP1').id)
                ALCAL = str(models.ParametroEspecifico.objects.get(codigo='AR-ALCAL-T').id)
                DUREZA = str(models.ParametroEspecifico.objects.get(codigo='AR-DUREZA-CA').id)
                PH = str(models.ParametroEspecifico.objects.get(codigo='AR-PH-SM').id)
                PH2 = str(models.ParametroEspecifico.objects.get(codigo='AR-PH-NCH').id)
                SDT = str(models.ParametroEspecifico.objects.get(codigo='AR-SDT-GRV').id)
                anex_param(CA)
                anex_param(ALCAL)
                anex_param(DUREZA)
                anex_param2(p=PH, p2=PH2)
                anex_param(SDT)

            elif 'AP-LANGELIER'==parametro:
                CA = str(models.ParametroEspecifico.objects.get(codigo='AP-CA-ICP1').id)
                ALCAL = str(models.ParametroEspecifico.objects.get(codigo='AP-ALCAL-T').id)
                DUREZA = str(models.ParametroEspecifico.objects.get(codigo='AP-DUREZA-CA').id)
                PH = str(models.ParametroEspecifico.objects.get(codigo='AP-PH-SM').id)
                PH2 = str(models.ParametroEspecifico.objects.get(codigo='AP-PH-ME').id)
                SDT = str(models.ParametroEspecifico.objects.get(codigo='AP-SDT-GRV').id)
                SDT2 = str(models.ParametroEspecifico.objects.get(codigo='AP-SDT-ME-GRV').id)
                anex_param(CA)
                anex_param(ALCAL)
                anex_param(DUREZA)
                anex_param2(p=PH, p2=PH2)
                anex_param2(p=SDT, p2=SDT2)

            elif 'AFI-LANGELIER'==parametro:
                CA = str(models.ParametroEspecifico.objects.get(codigo='AFI-CA-AAS').id)
                ALCAL = str(models.ParametroEspecifico.objects.get(codigo='AFI-ALCAL-T').id)
                DUREZA = str(models.ParametroEspecifico.objects.get(codigo='AFI-DUREZA-CA').id)
                PH = str(models.ParametroEspecifico.objects.get(codigo='AFI-PH-SM').id)
                SDT = str(models.ParametroEspecifico.objects.get(codigo='AFI-SDT-GRV').id)
                anex_param(CA)
                anex_param(ALCAL)
                anex_param(DUREZA)
                anex_param(PH)
                anex_param(SDT)


        elif 'NT' in parametro:
            if 'AFI-NT'==parametro:
                NO3 = str(models.ParametroEspecifico.objects.get(codigo='AFI-NO3-CI').id)
                NO2 = str(models.ParametroEspecifico.objects.get(codigo='AFI-NO2-CI').id)
                NKT = str(models.ParametroEspecifico.objects.get(codigo='AFI-NKT').id)                       
                anex_param(NO3)
                anex_param(NO2)
                anex_param(NKT)
            
            elif 'AP-NT'==parametro:
                NO3 = str(models.ParametroEspecifico.objects.get(codigo='AP-NO3-CI').id)
                NO2 = str(models.ParametroEspecifico.objects.get(codigo='AP-NO2-CI').id)
                NKT = str(models.ParametroEspecifico.objects.get(codigo='AP-NKT').id)                       
                anex_param(NO3)
                anex_param(NO2)
                anex_param(NKT)
            
            elif 'AR-NT'==parametro:
                NO3 = str(models.ParametroEspecifico.objects.get(codigo='AR-NO3-CI').id)
                NO2 = str(models.ParametroEspecifico.objects.get(codigo='AR-NO2-CI').id)
                NKT = str(models.ParametroEspecifico.objects.get(codigo='AR-NKT-SM').id)                       
                anex_param(NO3)
                anex_param(NO2)
                anex_param(NKT)
            
            elif 'SUB-NT'==parametro:
                NO3 = str(models.ParametroEspecifico.objects.get(codigo='SUB-NO3-CI').id)
                NO2 = str(models.ParametroEspecifico.objects.get(codigo='SUB-NO2-CI').id)
                NKT = str(models.ParametroEspecifico.objects.get(codigo='SUB-NKT').id)                       
                anex_param(NO3)
                anex_param(NO2)
                anex_param(NKT)

            elif 'SUP-NT'==parametro:
                NO3 = str(models.ParametroEspecifico.objects.get(codigo='SUP-NO3-CI').id)
                NO2 = str(models.ParametroEspecifico.objects.get(codigo='SUP-NO2-CI').id)
                NKT = str(models.ParametroEspecifico.objects.get(codigo='SUP-NKT').id)                       
                anex_param(NO3)
                anex_param(NO2)
                anex_param(NKT)

            elif 'S-NT'==parametro:
                NO3 = str(models.ParametroEspecifico.objects.get(codigo='S-NO3-CI').id)
                NO2 = str(models.ParametroEspecifico.objects.get(codigo='S-NO2-CI').id)
                NKT = str(models.ParametroEspecifico.objects.get(codigo='S-NKT').id)                       
                anex_param(NO3)
                anex_param(NO2)
                anex_param(NKT)

            elif 'L-NT'==parametro:
                NO3 = str(models.ParametroEspecifico.objects.get(codigo='L-NO3-CI').id)
                NO2 = str(models.ParametroEspecifico.objects.get(codigo='L-NO2-CI').id)
                NKT = str(models.ParametroEspecifico.objects.get(codigo='L-NKT').id)                       
                anex_param(NO3)
                anex_param(NO2)
                anex_param(NKT)

            elif 'SD-NT'==parametro:
                NO3 = str(models.ParametroEspecifico.objects.get(codigo='SD-NO3-CI').id)
                NO2 = str(models.ParametroEspecifico.objects.get(codigo='SD-NO2-CI').id)
                NKT = str(models.ParametroEspecifico.objects.get(codigo='SD-NKT').id)                       
                anex_param(NO3)
                anex_param(NO2)
                anex_param(NKT)
        
        elif 'RAS' in parametro:
            if 'AP-RAS'==parametro:
                CA = str(models.ParametroEspecifico.objects.get(codigo='AP-CA-ICP1').id)
                MG = str(models.ParametroEspecifico.objects.get(codigo='AP-MG-ICP1').id)
                NA = str(models.ParametroEspecifico.objects.get(codigo='AP-NA-ICP1').id)                       
                anex_param(CA)
                anex_param(MG)
                anex_param(NA)

            elif 'AR-RAS'==parametro:
                CA = str(models.ParametroEspecifico.objects.get(codigo='AR-CA-ICP1').id)
                MG = str(models.ParametroEspecifico.objects.get(codigo='AR-MG-ICP1').id)
                NA = str(models.ParametroEspecifico.objects.get(codigo='AR-NA-ICP1').id)                       
                anex_param(CA)
                anex_param(MG)
                anex_param(NA)

            elif 'SUB-RAS'==parametro:
                CA = str(models.ParametroEspecifico.objects.get(codigo='SUB-CA-ICP1').id)
                MG = str(models.ParametroEspecifico.objects.get(codigo='SUB-MG-ICP1').id)
                NA = str(models.ParametroEspecifico.objects.get(codigo='SUB-NA-ICP1').id)                       
                anex_param(CA)
                anex_param(MG)
                anex_param(NA)

            elif 'SUP-RAS'==parametro:
                CA = str(models.ParametroEspecifico.objects.get(codigo='SUP-CA-ICP1').id)
                MG = str(models.ParametroEspecifico.objects.get(codigo='SUP-MG-ICP1').id)
                NA = str(models.ParametroEspecifico.objects.get(codigo='SUP-NA-ICP1').id)                       
                anex_param(CA)
                anex_param(MG)
                anex_param(NA)

        elif 'NA100' in parametro:
            if 'AP-NA100'==parametro:
                CA = str(models.ParametroEspecifico.objects.get(codigo='AP-CA-ICP1').id)
                MG = str(models.ParametroEspecifico.objects.get(codigo='AP-MG-ICP1').id)
                NA = str(models.ParametroEspecifico.objects.get(codigo='AP-NA-ICP1').id)
                K = str(models.ParametroEspecifico.objects.get(codigo='AP-K-ICP1').id)                       
                anex_param(CA)
                anex_param(MG)
                anex_param(NA)
                anex_param(K)

            elif 'AR-NA100'==parametro:
                CA = str(models.ParametroEspecifico.objects.get(codigo='AR-CA-ICP1').id)
                MG = str(models.ParametroEspecifico.objects.get(codigo='AR-MG-ICP1').id)
                NA = str(models.ParametroEspecifico.objects.get(codigo='AR-NA-ICP1').id) 
                K = str(models.ParametroEspecifico.objects.get(codigo='AR-K-ICP1').id)                      
                anex_param(CA)
                anex_param(MG)
                anex_param(NA)
                anex_param(K)

            elif 'SUB-NA100'==parametro:
                CA = str(models.ParametroEspecifico.objects.get(codigo='SUB-CA-ICP1').id)
                MG = str(models.ParametroEspecifico.objects.get(codigo='SUB-MG-ICP1').id)
                NA = str(models.ParametroEspecifico.objects.get(codigo='SUB-NA-ICP1').id)
                K = str(models.ParametroEspecifico.objects.get(codigo='SUB-K-ICP1').id)                       
                anex_param(CA)
                anex_param(MG)
                anex_param(NA)
                anex_param(K)

            elif 'SUP-NA100'==parametro:
                CA = str(models.ParametroEspecifico.objects.get(codigo='SUP-CA-ICP1').id)
                MG = str(models.ParametroEspecifico.objects.get(codigo='SUP-MG-ICP1').id)
                NA = str(models.ParametroEspecifico.objects.get(codigo='SUP-NA-ICP1').id) 
                K = str(models.ParametroEspecifico.objects.get(codigo='SUP-K-ICP1').id)                      
                anex_param(CA)
                anex_param(MG)
                anex_param(NA)
                anex_param(K)

        elif 'DUREZA-T' in parametro:
            if 'AFI-DUREZA-T'==parametro:
                CA = str(models.ParametroEspecifico.objects.get(codigo='AFI-CA-AAS').id)
                DCA = str(models.ParametroEspecifico.objects.get(codigo='AFI-DUREZA-CA').id)
                MG = str(models.ParametroEspecifico.objects.get(codigo='AFI-MG-AAS').id)
                DMG = str(models.ParametroEspecifico.objects.get(codigo='AFI-DUREZA-MG').id)                      
                anex_param(CA)
                anex_param(DCA)
                anex_param(MG)
                anex_param(DMG)
            
            elif 'AP-DUREZA-T'==parametro:
                CA = str(models.ParametroEspecifico.objects.get(codigo='AP-CA-ICP1').id)
                DCA = str(models.ParametroEspecifico.objects.get(codigo='AP-DUREZA-CA').id)
                MG = str(models.ParametroEspecifico.objects.get(codigo='AP-MG-ICP1').id)
                DMG = str(models.ParametroEspecifico.objects.get(codigo='AP-DUREZA-MG').id)                      
                anex_param(CA)
                anex_param(DCA)
                anex_param(MG)
                anex_param(DMG)

            elif 'AR-DUREZA-T'==parametro:
                CA = str(models.ParametroEspecifico.objects.get(codigo='AR-CA-ICP1').id)
                DCA = str(models.ParametroEspecifico.objects.get(codigo='AR-DUREZA-CA').id)
                MG = str(models.ParametroEspecifico.objects.get(codigo='AR-MG-ICP1').id)
                DMG = str(models.ParametroEspecifico.objects.get(codigo='AR-DUREZA-MG').id)                      
                anex_param(CA)
                anex_param(DCA)
                anex_param(MG)
                anex_param(DMG)
            
            elif 'SUB-DUREZA-T'==parametro:
                CA = str(models.ParametroEspecifico.objects.get(codigo='SUB-CA-ICP1').id)
                DCA = str(models.ParametroEspecifico.objects.get(codigo='SUB-DUREZA-CA').id)
                MG = str(models.ParametroEspecifico.objects.get(codigo='SUB-MG-ICP1').id)
                DMG = str(models.ParametroEspecifico.objects.get(codigo='SUB-DUREZA-MG').id)                      
                anex_param(CA)
                anex_param(DCA)
                anex_param(MG)
                anex_param(DMG)

            elif 'SUP-DUREZA-T'==parametro:
                CA = str(models.ParametroEspecifico.objects.get(codigo='SUP-CA-ICP1').id)
                DCA = str(models.ParametroEspecifico.objects.get(codigo='SUP-DUREZA-CA').id)
                MG = str(models.ParametroEspecifico.objects.get(codigo='SUP-MG-ICP1').id)
                DMG = str(models.ParametroEspecifico.objects.get(codigo='SUP-DUREZA-MG').id)                      
                anex_param(CA)
                anex_param(DCA)
                anex_param(MG)
                anex_param(DMG)
    
    return parameters


def calc_envases(parameters):
    """Esta función cálcula los envases necesarios en un servicio, tomado en cuenta el atributo envase de cada parametro dentro de la lista parameters"""
    par_x_env = {}
    P_1L_HNO3 = 0
    P_1L_HNO3_F = 0 
    P_1L_NAOH = 0 
    P_1L_SP = 0
    P_1L_SP1 = 0
    P_1L_SP2 = 0
    P_250_EST = 0
    P_250_EST1 = 0
    P_250_EST2 = 0 
    P_500_H2SO4 = 0
    P_500_NAOH = 0
    V_1L_HCL = 0
    V_1L_HCL_ASC = 0
    V_1L_HCL_ASC1 = 0
    V_1L_HCL_ASC2 = 0
    V_500_H2SO4 = 0
    V_500_SP = 0
    VA_1L_TIOSUL1= 0
    VA_1L_TIOSUL2= 0
    VA_1L_TIOSUL = 0
    VA_1L_SP = 0
    B_PLAS = 0
    P_1L_PEROX = 0

    for p in parameters:
        param = models.ParametroEspecifico.objects.get(pk=p).envase
        if param == models.Envase.objects.get(codigo='V-1L-HCL'):
            V_1L_HCL +=1
        elif param == models.Envase.objects.get(codigo='VA-1L-SP'):
            VA_1L_SP = 1
        elif param == models.Envase.objects.get(codigo='B-PLAS'):
            B_PLAS = 1
        elif param == models.Envase.objects.get(codigo='P-1L-NAOH'):
            P_1L_NAOH = 1
        elif param == models.Envase.objects.get(codigo='P-500-H2SO4'):
            P_500_H2SO4 = 1
        elif param == models.Envase.objects.get(codigo='V-500-SP'):
            V_500_SP = 1
        elif param == models.Envase.objects.get(codigo='P-500-NAOH'):
            P_500_NAOH = 1
        elif param == models.Envase.objects.get(codigo='V-500-H2SO4'):
            V_500_H2SO4 = 1
        elif param == models.Envase.objects.get(codigo='VA-1L-TIOSUL'):
            if '2,4D' not in models.ParametroEspecifico.objects.get(pk=p).codigo or 'PENTACL' not in models.ParametroEspecifico.objects.get(pk=p).codigo :
                VA_1L_TIOSUL1 = 1
        elif '2,4D' in models.ParametroEspecifico.objects.get(pk=p).codigo or 'PENTACL' in models.ParametroEspecifico.objects.get(pk=p).codigo :
            VA_1L_TIOSUL2 = 1
        elif param == models.Envase.objects.get(codigo='P-250-EST'):
            if 'HETEROT' not in models.ParametroEspecifico.objects.get(pk=p).codigo:
                P_250_EST1 = 1
        elif 'HETEROT' in models.ParametroEspecifico.objects.get(pk=p).codigo:
            P_250_EST2 = 1
        
        elif 'SDT' in models.ParametroEspecifico.objects.get(pk=p).codigo:
            P_1L_SP += 1
        elif 'SF' in models.ParametroEspecifico.objects.get(pk=p).codigo:
            P_1L_SP += 1
        elif 'SSD' in models.ParametroEspecifico.objects.get(pk=p).codigo:
            P_1L_SP += 2
        elif 'SST' in models.ParametroEspecifico.objects.get(pk=p).codigo:
            P_1L_SP += 1
        elif 'ST' in models.ParametroEspecifico.objects.get(pk=p).codigo:
            P_1L_SP += 1
        elif 'SV' in models.ParametroEspecifico.objects.get(pk=p).codigo:
            P_1L_SP += 1
        elif param == models.Envase.objects.get(codigo='P-1L-SP'):
            if 'SDT' not in models.ParametroEspecifico.objects.get(pk=p).codigo or 'SF' not in models.ParametroEspecifico.objects.get(pk=p).codigo or 'SSD' not in models.ParametroEspecifico.objects.get(pk=p).codigo or 'SST' not in models.ParametroEspecifico.objects.get(pk=p).codigo or 'ST' not in models.ParametroEspecifico.objects.get(pk=p).codigo or 'SV' not in models.ParametroEspecifico.objects.get(pk=p).codigo:
                if 'BROMURO' in models.ParametroEspecifico.objects.get(pk=p).codigo or 'PO4-CI' in models.ParametroEspecifico.objects.get(pk=p).codigo or 'CL-CI' in models.ParametroEspecifico.objects.get(pk=p).codigo or 'F-CI' in models.ParametroEspecifico.objects.get(pk=p).codigo or 'NO3-CI' in models.ParametroEspecifico.objects.get(pk=p).codigo or 'NO2-CI' in models.ParametroEspecifico.objects.get(pk=p).codigo or 'SO4-CI' in models.ParametroEspecifico.objects.get(pk=p).codigo:
                    P_1L_SP1 = 1 
                else: 
                    P_1L_SP2 = 1
        elif param == models.Envase.objects.get(codigo='P-1L-HNO3-F'):
            P_1L_HNO3_F += 0.1

        elif param == models.Envase.objects.get(codigo='P-1L-HNO3'):
            P_1L_HNO3 += 0.1
        
        elif param == models.Envase.objects.get(codigo='V-1L-HCL+ASC'):
            if 'BENCE' in models.ParametroEspecifico.objects.get(pk=p).codigo or 'ETILBEN' in models.ParametroEspecifico.objects.get(pk=p).codigo or 'XILENO' in models.ParametroEspecifico.objects.get(pk=p).codigo or 'TOLUENO' in models.ParametroEspecifico.objects.get(pk=p).codigo:  
                V_1L_HCL_ASC1 = 1
            if 'BROMODICL' in models.ParametroEspecifico.objects.get(pk=p).codigo or 'DIBROMOCL' in models.ParametroEspecifico.objects.get(pk=p).codigo or 'TETRACL' in models.ParametroEspecifico.objects.get(pk=p).codigo or 'TRIBROM' in models.ParametroEspecifico.objects.get(pk=p).codigo or 'TRICLOR' in models.ParametroEspecifico.objects.get(pk=p).codigo or 'THM' in models.ParametroEspecifico.objects.get(pk=p).codigo:  
                V_1L_HCL_ASC2 = 1
    
    if P_1L_HNO3>0: 
        par_x_env['P-1L-HNO3'] = str(ceil(P_1L_HNO3)) + (' Envases' if P_1L_HNO3>1 else ' Envase')  + ' de plástico - 1 L - HNO3 \n' 
    
    if P_1L_HNO3_F>0: 
        par_x_env['P-1L-HNO3-F'] = str(ceil(P_1L_HNO3_F)) + (' Envases' if P_1L_HNO3_F>1 else ' Envase') + ' de plástico - 1 L - HNO3 - Filtrada \n'
    
    if P_1L_NAOH>0:
        par_x_env['P-1L-NAOH'] = str(P_1L_NAOH) + ' Envase de plástico - 1 L - NaOH \n'
    
    P_1L_SP = P_1L_SP + P_1L_SP1 + P_1L_SP2
    if P_1L_SP>0: 
        par_x_env['P-1L-SP']  = str(P_1L_SP) + (' Envases' if P_1L_SP>1 else ' Envase') + ' de plástico - 1 L - S/P \n'
    
    P_250_EST = P_250_EST1 + P_250_EST2
    if P_250_EST>0: 
        par_x_env['P-250-EST'] = str(P_250_EST) + (' Envases' if P_250_EST>1 else ' Envase') + ' de plástico - 250 mL - Estéril - Na2S2O3 + EDTA \n'
    
    if P_500_H2SO4>0: 
        par_x_env['P-500-H2SO4'] = str(P_500_H2SO4) + (' Envases' if P_500_H2SO4>1 else ' Envase') + ' de plástico - 500 mL - H2SO4 \n'
    
    if P_500_NAOH>0:
        par_x_env['P-500-NAOH']= str(P_500_NAOH) + ' Envase de plástico - 500 mL - NaOH + ZnAc \n'

    if V_1L_HCL>0: 
        par_x_env['V-1L-HCL']= str(V_1L_HCL) + (' Envases' if V_1L_HCL>1 else ' Envase') + ' de vidrio - 1 L - HCl \n'
    
    V_1L_HCL_ASC = V_1L_HCL_ASC1 + V_1L_HCL_ASC2
    if V_1L_HCL_ASC>0: 
        par_x_env['V-1L-HCL+ASC']= str(V_1L_HCL_ASC) + (' Envases' if V_1L_HCL_ASC>1 else ' Envase') + ' de vidrio - 1 L - HCl + Ác. Ascórbico \n' 
    
    if V_500_H2SO4>0: 
        par_x_env['V-500-SP']= str(V_500_H2SO4) + (' Envases' if V_500_H2SO4>1 else ' Envase') + ' de vidrio - 500 mL - H2SO4 \n' 
    
    if V_500_SP>0: 
        par_x_env['V-500-SP']= str(V_500_SP) + (' Envases' if V_500_SP>1 else ' Envase') + ' de vidrio - 500 mL - S/P \n' 

    VA_1L_TIOSUL = VA_1L_TIOSUL1 + VA_1L_TIOSUL2
    if VA_1L_TIOSUL>0: 
        par_x_env['VA-1L-TIOSUL'] = str(VA_1L_TIOSUL) + (' Envases' if VA_1L_TIOSUL>1 else ' Envase') + ' de vidrio ámbar - 1 L - Na2S2O3 \n'

    if VA_1L_SP>0: 
        par_x_env['VA-1L-SP'] = str(VA_1L_SP) + ' Envase de vidrio ámbar - 1 L \n'
    
    if B_PLAS>0: 
        par_x_env['B-PLAS']= str(B_PLAS) + ' Bolsa plástica ó envase plastico de boca ancha - 1L -S/P'
    
    if P_1L_PEROX>0: 
        par_x_env['P-1L-PEROX'] = P_1L_PEROX
    
    # if P_1L_BA_SP>0: 
    #     par_x_env['P-1L-BA-SP'] = str(P_1L_BA_SP) + (' Envases' if VA_1L_TIOSUL>1 else ' Envase') + ' de plástico boca ancha - 1 L - S/P'
    
    envases = ''
    for envase in par_x_env.values():
        envases += envase

    
    return envases


@login_required
@user_passes_test(is_lab)
def index(request):
    """Index view."""
    return render(request, 'LIMS/menu.html')


@login_required
@user_passes_test(is_commercial,login_url='lims:index')
def clients(request):
    """Clients view."""

    clientes = models.Cliente.objects.all().order_by('titular')
    paginator = Paginator(clientes, 35)
    page = request.GET.get('page')
    clients = paginator.get_page(page)
    template = 'LIMS/clients.html'

    if request.method == 'POST':
        if 'search_text' in request.POST and 'opcion' in request.POST:
            if request.POST['search_text'] == '' or request.POST['opcion'] == '':
                pass
            elif request.POST['opcion'] == 'titular':
                clientes = models.Cliente.objects.filter(titular__icontains = request.POST['search_text']).order_by('titular')
                paginator = Paginator(clientes, 25)
                page = request.GET.get('page')
                clients = paginator.get_page(page)


            elif request.POST['opcion'] == 'rut':
                clientes = models.Cliente.objects.filter(rut__contains = request.POST['search_text']).order_by('titular')
                paginator = Paginator(clientes, 25)
                page = request.GET.get('page')
                clients = paginator.get_page(page)
        else:
            if 'excel_file' in request.POST.keys():
                if request.POST['excel_clientes'] == '':
                    pass
            
            elif 'excel_clientes' in request.FILES:
                excel_file = request.FILES['excel_clientes']
                df = pd.read_excel(excel_file)

                responsable_de_analisis = models.User.objects.get(pk=request.POST['responsable'])
                
                for index, row in df.iterrows():
                    if   models.Cliente.objects.filter(rut=rut_fix(str(row['rut']))).exists():
                        continue
                    else:
                        if type(row['nombre']) != str: titular = '-'
                        else: titular = title_fix(str(row['nombre']))

                        if type(row['direccion']) != str: direccion = '-'
                        else: direccion = title_fix(str(row['direccion']))

                        if type(row['giro']) != str: giro = '-'
                        else: giro = cap_fix(str(row['giro']))

                        models.Cliente.objects.update_or_create(
                            id=row['id'], 
                            titular = titular, 
                            rut= rut_fix(str(row['rut'])), 
                            direccion = direccion, 
                            actividad = giro, 
                            creator_user = responsable_de_analisis
                            )
            elif 'excel_contactos' in request.FILES:
                excel_file = request.FILES['excel_contactos']
                df = pd.read_excel(excel_file)

                responsable_de_analisis = models.User.objects.get(pk=request.POST['responsable'])
                
                for index, row in df.iterrows():
                    if   models.ContactoCliente.objects.filter(id=row['id']).exists() or models.Cliente.objects.filter(id=row['cliente_id']).exists()==False:
                        continue
                    else:
                        if type(row['nombre']) != str: nombre = '-'
                        else: nombre = title_fix(str(row['nombre']))

                        models.ContactoCliente.objects.update_or_create(
                            id=row['id'], 
                            nombre = nombre, 
                            creator_user = responsable_de_analisis,
                            cliente_id = row['cliente_id']
                            )
            return redirect(request.META.get('HTTP_REFERER', '/'))
    
    context = {
                'clients': clients,
                }
    return render_view(request, template, context)


@login_required
@user_passes_test(is_commercial, login_url='lims:index')
def add_client(request):
    """Add client view."""
    if request.method == 'POST':
        titular = request.POST['titular']
        rut = request.POST['rut']
        direccion = request.POST['direccion']
        actividad = request.POST['actividad']
        usuario = request.POST['creador']
        try:
            models.Cliente.objects.create(
                titular=title_fix(titular), 
                rut=rut_fix(rut), 
                direccion=title_fix(direccion), 
                actividad=cap_fix(actividad), 
                creator_user=usuario
                )
            return redirect('lims:clients')
        except:
            error = "El titular o el RUT ya existe."
            return render(request, 'LIMS/add_client.html', {
                'error_client': error,
            })

    return render(request, 'LIMS/add_client.html')


@login_required
@user_passes_test(is_commercial, login_url='lims:index')
def client(request, id_cliente):
    """Client model."""

    cliente = models.Cliente.objects.get(id=id_cliente)
    
    queryset_contacts = models.ContactoCliente.objects.filter(cliente_id = id_cliente).order_by('nombre')
    paginator_contact = Paginator(queryset_contacts, 5)
    page_contact = request.GET.get('page_contact')
    contacts = paginator_contact.get_page(page_contact)

    queryset_monitoring_place = models.LugarDeMonitoreo.objects.filter(cliente_id = id_cliente).order_by('nombre')
    paginator_sp = Paginator(queryset_monitoring_place, 5)
    page_sp = request.GET.get('page_sp')
    monitoring_place = paginator_sp.get_page(page_sp)

    queryset_sample_points = models.PuntoDeMuestreo.objects.filter(cliente_id = id_cliente).order_by('nombre')
    paginator_sp = Paginator(queryset_sample_points, 5)
    page_sp = request.GET.get('page_sp')
    sample_points = paginator_sp.get_page(page_sp)
    
    queryset_legal_representatives = models.RepresentanteLegalCliente.objects.filter(cliente_id = id_cliente).order_by('nombre')
    paginator_lr = Paginator(queryset_legal_representatives, 5)
    page_lr = request.GET.get('page_lr')
    legal_representatives = paginator_lr.get_page(page_lr)

    queryset_rcas = models.RCACliente.objects.filter(cliente_id = id_cliente).order_by('rca_asociada')
    paginator_rca = Paginator(queryset_rcas, 5)
    page_rca = request.GET.get('page_rca')
    rcas = paginator_rca.get_page(page_rca)

    queryset_projects = models.Proyecto.objects.filter(cliente_id = id_cliente).order_by('-created')
    paginator_projects = Paginator(queryset_projects, 5)
    page_project = request.GET.get('page_project')
    projects = paginator_projects.get_page(page_project)
    template = 'LIMS/client.html'
    context = {
        'cliente':cliente,
        'contacts': contacts,
        'monitoring_places': monitoring_place,
        'sample_points':sample_points,
        'legal_representatives': legal_representatives,
        'rcas': rcas,
        'projects': projects,
    }
    return render_view(request, template, context)


@login_required
@user_passes_test(is_commercial, login_url='lims:index')
def client_add_legal_representative(request, id_cliente):
    """Client add legal representative view."""

    template = 'LIMS/client_add_legal_representative.html'
    context = {
        'pm':[0],
        'len_pm': 1,
    }
    if request.method == 'POST':
        if 'contact-number' in request.POST.keys():
            if request.POST['contact-number'] != None:
                pm = [x for x in range(int(request.POST['contact-number']))]
                len_pm = len(pm)
                if len_pm != 1:
                    context['pm'] = pm
                    context['len_pm'] = len_pm
        else:
            todo = []
            for valor in request.POST.values():
                todo.append(valor)
            contactos = todo[1::3]
            ruts = todo[2::3]
            usuarios = todo[3::3]
            duplicados = []
            for rut in ruts:
                try:
                    if rut == models.RepresentanteLegalCliente.objects.get(rut=rut).rut:
                            duplicados.append(rut) 
                            duplicado =  ruts.index(rut)
                            usuarios.pop(duplicado)
                            contactos.pop(duplicado)
                            ruts.pop(duplicado)
                except:
                    continue
            for contacto, rut, usuario in zip(contactos, ruts, usuarios):
                models.RepresentanteLegalCliente.objects.create(
                    nombre= title_fix(contacto), 
                    rut=rut_fix(rut), 
                    cliente_id= id_cliente, 
                    creator_user= usuario
                    ) 
            if duplicados != []:
                if len(duplicados)==1:
                    error_duplicados = f'El RUT {duplicados[0]}, ya se encuentra en la base de datos.'
                else:
                    error_duplicados = f'Los RUT: {list_to_string(duplicados)}, ya se encuentran en la base de datos.'
                context['error_duplicados'] = error_duplicados
            else:
                return redirect('lims:client', id_cliente)
    
    return render_view(request, template, context )


@login_required
@user_passes_test(is_commercial, login_url='lims:index')
def client_add_contact(request, id_cliente):
    """Client add contact view."""

    context = {
        'pm':[0],
        'len_pm': 1,
    }

    if request.method == 'POST':
        if 'contact-number' in request.POST.keys():
            if request.POST['contact-number'] != None:
                pm = [x for x in range(int(request.POST['contact-number']))]
                len_pm = len(pm)
                if len_pm != 1:
                    context['pm'] = pm
                    context['len_pm'] = len_pm
        else:
            todo = []
            for valor in request.POST.values():
                todo.append(valor)
            contactos = todo[1::3]
            ruts = todo[2::3]
            usuarios = todo[3::3]
            duplicados = []
            for rut in ruts:
                try:
                    if rut == models.ContactoCliente.objects.get(rut=rut).rut:
                            duplicados.append(rut) 
                            duplicado =  ruts.index(rut)
                            usuarios.pop(duplicado)
                            contactos.pop(duplicado)
                            ruts.pop(duplicado)
                except:
                    continue
            for contacto, rut, usuario in zip(contactos, ruts, usuarios):
                models.ContactoCliente.objects.create(
                    nombre= title_fix(contacto), 
                    rut=rut_fix(rut), 
                    cliente_id= id_cliente, 
                    creator_user= usuario
                    ) 
            if duplicados != []:
                if len(duplicados)==1:
                    error_duplicados = f'El RUT {duplicados[0]}, ya se encuentra en la base de datos.'
                else:
                    error_duplicados = f'Los RUT: {list_to_string(duplicados)}, ya se encuentran en la base de datos.'

                context[error_duplicados] = error_duplicados

            else:
                return redirect('lims:client', id_cliente)
    return render(request, 'LIMS/client_add_contact.html', context)


@login_required
@user_passes_test(is_commercial, login_url='lims:index')
def client_add_sample_point(request, id_cliente):
    '''Client add sample point view.'''

    context = {
        'pm':[0],
        'len_pm': 1,
    }

    if request.method == 'POST':
        if 'sp-number' in request.POST.keys():
            if request.POST['sp-number'] != None:
                pm = [x for x in range(int(request.POST['sp-number']))]
                len_pm = len(pm)
                if len_pm != 1:
                    context['pm'] = pm
                    context['len_pm'] = len_pm
        else:
            todo = []
            for valor in request.POST.values():
                todo.append(valor)
            puntos = todo[1::2]
            usuarios = todo[2::2]
            duplicados = []
            for punto in puntos:
                try:
                    if punto == models.PuntoDeMuestreo.objects.get(nombre=punto).nombre:
                            duplicados.append(punto) 
                            duplicado =  puntos.index(punto)
                            usuarios.pop(duplicado)
                            puntos.pop(duplicado)
                except:
                    continue
            for punto, usuario in zip(puntos, usuarios):
                models.PuntoDeMuestreo.objects.create(
                    nombre= cap_fix(punto), 
                    cliente_id= id_cliente, 
                    creator_user= usuario
                    ) 
            if duplicados != []:
                if len(duplicados)==1:
                    error_duplicados = f'El punto de muestreo {duplicados[0]}, ya se encuentra en la base de datos.'
                else:
                    error_duplicados = f'Los puntos de muestreo: {list_to_string(duplicados)}, ya se encuentran en la base de datos.'
                
                context['error_duplicados'] = error_duplicados

            else:        
                return redirect('lims:client', id_cliente)

    return render(request, 'LIMS/client_add_sample_point.html', context)


@login_required
@user_passes_test(is_commercial, login_url='lims:index')
def client_add_monitoring_place(request, id_cliente):
    '''Client add monitoring place view.'''

    context = {
        'pm':[0],
        'len_pm': 1,
    }

    if request.method == 'POST':
        if 'sp-number' in request.POST.keys():
            if request.POST['sp-number'] != None:
                pm = [x for x in range(int(request.POST['sp-number']))]
                len_pm = len(pm)
                if len_pm != 1:
                    context['pm'] = pm
                    context['len_pm'] = len_pm
        else:
            todo = []
            for valor in request.POST.values():
                todo.append(valor)
            puntos = todo[1::2]
            usuarios = todo[2::2]
            duplicados = []
            for punto in puntos:
                try:
                    if punto == models.LugarDeMonitoreo.objects.get(nombre=punto).nombre:
                            duplicados.append(punto) 
                            duplicado =  puntos.index(punto)
                            usuarios.pop(duplicado)
                            puntos.pop(duplicado)
                except:
                    continue
            for punto, usuario in zip(puntos, usuarios):
                models.LugarDeMonitoreo.objects.create(
                    nombre= title_fix(punto), 
                    cliente_id= id_cliente, 
                    creator_user= usuario
                    ) 
            if duplicados != []:
                if len(duplicados)==1:
                    error_duplicados = f'El lugar de monitoreo {duplicados[0]}, ya se encuentra en la base de datos.'
                else:
                    error_duplicados = f'Los lugares de monitoreos: {list_to_string(duplicados)}, ya se encuentran en la base de datos.'
                
                context['error_duplicados'] = error_duplicados

            else:        
                return redirect('lims:client', id_cliente)

    return render(request, 'LIMS/client_add_monitoring_place.html', context)


@login_required
@user_passes_test(is_commercial, login_url='lims:index')
def client_add_rca(request, id_cliente):
    '''Client add RCA view.'''

    context = {
        'pm':[0],
        'len_pm': 1,
    }

    if request.method == 'POST':
        if 'sp-number' in request.POST.keys():
            if request.POST['sp-number'] != None:
                pm = [x for x in range(int(request.POST['sp-number']))]
                len_pm = len(pm)
                if len_pm != 1:
                    context['pm'] = pm
                    context['len_pm']= len_pm
        else:
            todo = []
            for valor in request.POST.values():
                todo.append(valor)
            puntos = todo[1::2]
            usuarios = todo[2::2]
            duplicados = []
            for rca in puntos:
                try:
                    if rca == models.RCACliente.objects.get(rca_asociada=rca).rca_asociada:
                            duplicados.append(rca) 
                            duplicado =  puntos.index(rca)
                            usuarios.pop(duplicado)
                            puntos.pop(duplicado)
                except:
                    continue
            for punto, usuario in zip(puntos, usuarios):
                models.RCACliente.objects.create(
                    rca_asociada= punto, 
                    cliente_id= id_cliente, 
                    creator_user= usuario
                    ) 
            if duplicados != []:
                if len(duplicados)==1:
                    error_duplicados = f'El RCA {duplicados[0]}, ya se encuentra en la base de datos.'
                else:
                    error_duplicados = f'Los RCA: {list_to_string(duplicados)}, ya se encuentran en la base de datos.'
                
                context['error_duplicados'] = error_duplicados

            else:
                return redirect('lims:client', id_cliente)

    return render(request, 'LIMS/client_add_rca.html', context)


@login_required
@user_passes_test(is_commercial, login_url='lims:index')
def client_add_project(request, id_cliente):
    """Add Standards of reference view."""

    cliente = models.Cliente.objects.get(id=id_cliente)
    sample_points = models.PuntoDeMuestreo.objects.filter(cliente_id = id_cliente)
    rcas = models.RCACliente.objects.filter(cliente_id = id_cliente)
    normas = models.NormaDeReferencia.objects.all()
    matrices = models.TipoDeMuestra.objects.all()
    
    context = {
        'sample_points' : sample_points,
        'rcas': rcas,
        'normas': normas,
        'matrices': matrices,
        'cliente': cliente,
    }

    if request.method == 'POST':
        client = request.POST['cliente']
        codigo = request.POST['codigo']
        nombre = request.POST['nombre']
        creator_user = request.POST['creator_user']
        try:
            models.Proyecto.objects.create(
            codigo=codigo, 
            nombre=cap_fix(nombre), 
            creator_user=creator_user,
            cliente_id=client)

            return redirect('lims:client', id_cliente)
        except:
            context['error'] = "El Codigo de Proyecto ya existe."
    
    return render(request, 'LIMS/client_add_project.html', context)


@login_required
@user_passes_test(is_commercial, login_url='lims:index')
def client_add_project_cot(request, id_cliente):
    """Add Standards of reference view."""

    cliente = models.Cliente.objects.get(id=id_cliente)
    parameters = models.ParametroEspecifico.objects.all().order_by('ensayo')
    tipo_de_muestra = models.TipoDeMuestra.objects.all().order_by('nombre')
    tipo_muestra = ''
    rcas = models.RCACliente.objects.filter(cliente_id=cliente.id).order_by('rca_asociada')
    representantes_legales = models.RepresentanteLegalCliente.objects.filter(cliente_id=cliente.id).order_by('nombre')
    normas = models.NormaDeReferencia.objects.all().order_by('norma')
    
    context = {
        'cliente': cliente,
        'parameters': parameters,
        'tipo_de_muestra': tipo_muestra,
        'tipos_de_muestras': tipo_de_muestra,
        'rcas': rcas,
        'representantes_legales': representantes_legales,
        'normas': normas,
    }

    if request.method == 'POST':
        if 'tipo_muestra' in request.POST:
            tipo_de_muestra = models.TipoDeMuestra.objects.filter(nombre= request.POST['tipo_muestra']).order_by('nombre')
            tipo_muestra = request.POST['tipo_muestra']
            parameters = parameters.filter(tipo_de_muestra= tipo_muestra).order_by('codigo')
            context['tipos_de_muestras'] = tipo_de_muestra
            context['tipo_de_muestra'] = tipo_muestra
            context['parameters']= parameters
        else:
            client = request.POST['cliente']
            codigo = request.POST['codigo']
            nombre = request.POST['nombre']
            tipodemuestra = request.POST['tipo_de_muestra']
            creator_user = request.POST['creator_user']
            parameters = request.POST.getlist('parameters')
            parameters_analisis_externos = []
            norma_de_referencia = request.POST['norma_de_referencia']
            representante_legal = request.POST['representante_legal']
            rCA = request.POST['rCA']
            
            parameters = calc_param_no_etfa(parameters=parameters)
            
            if norma_de_referencia == '': norma_de_referencia = None
            else: norma_de_referencia = norma_de_referencia

            if rCA == '': rCA = None
            else: rCA = rCA

            if representante_legal == '': representante_legal = None
            else: representante_legal = models.RepresentanteLegalCliente.objects.get(id=representante_legal)

            try:
                project = models.Proyecto.objects.create(
                    codigo=codigo, 
                    nombre=cap_fix(nombre), 
                    tipo_de_muestra = tipodemuestra,
                    creator_user=creator_user,
                    cliente_id=client, 
                    cotizado=True,
                    )
                
                project.parametros_cotizados.set(parameters)
                return redirect('lims:client', id_cliente)
            except:
                context['error'] = "El Codigo de Proyecto ya existe."

    return render(request, 'LIMS/client_add_project_cot.html', context)


@login_required
@user_passes_test(is_commercial, login_url='lims:index')
def client_add_project_cot_etfa(request, id_cliente):
    """Add Standards of reference view."""

    cliente = models.Cliente.objects.get(id=id_cliente)
    parameters = models.ParametroEspecifico.objects.exclude(Q(codigo_etfa = None)|Q(codigo_etfa = 'nan')|Q(codigo_etfa = 'Cálculo')).order_by('ensayo')
    tipo_de_muestra = models.TipoDeMuestra.objects.all().order_by('nombre')
    tipo_muestra = ''
    rcas = models.RCACliente.objects.filter(cliente_id=id_cliente).order_by('rca_asociada')
    representantes_legales = models.RepresentanteLegalCliente.objects.filter(cliente_id=id_cliente).order_by('nombre')
    normas = models.NormaDeReferencia.objects.all().order_by('norma')
    parametros_i = [parameter.id for parameter in parameters.filter(codigo_etfa__icontains='Cálculo-E')]
    print(parametros_i)
    parametros_f = calc_param_cot_etfa(parametros_i)
    print(parametros_f)
    parameters = parameters.exclude(id__in=parametros_f)
    
    context = {
        'cliente': cliente,
        'parameters': parameters,
        'tipo_de_muestra': tipo_muestra,
        'tipos_de_muestras': tipo_de_muestra,
        'rcas': rcas,
        'representantes_legales': representantes_legales,
        'normas': normas,
    }

    if request.method == 'POST':
        if 'tipo_muestra' in request.POST:
            tipo_de_muestra = models.TipoDeMuestra.objects.filter(nombre= request.POST['tipo_muestra']).order_by('nombre')
            tipo_muestra = request.POST['tipo_muestra']
            parameters = parameters.filter(tipo_de_muestra= tipo_muestra).order_by('codigo')
            context['tipos_de_muestras'] = tipo_de_muestra
            context['tipo_de_muestra'] = tipo_muestra
            context['parameters']= parameters
        else:
            client = request.POST['cliente']
            codigo = request.POST['codigo']
            nombre = request.POST['nombre']
            tipodemuestra = request.POST['tipo_de_muestra']
            creator_user = request.POST['creator_user']
            parameters = request.POST.getlist('parameters')
            representante_legal = models.RepresentanteLegalCliente.objects.get(id=request.POST['representante_legal']) 
            norma_de_referencia = request.POST['norma_de_referencia']
            rCA = request.POST['rCA']
            parameters_analisis_externos = []

            parameters, parameters_analisis_externos = calc_param_etfa(parameters=parameters, parameters_analisis_externos=parameters_analisis_externos)

            if norma_de_referencia == '': norma_de_referencia = None
            else: norma_de_referencia = norma_de_referencia

            try:
                project = models.Proyecto.objects.create(
                    codigo=codigo, 
                    nombre=cap_fix(nombre), 
                    creator_user=creator_user,
                    tipo_de_muestra = tipodemuestra,
                    cliente_id=client, 
                    cotizado=True,
                    etfa=True,
                    rCA = rCA,
                    representante_legal = representante_legal,
                    norma_de_referencia = norma_de_referencia,
                    )
                
                project.parametros_cotizados.set(parameters)
                # project.parametros_externos.set(parameters_analisis_externos)

                return redirect('lims:client', id_cliente)
            except:
                context['error'] = "El Codigo de Proyecto ya existe."

    return render(request, 'LIMS/client_add_project_cot_etfa.html', context)


@login_required
@user_passes_test(is_commercial, login_url='lims:index')
def normas_ref(request):
    """Normas de referencias view."""

    queryset_normas = models.NormaDeReferencia.objects.all().order_by('norma')
    user = request.user
    manager = user.groups.filter(name='manager').exists()

    if request.method == 'POST':

        if 'search_text' in request.POST.keys():
            if request.POST['search_text'] == '' or request.POST['buscar'] == '':
                pass

            elif request.POST['buscar'] == 'norma':
                queryset_normas = queryset_normas.filter(norma__contains=request.POST['search_text'])

            elif request.POST['buscar'] == 'descripcion':
                queryset_normas = queryset_normas.filter(descripcion__contains=request.POST['search_text'])
        
        else:
            if 'excel_file' in request.POST.keys():
                if request.POST['excel_file'] == '':
                    pass
            
            elif request.FILES['excel_file']:
                excel_file = request.FILES['excel_file']
                df = pd.read_excel(excel_file)

                responsable_de_analisis = models.User.objects.get(pk=request.POST['responsable_de_analisis'])
                
                for index, row in df.iterrows():
                    if   models.NormaDeReferencia.objects.filter(norma=row['Norma']).exists():
                        continue
                    else:
                        models.NormaDeReferencia.objects.create(norma = row['Norma'], descripcion= row['Descripción'],creator_user = responsable_de_analisis)
            return redirect(request.META.get('HTTP_REFERER', '/'))
    
    paginator = Paginator(queryset_normas, 35)
    page = request.GET.get('page')
    normas = paginator.get_page(page)
    return render(request, 'LIMS/normas_ref.html',{
        'normas': normas,
        'manager': manager,
    })


@login_required
@user_passes_test(is_manager, login_url='lims:index')
def add_normas_ref(request):
    """Add Standards of reference view."""

    context = {
        'pm':[0],
        'len_pm': 1,
    }

    if request.method == 'POST':
        if 'sp-number' in request.POST.keys():
            if request.POST['sp-number'] != None:
                pm = [x for x in range(int(request.POST['sp-number']))]
                len_pm = len(pm)
                if len_pm != 1:
                    context['pm'] = pm
                    context['len_pm'] = len_pm
        else:
            todo = []
            for valor in request.POST.values():
                todo.append(valor)
            normas = todo[1::2]
            usuarios = todo[2::2]
            duplicados = []
            for norma in normas:
                try:
                    if norma == models.NormaDeReferencia.objects.get(norma=norma).norma:
                            duplicados.append(norma) 
                            duplicado =  normas.index(norma)
                            usuarios.pop(duplicado)
                            normas.pop(duplicado)
                except:
                    continue
            for norma, usuario in zip(normas, usuarios):
                models.NormaDeReferencia.objects.create(
                    norma=norma, 
                    creator_user=usuario
                    ) 
            if duplicados != []:
                if len(duplicados)==1:
                    error_duplicados = f'La norma {duplicados[0]}, ya se encuentra en la base de datos.'
                else:
                    error_duplicados = f'Las normas: {list_to_string(duplicados)}, ya se encuentran en la base de datos.'
                context['error_duplicados'] = error_duplicados
            else:
                return redirect('lims:normas_ref')

    return render(request, 'LIMS/add_normas_ref.html', context)


@login_required
@user_passes_test(is_commercial, login_url='lims:index')
def methods(request):
    """Normas de referencias view."""

    queryset_metodos = models.Metodo.objects.all().order_by('nombre')
    user = request.user
    manager = user.groups.filter(name='manager').exists()
    
    if request.method == 'POST':
        if 'search_text' in request.POST.keys():
            if request.POST['search_text'] == '' or request.POST['buscar'] == '':
                pass

            elif request.POST['buscar'] == 'nombre':
                queryset_metodos = queryset_metodos.filter(nombre__contains=request.POST['search_text'])

            elif request.POST['buscar'] == 'descripcion':
                queryset_metodos = queryset_metodos.filter(descripcion__contains=request.POST['search_text'])

    paginator = Paginator(queryset_metodos, 35)
    page = request.GET.get('page')
    metodos = paginator.get_page(page)
    return render(request, 'LIMS/methods.html',{
        'metodos': metodos,
        'manager': manager,
    })


@login_required
@user_passes_test(is_manager, login_url='lims:index')
def add_method(request):
    """Add method view."""

    context = {
        'pm':[0],
        'len_pm': 1,
    }

    if request.method == 'POST':
        if 'sp-number' in request.POST.keys():
            if request.POST['sp-number'] != None:
                pm = [x for x in range(int(request.POST['sp-number']))]
                len_pm = len(pm)
                if len_pm != 1:
                    context['pm'] = pm
                    context['len_pm'] = len_pm
        else:
            todo = []
            for valor in request.POST.values():
                todo.append(valor)
            metodos = todo[1::3]
            descripciones = todo[2::3]
            usuarios = todo[3::3]
            duplicados = []
            for metodo in metodos:
                try:
                    if metodo == models.Metodo.objects.get(nombre=metodo).nombre:
                            duplicados.append(metodo) 
                            duplicado =  metodos.index(metodo)
                            usuarios.pop(duplicado)
                            descripciones.pop(duplicado)
                            metodos.pop(duplicado)
                except:
                    continue
            for nombre, descripcion, usuario in zip(metodos, descripciones, usuarios):
                models.Metodo.objects.create(
                    nombre= nombre, 
                    descripcion= descripcion,
                    creator_user=usuario
                    ) 
            
            if duplicados != []:
                if len(duplicados)==1:
                    error_duplicados = f'El método {duplicados[0]}, ya se encuentra en la base de datos.'
                else:
                    error_duplicados = f'Los métodos: {list_to_string(duplicados)}, ya se encuentran en la base de datos.'

                context['error_duplicados'] = error_duplicados

            else:
                return redirect('lims:methods')

    
    return render(request, 'LIMS/add_method.html', context)


@login_required
@user_passes_test(is_commercial, login_url='lims:index')
def containers(request):
    '''Containers view.'''

    queryset_envases = models.Envase.objects.all().order_by('nombre')
    paginator = Paginator(queryset_envases, 35)
    page = request.GET.get('page')
    envases = paginator.get_page(page)
    user = request.user
    manager = user.groups.filter(name='manager').exists()
    
    if request.method == 'POST':
        if 'excel_file' in request.POST.keys():
            if request.POST['excel_file'] == '':
                pass
        
        elif request.FILES['excel_file']:
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)

            responsable_de_analisis = models.User.objects.get(pk=request.POST['responsable_de_analisis'])
            
            for index, row in df.iterrows():
                if   models.Envase.objects.filter(codigo=row['Código Envase']).exists():
                    continue
                else:
                    if type(row['Preservante']) == str: preservante = row['Preservante']
                    else: preservante = '-'

                    if type(row['Volumen']) == str: volumen = row['Volumen']
                    else: volumen = '-'

                    models.Envase.objects.create(
                        codigo = row['Código Envase'], 
                        nombre= row['Descripción'],
                        volumen = volumen,
                        material = row['Material'],
                        preservante = preservante,
                        creator_user = responsable_de_analisis)
        return redirect(request.META.get('HTTP_REFERER', '/'))

    return render(request, 'LIMS/containers.html',{
        'envases': envases,
        'manager': manager,
    })


@login_required
@user_passes_test(is_manager, login_url='lims:index')
def add_container(request):
    """Add container view."""

    if request.method == 'POST':
        codigo = request.POST['codigo']
        nombre = request.POST['nombre']
        volumen = request.POST['volumen']
        material = request.POST['material']
        preservante = request.POST['preservante']
        usuario = request.POST['creador']
        models.Envase.objects.create(
            codigo= codigo,
            nombre=nombre, 
            volumen=volumen, 
            material=material, 
            preservante=preservante, 
            creator_user=usuario
            )

        return redirect('lims:containers')

    return render(request, 'LIMS/add_containers.html')


@login_required
@user_passes_test(is_commercial, login_url='lims:index')
def filters(request):
    '''Filters view.'''

    queryset_filters = models.Filtro.objects.all().order_by('codigo')
    paginator = Paginator(queryset_filters, 35)
    page = request.GET.get('page')
    filtros = paginator.get_page(page)
    user = request.user
    manager = user.groups.filter(name='manager').exists()
    
    if request.method == 'POST':
        if 'excel_file' in request.POST.keys():
            if request.POST['excel_file'] == '':
                pass
        
        elif request.FILES['excel_file']:
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)

            responsable_de_analisis = models.User.objects.get(pk=request.POST['responsable_de_analisis'])
            
            for index, row in df.iterrows():
                if   models.Filtro.objects.filter(codigo=row['Código Filtro']).exists():
                    continue
                else:

                    models.Filtro.objects.create(
                        codigo = row['Código Filtro'], 
                        descripcion = row['Descripción'],
                        creator_user = responsable_de_analisis)
        return redirect(request.META.get('HTTP_REFERER', '/'))

    return render(request, 'LIMS/filters.html',{
        'filtros': filtros,
        'manager': manager,
    })


@login_required
@user_passes_test(is_manager, login_url='lims:index')
def add_filter(request):
    """Add filter view."""

    if request.method == 'POST':
        codigo = request.POST['codigo']
        nombre = request.POST['nombre']
        volumen = request.POST['volumen']
        material = request.POST['material']
        preservante = request.POST['preservante']
        usuario = request.POST['creador']
        models.Envase.objects.create(
            codigo = codigo,
            nombre=nombre, 
            creator_user=usuario
            )

        return redirect('lims:filters')

    return render(request, 'LIMS/add_filters.html')


@login_required
@user_passes_test(is_commercial, login_url='lims:index')
def parameters(request):
    '''Parameters view.'''

    metodos = models.Metodo.objects.all()
    queryset_parameters = models.ParametroEspecifico.objects.all().order_by('ensayo', 'codigo')
    user = request.user
    manager = user.groups.filter(name='manager').exists()
   
    if request.method == 'POST':
        if 'search_text' in request.POST.keys():
            if request.POST['search_text'] == '' or request.POST['buscar'] == '':
                queryset_parameters = models.ParametroEspecifico.objects.all().order_by('ensayo')

            if request.POST['buscar'] == 'ensayo':
                queryset_parameters = models.ParametroEspecifico.objects.filter(ensayo__icontains=request.POST['search_text']).order_by('ensayo')

            if request.POST['buscar'] == 'codigo':
                queryset_parameters = models.ParametroEspecifico.objects.filter(codigo__icontains=request.POST['search_text']).order_by('ensayo')

            if request.POST['buscar'] == 'metodo':
                queryset_parameters = models.ParametroEspecifico.objects.filter(metodo__icontains=request.POST['search_text']).order_by('ensayo')
                
    paginator = Paginator(queryset_parameters, 35)
    page = request.GET.get('page')
    parameters = paginator.get_page(page)
    return render(request, 'LIMS/parameters.html', {
        'parameters': parameters,
        'metodos': metodos,
        'manager': manager,
    })


@login_required
@user_passes_test(is_manager, login_url='lims:index')
def add_parameter(request):
    """Add parameter view."""

    metodos = models.Metodo.objects.all().order_by('nombre')
    tipos_de_muestras = models.TipoDeMuestra.objects.all().order_by('nombre')
    envases = models.Envase.objects.all().order_by('codigo')
    
    context = {
        'metodos': metodos,
        'tipos_de_muestras': tipos_de_muestras,
        'envases': envases,
    }

    if request.method == 'POST':
        ensayo = request.POST['ensayo']
        codigo = request.POST['codigo']
        metodo = request.POST['metodo']
        acreditado = request.POST['acreditado']
        ldm = request.POST['LDM']
        if ldm=='': ldm = '-'
        lcm = request.POST['LCM']
        if lcm=='': lcm = '-'
        unidad = request.POST['unidad']
        if unidad=='': unidad = '-'
        envase = request.POST['envase']
        envase = models.Envase.objects.get(codigo=envase)
        tipo_de_muestra = request.POST['tipo_de_muestra']
        creator_user = request.POST['creator_user']

        try:
            models.ParametroEspecifico.objects.create(ensayo=ensayo, codigo= codigo, metodo= metodo, LDM= ldm, LCM= lcm, unidad=unidad, tipo_de_muestra= tipo_de_muestra, envase_id=envase, acreditado=acreditado, creator_user= creator_user)
            return redirect('lims:parameters')
        except:
            error = 'EL código del parametro ya existe.'
            context['error'] = error

    return render(request, 'LIMS/add_parameter.html', context)
    

@login_required
@user_passes_test(is_manager, login_url='lims:index')
def edit_parameter(request, parameter_id):
    """Add parameter view."""

    parameter = models.ParametroEspecifico.objects.get(codigo=parameter_id)    
    context = {
        'parameter': parameter,
    }

    if request.method == 'POST':
        acreditado = request.POST['acreditado']
        if acreditado == '':
            parameter.acreditado = 'nan'
        else: parameter.acreditado = acreditado
        parameter.updated_at = datetime.now()
        parameter.save()

    return render(request, 'LIMS/edit_parameter.html', context)


@login_required
@user_passes_test(is_commercial, login_url='lims:index')
def samples_type(request):
    """Samples type view."""

    queryset_samples_type = models.TipoDeMuestra.objects.all().order_by('nombre')
    paginator = Paginator(queryset_samples_type, 35)
    page = request.GET.get('page')
    samples_type = paginator.get_page(page)
    user = request.user
    manager = user.groups.filter(name='manager').exists()
    
    return render(request, 'LIMS/samples_type.html', {
        'samples_type':samples_type,
        'manager': manager,
    })


@login_required
@user_passes_test(is_manager, login_url='lims:index')
def add_sample_type(request):
    """Add Standards of reference view."""

    context = {
        'pm':[0],
        'len_pm': 1,
    }

    if request.method == 'POST':
        if 'sp-number' in request.POST.keys():
            if request.POST['sp-number'] != None:
                pm = [x for x in range(int(request.POST['sp-number']))]
                len_pm = len(pm)
                if len_pm != 1:
                    context['pm'] = pm
                    context['len_pm']: len_pm
        else:
            todo = []
            for valor in request.POST.values():
                todo.append(valor)
            nombres = todo[1::2]
            usuarios = todo[2::2]
            duplicados = []
            for nombre in nombres:
                try:
                    if nombre == models.TipoDeMuestra.objects.get(nombre=nombre).nombre:
                            duplicados.append(nombre) 
                            duplicado =  nombres.index(nombre)
                            usuarios.pop(duplicado)
                            nombres.pop(duplicado)
                except:
                    continue
            for nombre, usuario in zip(nombres, usuarios):
                models.TipoDeMuestra.objects.create(
                    nombre=nombre, 
                    creator_user=usuario
                    ) 
            
            if duplicados != []:
                if len(duplicados)==1:
                    error_duplicados = f'El tipo de muestra {duplicados[0]}, ya se encuentra en la base de datos.'
                else:
                    error_duplicados = f'Los tipos de muestra: {list_to_string(duplicados)}, ya se encuentran en la base de datos.'
                
                context['error_duplicados'] = error_duplicados
            
            else:
                return redirect('lims:samples_type')

    return render(request, 'LIMS/add_sample_type.html', context)


@login_required
@user_passes_test(is_commercial, login_url='lims:index')
def etfa(request):
    """ETFA view."""

    queryset_services = models.ParametroEspecifico.objects.exclude(Q(codigo_etfa = None) | Q(codigo_etfa='Cálculo')).order_by('codigo_etfa')
    user = request.user
    manager = user.groups.filter(name='manager').exists()

    if request.method == 'POST':
        if 'search_text' in request.POST.keys():
            if request.POST['search_text'] == '' or request.POST['buscar'] == '':
                pass

            elif request.POST['buscar'] == 'autorizacion':
                queryset_services = queryset_services.filter(codigo_etfa__contains=request.POST['search_text'])

            elif request.POST['buscar'] == 'ensayo':
                queryset_services = queryset_services.filter(ensayo__contains=request.POST['search_text'])

            elif request.POST['buscar'] == 'codigo':
                queryset_services = queryset_services.filter(codigo__icontains=request.POST['search_text'])


            elif request.POST['buscar'] == 'metodo':
                queryset_services = queryset_services.filter(metodo__contains=request.POST['search_text'])


    paginator = Paginator(queryset_services, 35)
    page = request.GET.get('page')
    services = paginator.get_page(page)
    return render(request, 'LIMS/etfa.html',{
        'services':services,
        'manager': manager,
    })


@login_required
@user_passes_test(is_manager, login_url='lims:index')
def add_etfa(request):
    """Add ETFA view."""

    parameters = models.ParametroEspecifico.objects.filter(Q(codigo_etfa = None)|Q(codigo_etfa='nan')).order_by('codigo')
    
    if request.method == 'POST':
        parametro = models.ParametroEspecifico.objects.get(id=request.POST['parametro'])
        parametro.codigo_etfa = request.POST['codigo']
        parametro.save()
        return redirect('lims:etfa')

    return  render(request, 'LIMS/add_etfa.html', {
        'parameters': parameters,
    })


@login_required
@user_passes_test(is_manager, login_url='lims:index')
def delete_etfa(request, parameter_id):
    parameter = models.ParametroEspecifico.objects.get(id=parameter_id)
    parameter.codigo_etfa = None
    parameter.updated_at = datetime.now()
    parameter.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))
    

@login_required
@user_passes_test(is_commercial_or_income, login_url='lims:index')
def project(request, project_id):
    """Project view."""

    project = models.Proyecto.objects.get(pk = project_id)
    cliente = models.Cliente.objects.get(pk=project.cliente_id)
    sample_points = models.PuntoDeMuestreo.objects.filter(cliente_id=cliente.id)
    queryset_services = models.Servicio.objects.filter(proyecto_id=project_id).order_by('-created', 'codigo')
    paginator = Paginator(queryset_services, 20)
    page = request.GET.get('page')
    services = paginator.get_page(page)
    queryset_models = models.ModeloDeServicioDeFiltro.objects.filter(proyecto_id=project_id).order_by('-created', 'codigo_modelo')
    paginator = Paginator(queryset_models, 20)
    page = request.GET.get('page')
    modelos = paginator.get_page(page)
    parameters_service = models.ParametroDeMuestra.objects.all()
    
    return render(request, 'LIMS/project.html', {
        'project': project, 
        'cliente': cliente,
        'sample_points': sample_points,
        'services': services,
        'modelos': modelos,
        'parameters': parameters_service,
    })


@login_required
@user_passes_test(is_commercial_or_income, login_url='lims:index')
def project_cot(request, project_id):
    """Project view."""

    project = models.Proyecto.objects.get(pk = project_id)
    cliente = models.Cliente.objects.get(pk=project.cliente_id)
    sample_points = models.PuntoDeMuestreo.objects.filter(cliente_id=cliente.id)
    queryset_services = models.Servicio.objects.filter(proyecto_id=project_id).order_by('-created', 'codigo')
    paginator = Paginator(queryset_services, 20)
    page = request.GET.get('page')
    services = paginator.get_page(page)
    parameters_service = models.ParametroDeMuestra.objects.all()
    parametros_cotizados = project.parametros_cotizados.all()
    # parametros_externos = project.parametros_externos.all()

    context = {
        'project': project, 
        'cliente': cliente,
        'sample_points': sample_points,
        'services': services,
        'parameters': parameters_service,
        'parametros_cotizados':parametros_cotizados,
        # 'parametros_externos': parametros_externos,
    }
    if project.rCA != None: 
        rca = models.RCACliente.objects.get(id=project.rCA)
        context['rca'] = rca
    
    return render(request, 'LIMS/project_cot.html', context)


@login_required
@user_passes_test(is_commercial, login_url='lims:project')
def add_service(request, project_id):
    """Add service view."""

    project = models.Proyecto.objects.get(pk = project_id)
    cliente = models.Cliente.objects.get(pk=project.cliente_id)
    sample_points = models.PuntoDeMuestreo.objects.filter(cliente_id=cliente.id).order_by('nombre')
    monitoring_places = models.LugarDeMonitoreo.objects.filter(cliente_id=cliente.id).order_by('nombre')
    rcas = models.RCACliente.objects.filter(cliente_id=cliente.id).order_by('rca_asociada')
    representantes_legales = models.RepresentanteLegalCliente.objects.filter(cliente_id=cliente.id).order_by('nombre')
    tipo_de_muestra = models.TipoDeMuestra.objects.all().order_by('nombre')
    tipo_muestra = ''
    parametros = models.ParametroEspecifico.objects.all().order_by('codigo')
    normas = models.NormaDeReferencia.objects.all().order_by('norma')
    
    if request.method == 'POST':

        if 'tipo_muestra' in request.POST:
            tipo_de_muestra = models.TipoDeMuestra.objects.filter(nombre= request.POST['tipo_muestra']).order_by('nombre')
            tipo_muestra = request.POST['tipo_muestra']
            parametros = parametros.filter(tipo_de_muestra= tipo_muestra)
        else:
            proyecto = request.POST['proyecto']
            cliente = request.POST['cliente']
            punto_de_muestreo = request.POST['punto_de_muestreo']
            area = request.POST['area']
            tipo_de_muestra = request.POST['tipo_de_muestra']
            fecha_de_muestreo = request.POST['fecha_de_muestreo']
            observacion = request.POST['observacion']
            habiles = request.POST['habiles']
            fecha_de_contenedores = request.POST['fecha_de_contenedores']
            norma_de_referencia = request.POST['norma_de_referencia']
            representante_legal = request.POST['representante_legal']
            rCA = request.POST['rCA']
            etfa = False
            muestreado_por_algoritmo = request.POST['muestreado_por_algoritmo']
            creator_user = request.POST['creator_user']
            parameters = request.POST.getlist('parameters')
            
            parameters = calc_param_no_etfa(parameters=parameters)

            envases = calc_envases(parameters=parameters)

            fecha_de_muestreo= datetime.strptime(fecha_de_muestreo, "%Y-%m-%d")
            fecha_de_entrega_cliente = add_workdays(fecha_de_muestreo, int(habiles))
            current_year = datetime.now().year
            current_year = str(current_year)[2:]

            if models.Servicio.objects.exists()==False:
                codigo_de_servicio = ('1').zfill(5)
                codigo_generado = f'{codigo_de_servicio}-{current_year}'
            if models.Servicio.objects.filter(codigo_muestra__endswith = '-'+current_year).exists()!=False:
                last_service = models.Servicio.objects.filter(codigo_muestra__endswith = '-'+current_year).latest('codigo_muestra')

                if last_service.codigo_muestra[-2:] != current_year: 
                    codigo_central = ('1').zfill(5)
                    codigo_generado = f'{codigo_central}-{current_year}'
                
                elif models.Servicio.objects.exists()==True and last_service.codigo_muestra[-2:] == current_year:
                    codigo_de_servicio = str(int(last_service.codigo_muestra[-7:-3]) +1).zfill(5)
                    codigo_generado = f'{codigo_de_servicio}-{current_year}'
            
            if norma_de_referencia == '': norma_de_referencia = None
            else: norma_de_referencia = norma_de_referencia

            if rCA == '': rCA = None
            else: rCA = rCA

            if observacion == '': observacion = None
            else: observacion = observacion

            if representante_legal == '': representante_legal = None
            else: representante_legal = models.RepresentanteLegalCliente.objects.get(id=representante_legal)

            

            models.Servicio.objects.create(
                codigo = codigo_de_servicio,
                codigo_muestra = codigo_generado, 
                proyecto_id = proyecto, 
                area = area,
                punto_de_muestreo = punto_de_muestreo,
                tipo_de_muestra = tipo_de_muestra,
                fecha_de_muestreo = fecha_de_muestreo,
                observacion = observacion,
                fecha_de_entrega_cliente = fecha_de_entrega_cliente,
                fecha_de_contenedores_o_filtros = fecha_de_contenedores,
                norma_de_referencia = norma_de_referencia,
                representante_legal= representante_legal,
                rCA = rCA,
                etfa = etfa,
                envases = envases,
                muestreado_por_algoritmo = muestreado_por_algoritmo,
                creator_user = creator_user,
                cliente = cliente,
                created = datetime.now()
                )                    

            for pid in parameters:
                ensayo = models.ParametroEspecifico.objects.get(pk=pid)
                models.ParametroDeMuestra.objects.create(
                    servicio_id = codigo_de_servicio, 
                    parametro_id= pid,
                    ensayo= ensayo.codigo, 
                    codigo_servicio= codigo_generado,
                    creator_user = creator_user,
                    created = datetime.now()
                    )

            return redirect('lims:project', project_id)
        
    return render(request, 'LIMS/add_service.html', {
        'project': project, 
        'cliente': cliente,
        'sample_points': sample_points,
        'monitoring_places': monitoring_places,
        'rcas': rcas,
        'tipo_de_muestra': tipo_muestra,
        'tipos_de_muestras': tipo_de_muestra,
        'parameters': parametros,
        'normas': normas,
        'representantes_legales': representantes_legales,
    })


@login_required
@user_passes_test(is_commercial, login_url='lims:project')
def add_service_etfa(request, project_id):
    """Add service view."""

    project = models.Proyecto.objects.get(pk = project_id)
    cliente = models.Cliente.objects.get(pk=project.cliente_id)
    sample_points = models.PuntoDeMuestreo.objects.filter(cliente_id=cliente.id).order_by('nombre')
    monitoring_places = models.LugarDeMonitoreo.objects.filter(cliente_id=cliente.id).order_by('nombre')
    rcas = models.RCACliente.objects.filter(cliente_id=cliente.id).order_by('rca_asociada')
    representantes_legales = models.RepresentanteLegalCliente.objects.filter(cliente_id=cliente.id).order_by('nombre')
    tipo_de_muestra = models.TipoDeMuestra.objects.all().order_by('nombre')
    tipo_muestra = ''
    parametros = models.ParametroEspecifico.objects.exclude(Q(codigo_etfa = 'nan') | Q(codigo_etfa = None) | Q(codigo_etfa='Cálculo')).order_by('ensayo')
    parametros_externos = models.ParametroEspecifico.objects.exclude(Q(codigo_etfa='Cálculo') | Q(codigo_etfa='Cálculo-E')).order_by('ensayo')
    normas = models.NormaDeReferencia.objects.all().order_by('norma')
                        

    if request.method == 'POST':

        if 'tipo_muestra' in request.POST:
            tipo_de_muestra = models.TipoDeMuestra.objects.filter(nombre= request.POST['tipo_muestra']).order_by('nombre')
            tipo_muestra = request.POST['tipo_muestra']
            parametros = parametros.filter(tipo_de_muestra= tipo_muestra).order_by('codigo')
            parametros_externos = parametros_externos.filter(tipo_de_muestra= tipo_muestra).order_by('codigo')
        else:
            proyecto = request.POST['proyecto']
            cliente = request.POST['cliente']
            punto_de_muestreo = request.POST['punto_de_muestreo']
            tipo_de_muestra = request.POST['tipo_de_muestra']
            area = request.POST['area']
            fecha_de_muestreo = request.POST['fecha_de_muestreo']
            observacion = request.POST['observacion']
            habiles = request.POST['habiles']
            fecha_de_contenedores = request.POST['fecha_de_contenedores']
            norma_de_referencia = request.POST['norma_de_referencia']
            rCA = request.POST['rCA']
            representante_legal = models.RepresentanteLegalCliente.objects.get(id=request.POST['representante_legal']) 
            etfa = True
            muestreado_por_algoritmo = request.POST['muestreado_por_algoritmo']
            creator_user = request.POST['creator_user']
            parameters = request.POST.getlist('parameters')
            parameters_analisis_externos = request.POST.getlist('analisis_externos')
            

            parameters, parameters_analisis_externos = calc_param_etfa(parameters=parameters, parameters_analisis_externos=parameters_analisis_externos)
            
            envases = calc_envases(parameters=parameters)
            
            fecha_de_muestreo= datetime.strptime(fecha_de_muestreo, "%Y-%m-%d")
            fecha_de_entrega_cliente = add_workdays(fecha_de_muestreo, int(habiles))
            current_year = datetime.now().year
            current_year = str(current_year)[2:]


            if models.Servicio.objects.exists()==False:
                codigo_de_servicio = ('1').zfill(5)
                codigo_generado = f'{codigo_de_servicio}-{current_year}'
            
            if models.Servicio.objects.filter(codigo_muestra__endswith = '-'+current_year).exists()!=False:
                last_service = models.Servicio.objects.filter(codigo_muestra__endswith = '-'+current_year).latest('codigo_muestra')

                if last_service.codigo_muestra[-2:] != current_year: 
                    codigo_central = ('1').zfill(5)
                    codigo_generado = f'{codigo_central}-{current_year}'
                
                elif models.Servicio.objects.exists()==True and last_service.codigo_muestra[-2:] == current_year:
                    codigo_de_servicio = str(int(last_service.codigo_muestra[-7:-3]) +1).zfill(5)
                    codigo_generado = f'{codigo_de_servicio}-{current_year}'
            if norma_de_referencia == '': norma_de_referencia = None
            else: norma_de_referencia = norma_de_referencia
            
            if observacion == '': observacion = None
            else: observacion = observacion

            models.Servicio.objects.create(
                codigo = codigo_de_servicio,
                codigo_muestra = codigo_generado, 
                proyecto_id = proyecto, 
                punto_de_muestreo = punto_de_muestreo,
                area= area,
                tipo_de_muestra = tipo_de_muestra,
                fecha_de_muestreo = fecha_de_muestreo,
                observacion = observacion,
                fecha_de_entrega_cliente = fecha_de_entrega_cliente,
                fecha_de_contenedores_o_filtros = fecha_de_contenedores,
                norma_de_referencia = norma_de_referencia,
                rCA = rCA,
                etfa = etfa,
                envases = envases,
                muestreado_por_algoritmo = muestreado_por_algoritmo,
                representante_legal = representante_legal,
                creator_user = creator_user,
                cliente = cliente,
                created = datetime.now()
                )                    

            for pid in parameters:
                ensayo = models.ParametroEspecifico.objects.get(pk=pid)
                models.ParametroDeMuestra.objects.create(
                    servicio_id = codigo_de_servicio, 
                    parametro_id= pid,
                    ensayo= ensayo.codigo, 
                    codigo_servicio= codigo_generado,
                    creator_user = creator_user,
                    created = datetime.now()
                    )
            
            if len(parameters_analisis_externos)>0:
                for pid in parameters_analisis_externos:
                    ensayo = models.ParametroEspecifico.objects.get(pk=pid)
                    models.ParametroDeMuestra.objects.create(
                        servicio_id = codigo_de_servicio, 
                        parametro_id= pid,
                        ensayo= ensayo.codigo, 
                        codigo_servicio= codigo_generado,
                        analisis_externos = True,
                        creator_user = creator_user,
                        created = datetime.now()
                        )

            return redirect('lims:project', project_id)
        
    return render(request, 'LIMS/add_service_etfa.html', {
        'project': project, 
        'cliente': cliente,
        'sample_points': sample_points,
        'monitoring_places': monitoring_places,
        'rcas': rcas,
        'tipo_de_muestra': tipo_muestra,
        'tipos_de_muestras': tipo_de_muestra,
        'parameters': parametros,
        'parameters_externos': parametros_externos,
        'normas': normas,
        'representantes_legales': representantes_legales,
    })


@login_required
@user_passes_test(is_income, login_url='lims:services')
def add_reception_observation(request, service_id):
    service = models.Servicio.objects.get(pk = service_id)
    if request.method == 'POST':
        service.observacion_de_recepcion = request.POST['observacion']
        service.updated_at = datetime.now()
        service.save()

        return redirect('lims:services')
    return render(request, 'LIMS/add_reception_observation.html')


@login_required
@user_passes_test(is_commercial, login_url='lims:project')
def add_model_service(request, project_id):
    """Add service view."""

    project = models.Proyecto.objects.get(pk = project_id)
    cliente = models.Cliente.objects.get(pk=project.cliente_id)
    sample_points = models.PuntoDeMuestreo.objects.filter(cliente_id=cliente.id).order_by('nombre')
    monitoring_places = models.LugarDeMonitoreo.objects.filter(cliente_id=cliente.id).order_by('nombre')
    rcas = models.RCACliente.objects.filter(cliente_id=cliente.id).order_by('rca_asociada')
    tipo_de_muestra = models.TipoDeMuestra.objects.all().order_by('nombre')
    tipo_muestra = ''
    parametros = models.ParametroEspecifico.objects.all().order_by('ensayo')
    normas = models.NormaDeReferencia.objects.all().order_by('norma')
    filtros = models.Filtro.objects.all().order_by('codigo')         

    if request.method == 'POST':

        if 'tipo_muestra' in request.POST:
            tipo_de_muestra = models.TipoDeMuestra.objects.filter(nombre= request.POST['tipo_muestra']).order_by('nombre')
            tipo_muestra = request.POST['tipo_muestra']
            parametros = parametros.filter(tipo_de_muestra= tipo_muestra).order_by('codigo')
        else:
            proyecto = request.POST['proyecto']
            cliente = request.POST['cliente']
            punto_de_muestreo = request.POST['punto_de_muestreo']
            tipo_de_muestra = request.POST['tipo_de_muestra']
            filtro = request.POST['filtro']
            area = request.POST['area']
            observacion = request.POST['observacion']
            norma_de_referencia = request.POST['norma_de_referencia']
            rCA = request.POST['rCA']
            muestreado_por_algoritmo = request.POST['muestreado_por_algoritmo']
            creator_user = request.POST['creator_user']
            parameters = request.POST.getlist('parameters')

            current_year = datetime.now().year
            current_year = str(current_year)[2:]


            if models.ModeloDeServicioDeFiltro.objects.exists()==False:
                codigo_de_modelo = ('1').zfill(5)
                codigo_generado = f'M-{codigo_de_modelo}-{current_year}'

            if models.ModeloDeServicioDeFiltro.objects.filter(codigo_modelo__endswith = '-'+current_year).exists()!=False:
                last_service = models.ModeloDeServicioDeFiltro.objects.filter(codigo_modelo__endswith = '-'+current_year).latest('codigo_modelo')

                if last_service.codigo_modelo[-2:] != current_year: 
                    codigo_central = ('1').zfill(5)
                    codigo_generado = f'M-{codigo_central}-{current_year}'
                
                elif models.ModeloDeServicioDeFiltro.objects.exists()==True and last_service.codigo_modelo[-2:] == current_year:
                    codigo_de_modelo = str(int(last_service.codigo_modelo[-7:-3]) +1).zfill(5)
                    codigo_generado = f'M-{codigo_de_modelo}-{current_year}'  
            

            modelo = models.ModeloDeServicioDeFiltro.objects.create(
                codigo_modelo =codigo_generado ,
                proyecto_id = proyecto, 
                punto_de_muestreo = punto_de_muestreo,
                area= area,
                tipo_de_muestra = tipo_de_muestra,
                filtro = models.Filtro.objects.get(codigo = filtro),
                observacion = observacion,
                norma_de_referencia = norma_de_referencia,
                rCA = rCA,
                muestreado_por_algoritmo = muestreado_por_algoritmo,
                creator_user = creator_user,
                cliente = cliente,
                created = datetime.now()
                )  

            modelo.parametros.set(parameters)            

            return redirect('lims:project', project_id)
        
    return render(request, 'LIMS/add_model_service.html', {
        'project': project, 
        'cliente': cliente,
        'sample_points': sample_points,
        'monitoring_places': monitoring_places,
        'rcas': rcas,
        'tipo_de_muestra': tipo_muestra,
        'tipos_de_muestras': tipo_de_muestra,
        'parameters': parametros,
        'normas': normas,
        'filtros': filtros,
    })


@login_required
@user_passes_test(is_commercial_or_income, login_url='lims:index')
def modelo(request, model_id):
    modelo = models.ModeloDeServicioDeFiltro.objects.get(codigo_modelo = model_id)
    parameters = modelo.parametros.all()

    context = {
        'modelo': modelo,
        'parameters': parameters,
    }
    return render(request, 'LIMS/modelo.html', context)


@login_required
@user_passes_test(is_income, login_url='lims:modelo')
def generate_service(request, model_id):

    modelo = models.ModeloDeServicioDeFiltro.objects.get(codigo_modelo = model_id)
    parameters = modelo.parametros.all()

    if request.method == 'POST':

        fecha_de_muestreo = request.POST['fecha_de_muestreo']
        habiles = request.POST['habiles']
        observacion = request.POST['observacion']
        creator_user = request.POST['creator_user']
        fecha_de_envio = request.POST['fecha_de_envio']

        fecha_de_muestreo= datetime.strptime(fecha_de_muestreo, "%Y-%m-%d")
        fecha_de_entrega_cliente = add_workdays(fecha_de_muestreo, int(habiles))
        current_year = datetime.now().year
        current_year = str(current_year)[2:]


        if models.Servicio.objects.exists()==False:
            codigo_de_servicio = ('1').zfill(5)
            codigo_generado = f'{codigo_de_servicio}-{current_year}'
        
        if models.Servicio.objects.filter(codigo_muestra__endswith = '-'+current_year).exists()!=False:
            last_service = models.Servicio.objects.filter(codigo_muestra__endswith = '-'+current_year).latest('codigo_muestra')

            if last_service.codigo_muestra[-2:] != current_year: 
                codigo_central = ('1').zfill(5)
                codigo_generado = f'{codigo_central}-{current_year}'
            
            elif models.Servicio.objects.exists()==True and last_service.codigo_muestra[-2:] == current_year:
                codigo_de_servicio = str(int(last_service.codigo_muestra[-7:-3]) +1).zfill(5)
                codigo_generado = f'{codigo_de_servicio}-{current_year}'
            
            models.Servicio.objects.create(
                codigo = codigo_de_servicio,
                codigo_muestra = codigo_generado, 
                proyecto_id = modelo.proyecto.codigo, 
                punto_de_muestreo = modelo.punto_de_muestreo,
                area= modelo.area,
                tipo_de_muestra = modelo.tipo_de_muestra,
                fecha_de_muestreo = fecha_de_muestreo,
                observacion = observacion,
                fecha_de_entrega_cliente = fecha_de_entrega_cliente,
                fecha_de_contenedores_o_filtros = fecha_de_envio,
                filtros = modelo.filtro,
                norma_de_referencia = modelo.norma_de_referencia.id,
                rCA = modelo.rCA.id,
                muestreado_por_algoritmo = modelo.muestreado_por_algoritmo,
                creator_user = creator_user,
                cliente = modelo.cliente.id,
                created = datetime.now()
                )                    

            for p in parameters:
                models.ParametroDeMuestra.objects.create(
                    servicio_id = codigo_de_servicio, 
                    parametro_id= p.id,
                    ensayo= p.codigo, 
                    codigo_servicio= codigo_generado,
                    creator_user = creator_user,
                    created = datetime.now()
                    )

            return redirect('lims:project', modelo.proyecto.codigo)
        
        

    return render(request, 'LIMS/generate_service_filter.html')

@login_required
@user_passes_test(is_commercial, login_url='lims:project_cot')
def clone_service(request, service_id):
    """Clone service view."""

    service = models.Servicio.objects.get(pk = service_id)
    proyectos = models.Proyecto.objects.filter(cliente_id = service.proyecto.cliente)
    parameters = models.ParametroDeMuestra.objects.filter(codigo_servicio = service.codigo_muestra)
    parameters = [p.parametro_id for p in parameters]
    rcas = models.RCACliente.objects.filter(cliente_id = service.proyecto.cliente)
    sample_points = models.PuntoDeMuestreo.objects.filter(cliente_id= service.proyecto.cliente)
    normas = models.NormaDeReferencia.objects.all()
    tipos_de_muestras = models.TipoDeMuestra.objects.all()

    context = {
        'service': service,
        'proyectos': proyectos,
        'parameters': parameters,
        'rcas': rcas,
        'normas': normas,
        'sample_points': sample_points,
        'tipos_de_muestras': tipos_de_muestras,
    }

    if request.method == 'POST':
        proyecto = request.POST['proyecto']
        project = models.Proyecto.objects.get(pk = proyecto)

        parameters_cot = project.parametros_cotizados.all()
        parameters_cot = [p.id for p  in parameters_cot]

        def comprobador_de_parametros(parameters=parameters, parameters_cot= parameters_cot):
            for p in parameters:
                if p not in parameters_cot:
                    return False
                else: continue
            return True

        punto_de_muestreo = request.POST['punto_de_muestreo']
        fecha_de_muestreo = request.POST['fecha_de_muestreo']
        observacion = request.POST['observacion']
        habiles = request.POST['habiles']
        fecha_de_contenedores = request.POST['fecha_de_contenedores']
        norma_de_referencia = request.POST['norma_de_referencia']
        rCA = request.POST['rCA']
        muestreado_por_algoritmo = request.POST['muestreado_por_algoritmo']
        creator_user = request.POST['creator_user']
        
        fecha_de_muestreo= datetime.strptime(fecha_de_muestreo, "%Y-%m-%d")
        fecha_de_entrega_cliente = add_workdays(fecha_de_muestreo, int(habiles))
        current_year = datetime.now().year
        current_year = str(current_year)[2:]

        last_service = models.Servicio.objects.filter(codigo_muestra__endswith = '-'+current_year).latest('codigo_muestra')

        if models.Servicio.objects.exists()==False:
            codigo_de_servicio = ('1').zfill(5)
            codigo_generado = f'{codigo_de_servicio}-{current_year}'
        
        if models.Servicio.objects.filter(codigo_muestra__endswith = '-'+current_year).exists()!=False:
            last_service = models.Servicio.objects.filter(codigo_muestra__endswith = '-'+current_year).latest('codigo_muestra')

            if last_service.codigo_muestra[-2:] != current_year: 
                codigo_central = ('1').zfill(5)
                codigo_generado = f'{codigo_central}-{current_year}'
            
            elif models.Servicio.objects.exists()==True and last_service.codigo_muestra[-2:] == current_year:
                codigo_de_servicio = str(int(last_service.codigo_muestra[-7:-3]) +1).zfill(5)
                codigo_generado = f'{codigo_de_servicio}-{current_year}'

 
        if len(parameters_cot)==0 or comprobador_de_parametros():
            for sp in sample_points:
                if int(punto_de_muestreo) == int(sp.id):   
                    models.Servicio.objects.create(
                        codigo = codigo_de_servicio,
                        codigo_muestra = codigo_generado, 
                        proyecto_id = proyecto, 
                        punto_de_muestreo = sp.nombre,
                        tipo_de_muestra = service.tipo_de_muestra,
                        fecha_de_muestreo = fecha_de_muestreo,
                        observacion = observacion,
                        fecha_de_entrega_cliente = fecha_de_entrega_cliente,
                        fecha_de_contenedores_o_filtros = fecha_de_contenedores,
                        norma_de_referencia = norma_de_referencia,
                        rCA = rCA,
                        etfa = service.etfa,
                        muestreado_por_algoritmo = muestreado_por_algoritmo,
                        creator_user = creator_user,
                        cliente = service.cliente,
                        created = datetime.now()
                        )                    

            for pid in parameters:
                ensayo = models.ParametroEspecifico.objects.get(pk=pid)
                models.ParametroDeMuestra(
                    servicio_id = codigo_de_servicio, 
                    parametro_id= pid,
                    ensayo= ensayo.codigo, 
                    codigo_servicio= codigo_generado,
                    creator_user = creator_user,
                    created = datetime.now()
                    ).save()

            return redirect('lims:project', service.proyecto_id)

        else:
            error = 'No se pudo clonar el servicio debido a que algún parámetro no se encuentra entre los cotizados para el proyecto seleccionado.'
            context['error'] = error


    return render(request, "LIMS/clone_service.html", context)


@login_required
@user_passes_test(is_income, login_url='lims:project_cot')
def add_service_cot(request, project_id):
    """Add service view."""

    project = models.Proyecto.objects.get(pk = project_id)
    parametros_cot = project.parametros_cotizados.all()
    parameters_externos = project.parametros_externos.all()
    cliente = models.Cliente.objects.get(pk=project.cliente_id)
    sample_points = models.PuntoDeMuestreo.objects.filter(cliente_id=cliente.id).order_by('nombre')
    monitoring_places = models.LugarDeMonitoreo.objects.filter(cliente_id=cliente.id).order_by('nombre')
    rcas = models.RCACliente.objects.filter(cliente_id=cliente.id).order_by('rca_asociada')
    tipo_de_muestra = models.TipoDeMuestra.objects.all().order_by('nombre')
    normas = models.NormaDeReferencia.objects.all().order_by('norma')
    
    if request.method == 'POST':
        proyecto = request.POST['proyecto']
        cliente = request.POST['cliente']
        punto_de_muestreo = request.POST['punto_de_muestreo']
        area = request.POST['area']
        fecha_de_muestreo = request.POST['fecha_de_muestreo']
        fecha_de_recepcion = request.POST['fecha_de_recepcion']
        observacion = request.POST['observacion']
        habiles = request.POST['habiles']
        etfa = request.POST['etfa']
        muestreado_por_algoritmo = request.POST['muestreado_por_algoritmo']
        creator_user = request.POST['creator_user']
        parameters = request.POST.getlist('parameters')
        parameters_externos = request.POST.getlist('parameters_externos')
        
        
        fecha_recepcion= datetime.strptime(fecha_de_recepcion[:10], "%Y-%m-%d")
        fecha_de_entrega_cliente = add_workdays(fecha_recepcion, int(habiles))
        current_year = datetime.now().year
        current_year = str(current_year)[2:]

        last_service = models.Servicio.objects.filter(codigo_muestra__endswith = '-'+current_year).latest('codigo_muestra')

        if 'SI' in etfa: 
            etfa=True
        else: 
            etfa=False

        if models.Servicio.objects.exists()==False:
            codigo_de_servicio = ('1').zfill(5)
            codigo_generado = f'{codigo_de_servicio}-{current_year}'
        
        if models.Servicio.objects.filter(codigo_muestra__endswith = '-'+current_year).exists()!=False:
            last_service = models.Servicio.objects.filter(codigo_muestra__endswith = '-'+current_year).latest('codigo_muestra')
            
            if last_service.codigo_muestra[-2:] != current_year: 
                codigo_central = ('1').zfill(5)
                codigo_generado = f'{codigo_central}-{current_year}'
            
            elif models.Servicio.objects.exists()==True and last_service.codigo_muestra[-2:] == current_year:
                codigo_de_servicio = str(int(last_service.codigo_muestra[-7:-3]) +1).zfill(5)
                codigo_generado = f'{codigo_de_servicio}-{current_year}'

        if observacion == '': observacion = None
        else: observacion = observacion    

        models.Servicio.objects.create(
            codigo = codigo_de_servicio,
            codigo_muestra = codigo_generado, 
            proyecto_id = proyecto, 
            punto_de_muestreo = punto_de_muestreo,
            area = area,
            tipo_de_muestra = project.tipo_de_muestra,
            fecha_de_muestreo = fecha_de_muestreo,
            fecha_de_recepcion = fecha_de_recepcion,
            observacion_de_recepcion = observacion,
            fecha_de_entrega_cliente = fecha_de_entrega_cliente,
            norma_de_referencia = project.norma_de_referencia,
            rCA = project.rCA,
            representante_legal = project.representante_legal,
            etfa = etfa,
            muestreado_por_algoritmo = muestreado_por_algoritmo,
            creator_user = creator_user,
            cliente = cliente,
            created = datetime.now()
            )                    

        for pid in parameters:
            ensayo = models.ParametroEspecifico.objects.get(pk=pid)
            models.ParametroDeMuestra.objects.create(
                servicio_id = codigo_de_servicio, 
                parametro_id= pid,
                ensayo= ensayo.codigo, 
                codigo_servicio= codigo_generado,
                creator_user = creator_user,
                created = datetime.now()
                )
        
        if len(parameters_externos)>0:
                for pid in parameters_externos:
                    ensayo = models.ParametroEspecifico.objects.get(pk=pid)
                    models.ParametroDeMuestra.objects.create(
                        servicio_id = codigo_de_servicio, 
                        parametro_id= pid,
                        ensayo= ensayo.codigo, 
                        codigo_servicio= codigo_generado,
                        analisis_externos = True,
                        creator_user = creator_user,
                        created = datetime.now()
                        )

        return redirect('lims:project_cot', project_id)
        
    return render(request, 'LIMS/add_service_cot.html', {
        'project': project, 
        'cliente': cliente,
        'sample_points': sample_points,
        'monitoring_places': monitoring_places,
        'rcas': rcas,
        'tipos_de_muestras': tipo_de_muestra,
        'normas': normas,
        'parametros_cot': parametros_cot,
        'parameters_externos': parameters_externos
    })


@login_required
@user_passes_test(is_commercial, login_url='lims:index')
def add_service_parameter(request, service_id):
    """Add service parameter view."""

    servicio = models.Servicio.objects.get(pk=service_id)
    project = models.Proyecto.objects.get(pk = servicio.proyecto_id)
    parametros = models.ParametroEspecifico.objects.filter(Q(codigo_etfa = None) | Q(codigo_etfa='Cálculo')).order_by('ensayo').filter(tipo_de_muestra=servicio.tipo_de_muestra)
    parametros_muestra = models.ParametroDeMuestra.objects.filter(servicio_id = service_id)
    for pm in parametros_muestra:
        parametros = parametros.exclude(pk= pm.parametro_id)

    if request.method == 'POST':
        creator_user = request.POST['creator_user']
        parameters = request.POST.getlist('parameters')

        for pid in parameters:
            ensayo = models.ParametroEspecifico.objects.get(pk=pid)
            models.ParametroDeMuestra(
                servicio_id = service_id, 
                parametro_id= pid, 
                ensayo= ensayo.codigo,
                codigo_servicio= servicio.codigo_muestra,
                creator_user=creator_user,
                created = datetime.now()
                ).save()

        return redirect('lims:project', servicio.proyecto_id)
    return render(request, 'LIMS/add_service_parameter.html', {
        'project': project, 
        'parameters': parametros,
    })


@login_required
@user_passes_test(is_commercial, login_url='lims:index')
def add_service_parameter_etfa(request, service_id):
    """Add service parameter view."""

    servicio = models.Servicio.objects.get(pk=service_id)
    project = models.Proyecto.objects.get(pk = servicio.proyecto_id)
    parametros = models.ParametroEspecifico.objects.exclude(codigo_etfa = None).order_by('ensayo').filter(tipo_de_muestra=servicio.tipo_de_muestra)
    parametros_muestra = models.ParametroDeMuestra.objects.filter(servicio_id = service_id)
    parametros_en_sevicio = []

    for pm in parametros_muestra:
        parametros = parametros.exclude(pk= pm.parametro_id)
        if pm.analisis_externos == False:
            parametros_en_sevicio.append(models.ParametroEspecifico.objects.get(id= pm.parametro_id).id)
    
    if request.method == 'POST':
        creator_user = request.POST['creator_user']
        parameters = request.POST.getlist('parameters')
        parametros_totales = parameters + parametros_en_sevicio

        for pid in parameters:
            ensayo = models.ParametroEspecifico.objects.get(pk=pid)
            models.ParametroDeMuestra(
                servicio_id = service_id, 
                parametro_id= pid, 
                ensayo= ensayo.codigo,
                codigo_servicio= servicio.codigo_muestra,
                creator_user=creator_user,
                created = datetime.now()
                ).save()
                
        envases = calc_envases(parametros_totales)
        servicio.envases = envases
        servicio.save()

        return redirect('lims:project', servicio.proyecto_id)
    return render(request, 'LIMS/add_service_parameter_etfa.html', {
        'project': project, 
        'parameters': parametros,
    })


@login_required
@user_passes_test(is_commercial_or_income, login_url='lims:index')
def service(request, service_id):
    """Service view."""

    service = models.Servicio.objects.get(pk=service_id)
    client = models.Cliente.objects.get(pk=service.cliente)
    parametros = models.ParametroEspecifico.objects.all().order_by('ensayo')
    queryset_parameters = models.ParametroDeMuestra.objects.filter(servicio_id=service_id).order_by('ensayo')
    paginator = Paginator(queryset_parameters, 10)
    page = request.GET.get('page')
    parameters = paginator.get_page(page)
    project = models.Proyecto.objects.get(pk=service.proyecto_id)
    user = request.user
    manager = user.groups.filter(name='manager').exists()
    comercial = user.groups.filter(name='comercial').exists()
    context = {
        'service': service,
        'client': client,
        'parametros': parametros,
        'parameters': parameters,
        'project': project,
        'manager': manager,
        'total': len(queryset_parameters),
        'comercial': comercial,
    }

    if service.norma_de_referencia != None:
        norma = models.NormaDeReferencia.objects.get(pk=service.norma_de_referencia)
        context['norma'] = norma

    if service.rCA != None:
        rca = models.RCACliente.objects.get(pk=service.rCA)
        context['rca'] = rca
    
    def prog():
        progreso = 0
        for p in queryset_parameters:
            if p.resultado_final!=None: 
                progreso+=1
        analizado = progreso
        return analizado, (progreso/len(queryset_parameters))*100 if analizado!= 0 else 0

    analizado, progreso  = prog()
    context['analizado'] = analizado
    context['progreso'] = progreso

    return render(request, 'LIMS/service.html', context)

 
@login_required 
@user_passes_test(is_manager, login_url='lims:index')
def edit_sample_parameter(request,parameter_id):
    """Edit sample parameter model."""
    
    parametro = models.ParametroDeMuestra.objects.get(id=parameter_id)   
    verify = 'GRV' in parametro.ensayo
    if request.method == 'POST':
        responsable = User.objects.get(pk=request.POST['responsable_de_analisis'])
        parametro.responsable_de_analisis= responsable
        parametro.fecha_de_inicio = request.POST['fecha_de_inicio']
        parametro.fecha_de_terminado = request.POST['fecha_de_terminado']
        
        if verify:
            parametro.peso_inicial = float(request.POST['peso_inicial'].replace(',','.'))
            parametro.peso_final = float(request.POST['peso_final'].replace(',','.'))
        else:
            parametro.resultado = float(request.POST['resultado'].replace(',','.'))
            parametro.factor_de_dilucion = float(request.POST['factor_de_dilucion'].replace(',','.'))
        
        parametro.resultado_final = float(request.POST['resultado_final'].replace(',','.'))
        parametro.creator_user = request.POST['creator_user']
        parametro.updated_at = datetime.now()
        parametro.save()
        
        servicio_id = parametro.servicio_id
        return redirect('lims:service', servicio_id)
    
    return render(request, 'LIMS/edit_sample_parameter.html', {
       'parameter': parametro,
       'verify': verify,
    })


@login_required
@user_passes_test(is_analyst, login_url='lims:index')
def service_parameters(request):
    """Service parameters view."""

    queryset_service_parameters = models.ParametroDeMuestra.objects.exclude(ensayo__icontains='GRV').order_by('-created')
    parameters = set([p.parametro.id for p in queryset_service_parameters])
    parametros = models.ParametroEspecifico.objects.exclude(codigo__icontains = 'GRV').filter(id__in= parameters).order_by('codigo')
    parameters = parametros

    if request.method == 'POST':
        if 'parametro' in request.POST.keys():
            if request.POST['parametro'] == '':
                pass
            else:
                queryset_service_parameters = models.ParametroDeMuestra.objects.filter(parametro_id=request.POST['parametro'])
                queryset_service_parameters = queryset_service_parameters.exclude(ensayo__icontains='GRV').order_by('-created')

        elif 'search_text' in request.POST.keys():
            if request.POST['search_text'] == '' or request.POST['buscar'] == '':
                pass

            elif request.POST['buscar'] == 'servicio':
                queryset_service_parameters = models.ParametroDeMuestra.objects.filter(codigo_servicio__contains=request.POST['search_text'])
                queryset_service_parameters = queryset_service_parameters.exclude(ensayo__icontains='GRV').order_by('-created')

            elif request.POST['buscar'] == 'ensayo':
                queryset_service_parameters = models.ParametroDeMuestra.objects.filter(ensayo__icontains=request.POST['search_text'])
                queryset_service_parameters = queryset_service_parameters.exclude(ensayo__icontains='GRV').order_by('-created')

            elif request.POST['buscar'] == 'inicio':
                queryset_service_parameters = models.ParametroDeMuestra.objects.filter(fecha_de_inicio__contains=request.POST['search_text'])
                queryset_service_parameters = queryset_service_parameters.exclude(ensayo__icontains='GRV').order_by('-created')

        elif 'fecha_de_inicio' in request.POST.keys():
            
            parametro = models.ParametroDeMuestra.objects.get(id=request.POST['parametro_id'])
            responsable = User.objects.get(pk=request.POST['responsable_de_analisis'])
            parametro.responsable_de_analisis= responsable
            fecha_inicio = request.POST['fecha_de_inicio']
            if fecha_inicio.endswith(str(datetime.now().year)):
                fecha_de_inicio = datetime.strptime(fecha_inicio, "%d-%m-%Y")
                parametro.fecha_de_inicio = fecha_de_inicio.strftime("%Y-%m-%d")
            else: parametro.fecha_de_inicio = request.POST['fecha_de_inicio']
            fecha_terminado = request.POST['fecha_de_terminado']
            if fecha_terminado.endswith(str(datetime.now().year)):
                fecha_de_terminado = datetime.strptime(fecha_terminado, "%d-%m-%Y")
                parametro.fecha_de_terminado = fecha_de_terminado.strftime("%Y-%m-%d")
            else: parametro.fecha_de_terminado = request.POST['fecha_de_terminado']
            parametro.resultado = float(request.POST['resultado'].replace(',','.'))
            parametro.factor_de_dilucion = float(request.POST['factor_de_dilucion'].replace(',','.'))
            parametro.resultado_final = float(request.POST['resultado_final'].replace(',','.'))
            parametro.save()

            return redirect('lims:service_parameters')

        elif 'excel_file' in request.POST.keys():
            if request.POST['excel_file'] == '':
                pass
        
        elif request.FILES['excel_file']:
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)
            responsable_de_analisis = models.User.objects.get(pk=request.POST['responsable_de_analisis'])
            for index, row in df.iterrows():
                if models.ParametroDeMuestra.objects.filter(Q(codigo_servicio=row['servicio']) & Q(ensayo=row['ensayo'])).exists():
                    parametro = models.ParametroDeMuestra.objects.get(Q(codigo_servicio=row['servicio']) & Q(ensayo=row['ensayo']))
                    if parametro.resultado_final == None:
                        parametro.fecha_de_inicio = row['fecha_de_inicio']
                        parametro.fecha_de_terminado = row['fecha_de_terminado']
                        parametro.resultado = row['resultado']
                        parametro.factor_de_dilucion = row['factor_de_dilucion']
                        parametro.resultado_final = round(row['resultado_final'],4)
                        parametro.responsable_de_analisis = responsable_de_analisis
                        parametro.save()
                    else: continue

            return redirect('lims:service_parameters')

    paginator = Paginator(queryset_service_parameters, 35)
    page = request.GET.get('page')
    service_parameters = paginator.get_page(page)
    return render(request, 'LIMS/service_parameters.html',{
        'service_parameters': service_parameters,
        'parametros': parametros,
        'parameters': parameters,
    })


@login_required
@user_passes_test(is_analyst, login_url='lims:index')
def service_parameters_filter(request):
    """Service parameters for filter view."""

    queryset_service_parameters = models.ParametroDeMuestra.objects.filter(ensayo__icontains='GRV').order_by('-created')
    parameters = set([p.parametro.id for p in queryset_service_parameters])
    parametros = models.ParametroEspecifico.objects.filter(codigo__icontains = 'GRV').filter(id__in= parameters).order_by('codigo')
    parameters = parametros
    

    if request.method == 'POST':
        if 'parametro' in request.POST.keys():
            if request.POST['parametro'] == '':
                pass
            else:
                queryset_service_parameters = models.ParametroDeMuestra.objects.filter(Q(ensayo__icontains='GRV') & Q(parametro_id=request.POST['parametro'])).order_by('-created')

        elif 'search_text' in request.POST.keys():
            if request.POST['search_text'] == '' or request.POST['buscar'] == '':
                pass

            elif request.POST['buscar'] == 'servicio':
                queryset_service_parameters = models.ParametroDeMuestra.objects.filter(Q(ensayo__icontains='GRV') & Q(codigo_servicio__contains=request.POST['search_text'])).order_by('-created')

            elif request.POST['buscar'] == 'ensayo':
                queryset_service_parameters = models.ParametroDeMuestra.objects.filter(Q(ensayo__icontains='GRV') & Q(ensayo__icontains=request.POST['search_text'])).order_by('-created')

            elif request.POST['buscar'] == 'inicio':
                queryset_service_parameters = models.ParametroDeMuestra.objects.filter(Q(ensayo__icontains='GRV') & Q(fecha_de_inicio__contains=request.POST['search_text'])).order_by('-created')

        elif 'fecha_de_inicio' in request.POST.keys():

            parametro = models.ParametroDeMuestra.objects.get(id=request.POST['parametro_id'])
            responsable = User.objects.get(pk=request.POST['responsable_de_analisis'])
            parametro.responsable_de_analisis= responsable
            fecha_inicio = request.POST['fecha_de_inicio']
            if fecha_inicio.endswith(str(datetime.now().year)):
                fecha_de_inicio = datetime.strptime(fecha_inicio, "%d-%m-%Y")
                parametro.fecha_de_inicio = fecha_de_inicio.strftime("%Y-%m-%d")
            else: parametro.fecha_de_inicio = request.POST['fecha_de_inicio']
            fecha_terminado = request.POST['fecha_de_terminado']
            if fecha_terminado.endswith(str(datetime.now().year)):
                fecha_de_terminado = datetime.strptime(fecha_terminado, "%d-%m-%Y")
                parametro.fecha_de_terminado = fecha_de_terminado.strftime("%Y-%m-%d")
            else: parametro.fecha_de_terminado = request.POST['fecha_de_terminado']
            parametro.peso_inicial = float(request.POST['peso_inicial'].replace(',','.'))
            parametro.peso_final = float(request.POST['peso_final'].replace(',','.'))
            parametro.resultado_final = float(request.POST['resultado_final'].replace(',','.'))
            parametro.save()
           
            return redirect('lims:service_parameters_filter')

        elif 'excel_file' in request.POST.keys():
            if request.POST['excel_file'] == '':
                pass

        elif request.FILES['excel_file']:
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)
            responsable_de_analisis = models.User.objects.get(pk=request.POST['responsable_de_analisis'])
            for index, row in df.iterrows():
                if models.ParametroDeMuestra.objects.filter(Q(codigo_servicio=row['servicio']) & Q(ensayo=row['ensayo'])).exists():
                    parametro = models.ParametroDeMuestra.objects.get(Q(codigo_servicio=row['servicio']) & Q(ensayo=row['ensayo']))
                    if parametro.resultado_final == None:
                        parametro.fecha_de_inicio = row['fecha_de_inicio']
                        parametro.fecha_de_terminado = row['fecha_de_terminado']
                        parametro.peso_inicial = row['peso_inicial']
                        parametro.peso_final = row['peso_final']
                        parametro.resultado_final = round(row['resultado_final'],4)
                        parametro.responsable_de_analisis = responsable_de_analisis
                        parametro.save()
                    else: continue 

            return redirect('lims:service_parameters_filter')
    
    paginator = Paginator(queryset_service_parameters, 35)
    page = request.GET.get('page')
    service_parameters = paginator.get_page(page)
    return render(request, 'LIMS/service_parameters_filter.html',{
        'service_parameters': service_parameters,
        'parametros': parametros,
        'parameters': parameters,
    })


@login_required
@user_passes_test(is_manager, login_url='lims:index')
def service_parameter_dropped(request, parameter_id):
    """View to discard service parameter."""
    parameter = models.ParametroDeMuestra.objects.get(id = parameter_id)

    models.ParametroDeMuestraDescartada.objects.create(
        servicio = parameter.servicio,
        batch = parameter.batch,
        codigo_servicio = parameter.codigo_servicio,
        parametro = parameter.parametro,
        responsable_de_analisis= parameter.responsable_de_analisis,
        fecha_de_inicio = parameter.fecha_de_inicio,
        fecha_de_terminado = parameter.fecha_de_terminado,
        resultado = parameter.resultado,
        factor_de_dilucion = parameter.factor_de_dilucion,
        resultado_final = parameter.resultado_final,
        peso_inicial = parameter.peso_inicial,
        peso_final = parameter.peso_final,
        ensayo = parameter.ensayo,
        created = parameter.created,
        discarder = request.user.username,
        creator_user = parameter.creator_user,
        )

    parameter.responsable_de_analisis = None
    parameter.fecha_de_inicio = None
    parameter.fecha_de_terminado = None
    parameter.resultado = None
    parameter.factor_de_dilucion = None
    parameter.peso_inicial = None
    parameter.peso_final = None
    parameter.resultado_final = None
    parameter.updated_at = datetime.now()
    parameter.save()
    
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
@user_passes_test(is_manager, 'lims:index')
def discarded_service_parameters(request):
    """Discarded service parameters view."""

    queryset_service_parameters = models.ParametroDeMuestraDescartada.objects.exclude(ensayo__icontains='GRV').order_by('-discarded')
    parameters = set([p.parametro.id for p in queryset_service_parameters])
    parametros = models.ParametroEspecifico.objects.exclude(codigo__icontains = 'GRV').filter(id__in=parameters).order_by('codigo')
    parameters = parametros

    if request.method == 'POST':
        if 'parametro' in request.POST.keys():
            if request.POST['parametro'] == '':
                pass
            else:
                queryset_service_parameters = models.ParametroDeMuestraDescartada.objects.filter(parametro_id=request.POST['parametro'])
                queryset_service_parameters = queryset_service_parameters.exclude(ensayo__icontains='GRV').order_by('-discarded')

        elif 'search_text' in request.POST.keys():
            if request.POST['search_text'] == '' or request.POST['buscar'] == '':
                pass

            elif request.POST['buscar'] == 'servicio':
                queryset_service_parameters = models.ParametroDeMuestraDescartada.objects.filter(codigo_servicio__contains=request.POST['search_text'])
                queryset_service_parameters = queryset_service_parameters.exclude(ensayo__icontains='GRV').order_by('-discarded')

            elif request.POST['buscar'] == 'ensayo':
                queryset_service_parameters = models.ParametroDeMuestraDescartada.objects.filter(ensayo__icontains=request.POST['search_text'])
                queryset_service_parameters = queryset_service_parameters.exclude(ensayo__icontains='GRV').order_by('-discarded')

            elif request.POST['buscar'] == 'inicio':
                queryset_service_parameters = models.ParametroDeMuestraDescartada.objects.filter(fecha_de_inicio__contains=request.POST['search_text'])
                queryset_service_parameters = queryset_service_parameters.exclude(ensayo__icontains='GRV').order_by('-discarded')

    paginator = Paginator(queryset_service_parameters,35)
    page = request.GET.get('page')
    service_parameters = paginator.get_page(page)
    return render(request, 'LIMS/discarded_service_parameters.html',{
        'service_parameters': service_parameters,
        'parametros': parametros,
        'parameters': parameters,
    })


@login_required
@user_passes_test(is_manager, login_url='lims:index')
def discarded_service_parameters_filter(request):
    """Service parameters for filter view."""

    queryset_service_parameters = models.ParametroDeMuestraDescartada.objects.filter(ensayo__icontains='GRV').order_by('-discarded')
    parameters = set([p.parametro.id for p in queryset_service_parameters])
    parametros = models.ParametroEspecifico.objects.filter(codigo__icontains = 'GRV').filter(id__in=parameters).order_by('codigo')
    parameters = parametros
    

    if request.method == 'POST':
        if 'parametro' in request.POST.keys():
            if request.POST['parametro'] == '':
                pass
            else:
                queryset_service_parameters = models.ParametroDeMuestraDescartada.objects.filter(Q(ensayo__icontains='GRV') & Q(parametro_id=request.POST['parametro'])).order_by('-discarded')

        elif 'search_text' in request.POST.keys():
            if request.POST['search_text'] == '' or request.POST['buscar'] == '':
                pass

            elif request.POST['buscar'] == 'servicio':
                queryset_service_parameters = models.ParametroDeMuestraDescartada.objects.filter(Q(ensayo__icontains='GRV') & Q(codigo_servicio__contains=request.POST['search_text'])).order_by('-discarded')

            elif request.POST['buscar'] == 'ensayo':
                queryset_service_parameters = models.ParametroDeMuestraDescartada.objects.filter(Q(ensayo__icontains='GRV') & Q(ensayo__icontains=request.POST['search_text'])).order_by('-discarded')

            elif request.POST['buscar'] == 'inicio':
                queryset_service_parameters = models.ParametroDeMuestraDescartada.objects.filter(Q(ensayo__icontains='GRV') & Q(fecha_de_inicio__contains=request.POST['search_text'])).order_by('-discarded')
    
    paginator = Paginator(queryset_service_parameters, 35)
    page = request.GET.get('page')
    service_parameters = paginator.get_page(page)
    return render(request, 'LIMS/discarded_service_parameters_filter.html',{
        'service_parameters': service_parameters,
        'parametros': parametros,
        'parameters': parameters,
    })

@login_required
@user_passes_test(is_commercial, login_url='lims:index')
def projects(request):
    """Projects view."""

    queryset_proyectos = models.Proyecto.objects.all().order_by('codigo')
    clientes = models.Cliente.objects.all().order_by('titular')
    if request.method == 'POST':
        if 'client' in request.POST.keys():
            if request.POST['client'] == '' :
                pass
            else:
                queryset_proyectos = models.Proyecto.objects.filter(cliente_id=request.POST['client']).order_by('codigo')


        if 'search_text' in request.POST.keys():
            
            if request.POST['search_text'] == '' or request.POST['opcion'] == '':
                pass

            if request.POST['opcion'] == 'codigo':
                queryset_proyectos = models.Proyecto.objects.filter(codigo__contains=request.POST['search_text']).order_by('codigo')


            if request.POST['opcion'] == 'nombre':
                queryset_proyectos = models.Proyecto.objects.filter(nombre__icontains=request.POST['search_text']).order_by('codigo')

    paginator = Paginator(queryset_proyectos, 35)
    page = request.GET.get('page')
    proyectos = paginator.get_page(page)
    return render(request, 'LIMS/projects.html',{
        'proyectos': proyectos,
        'clientes': clientes,
    })


@login_required
@user_passes_test(is_income_or_coordinador, login_url='lims:index')
def services(request):
    """Services view."""

    queryset_servicios = models.Servicio.objects.all().order_by('-created')
    clientes = models.Cliente.objects.all().order_by('titular')

    if request.method == 'POST':
        if 'client' in request.POST.keys():
            if request.POST['client'] == '' :
                pass

            else:
                queryset_servicios = models.Servicio.objects.filter(cliente=request.POST['client']).order_by('-created')


        elif 'search_text' in request.POST.keys():
            
            if request.POST['search_text'] == '' or request.POST['opcion'] == '':
                pass

            if request.POST['opcion'] == 'codigo':
                queryset_servicios = models.Servicio.objects.filter(codigo_muestra__contains=request.POST['search_text']).order_by('-created')


            if request.POST['opcion'] == 'punto':
                queryset_servicios = models.Servicio.objects.filter(punto_de_muestreo__icontains=request.POST['search_text']).order_by('-created')


            if request.POST['opcion'] == 'muestreo':
                queryset_servicios = models.Servicio.objects.filter(fecha_de_muestreo__contains=request.POST['search_text']).order_by('-created')

            
            if request.POST['opcion'] == 'recepcion':
                queryset_servicios = models.Servicio.objects.filter(fecha_de_recepcion__contains=request.POST['search_text']).order_by('-created')


        else:
            servicio = models.Servicio.objects.get(codigo_muestra=request.POST['servicio_id'])
            servicio.responsable = request.POST['responsable']
            fecha_muestreo = request.POST['fecha_de_muestreo']
            fecha_de_muestreo = datetime.strptime(fecha_muestreo, "%d-%m-%Y %H:%M")
            servicio.fecha_de_muestreo = fecha_de_muestreo.strftime("%Y-%m-%d %H:%M")
            fecha_recepcion = request.POST['fecha_de_recepcion']
            if len(fecha_recepcion)!=0:
                servicio.fecha_de_recepcion = fecha_recepcion
            servicio.save()
            
           
            return redirect('lims:services')

    paginator = Paginator(queryset_servicios, 35)
    page = request.GET.get('page')
    servicios = paginator.get_page(page)            
    return render(request, 'LIMS/services.html',{
        'servicios': servicios,
        'clientes': clientes,
    })


@login_required
@user_passes_test(is_income, login_url='lims:index')
def edit_sample_code(request, service_id):
    """Edit sample code view."""

    service = models.Servicio.objects.get(pk= service_id)
    parameters = models.ParametroDeMuestra.objects.filter(servicio_id = service_id)
    
    context = {
        'service': service,
    }

    try:
        if request.method == 'POST':
            codigo_muestra = request.POST['codigo_muestra']
            service.codigo_muestra = codigo_muestra
            service.editor_sample_code = request.POST['edit_code']
            service.updated_at = datetime.now()
            service.save()

            for parameter in parameters:
                parameter.codigo_servicio = codigo_muestra
                parameter.updated_at = datetime.now()
                parameter.save()

            return redirect('lims:services')
    except:
        context['error'] = 'El código de muestra ya existe.'

    return render(request, 'LIMS/edit_service_code.html', context )


@login_required
def export_data_to_excel(request, username):
    """Export data to excel view."""
    usuario = User.objects.get(username = username)
    clave = models.Cliente.objects.get(titular=User.objects.get(username = usuario.username).first_name).id
    parametros = models.ParametroDeMuestra.objects.filter(servicio_id__proyecto_id__cliente_id__pk = clave)
    parametros = parametros.select_related('servicio').all()
    parametros = parametros.select_related('parametro').all().order_by('-codigo_servicio')
    
    data = [
        {
        'ID Muestra':parametro.codigo_servicio,
        'Descripción':parametro.servicio.punto_de_muestreo,
        'Fecha de muestreo': parametro.servicio.fecha_de_muestreo,
        'Fecha de recepción': parametro.servicio.fecha_de_recepcion,
        'Parametro': parametro.ensayo,
        'Unidad': parametro.parametro.unidad,
        'Resultado': parametro.resultado_final
        }
        for parametro in parametros
    ]
    
    df = pd.DataFrame.from_records(data)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=data_algoritmos.xlsx'
    df.to_excel(response, index=False)
    return response
    

@login_required
def project_client(request, project_id):
    """Project view."""

    project = models.Proyecto.objects.get(pk = project_id)
    cliente = models.Cliente.objects.get(pk = project.cliente_id)
    queryset_parametros = models.ParametroDeMuestra.objects.filter(servicio_id__proyecto_id = project_id)
    queryset_parametros = queryset_parametros.select_related('servicio').all()
    queryset_parametros = queryset_parametros.select_related('parametro').all().order_by('-codigo_servicio')
    paginator = Paginator(queryset_parametros, 20)
    page = request.GET.get('page')
    parametros = paginator.get_page(page)

    if request.method == 'POST':
        if request.POST['search_text'] == '' or request.POST['buscar'] == '':
            return render(request, 'LIMS/client_analysis.html', {
                'project': project, 
                'cliente': cliente,
                'parametros': parametros,
            })

        elif request.POST['buscar'] == 'servicio':
            queryset_parametros = queryset_parametros.filter(codigo_servicio__contains=request.POST['search_text'])
            paginator = Paginator(queryset_parametros, 20)
            page = request.GET.get('page')
            parametros = paginator.get_page(page)
            return render(request, 'LIMS/client_analysis.html', {
                'project': project, 
                'cliente': cliente,
                'parametros': parametros,
            })

        elif request.POST['buscar'] == 'ensayo':
            queryset_parametros = queryset_parametros.filter(ensayo__icontains=request.POST['search_text'])
            paginator = Paginator(queryset_parametros, 20)
            page = request.GET.get('page')
            parametros = paginator.get_page(page)
            return render(request, 'LIMS/client_analysis.html', {
                'project': project, 
                'cliente': cliente,
                'parametros': parametros,
            })

        elif request.POST['buscar'] == 'muestreo':
            queryset_parametros = queryset_parametros.filter(servicio__fecha_de_muestreo__contains=request.POST['search_text'])
            paginator = Paginator(queryset_parametros, 20)
            page = request.GET.get('page')
            parametros = paginator.get_page(page)
            return render(request, 'LIMS/client_analysis.html', {
                'project': project, 
                'cliente': cliente,
                'parametros': parametros,
            })
        
        elif request.POST['buscar'] == 'punto':
            queryset_parametros = queryset_parametros.filter(servicio__punto_de_muestreo__icontains=request.POST['search_text'])
            paginator = Paginator(queryset_parametros, 20)
            page = request.GET.get('page')
            parametros = paginator.get_page(page)
            return render(request, 'LIMS/client_analysis.html', {
                'project': project, 
                'cliente': cliente,
                'parametros': parametros,
            })



    return render(request, 'LIMS/client_analysis.html', {
        'project': project, 
        'cliente': cliente,
        'parametros': parametros,
    })


@login_required
def export_data_project_to_excel(request, project_id):
    """Export data to excel view."""
    parametros = models.ParametroDeMuestra.objects.filter(servicio_id__proyecto_id = project_id)
    parametros = parametros.select_related('servicio').all()
    parametros = parametros.select_related('parametro').all().order_by('-codigo_servicio')
    
    data = [
        {
        'ID Muestra':parametro.codigo_servicio,
        'Descripción':parametro.servicio.punto_de_muestreo,
        'Fecha de muestreo': parametro.servicio.fecha_de_muestreo,
        'Fecha de recepción': parametro.servicio.fecha_de_recepcion,
        'Parametro': parametro.ensayo,
        'Unidad': parametro.parametro.unidad,
        'Resultado': parametro.resultado_final
        }
        for parametro in parametros
    ]
    
    df = pd.DataFrame.from_records(data)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=data_algoritmos.xlsx'
    df.to_excel(response, index=False)
    return response


@login_required
def grafico(request, service_id):
    """vista para graficar."""
    parametros = models.ParametroDeMuestra.objects.filter(codigo_servicio=service_id)
    parametros_x = [p.ensayo for p in parametros]
    resultados_y = [0 if p.resultado_final == None else 1 for p in parametros]

    source = ColumnDataSource(data=dict(parametros_x=parametros_x, resultados_y=resultados_y))
    
    plot = figure(
        x_range=parametros_x, 
        y_range=(0,1.1), 
        height=350,
        toolbar_location=None, 
        tools=""
        )

    plot.vbar(x='parametros_x', top='resultados_y', width=0.9, source=source)
   
    script, div = components(plot)

    return render(request, 'LIMS/service_chart.html', {
        'script': script, 
        'div': div
        })

@login_required
@user_passes_test(is_analyst, login_url='lims:index')
def batches(request):
    """Batches view."""
    queryset_batches = models.Batch.objects.all().order_by("-created")
   
    services = models.ParametroDeMuestra.objects.select_related('batch').order_by('-created')
    user = request.user
    coordinador = user.groups.filter(name='coordinador').exists()

    if request.method == 'POST':
        text = request.POST['search_text']
        opcion = request.POST['opcion']
        if text=='' or opcion == '':
            pass
        elif opcion == 'codigo':
            queryset_batches = queryset_batches.filter(codigo__icontains = text)
        elif opcion == 'responsable':
            queryset_batches = queryset_batches.filter(responsable__icontains = text)
        elif opcion == 'parametro':
            queryset_batches = queryset_batches.filter(parametro__icontains= text)
    
    paginator = Paginator(queryset_batches, 35)
    page = request.GET.get('page')
    lotes = paginator.get_page(page)
    return render(request, "LIMS/batches.html", {
        'lotes': lotes,
        'services': services,
        'coordinador': coordinador,
    })

@login_required
@user_passes_test(is_coordinador, login_url='lims:index')
def add_batch(request):
    """Add batch view."""

    servicios = models.ParametroDeMuestra.objects.select_related('parametro').filter(Q(resultado_final=None) & Q(batch_id=None)).filter(analisis_externos=False ).order_by("-created")
    set_parametros = set([servicio.parametro.id  for servicio in servicios])
    parametros = models.ParametroEspecifico.objects.filter(id__in=set_parametros).order_by('codigo')
    group = Group.objects.get(name='analista')
    analistas = User.objects.filter(groups = group).order_by('username')
    context = {
                    'servicios': servicios,
                    'analistas': analistas,
                    'parametros': parametros, 
                }
    if request.method == 'POST':
        if 'parametro' in request.POST:
            if request.POST['parametro']=='':
                pass

            else:
                servicios = models.ParametroDeMuestra.objects.select_related('parametro').filter(Q(resultado_final=None) & Q(batch_id=None)).order_by("-created")
                servicios = servicios.filter(parametro__codigo = request.POST['parametro'])
                context['servicios']= servicios
                context['parametro'] = request.POST['parametro']
        
        else: 
            current_year = datetime.now().year
            current_year = str(current_year)[2:]
            
            if models.Batch.objects.exists()==False:
                codigo_de_batch = ('1').zfill(5)
                codigo_generado = f'L-{codigo_de_batch}-{current_year}'
            
            else:
                last_batch = models.Batch.objects.all().latest('codigo')

                if last_batch.codigo[-2:] != current_year:
                    codigo_central = ('1').zfill(5)
                    codigo_generado = f'L-{codigo_central}-{current_year}'

                elif models.Batch.objects.exists()==True and last_batch.codigo[-2:] == current_year:
                    last_batch = models.Batch.objects.filter(codigo__endswith = '-'+current_year).latest('codigo')
                    codigo_de_batch = str(int(last_batch.codigo[-7:-3]) +1).zfill(5)
                    codigo_generado = f'L-{codigo_de_batch}-{current_year}'
            

            services = request.POST.getlist('service')
            batch = models.Batch.objects.create(
                codigo = codigo_generado, 
                parametro = request.POST['parametro_escogido'], 
                responsable_asignado_id = request.POST['analista'],
                responsable= User.objects.get(id = request.POST['analista']).username, 
                creator_user= request.POST['creator_user'])
            for service in services:
                parameter = models.ParametroDeMuestra.objects.get(id=service)
                parameter.batch = batch
                parameter.save()
            
            return redirect('lims:batches')

    return render(request, "LIMS/add_batch.html", context)


@login_required
@user_passes_test(is_analyst, login_url='lims:index')
def batch(request, batch_id):
    lote = models.Batch.objects.get(codigo = batch_id)
    parametros = models.ParametroDeMuestra.objects.filter(batch_id = lote).exclude(ensayo__icontains='GRV').order_by('servicio_id')
    service_parameters = models.ParametroDeMuestra.objects.filter(ensayo__icontains='GRV').order_by('servicio_id')

    if request.method == 'POST':            
            parametro = models.ParametroDeMuestra.objects.get(id=request.POST['parametro_id'])
            responsable = User.objects.get(pk=request.POST['responsable_de_analisis'])
            parametro.responsable_de_analisis= responsable
            fecha_inicio = request.POST['fecha_de_inicio']
            if fecha_inicio.endswith(str(datetime.now().year)):
                fecha_de_inicio = datetime.strptime(fecha_inicio, "%d-%m-%Y")
                parametro.fecha_de_inicio = fecha_de_inicio.strftime("%Y-%m-%d")
            else: parametro.fecha_de_inicio = request.POST['fecha_de_inicio']
            fecha_terminado = request.POST['fecha_de_terminado']
            if fecha_terminado.endswith(str(datetime.now().year)):
                fecha_de_terminado = datetime.strptime(fecha_terminado, "%d-%m-%Y")
                parametro.fecha_de_terminado = fecha_de_terminado.strftime("%Y-%m-%d")
            else: parametro.fecha_de_terminado = request.POST['fecha_de_terminado']
            parametro.resultado = request.POST['resultado']
            parametro.factor_de_dilucion = request.POST['factor_de_dilucion']
            parametro.resultado_final = request.POST['resultado_final']
            parametro.updated_at = datetime.now()
            parametro.save()

            return redirect(request.META.get('HTTP_REFERER', '/'))

    return render(request, "LIMS/batch_service_parameters.html", {
        'lote': lote,
        'parametros': parametros,
        'service_parameter': service_parameters,
    })


@login_required
@user_passes_test(is_manager, login_url='lims:index')
def base_importation(request):
    if request.method == 'POST':
        if 'excel_file' in request.POST.keys():
            if request.POST['excel_file'] == '':
                pass
        
        elif request.FILES['excel_file']:
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)

            responsable_de_analisis = models.User.objects.get(pk=request.POST['responsable_de_analisis'])
            for index, row in df.iterrows():
                if models.TipoDeMuestra.objects.filter(nombre=row['Matriz']).exists():
                    continue
                else:
                    models.TipoDeMuestra.objects.create(nombre=row['Matriz'], creator_user = responsable_de_analisis)

            for index, row in df.iterrows():
                if   models.Metodo.objects.filter(nombre=row['Código de Metodología']).exists():
                    continue
                else:
                    models.Metodo.objects.create(nombre = row['Código de Metodología'], descripcion= row['Metodología'],creator_user = responsable_de_analisis)
            
            for index, row in df.iterrows():
                if   models.ParametroEspecifico.objects.filter(codigo=row['Código de Parámetro']).exists():
                    continue
                else:
                    if row['LDM']>=0: ldm = row['LDM']
                    else: ldm = '-'
                    
                    if row['LCM']>=0: lcm = row['LCM']
                    else: lcm = '-'

                    if ldm != '-' and lcm != '-':
                        ldm_str = str(ldm)
                        int_part, dec_part = ldm_str.split('.')
                        lcm = round(lcm, len(dec_part))

                    if type(row['Envases']) == str: envase = models.Envase.objects.get(pk= row['Envases'])
                    else: envase = None

                    models.ParametroEspecifico.objects.create(
                        ensayo = row['Parámetro'] , 
                        codigo= row['Código de Parámetro'], 
                        metodo = row['Código de Metodología'],
                        LDM = ldm,
                        LCM = lcm,
                        unidad = row['Unidad'],
                        tipo_de_muestra = row['Matriz'],
                        codigo_etfa = row['Código Autorización ETFA'],
                        acreditado = row['Acreditado'],
                        envase = envase,
                        creator_user = responsable_de_analisis)

            return redirect(request.META.get('HTTP_REFERER', '/'))

    return render(request, 'LIMS/base_importation.html')


@login_required
@user_passes_test(is_commercial, login_url='lims:index')
def service_simulator(request):
    """Vista para simular un servicio."""

    tipos_de_muestras = models.TipoDeMuestra.objects.all().order_by('nombre')
    context = {
        'tipos_de_muestras': tipos_de_muestras,
    }
    if request.method == 'POST':

        if 'parameters' not in request.POST:
            etfa = request.POST['etfa']
            tipo_de_muestra = request.POST['tipo_muestra']
            parameters = models.ParametroEspecifico.objects.filter(tipo_de_muestra = tipo_de_muestra).order_by('codigo')
            if etfa == 'SI':
                parameters = parameters.exclude(Q(codigo_etfa = 'nan') | Q(codigo_etfa = None) | Q(codigo_etfa= 'Cálculo'))
            elif etfa == 'NO':
                parameters = parameters.all()
            context['parameters'] = parameters
            context['etfa'] = etfa
            context['tipo_de_muestra'] = tipo_de_muestra
        
        else:
            etfa = request.POST['etfa']
            tipo_de_muestra = request.POST['tipo_de_muestra']
            context['etfa'] = etfa
            context['tipo_de_muestra'] = tipo_de_muestra
            parameters = request.POST.getlist('parameters')
            
            if etfa == 'SI':
                parameters,  parameters_analisis_externos = calc_param_etfa(parameters=parameters, parameters_analisis_externos=parameters_analisis_externos)
            else:
                parameters = calc_param_no_etfa(parameters=parameters)
            
            if len(parameters)>0: 
                parametros = [models.ParametroEspecifico.objects.get(id=p) for p in parameters]
                context['parametros'] = parametros
                
    return render(request, 'LIMS/service_simulator.html', context)