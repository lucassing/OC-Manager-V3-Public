from django.shortcuts import render
from django.views.generic import FormView,View
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import Development_Form, PlateProperties_Form, DevelopmentBandSettings_Form, MovementSettings_Form, PressureSettings_Form
from .models import Development_Db, BandSettings_Dev_Db, PlateProperties_Dev_Db, MovementSettings_Dev_Db, PressureSettings_Dev_Db
import math
from django.forms.models import model_to_dict
from connection.forms import OC_LAB
from printrun import printcore, gcoder
from types import SimpleNamespace
import json
from decimal import *

forms = {
    'Development_Form': Development_Form(),
    'PlateProperties_Form': PlateProperties_Form(),
    'DevelopmentBandSettings_Form': DevelopmentBandSettings_Form(),
    'MovementSettings_Form': MovementSettings_Form(),
    'PressureSettings_Form':PressureSettings_Form(),
    }

class HommingSetup(View):
    def post(self, request):
        try:
            x = Decimal(request.POST.get('x'))
            y = Decimal(request.POST.get('y'))
            # Calculate the movement
            x_mov = 50-(x/2)
            y_mov = 30+((100-y)/2)
            gcode = f'G28\nG0X{x_mov}Y{y_mov}\nG92X0Y0'
            OC_LAB.send(gcode)
            return JsonResponse({'message':'ok'})
        except ValueError:
            return JsonResponse({'error':'Error check values'})

class Development(FormView):
    def get(self, request):
        # Send the saved config files
        forms['list_load'] = Development_Db.objects.filter(auth_id=request.user).order_by('-id')
        return render(request,'development.html',forms)

class DevelopmentPlay(View):
    def post(self, request):
        print(request.POST)
        # Treatment for play button
        if 'START' in request.POST:
            if OC_LAB.paused == True:
                OC_LAB.resume()
            else:
                # Run the form validations and return the clean data
                forms_data = data_validations(   plate_properties_form    =   PlateProperties_Form(request.POST),
                                    developmentband_settings_form       =   DevelopmentBandSettings_Form(request.POST),
                                    movement_settings_form   =   MovementSettings_Form(request.POST),
                                    pressure_settings_form   =   PressureSettings_Form(request.POST))

                # With the data, gcode is generated
                gcode = calculate(forms_data)
                # Printrun
                light_gcode = gcoder.LightGCode(gcode)
                OC_LAB.startprint(light_gcode)
                return JsonResponse({'error':'f.errors'})
        if 'STOP' in request.POST:
            OC_LAB.cancelprint()
            return JsonResponse({'message':'stopped'})
        if 'PAUSE' in request.POST:
            OC_LAB.pause()
            return JsonResponse({'message':'paused'})

