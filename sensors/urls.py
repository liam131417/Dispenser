from django.urls import path
from sensors.views import get_distance
from sensors.views import get_motion
from sensors.views import get_temphumid
from sensors.views import add_tempAndHumid
from sensors.views import add_tempAndHumidCreatedAt
from sensors.views import add_dist
from sensors.views import add_motion
from sensors.views import temphumid
from sensors.views import motion
from sensors.views import distance
from sensors.views import get_disp
from sensors.views import incrementDist
from sensors.views import incrementTemp
from sensors.views import motionDetected
from sensors.views import motionNotDetected
from sensors.views import isDispensing
from sensors.views import isNotDispensing
from sensors.views import getSeed


urlpatterns = [
    path('temp/',temphumid,name='alltemphumid'),
    path('temp/<int:id>/',get_temphumid,name = 'tempHumid'),
    path('temp/add/',add_tempAndHumid,name="addTempHumid"),
    path('temp/adda/',add_tempAndHumidCreatedAt,name="addTempHumid"),
    path('distance/',distance,name='allDistance'),
    path('distance/<int:id>/',get_distance,name='getdistance'),
    path('distance/add/',add_dist,name='addDistance'),
    path('motion/',motion,name='allMotion'),
    path('motion/<int:id>/',get_motion,name='getMotion'),
    path('motion/add/',add_motion,name='addMotion'),
    path('motion/isDetected',motionDetected,name='motionDetected'),
    path('motion/isNotDetected',motionNotDetected,name='motionNotDetected'),
    path('disp/<id>',get_disp,name='getDisp'),
    path("disp/dist/<id>",incrementDist,name='incrementDist'),
    path("disp/temp/<id>",incrementTemp,name='incrementTemp'),
    path('disp//<int:id>/isDispensing',isDispensing,name='isDispensing'),
    path('disp/<int:id>/isNotDispensing',isNotDispensing,name='isNotDispensing'),
    path('seed/',getSeed,name='s')
    ]
