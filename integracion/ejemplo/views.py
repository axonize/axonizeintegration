# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SensoresClaro

from .models import Ejemplo
import json
import requests
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.utils.timezone import utc
from pprint import pprint

#with open('ejem') as f:
 #   data = json.load(f)

#pprint(data["gatewayMessage"]["count"])


@csrf_exempt
def hello(request):

    received = json.loads(request.body)
    #the commented lines will change when you define de IP address

    headers={'Content-Type':'application/json', 'Authorization':'SharedAccessSignature sr=axonizeStagingHub.azure-devices.net%2Fdevices%2F5b64b583e5cdcf0f74d0fd08&sig=YbK%2FkzQ8sbpIhmSGDKXjH1TSG%2FnWSDsYoH3H1icEKc4%3D&se=1538823341'}
    dictjson={
    "app_id":"b2240a12-f5fa-47ef-893a-a7562d57de61",
    "product_id": "5b3b8b35e5cdcf07248524d5",
    "device_id": "5b64b583e5cdcf0f74d0fd08",
    "dateTime":"2018-08-22T07:05:00Z",
    "type":"7",

    "name":"Corriente",
    "value":received["gatewayMessage"]["batteryLevel"],
    #"value":"25",b
    #"value":"25",b
    "unit": "%",
    }
    response = requests.post('https://axonizestaginghub.azure-devices.net/devices/5b64b583e5cdcf0f74d0fd08/messages/events?api-version=2016-02-03',json.dumps(dictjson),headers=headers)
    Ejemplo.objects.create(datos=request.body)
    return HttpResponse("pong")

@csrf_exempt
def definitiva(request):
    received = json.loads(request.body)
    Ejemplo.objects.create(datos=request.body)

    sensores=received["sensorMessages"]
    Nombre=""
    Bateria=""
    Senal=""
    print "existen "+ str(len(sensores))
    datossensores=[]

    for i in reversed(sensores):
        codigosensor=str(i["sensorID"])




        if not codigosensor in datossensores:
            datossensores.append(codigosensor)
            try:
                sensor = SensoresClaro.objects.get(Monnit_ID=str(i["sensorID"]))
                Nombre=i["sensorName"]
                Bateria = i["batteryLevel"]
                Senal = i["signalStrength"]
                aux = str(i["dataValue"])
                print "Se encontro el objeto"
                #https://api.stg.axonize.com/odata/devices/5b62b383e5cdcf1cd4d1c9ad
                url = "https://api.stg.axonize.com/odata/devices?$filter=customId eq \'"+str(sensor.Monnit_ID)+"\'"
                #data = {'ClientSecret': 'de82ebc0-ea6f-40bb-90c2-0e7f56654d06', 'ClientId': '40dced68-e1da-4ccd-93c9-ed2d3b4f431c'}
                headers = {'content-type': 'application/json','ClientSecret': 'de82ebc0-ea6f-40bb-90c2-0e7f56654d06', 'ClientId': '40dced68-e1da-4ccd-93c9-ed2d3b4f431c'}
                #r = requests.get(url+str(sensor.Device_ID), data=json.dumps(data), headers=headers)
                r = requests.get(url,  headers=headers)
                val=r.text
                #print val
                resultado=json.loads(val)

                #aux=aux.split("|")
                #print "antes de enviar"
                envioazure(str(sensor.Autorizacion),str(resultado["value"][0]["id"]),Nombre,str(resultado["value"][0]["appId"]),str(resultado["value"][0]["productId"]),aux,sensor.Tipo,Bateria,Senal)
                #print "despues de enviar"
                #print r.text
                #break

            except ObjectDoesNotExist:
                print "Error "+codigosensor
    return HttpResponse("pong")