class DevelopmentSaveAndLoad(View):
    def post(self, request):
        print(request.POST)
        development_form  =   Development_Form(request.POST, request.user)
        plate_properties_form    =   PlateProperties_Form(request.POST)
        developmentband_settings_form       =   DevelopmentBandSettings_Form(request.POST)
        movement_settings_form   =   MovementSettings_Form(request.POST)
        pressure_settings_form   =   PressureSettings_Form(request.POST)

        # Check Plate Property Formular
        if plate_properties_form.is_valid():
            plate_properties_object = plate_properties_form.save()
        else:
            return JsonResponse({'error':'Check plate properties'})

        # Check Band Settings Formular
        if developmentband_settings_form.is_valid():
            developmentband_settings_object = developmentband_settings_form.save()
        else:
            return JsonResponse({'error':'Check band properties'})

        # Check Movement Settings Formular
        if movement_settings_form.is_valid():
            movement_settings_object = movement_settings_form.save()
        else:
            return JsonResponse({'error':'Check movement settings'})

        # Check Pressure Settings Formular
        if pressure_settings_form.is_valid():
            pressure_settings_object = pressure_settings_form.save()
        else:
            return JsonResponse({'error':'Check pressure settings'})


        # If everything is OK then it checks the name and tries to save the Complete Sample App
        if development_form.is_valid():
            filename = development_form.cleaned_data['file_name']
            in_db=Development_Db.objects.filter(file_name=filename).filter(auth_id=request.user)

            # Check if theres
            if len(in_db)>0:
                return JsonResponse({'error':'File Name exist!'})
            else:
                development_instance = development_form.save(commit=False)
                development_instance.auth = request.user
                development_instance.movement_settings = movement_settings_object
                development_instance.pressure_settings = pressure_settings_object
                development_instance.plate_properties = plate_properties_object
                development_instance.developmentband_settings = developmentband_settings_object
                new_development=development_instance.save()

                return JsonResponse({'message':f'The File {filename} was saved!'})

        else:
            return JsonResponse({'error':'Please fill the filename!'})

    def get(self, request):
        file_name=request.GET.get('filename')

        # print(file_name)
        development_conf=model_to_dict(Development_Db.objects.filter(file_name=file_name).filter(auth_id=request.user)[0])
        plate_properties_conf=model_to_dict(PlateProperties_Dev_Db.objects.get(id=development_conf['plate_properties']))
        developmentband_settings_conf=model_to_dict(BandSettings_Dev_Db.objects.get(id=development_conf['developmentband_settings']))
        movement_settings_conf=model_to_dict(MovementSettings_Dev_Db.objects.get(id=development_conf['movement_settings']))
        pressure_settings_conf=model_to_dict(PressureSettings_Dev_Db.objects.get(id=development_conf['pressure_settings']))

        development_conf.update(plate_properties_conf)
        development_conf.update(developmentband_settings_conf)
        development_conf.update(movement_settings_conf)
        development_conf.update(pressure_settings_conf)
        #print(development_conf)
        return JsonResponse(development_conf)

# AUX Functions

def data_validations(**kwargs):
    # Iterate each form and run validations
    forms_data = {}
    for key_form, form in kwargs.items():
        if form.is_valid():
            forms_data.update(form.cleaned_data)
        else:
            print(f'Error on {key_form}')
            return
    return forms_data

def calculate(data):
    data = SimpleNamespace(**data)

    length = data.size_x-data.offset_left-data.offset_right

    applicationsurface = []
    current_height = 0
    while current_height <= data.height:

        applicationline=[]
        current_length=0
        while current_length<=length:
            applicationline.append([data.offset_bottom+current_height, data.offset_left+current_length])
            current_length+=data.delta_x
        applicationsurface.append(applicationline)
        current_height+=data.delta_y

    # Creates the Gcode for the application and return it
    return GcodeGen(applicationsurface, data.motor_speed, data.frequency, data.temperature, data.pressure)

def GcodeGen(listoflines, speed, frequency, temperature, pressure):
    gcode=list()
    # No HEATBED CASE
    if temperature!=0:
        gcode=[f'M190 R{temperature}']
    # Only MOVEMENT CASE
    if pressure==0 and frequency==0:
        gcode.append(f'G94 P{pressure}')
        for listofpoints in listoflines:
            for point in listofpoints:
                gline = 'G1Y{}X{}F{}'.format(str(point[0]), str(point[1]), speed)
                gcode.append(gline)
                gcode.append('M400')

    # Normal Application
    else:
        gcode.append(f'G94 P{pressure}')
        for listofpoints in listoflines:
            for point in listofpoints:
                gline = 'G1Y{}X{}F{}'.format(str(point[0]), str(point[1]), speed)
                gcode.append(gline)
                gcode.append('M400')
                gcode.append(f'G93 F{frequency} P{pressure}')
                gcode.append('M400')
    gcode.append('G28')
    return gcode

def dinamic_cleaning():
    # THE GCODE TO OPEN THE VALVE AT A CERTAIN frequency
    # range(start, stop, step)
    time = 5 # Minimun time for each frequency 5 sec
    f = open("dinamic_clean.gcode", "w+")
    for i in range(100,550,50):
        for j in range(1,5*i+1):
            f.write(f'G93 F{i} P300'+'\n')
    f.close()

def static_cleaning():
    # THE GCODE TO PUMP NO MATTER THE PRESSURE
    gcode = ''
    # OPEN DE VALVE AND LEAVE IT LIKE THAT
    f = open("static_clean.gcode", "w+")
    for i in range(0,100):
        f.write(gcode+f'{i}'+'\n')
    f.close()