def envioazure(Autorizacion, DeviceID,Nombre,appId,productId, values,tipo,bateria,senal):
    now = datetime.datetime.utcnow().replace(tzinfo=utc)


    headers={'Content-Type':'application/json', 'Authorization':Autorizacion}
    dictjson={
    "app_id":appId,
    "product_id": productId,
    "device_id": DeviceID,
    "dateTime":str(now),
    #"type":"7",

    "name":Nombre,
    #"value":values,
    #"value":"25",

    }
    if tipo == "Temperatura/Humedad":
        valores=values.split("|")
        dictjson["type"]=991
        #dictjson["unit"]: "%",
        dictjson["value"] =[
            {
                "name": "Temperatura",
                "type": "7",
                "value": valores[1]
            }, {
                "name": "Humedad",
                "type": "8",
                "value": valores[0]
            }
            , {
                "name": "Bateria",
                "type": "5",
                "value": bateria,
                "unit": "%"
            }
            , {
                "name": "Señal",
                "type": "15",
                "value": senal,
                "unit": "%"
            }

        ]
    if tipo == "Temperatura":
        
        dictjson["type"]=991
        #dictjson["unit"]: "%",
        dictjson["value"] =[
            {
                "name": "Temperatura",
                "type": "7",
                "value": values
            }
            , {
                "name": "Bateria",
                "type": "5",
                "value": bateria,
                "unit": "%"
            }
            , {
                "name": "Señal",
                "type": "15",
                "value": senal,
                "unit": "%"
            }

        ]
    if tipo == "Movimiento":
        dato=0
        print values
        if values=="True":
            dato=1
        elif values=="False":
            dato=0

        dictjson["type"] = 991

        dictjson["value"] = [
            {
                "name": "Movimiento",
                "type": "1026",
                "value": dato
            }
            , {
                "name": "Bateria",
                "type": "5",
                "value": bateria,
                "unit": "%"
            }
            , {
                "name": "Señal",
                "type": "15",
                "value": senal,
                "unit": "%"

            }

        ]

    if tipo == "Detector Puerta":
        dato=0
        print values
        if values=="True":
            dato=0
        elif values=="False":
            dato=1

        dictjson["type"] = 991

        dictjson["value"] = [
            {
                "name": "Puerta",
                "type": "1026",
                "value": dato
            }
            , {
                "name": "Bateria",
                "type": "5",
                "value": bateria,
                "unit": "%"
            }
            , {
                "name": "Señal",
                "type": "15",
                "value": senal,
                "unit": "%"

            }

        ]


    if tipo == "Ultrasonico":
        dictjson["type"] = 991
        print values

        dictjson["value"] = [
            {
                "name": "Nivel Liquidos",
                "type": "1033",
                "value": values,
                "unit": "cm"
            }
            , {
                "name": "Bateria",
                "type": "5",
                "value": bateria,
                "unit": "%"
            }
            , {
                "name": "Señal",
                "type": "15",
                "value": senal,
                "unit": "%"

            }

        ]
        #dsad
    if tipo == "Medidor Voltaje":
        dictjson["type"] = 991
        print values

        dictjson["value"] = [
            {
                "name": "Tensión",
                "type": "1106",
                "value": values,
                "unit": "V"
            }
            , {
                "name": "Bateria",
                "type": "5",
                "value": bateria,
                "unit": "%"
            }
            , {
                "name": "Señal",
                "type": "15",
                "value": senal,
                "unit": "%"

            }

        ]

    if tipo == "Detector Voltaje":
        dato = 0
        print values
        if values == "True":
            dato = 1
        elif values == "False":
            dato = 0

        dictjson["type"] = 991

        dictjson["value"] = [
        {
            "name": "Detección Voltaje",
            "type": "1026",
            "value": dato
        }
                , {
                    "name": "Bateria",
                    "type": "5",
                    "value": bateria,
                    "unit": "%"
                }
                , {
                    "name": "Señal",
                    "type": "15",
                    "value": senal,
                    "unit": "%"

                }

            ]

    if tipo == "Corriente Trifasica":
        print "Sensor Trifasico"
        valores = values.split("|")
        dictjson["type"] = 991
        # dictjson["unit"]: "%",
        dictjson["value"] = [
            {
                    "name": "Fase 1 Promedio",
                    "type": "1106",
                    "value": valores[0],
                    "unit": "A"
                },{
                    "name": "Fase 1 Max",
                    "type": "1106",
                    "value": valores[1],
                    "unit": "A"
                },{
                    "name": "Fase 1 Min",
                    "type": "1106",
                    "value": valores[2],
                    "unit": "A"
                },{
                    "name": "Fase 1 Duty",
                    "type": "1106",
                    "value": valores[3],
                    "unit": "A"
                },{
                    "name": "Fase 2 Promedio",
                    "type": "1106",
                    "value": valores[4],
                    "unit": "A"
                },{
                    "name": "Fase 2 Max",
                    "type": "1106",
                    "value": valores[5],
                    "unit": "A"
                },{
                    "name": "Fase 2 Min",
                    "type": "1106",
                    "value": valores[6],
                    "unit": "A"
                },{
                    "name": "Fase 2 Duty",
                    "type": "1106",
                    "value": valores[7],
                    "unit": "A"
                },{
                    "name": "Fase 2 Promedio",
                    "type": "1106",
                    "value": valores[4],
                    "unit": "A"
                },{
                    "name": "Fase 2 Max",
                    "type": "1106",
                    "value": valores[5],
                    "unit": "A"
                },{
                    "name": "Fase 2 Min",
                    "type": "1106",
                    "value": valores[6],
                    "unit": "A"
                },{
                    "name": "Fase 2 Duty",
                    "type": "1106",
                    "value": valores[7],
                    "unit": "A"
                },{
                    "name": "Fase 3 Promedio",
                    "type": "1106",
                    "value": valores[8],
                    "unit": "A"
                },{
                    "name": "Fase 3 Max",
                    "type": "1106",
                    "value": valores[9],
                    "unit": "A"
                },{
                    "name": "Fase 3 Min",
                    "type": "1106",
                    "value": valores[10],
                    "unit": "A"
                },{
                    "name": "Fase 3 Duty",
                    "type": "1106",
                    "value": valores[11],
                    "unit": "A"
                },{
                    "name": "Horas",
                    "type": "1106",
                    "value": valores[12],
                    "unit": "h"
                }, {
                    "name": "Bateria",
                    "type": "5",
                    "value": bateria,
                    "unit": "%"
                }
                ,





                {
                    "name": "Señal",
                    "type": "15",
                    "value": senal,
                    "unit": "%"
                }

            ]







    response = requests.post('https://axonizestaginghub.azure-devices.net/devices/'+DeviceID+'/messages/events?api-version=2016-02-03',json.dumps(dictjson),headers=headers)
    print "Sensor se ha enviado correctamente"
    #print response
