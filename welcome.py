#-*- coding: utf-8 -*-
# Copyright 2015 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import json
import time
from flask import Flask, jsonify, request
import smtplib
from datetime import datetime
from threading import Timer

app = Flask(__name__)

VersionString = u'0.80'

_State0KeyList = [ 
    u'1.고장 접수',
    u'2.고장 접수 내역 확인',    
    u'3.사용방법 안내', 
    u'4.기타'
    ]

_State1KeyList = [
      u'1.지하4층 실습실',
      u'2.지하4층 기공실',
      u'3.지하3층 실습실',
      u'4.지하3층 컴퓨터실',
      u'5.치의학관 시설' ,
      u'이전 메뉴'
    ]   

  
_State4KeyList = [
      u'1.학번(혹은 사번) 및 이름 입력',
      u'2.학번(혹은 사번) 및 이름 삭제' ,
      u'3.Forwarding Member 신청' , 
      u'4.Forwarding Member 해제' ,
      u'이전 메뉴'     
    ] 


_YesorNoKeyList = [  u'1.Yes', u'2.No' , u'이전 메뉴'  ]

_YesorNoKeyListv2 = [  u'1.Yes', u'2.Yes(+파트 추가 입력)', u'3.No' , u'이전 메뉴'  ]

_State13KeyList = [
      u'지하 3층 실습실(자리)',
      u'핸드피스',
      u'이전 메뉴'     
]

#_State42KeyList = _YesorNoKeyList
#_State4111KeyList = _YesorNoKeyList
#_State41111KeyList = _YesorNoKeyList

_State111KeyList = [
      u'1.라이트',
      u'2.모니터',
      u'3.가스토치',
      u'4.핸드피스 엔진',
      u'5.Air Suction(흡입구)',
      u'6.Air Spray(배출구)' ,
      u'7.직접 입력'  ,    
      u'이전 메뉴'     
    ]   

len_4work_part = len( _State111KeyList)

_State141KeyList = [
      u'1.모니터',
      u'2.본체',  
      u'3.네트워크',    
      u'5.직접 입력',    
      u'이전 메뉴'                
]
len_3com_part = len( _State141KeyList)


_State1311KeyList = [
      u'토마스',
      u'모니터',
      u'라이트',      
      u'3Way Air Water Syringe',   
      u'하이스피드 핸드피스 Connector'  ,
      u'로스피드 핸드피스 Connector'  ,               
      u'직접 입력'  ,    
      u'이전 메뉴'              
]
len_3work_part = len( _State1311KeyList)


_State1321KeyList = [
      u'1.하이스피드 핸드피스',
      u'2.로스피드 핸드피스',
      u'직접 입력'  ,    
      u'이전 메뉴'              
]
len_3handpiece_part = len( _State1321KeyList)


_LightSymptomKeyList = [
      u'안 켜짐',
      u'깜빡깜빡 거림',
      u'위치 고정 안 됨',
      u'증상 직접 입력' ,
      u'이전 메뉴'              
    ]   

_LightSymptomMultiChoiceList = [
      u'1:안 켜짐',
      u'2:깜빡깜빡 거림',
      u'3:위치 고정 안 됨'
    ]   

_LightSymptomJoinString = u'\n'.join(_LightSymptomMultiChoiceList)


_MonitorSymptomKeyList = [
      u'1.모니터 안 켜짐',
      u'2.모니터 깜빡깜빡 거림',
      u'3.모니터 흑백으로 나옴' ,
      u'4.증상 직접 입력'  ,
      u'이전 메뉴'         
    ]   


_MonitorSymptomMultiChoiceList = [
      u'1:모니터 안 켜짐',
      u'2:모니터 깜빡깜빡 거림',
      u'3:모니터 흑백으로 나옴' 
    ]   


_MonitorSymptomJoinString = u'\n'.join(_MonitorSymptomMultiChoiceList)

_110VoltSymptomKeyList = [
      u'1.전원 안 들어옴',
      u'2.구망에 안 들어감',
      u'3.구망에 들어가서 안 나옴',
      u'4.증상 직접 입력' ,
      u'이전 메뉴'         
]

_GastorchSymptomKeyList = [
      u'불 안 나옴',
      u'불 너무 약함',
      u'증상 직접 입력' ,
      u'이전 메뉴'    
]

_220VoltSymptomKeyList = _110VoltSymptomKeyList

_HandpieceengineSymptomKeyList = [
      u'안 켜짐',
      u'Hand로만 동작함',      
      u'증상 직접 입력' ,
      u'이전 메뉴'    
]

_AirinletSymptomKeyList = [
      u'흡입 안 됨',
      u'증상 직접 입력',
      u'이전 메뉴'    
]

_AiroutletSymptomKeyList = [
      u'공기 방출 안 됨',
      u'방출 단계 조절 안 됨',
      u'공기 방출구 빠짐' , 
      u'증상 직접 입력',
      u'이전 메뉴'    
]


_DollSymtomKeyList = [
      u'1:목 회전 안 됨' ,
      u'2:목 셕션 안 됨' , 
      u'3:상악 덴티폼 고정 나사 없음' , 
      u'4:하악 덴티폼 고정 나사 없음' ,       
      u'증상 직접 입력',
      u'이전 메뉴'        
]

_DollSymtomMultiChoiceList = [
      u'1:목 회전 안 됨' ,
      u'2:목 셕션 안 됨' ,
      u'3:상악 덴티폼 고정 나사 없음' , 
      u'4:하악 덴티폼 고정 나사 없음'        
]
_DollSymptomJoinString = u'\n'.join(_DollSymtomMultiChoiceList)


_3WaySymptomMultiChoiceList = [ 
      u'1:물 안 나옴' ,
      u'2:에어 안 나옴' 
]
_3WaySymptomJoinString = u'\n'.join(_3WaySymptomMultiChoiceList)


_HighspeedConnectorSymptomMultiChoiceList = [
      u'1:Connector 없음'  
]
_HighspeedConnectorSymptomJoinString = u'\n'.join(_HighspeedConnectorSymptomMultiChoiceList)

_LowspeedConnectorSymptomMultiChoiceList = [
      u'1:Connector 없음' 
]
_LowspeedConnectorSymptomJoinString = u'\n'.join(_LowspeedConnectorSymptomMultiChoiceList)



_HighspeedHandpieceSymtomKeyList = [
      u'1:회전 안 됨' , 
      u'2:물 안 나옴',             
      u'3:증상 직접 입력', 
      u'이전 메뉴'       
]

_LowspeedHandpieceSymptomList = [
      u'1:회전 안 됨' , 
      u'2:증상 직접 입력', 
      u'이전 메뉴'       
]

_ComnetworkSymptomKeyList = [
      u'오프라인으로 나옴' ,
      u'IP 충돌이라고 나옴' , 
      u'증상 직접 입력', 
      u'이전 메뉴'       
]

_ComnetworkSymptomMultiChoiceList = [
      u'1:오프라인으로 나옴' ,
      u'2:IP 충돌이라고 나옴' , 
    ]   


_ComnetworkSymptomJoinString = u'\n'.join(_ComnetworkSymptomMultiChoiceList)


_CombodySymptomMultiChoiceList = [
      u'1:전원이 안 켜짐'  ,
      u'2:부팅이 안 됨' ,
      u'3:USB 인식을 못 함'
]
_CombodySymptomJoinString = u'\n'.join(_CombodySymptomMultiChoiceList)


_Table1ButtonList = [
    u'Sand Blast 6', u'Sand Blast 5' , u'Vacuum Mixer 111',u'Sand Blast 4' , 
    u'Trimmer 10',   u'Sand Blast 3',  u'Sand Blast 7' ,
    u'직접 입력',      u'이전 메뉴'              
]
_Table2ButtonList = [
    u'Trimmer 8'   , u'Trimmer 9'  ,   u'Trimmer 14'  ,
    u'직접 입력'     ,  u'이전 메뉴'              
]
_Table3ButtonList = [
    u'Trimmer 10'   , u'Trimmer 17'  ,   u'Trimmer 12'  ,
    u'직접 입력'     ,  u'이전 메뉴'              
]
_Table4ButtonList = [
    u'Trimmer 15'   , u'Trimmer 17'  ,   u'Trimmer 11'  ,
    u'직접 입력'     ,  u'이전 메뉴'              
]
_Table5ButtonList = [
    u'캐스팅머신 ?',     u'전기로 69',        u'전기로 68',
    u'전기로 67',       u'전기로 67',
    u'직접 입력'     ,   u'이전 메뉴'              
]
_Table6ButtonList = [
    u'캐스팅머신 13',     u'전기로 65',        u'전기로 64',
    u'직접 입력'     ,   u'이전 메뉴'              
]
_Table7ButtonList = [
    u'캐스팅머신 14',     u'전기로 63',        u'전기로 62',
    u'직접 입력'     ,   u'이전 메뉴'              
]
_Table8ButtonList = [
    u'온성기 11',        u'온성기 13?',       u'스팀크리너 ?',
    u'스팀크리너 79',     u'온성기 12', 
    u'직접 입력'     ,   u'이전 메뉴'              
]
_Table9ButtonList = [
    u'분배기 1',         u'분배기 2',        u'스팀크리너 42',
    u'Vacuum Mixer 109',u'Vacuum Mixer 102', 
    u'직접 입력'     ,   u'이전 메뉴'         
]
_Table10ButtonList = [
    u'Trimmer 9'  ,    u'Vacuum Mixer 108', u'분배기 4',         u'분배기 3',
    u'직접 입력'     ,   u'이전 메뉴'              
]
_Table11ButtonList = [
    u'Trimmer 9'  ,    u'Vacuum Mixer 108', u'스팀크리너 79',
    u'직접 입력'     ,   u'이전 메뉴'                  
]
_Table12ButtonList = [
    u'Poll Cleaner 48',u'Poll Cleaner 51',u'Poll Cleaner 52',u'Poll Cleaner 53',
    u'직접 입력'     ,   u'이전 메뉴'                  
]

_TableButtonListList = [
    _Table1ButtonList,  _Table2ButtonList, _Table3ButtonList, _Table4ButtonList, 
    _Table5ButtonList,  _Table6ButtonList, _Table7ButtonList, _Table8ButtonList,
    _Table9ButtonList,  _Table10ButtonList,_Table11ButtonList,_Table12ButtonList         
]

_SandblastSymptomMultiChoiceList = [
      u'1:전원이 안 켜짐'  ,
      u'2:발판을 밟으면 바람은 나오나 모래가 안 나옴' 
]
_SandblastSymptomJoinString = u'\n'.join(_SandblastSymptomMultiChoiceList)
_VacuummixerSymptomMultiChoiceList = [
      u'1:전원이 안 켜짐'  ,
      u'2:비커가 회전이 안 됨' 
]
_VacuummixerSymptomJoinString = u'\n'.join(_VacuummixerSymptomMultiChoiceList)
_TrimmerSymptomMultiChoiceList = [
      u'1:전원이 안 켜짐'  ,
      u'2:날이 회전이 안 됨' 
]
_TrimmerSymptomJoinString = u'\n'.join(_TrimmerSymptomMultiChoiceList)
_CastingmachineSymptomMultiChoiceList = [
      u'1:전원이 안 켜짐'  
]
_CastingmachineSymptomJoinString = u'\n'.join(_CastingmachineSymptomMultiChoiceList)
_ElectricfurnaceSymptomMultiChoiceList = [
      u'1:전원이 안 켜짐'  
]
_ElectricfurnaceSymptomJoinString = u'\n'.join(_ElectricfurnaceSymptomMultiChoiceList)
_CuringwaterbathSymptomMultiChoiceList = [
      u'1:전원이 안 켜짐'  
]
_CuringwaterbathSymptomJoinString = u'\n'.join(_CuringwaterbathSymptomMultiChoiceList)
_SteamcleanerSymptomMultiChoiceList = [
      u'1:전원이 안 켜짐'  
]
_SteamcleanerSymptomJoinString = u'\n'.join(_SteamcleanerSymptomMultiChoiceList)
_DispenserSymptomMultiChoiceList = [
      u'1:전원이 안 켜짐'  
]
_DispenserSymptomJoinString = u'\n'.join(_DispenserSymptomMultiChoiceList)
_PollcleanerSymptomMultiChoiceList = [
      u'1:전원이 안 켜짐'  
]
_PollcleanerSymptomJoinString = u'\n'.join(_PollcleanerSymptomMultiChoiceList)





StateMultiChoiceList = {
                0x11114111: _MonitorSymptomMultiChoiceList ,  0x11114112:_CombodySymptomMultiChoiceList ,  0x11114113:_ComnetworkSymptomMultiChoiceList,
                0x111131111: _DollSymtomMultiChoiceList ,     0x111131112:_MonitorSymptomMultiChoiceList , 0x111131113:_LightSymptomMultiChoiceList ,  
                0x111131114:_3WaySymptomMultiChoiceList,      0x111131115: _HighspeedConnectorSymptomMultiChoiceList   ,     0x111131116:_LowspeedConnectorSymptomJoinString 
}

StateButtonList = { 0x1: _State0KeyList, 
                  0x14: _State4KeyList ,
                  0x142 : _YesorNoKeyList ,
                 0x1111: _State1KeyList ,             
                 0x11113:  _State13KeyList,            
                 0x111111: _State111KeyList,          0x111141: _State141KeyList,  
                 0x1111311: _State1311KeyList ,       0x1111321 : _State1321KeyList, 
                 0x14111: _YesorNoKeyList ,                 
                 0x11111111: _LightSymptomKeyList  ,  0x11111112: _MonitorSymptomKeyList ,    0x11111113 : _GastorchSymptomKeyList , 
                 0x11111114: _HandpieceengineSymptomKeyList ,0x11111115: _AirinletSymptomKeyList ,    0x11111116: _AiroutletSymptomKeyList ,
                 #11114111: _MonitorSymptomKeyList,  
                 #11114112: _ComnetworkSymptomKeyList, 
                 0x141111: _YesorNoKeyList  ,   
                 #111131111:          _DollSymtomKeyList  ,
                 #111131112: _MonitorSymptomKeyList,
                                                   0x111132111: _HighspeedHandpieceSymtomKeyList,    0x111132112: _LowspeedHandpieceSymptomList,                
                 0x1111111111: _YesorNoKeyListv2,    0x1111411111: _YesorNoKeyListv2,   #1111411111: _YesorNoKeyList,
                 0x11113111111: _YesorNoKeyListv2,   0x11113211111: _YesorNoKeyListv2                      
}

StatePhotoList = {  
                    0x11111:   {"url": u'static/images/4work_seats.png' , "width": 548, "height": 482 } ,
                    0x111111:  {"url": u'static/images/4work_oneseat.png' ,"width": 200, "height": 283 } ,
                    0x111131:  {"url": u'static/images/4work_seats.png'  ,"width": 548 ,"height": 482 }, 
                    0x1111311: {"url": u'static/images/3work_oneseat.png' ,"width": 200, "height": 283 } ,
                    0x111132:  {"url": u'static/images/3work_case.png' ,"width": 230,"height": 218}, 
                    0x1111321: {"url": u'static/images/3work_caseopen.png' ,"width": 200,"height": 283 } ,
                    0x11114:   {"url": u'static/images/3com_seats.png' ,   "width": 662,"height": 465 }, 
                    0x111141:  {"url": u'static/images/3com_oneseat.png' ,"width": 363,"height": 616 }
#                    141:  {"url": request.url_root+u'static/images/3com_oneseat.png' ,"width": 363,"height": 616 }
}

SelectString = u' 선택하셨습니다.'
InsertedString = u' 입력하셨습니다.'
SubmitString = u'접수되었습니다.'
CancelString = u'취소되었습니다'
UnderConstructionString =u'-Under Construction-'
UnInsertedString = u'필수 항목인 학번(혹은 사번)이 입력되지 않았습니다.'

AskLocationString = u'위치가 어디신가요?'
AskSeatNumberString = u'자리가 어디신가요?\n0:이전 메뉴'
AskTableNumberString = u'테이블이 어디신가요?\n0:이전 메뉴'
AskPartString = u'어떤 부분이 문제인가요?'
AskDeviceString = u'어떤 기계가 문제인가요?'
AskSymtomString = u'어떤 증상인가요?'
AskMultiSymtomString = u'어떤 증상인가요?(복수, 직접 입력 가능)\nex) 1,3,물이 샘\n\n0:이전 메뉴로 돌아가기'
InsertIDString = u'학번(혹은 사번)을 입력해주세요 ex)2011740011\n0:이전 메뉴'
InsertNameString = u'이름을 입력해주세요 ex)오승환, 강정호a, HyunsooKim\n0:이전 메뉴'
ReInsertString = u'다시 입력해 주세요'
InsertYesNoString = u'입력하시겠습니까?'
LastYesNoString = u'최종 접수하시겠습니까'
DirectInsertSymptomString = u'직접 증상을 입력해주세요\n0:이전 메뉴'
DirectInsertPartString = u'직접 고장난 부분을 입력해주세요\n0:이전 메뉴'
DirectInsertDeviceString = u'직접 고장난 기계를 입력해주세요\n0:이전 메뉴'

InsertValidNumberString = u'범위 내의 숫자를 입력해주세요'
InsertNumberString = u'숫자를 입력해주세요'
InsertCaseNumberString = u'Case의 번호를 입력해주세요\n0:이전 메뉴'

AskSeatHandpieceString = u'실습실 자리 문제인가요? 핸드피스 문제인가요?'
AskDeletionString = u'삭제하시겠습니까?'

fromStateMessageList = {  0x1:SelectString+u'\n' ,
                          0x11:SelectString+u'\n' ,
                          0x14:SelectString+u'\n' ,          0x111:SelectString+u'\n' ,          
                          0x1111:SelectString+u'\n' ,
                          0x11113:SelectString+u'\n' ,
                          0x11111:InsertedString+u'\n' ,    0x11114:SelectString+u'\n' ,          0x111131:SelectString+u'\n' ,       0x111132:SelectString+u'\n' ,                                                 
                          0x111111:InsertedString+u'\n' ,   0x111141:SelectString+u'\n' ,         0x1111311:SelectString+u'\n' ,      0x1111321:SelectString+u'\n' ,
                          0x1111111:SelectString+u'\n' ,    0x1111411:SelectString+u'\n' ,        0x11113111:SelectString+u'\n' ,     0x11113211:SelectString+u'\n' ,
                          0x11111111:SelectString+u'\n' ,   0x11114111:SelectString+u'\n' ,       0x111131111:SelectString+u'\n' ,    0x111132111:SelectString+u'\n' ,
                          0x11111112:SelectString+u'\n' ,   0x11114112:SelectString+u'\n' ,       0x111131112:SelectString+u'\n' ,    0x111132112:SelectString+u'\n' ,
                          0x11111113:SelectString+u'\n' ,   0x11114113:SelectString+u'\n' ,       0x111131113:SelectString+u'\n' ,                           
                          0x11111114:SelectString+u'\n' ,                                         0x111131114:SelectString+u'\n' ,  
                          0x11111115:SelectString+u'\n' ,                                         0x111131115:SelectString+u'\n' ,
                          0x11111116:SelectString+u'\n' ,                                         0x111131116:SelectString+u'\n' ,
                          0x111111111:SelectString+u'\n' ,  0x111141111:SelectString+u'\n' ,      0x1111311111:SelectString+u'\n' ,   0x1111321111:SelectString+u'\n' ,     
                          0x1111111111:SelectString+SubmitString+u'\n' ,0x1111411111:SelectString+SubmitString+u'\n' ,0x11113111111:SelectString+u'\n' ,0x11113211111:SelectString+u'\n' ,
                          0x141:SelectString+u'\n' ,        0x142:SelectString+u'\n' ,  
                          0x1411:SelectString+ u'\n' , 
                          0x14111:SelectString+ u'\n'
}

toStateMessageList = {    0x1:u'',                          
                          0x1111:AskLocationString,
                          0x11113:AskSeatHandpieceString,                                                    
                          0x11111:AskSeatNumberString,       0x11114:AskSeatNumberString,                 0x111131:AskSeatNumberString,       0x111132:InsertCaseNumberString,                          
                          0x111111:AskPartString,            0x111141:AskPartString,                      0x1111311:AskPartString,            0x1111321:AskPartString,       
                          0x1111111:DirectInsertPartString,  0x1111411:DirectInsertPartString,            0x11113111:DirectInsertPartString,  0x11113211:DirectInsertPartString,
                          0x11111111:AskSymtomString ,       
                          0x11114111:AskMultiSymtomString+u'\n'+ _MonitorSymptomJoinString ,                  
                          0x11114112:AskMultiSymtomString+u'\n'+ _CombodySymptomJoinString ,                                            
                          0x11114113:AskMultiSymtomString+u'\n'+ _ComnetworkSymptomJoinString ,
                          0x111131111:AskMultiSymtomString+u'\n'+ _DollSymptomJoinString,       
                          0x111131112:AskMultiSymtomString+u'\n'+ _MonitorSymptomJoinString,    
                          0x111131113:AskMultiSymtomString+u'\n'+ _LightSymptomJoinString,
                          0x111131114:AskMultiSymtomString+u'\n'+ _3WaySymptomJoinString,
                          0x111131115:AskMultiSymtomString+u'\n'+ _HighspeedConnectorSymptomJoinString,
                          0x111131116:AskMultiSymtomString+u'\n'+ _LowspeedConnectorSymptomJoinString ,        
                          0x111132111:AskSymtomString,
                          0x111132112:AskSymtomString, 
                          0x11111112:AskSymtomString ,                                                   
                          0x11111113:AskSymtomString ,
                          0x11111114:AskSymtomString ,
                          0x11111115:AskSymtomString ,
                          0x11111116:AskSymtomString ,
                          0x111111111:DirectInsertSymptomString,  0x111141111:DirectInsertSymptomString,                0x1111311111:DirectInsertPartString,  0x1111321111:DirectInsertPartString,
                          0x14:u'',
                          0x11:InsertIDString,                     0x141:InsertIDString,                  0x142:AskDeletionString,
                          0x111:InsertNameString,                  0x1411:InsertNameString,                
}

push_StateList = {
                  0x1111111:True, 0x11111111:True, 0x11111112:True, 0x11111113:True, 0x11111114:True, 0x11111115:True, 0x11111116:True, 0x111111111:True,
                  0x1111411:True, 0x11114111:True, 0x11114112:True, 0x11114113:True,                                                    0x111141111:True,
                  0x11113111:True,0x111131111:True,0x111131112:True,0x111131113:True,0x111131114:True,0x111131115:True,0x111131116:True,0x1111311111:True,                
                  0x11113211:True,0x111132111:True,0x111132112:True,                                                                    0x1111321111:True,
}

pop_pushedStateList = {
                       0x111111111:True , 0x111141111:True , 0x1111311111:True ,  0x1111321111:True     
}   

initial_State          = 0x1
first_4work_State      = 0x11111
first_3work_State      = 0x111131
first_3handpiece_State = 0x111132
first_3com_State       = 0x11114
first_4eng_State       = 0x11112
#last_4work_Light_State = 1111
last_4work_Light_State      = 0x111111111
last_3work_Doll_State       = 0x1111311111
last_3handpiece_High_State  = 0x1111321111
last_3com_State             = 0x111141111
last_4eng_State             = 0x111121111 #?

first_Independent_IDInsert_State = 0x141


state = { 0x1:0x1 , 
          0x11:0x11,                     0x2:0x2,                     0x3:0x3,                    0x14:0x14 , 
          0x111:0x111,
          0x1111:0x1111,
          0x11111:0x11111 ,                  0x11114:0x11114,                   0x11113:0x11113,                  0x141:0x141,                   0x142:0x142,    
          0x111111:0x111111 ,                0x111131:0x111131,                 0x111132:0x111132,                0x111141:0x111141,             0x1411:0x1411,
          0x1111111:0x1111111 ,              0x1111311:0x1111311,               0x1111321:0x1111321,              0x1111411:0x1111411,           0x14111:0x14111 , 
          0x11111111:0x11111111 ,            0x11111112:0x11111112,             0x11111113:0x11111113,            0x11111114:0x11111114 ,        0x11111115:0x11111115,
          0x11111116:0x11111116,                          
          0x11113111:0x11113111,             0x11113211:0x11113211,    
          0x11114111:0x11114111,             0x11114112:0x11114112,             0x11114113:0x11114113,
          0x141111:0x141111 ,     
          0x111111111:0x111111111,           0x111141111:0x111141111,       
          0x111131111:0x111131111  ,         0x111131112:0x111131112 ,          0x111131113:0x111131113 ,        0x111131114:0x111131114 ,     0x111131115:0x111131115 ,  0x111131116:0x111131116 , 
          0x111132111:0x111132111  ,         0x111132112:0x111132112 ,          0x111132113:0x111132113 , #??           
                                             0x1111311111:0x1111311111 ,        0x1111321111:0x1111321111 ,         
          0x1111111111:0x1111111111,         0x1111311111:0x1111311111,         0x1111321111:0x1111321111,        0x1111411111:0x1111411111,    
                                             0x11113111111:0x11113111111,       0x11113211111:0x11113211111             
}

_4EngSymptomStateList = []

len_4eng_tables = 0xc
def generate4EngStatesInformation() :
    def  _nx_Child_in(stage_num , score) :
        if score == 0 :
            return stage_num
        else :
            return _nx_Child_in(stage_num * 0x10 +1 , score-1)
    def  nx_Child_in( stage_num , score ) :
        num = _nx_Child_in(stage_num, score)
        return num
    len_tables = len_4eng_tables
    #len_devices_per_table = [7,3,3,3, 5,3,3,5, 5,4,3,4 ]
    len_devices_per_table = []
    for i in range(len_tables)  :
        len_devices_per_table.append( len('_Table'+ str(i+1) +'ButtonList') - 2 )    

    state[first_4eng_State] = first_4eng_State   # which table?
    for i in range(len_tables)  :
        state[ nx_Child_in(first_4eng_State,1)+i ]   =  nx_Child_in(first_4eng_State,1)+i  #which device?
        _current_State = nx_Child_in(first_4eng_State,1)+i
        state[ nx_Child_in(_current_State,1) ] = nx_Child_in(_current_State,1)      # insert device directly
        _current_State = nx_Child_in(_current_State,1)
        for j in range(len(len_devices_per_table)) : 
            state[ nx_Child_in(_current_State,1)+j ] = nx_Child_in(_current_State,1)+j      #which symtom?
            _4EngSymptomStateList.append(nx_Child_in(_current_State,1)+j)
        _current_State = nx_Child_in(_current_State,1)
        state[ nx_Child_in(_current_State,1) ] = nx_Child_in(_current_State,1)              #insert symptom directly
        _current_State = nx_Child_in(_current_State,1)
        state[ nx_Child_in(_current_State,1) ] = nx_Child_in(_current_State,1)              #Y or Y+ or N?

    StatePhotoList[first_4eng_State] = {"url": u'static/images/4eng_tables.png' , "width": 503, "height": 473 }
    for i in range(len_tables)  :
        StatePhotoList[nx_Child_in(first_4eng_State,1)+i] = {"url": u'static/images/table'+str(i+1)+u'.jpg' , "width": 412, "height": 231 }

    for i in range(len_tables)  :
        StateButtonList[nx_Child_in(first_4eng_State,1)+i] = _TableButtonListList[i]
        StateButtonList[  nx_Child_in(nx_Child_in(first_4eng_State,1)+i ,4) ] = _YesorNoKeyListv2

    _current_State =  nx_Child_in( nx_Child_in(first_4eng_State,1) + 0 , 2)
    StateMultiChoiceList[_current_State+0]   =  _SandblastSymptomMultiChoiceList
    StateMultiChoiceList[_current_State+1] =  _SandblastSymptomMultiChoiceList  
    StateMultiChoiceList[_current_State+2] =  _VacuummixerSymptomMultiChoiceList
    StateMultiChoiceList[_current_State+3] =  _SandblastSymptomMultiChoiceList
    StateMultiChoiceList[_current_State+4] =  _TrimmerSymptomMultiChoiceList
    StateMultiChoiceList[_current_State+5] =  _SandblastSymptomMultiChoiceList
    StateMultiChoiceList[_current_State+6] =  _SandblastSymptomMultiChoiceList
    # len_devices_per_table[0]?
    _current_State =  nx_Child_in( nx_Child_in(first_4eng_State,1) + 1 , 2)
    StateMultiChoiceList[_current_State+0] =  _TrimmerSymptomMultiChoiceList
    StateMultiChoiceList[_current_State+1] =  _TrimmerSymptomMultiChoiceList
    StateMultiChoiceList[_current_State+2] =  _TrimmerSymptomMultiChoiceList
    # len_devices_per_table[1]?
    _current_State =  nx_Child_in( nx_Child_in(first_4eng_State,1) + 2 , 2)
    StateMultiChoiceList[_current_State+0] =  _TrimmerSymptomMultiChoiceList
    StateMultiChoiceList[_current_State+1] =  _TrimmerSymptomMultiChoiceList
    StateMultiChoiceList[_current_State+2] =  _TrimmerSymptomMultiChoiceList
    # len_devices_per_table[2]?
    _current_State =  nx_Child_in( nx_Child_in(first_4eng_State,1) + 3 , 2)
    StateMultiChoiceList[_current_State+0] =  _TrimmerSymptomMultiChoiceList
    StateMultiChoiceList[_current_State+1] =  _TrimmerSymptomMultiChoiceList
    StateMultiChoiceList[_current_State+2] =  _TrimmerSymptomMultiChoiceList
    # len_devices_per_table[3]?
    _current_State =  nx_Child_in( nx_Child_in(first_4eng_State,1) + 4 , 2)
    StateMultiChoiceList[_current_State+0] =  _CastingmachineSymptomMultiChoiceList
    StateMultiChoiceList[_current_State+1] =  _ElectricfurnaceSymptomMultiChoiceList    
    StateMultiChoiceList[_current_State+2] =  _ElectricfurnaceSymptomMultiChoiceList    
    StateMultiChoiceList[_current_State+3] =  _ElectricfurnaceSymptomMultiChoiceList    
    StateMultiChoiceList[_current_State+4] =  _ElectricfurnaceSymptomMultiChoiceList    
    # len_devices_per_table[4]?
    _current_State =  nx_Child_in( nx_Child_in(first_4eng_State,1) + 5 , 2)
    StateMultiChoiceList[_current_State+0] =  _CastingmachineSymptomMultiChoiceList
    StateMultiChoiceList[_current_State+1] =  _ElectricfurnaceSymptomMultiChoiceList    
    StateMultiChoiceList[_current_State+2] =  _ElectricfurnaceSymptomMultiChoiceList    
    # len_devices_per_table[5]?
    _current_State =  nx_Child_in( nx_Child_in(first_4eng_State,1) + 6 , 2)
    StateMultiChoiceList[_current_State+0] =  _CastingmachineSymptomMultiChoiceList
    StateMultiChoiceList[_current_State+1] =  _ElectricfurnaceSymptomMultiChoiceList    
    StateMultiChoiceList[_current_State+2] =  _ElectricfurnaceSymptomMultiChoiceList    
    # len_devices_per_table[6]?
    _current_State =  nx_Child_in( nx_Child_in(first_4eng_State,1) + 7 , 2)
    StateMultiChoiceList[_current_State+0] =  _CuringwaterbathSymptomMultiChoiceList
    StateMultiChoiceList[_current_State+1] =  _CuringwaterbathSymptomMultiChoiceList    
    StateMultiChoiceList[_current_State+2] =  _SteamcleanerSymptomMultiChoiceList   
    StateMultiChoiceList[_current_State+3] =  _SteamcleanerSymptomMultiChoiceList   
    StateMultiChoiceList[_current_State+4] =  _CuringwaterbathSymptomMultiChoiceList
    # len_devices_per_table[7]?
    _current_State =  nx_Child_in( nx_Child_in(first_4eng_State,1) + 8 , 2)
    StateMultiChoiceList[_current_State+0] =  _DispenserSymptomMultiChoiceList
    StateMultiChoiceList[_current_State+1] =  _DispenserSymptomMultiChoiceList    
    StateMultiChoiceList[_current_State+2] =  _SteamcleanerSymptomMultiChoiceList   
    StateMultiChoiceList[_current_State+3] =  _VacuummixerSymptomMultiChoiceList   
    StateMultiChoiceList[_current_State+4] =  _VacuummixerSymptomMultiChoiceList
    # len_devices_per_table[8]?
    _current_State =  nx_Child_in( nx_Child_in(first_4eng_State,1) + 9 , 2)
    StateMultiChoiceList[_current_State+0] =  _TrimmerSymptomMultiChoiceList
    StateMultiChoiceList[_current_State+1] =  _VacuummixerSymptomMultiChoiceList    
    StateMultiChoiceList[_current_State+2] =  _DispenserSymptomMultiChoiceList
    StateMultiChoiceList[_current_State+3] =  _DispenserSymptomMultiChoiceList
    # len_devices_per_table[9]?
    _current_State =  nx_Child_in( nx_Child_in(first_4eng_State,1) + 10 , 2)
    StateMultiChoiceList[_current_State+0] =  _TrimmerSymptomMultiChoiceList
    StateMultiChoiceList[_current_State+1] =  _VacuummixerSymptomMultiChoiceList    
    StateMultiChoiceList[_current_State+2] =  _SteamcleanerSymptomMultiChoiceList
    # len_devices_per_table[10]?
    _current_State =  nx_Child_in( nx_Child_in(first_4eng_State,1) + 11 , 2)
    StateMultiChoiceList[_current_State+0] =  _PollcleanerSymptomMultiChoiceList
    StateMultiChoiceList[_current_State+1] =  _PollcleanerSymptomMultiChoiceList    
    StateMultiChoiceList[_current_State+2] =  _PollcleanerSymptomMultiChoiceList
    StateMultiChoiceList[_current_State+3] =  _PollcleanerSymptomMultiChoiceList
    # len_devices_per_table[11]?

    for i in range(len_tables)  :        
        pop_pushedStateList[nx_Child_in( nx_Child_in(first_4eng_State,1)+i ,3)] = True
    for i in range(len_tables)  :        
        push_StateList[nx_Child_in( nx_Child_in(first_4eng_State,1)+i ,1)] = True
        push_StateList[nx_Child_in( nx_Child_in(first_4eng_State,1)+i ,3)] = True
        for j in range(len(len_devices_per_table)) : 
            push_StateList[nx_Child_in( nx_Child_in(first_4eng_State,1)+i ,2)+j] = True


    fromStateMessageList[first_4eng_State] = SelectString+u'\n' 
    for i in range(len_tables)  :        
        fromStateMessageList[ nx_Child_in(first_4eng_State,1)+i ] = SelectString+u'\n'
        _current_State = nx_Child_in(first_4eng_State,1)+i
        fromStateMessageList[ nx_Child_in(_current_State,1) ] = SelectString+u'\n'  
        _current_State = nx_Child_in(_current_State,1)
        for j in range(len(len_devices_per_table)) : 
            fromStateMessageList[ nx_Child_in(_current_State,1)+j ] = SelectString+u'\n'
        _current_State = nx_Child_in(_current_State,1)
        fromStateMessageList[ nx_Child_in(_current_State,1) ] = SelectString+u'\n'            
        _current_State = nx_Child_in(_current_State,1)
        fromStateMessageList[ nx_Child_in(_current_State,1) ] = SelectString+SubmitString+u'\n'

    toStateMessageList[first_4eng_State] = AskTableNumberString
    for i in range(len_tables)  :        
        toStateMessageList[ nx_Child_in(first_4eng_State,1)+i ] = AskDeviceString
        _current_State = nx_Child_in(first_4eng_State,1)+i
        toStateMessageList[ nx_Child_in(_current_State,1) ] = DirectInsertDeviceString
        _current_State = nx_Child_in(_current_State,1)
        toStateMessageList[ nx_Child_in(_current_State,2) ] = DirectInsertSymptomString
    _current_State =  nx_Child_in( nx_Child_in(first_4eng_State,1) + 0 , 2)
    toStateMessageList[_current_State+0] =  AskMultiSymtomString+u'\n'+_SandblastSymptomJoinString
    toStateMessageList[_current_State+1] =  AskMultiSymtomString+u'\n'+_SandblastSymptomJoinString  
    toStateMessageList[_current_State+2] =  AskMultiSymtomString+u'\n'+_VacuummixerSymptomJoinString
    toStateMessageList[_current_State+3] =  AskMultiSymtomString+u'\n'+_SandblastSymptomJoinString
    toStateMessageList[_current_State+4] =  AskMultiSymtomString+u'\n'+_TrimmerSymptomJoinString
    toStateMessageList[_current_State+5] =  AskMultiSymtomString+u'\n'+_SandblastSymptomJoinString
    toStateMessageList[_current_State+6] =  AskMultiSymtomString+u'\n'+_SandblastSymptomJoinString
    # len_devices_per_table[0]?
    _current_State =  nx_Child_in( nx_Child_in(first_4eng_State,1) + 1 , 2)
    toStateMessageList[_current_State+0] =  AskMultiSymtomString+u'\n'+_TrimmerSymptomJoinString
    toStateMessageList[_current_State+1] =  AskMultiSymtomString+u'\n'+_TrimmerSymptomJoinString
    toStateMessageList[_current_State+2] =  AskMultiSymtomString+u'\n'+_TrimmerSymptomJoinString
    # len_devices_per_table[1]?
    _current_State =  nx_Child_in( nx_Child_in(first_4eng_State,1) + 2 , 2)
    toStateMessageList[_current_State+0] =  AskMultiSymtomString+u'\n'+_TrimmerSymptomJoinString
    toStateMessageList[_current_State+1] =  AskMultiSymtomString+u'\n'+_TrimmerSymptomJoinString
    toStateMessageList[_current_State+2] =  AskMultiSymtomString+u'\n'+_TrimmerSymptomJoinString
    # len_devices_per_table[2]?
    _current_State =  nx_Child_in( nx_Child_in(first_4eng_State,1) + 3 , 2)
    toStateMessageList[_current_State+0] =  AskMultiSymtomString+u'\n'+_TrimmerSymptomJoinString
    toStateMessageList[_current_State+1] =  AskMultiSymtomString+u'\n'+_TrimmerSymptomJoinString
    toStateMessageList[_current_State+2] =  AskMultiSymtomString+u'\n'+_TrimmerSymptomJoinString
    # len_devices_per_table[3]?
    _current_State =  nx_Child_in( nx_Child_in(first_4eng_State,1) + 4 , 2)
    toStateMessageList[_current_State+0] =  AskMultiSymtomString+u'\n'+_CastingmachineSymptomJoinString
    toStateMessageList[_current_State+1] =  AskMultiSymtomString+u'\n'+_ElectricfurnaceSymptomJoinString    
    toStateMessageList[_current_State+2] =  AskMultiSymtomString+u'\n'+_ElectricfurnaceSymptomJoinString    
    toStateMessageList[_current_State+3] =  AskMultiSymtomString+u'\n'+_ElectricfurnaceSymptomJoinString    
    toStateMessageList[_current_State+4] =  AskMultiSymtomString+u'\n'+_ElectricfurnaceSymptomJoinString    
    # len_devices_per_table[4]?
    _current_State =  nx_Child_in( nx_Child_in(first_4eng_State,1) + 5 , 2)
    toStateMessageList[_current_State+0] =  AskMultiSymtomString+u'\n'+_CastingmachineSymptomJoinString
    toStateMessageList[_current_State+1] =  AskMultiSymtomString+u'\n'+_ElectricfurnaceSymptomJoinString    
    toStateMessageList[_current_State+2] =  AskMultiSymtomString+u'\n'+_ElectricfurnaceSymptomJoinString    
    # len_devices_per_table[5]?
    _current_State =  nx_Child_in( nx_Child_in(first_4eng_State,1) + 6 , 2)
    toStateMessageList[_current_State+0] =  AskMultiSymtomString+u'\n'+_CastingmachineSymptomJoinString
    toStateMessageList[_current_State+1] =  AskMultiSymtomString+u'\n'+_ElectricfurnaceSymptomJoinString    
    toStateMessageList[_current_State+2] =  AskMultiSymtomString+u'\n'+_ElectricfurnaceSymptomJoinString    
    # len_devices_per_table[6]?
    _current_State =  nx_Child_in( nx_Child_in(first_4eng_State,1) + 7 , 2)
    toStateMessageList[_current_State+0] =  AskMultiSymtomString+u'\n'+_CuringwaterbathSymptomJoinString
    toStateMessageList[_current_State+1] =  AskMultiSymtomString+u'\n'+_CuringwaterbathSymptomJoinString    
    toStateMessageList[_current_State+2] =  AskMultiSymtomString+u'\n'+_SteamcleanerSymptomJoinString   
    toStateMessageList[_current_State+3] =  AskMultiSymtomString+u'\n'+_SteamcleanerSymptomJoinString   
    toStateMessageList[_current_State+4] =  AskMultiSymtomString+u'\n'+_CuringwaterbathSymptomJoinString
    # len_devices_per_table[7]?
    _current_State =  nx_Child_in( nx_Child_in(first_4eng_State,1) + 8 , 2)
    toStateMessageList[_current_State+0] =  AskMultiSymtomString+u'\n'+_DispenserSymptomJoinString
    toStateMessageList[_current_State+1] =  AskMultiSymtomString+u'\n'+_DispenserSymptomJoinString    
    toStateMessageList[_current_State+2] =  AskMultiSymtomString+u'\n'+_SteamcleanerSymptomJoinString   
    toStateMessageList[_current_State+3] =  AskMultiSymtomString+u'\n'+_VacuummixerSymptomJoinString   
    toStateMessageList[_current_State+4] =  AskMultiSymtomString+u'\n'+_VacuummixerSymptomJoinString
    # len_devices_per_table[8]?
    _current_State =  nx_Child_in( nx_Child_in(first_4eng_State,1) + 9 , 2)
    toStateMessageList[_current_State+0] =  AskMultiSymtomString+u'\n'+_TrimmerSymptomJoinString
    toStateMessageList[_current_State+1] =  AskMultiSymtomString+u'\n'+_VacuummixerSymptomJoinString    
    toStateMessageList[_current_State+2] =  AskMultiSymtomString+u'\n'+_DispenserSymptomJoinString
    toStateMessageList[_current_State+3] =  AskMultiSymtomString+u'\n'+_DispenserSymptomJoinString
    # len_devices_per_table[9]?
    _current_State =  nx_Child_in( nx_Child_in(first_4eng_State,1) + 10 , 2)
    toStateMessageList[_current_State+0] =  AskMultiSymtomString+u'\n'+_TrimmerSymptomJoinString
    toStateMessageList[_current_State+1] =  AskMultiSymtomString+u'\n'+_VacuummixerSymptomJoinString    
    toStateMessageList[_current_State+2] =  AskMultiSymtomString+u'\n'+_SteamcleanerSymptomJoinString
    # len_devices_per_table[10]?
    _current_State =  nx_Child_in( nx_Child_in(first_4eng_State,1) + 11 , 2)
    toStateMessageList[_current_State+0] =  AskMultiSymtomString+u'\n'+_PollcleanerSymptomJoinString
    toStateMessageList[_current_State+1] =  AskMultiSymtomString+u'\n'+_PollcleanerSymptomJoinString    
    toStateMessageList[_current_State+2] =  AskMultiSymtomString+u'\n'+_PollcleanerSymptomJoinString
    toStateMessageList[_current_State+3] =  AskMultiSymtomString+u'\n'+_PollcleanerSymptomJoinString
    # len_devices_per_table[11]?

Error_NoInt     = 0x9
Error_NoSubTree = 0x8
def determineSubGraph( _State , _wantInfo ) :
    if type( _State ) is not int :
        return  Error_NoInt
    else :
        num_str = format(_State,'02X')

        if len(num_str) < len( format(first_4work_State,'02X')) :
            return Error_NoSubTree
        else :
            if    num_str[:len(format(first_4work_State,'02X'))] ==  format(first_4work_State,'02X') :
                if _wantInfo == True :
                    return first_4work_State
                else :
                    return last_4work_Light_State
            elif  num_str[:len(format(first_3com_State,'02X'))] == format(first_3com_State,'02X') :
                if _wantInfo == True :
                    return first_3com_State 
                else :
                    return last_3com_State
            elif  num_str[:len(format(first_4eng_State,'02X'))] == format(first_4eng_State,'02X') :
                if _wantInfo == True :
                    return  first_4eng_State*0x10 +  int('0X'+num_str[len(format(first_4eng_State,'02X'))] ,0)
                else :
                    return last_4eng_State  #?                   
            elif  num_str[:len(format(first_3work_State,'02X'))] == format(first_3work_State ,'02X') :
                if _wantInfo == True :
                    return first_3work_State
                else :
                    return last_3work_Doll_State  
            elif  num_str[:len(format(first_3handpiece_State,'02X'))] == format(first_3handpiece_State,'02X' ) :
                if _wantInfo == True :
                    return first_3handpiece_State
                else :
                    return last_3handpiece_High_State 
            else :
                return Error_NoSubTree

sum_instance = { 'init' :  {} }

instance = { 'temp': {'state':initial_State, 
                      'location'    : '',
                      'seat number' : '' ,
                      'part'        : '',
                      'symptom'     : '' 
                     }
}

organization = { 'init' :  { 'id' : '' ,
                              'name' : ''  
                            }
}
temp_organization = { 'temp' :  { 'id' : '' ,
                                  'name' : ''  
                                }
} 


class  Arrow :
    def  __init__(self, mItemList = { } ) :
        self.mItemList = {   "message" : { "text": "" } ,    } 

    def  _make_Messages_change_State( self, _TextFlag, _text , _PhotoFlag  , _Photo , _mButtonFlag , _mButton,  _ButtonFlag , _fromState, _toState , _userRequest ) :
        self.mItemList["message"]["text"] = _text
        if _PhotoFlag   == True : 
            self.mItemList["message"]["photo"] = _Photo
        if _mButtonFlag == True : 
            self.mItemList["message"]["message_button"] = _mButton
        if _ButtonFlag  == True : 
            self.mItemList["keyboard"] = {  "type": "buttons" }
            self.mItemList["keyboard"]["buttons"] = StateButtonList[_toState]   
        instance[_userRequest['user_key']]['state'] = _toState

        if _fromState in push_StateList and \
           _fromState < _toState :
            if 'prev' in instance[_userRequest['user_key']] :
              instance[_userRequest['user_key']]['pprev'] = instance[_userRequest['user_key']]['prev'] 
            instance[_userRequest['user_key']]['prev']  = _fromState
        elif  _toState in pop_pushedStateList and \
              _fromState > _toState and \
            'pprev' in instance[_userRequest['user_key']] :
            instance[_userRequest['user_key']]['prev']  = instance[_userRequest['user_key']]['pprev']

        return jsonify(self.mItemList)

    def  _make_Message_Button_change_State( self, _TextFlag, _text , _ButtonFlag , _fromState ,_toState , _userRequest ) :
        return self._make_Messages_change_State(_TextFlag, _text , False , {} , False , {} , _ButtonFlag , _fromState ,_toState, _userRequest)

    def  make_Message_Button_change_State(self,  _fromState, _toState, _userRequest, _url_root=None)  :
        _textMessage = _userRequest['content']+ fromStateMessageList[_fromState]  +   toStateMessageList[_toState]
        _ButtonFlag = True
        _PhotoFlag  = True
        _Photo = {}
        if _toState in StateButtonList :
            _ButtonFlag = True 
        else :
            _ButtonFlag = False  
        if  _toState in StatePhotoList and \
            _url_root is not None :
            _PhotoFlag = True
            _Photo["url"] = _url_root + StatePhotoList[_toState]["url"] 
            _Photo["width"] = StatePhotoList[_toState]["width"]
            _Photo["height"] = StatePhotoList[_toState]["height"]
        else :
            _PhotoFlag = False
        return self._make_Messages_change_State(True, _textMessage , _PhotoFlag , _Photo  , False , {} , _ButtonFlag , _fromState, _toState, _userRequest)



def _isValidState(num) :
    if num in state :
        return True
    else:
        return False

def  _nx_Child(stage_num , score) :
    if score == 0 :
        return stage_num
    else :
        return _nx_Child(stage_num * 0x10 +1 , score-1)

def  nx_Child( stage_num , score ) :
    num = _nx_Child(stage_num, score)
    if _isValidState(num) :
        return num
    else :
        return  num*0x100 

def nx_Child_Sibling(stage_num , child_score, sibling_score) :
    num = nx_Child(stage_num, child_score) + sibling_score
    if _isValidState(num) :
        return num
    else :
        return  num*0x100 

def _prev_Parent(stage_num, score) :
    if score == 0 :
        return stage_num 
    else :
        return _prev_Parent( stage_num/0x10  , score-1)    

def prev_Parent(stage_num, score) :
    num = _prev_Parent(stage_num, score)
    if _isValidState(num) :
        return num
    else :
        return num * 0x100

def restore_prev_State(_UserRequestKey) :
    return instance[_UserRequestKey]['prev']

def isValidID( number ) :
    if number % 10000 in range(1, 80+1)  and \
       (number / 10000) % 100 == 74 :
       return True 
    else :
        return False
    return False 

class SummaryText :
    def  __init__(self, mText = '' ) :
        self.mText = '' 
    
    def  _generate(self, _TextMessage,_organization,_instance, _UserRequestKey, _key1=None, _OnlyPart=False) :
        self.mText += _TextMessage
        if _OnlyPart == False :
            self.mText += u'ID         :' + str(_organization[ _UserRequestKey ]['ID'])+u'\n'
            self.mText += u'Name       :' + _organization[ _UserRequestKey ]['Name']+u'\n'

        if _key1 is None :
            self.mText += u'location   :' + _instance[ _UserRequestKey ]['location']+u'\n'
            self.mText += u'seat number:' + _instance[ _UserRequestKey ]['seat number']+u'\n'
            self.mText += u'part       :' + _instance[ _UserRequestKey ]['part']+u'\n'
            self.mText += u'symptom    :' + _instance[ _UserRequestKey ]['symptom']
        else : 
            if _OnlyPart == False :
                self.mText += u'location   :' + _instance[ _UserRequestKey ][_key1]['location']+u'\n'
                self.mText += u'seat number:' + _instance[ _UserRequestKey ][_key1]['seat number']+u'\n'
            self.mText += u'part       :' + _instance[ _UserRequestKey ][_key1]['part']+u'\n'
            self.mText += u'symptom    :' + _instance[ _UserRequestKey ][_key1]['symptom']+u'\n'
        return self.mText

def mail( to, subject, body, attach=None):
    gmail_user = "khudfix@gmail.com"
    gmail_password = "khudfixars"

    email_text = """\  
    From: %s  
    To: %s  
    Subject: %s

    %s
    """ % (gmail_user, ", ".join(to), subject, body)
     
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(gmail_user , to, email_text )
    server.close()


x=datetime.today()
#y=x.replace(day=x.day, hour=12, minute=0, second=0, microsecond=0)
y=x.replace(day=x.day, hour=x.hour+3, minute=0, second=0, microsecond=0)
delta_t=y-x


secs=delta_t.seconds+1


def hello_world() :
    to = [ 'kws015@hanmail.net' ] 
    subject =  'My first email through python flask'
    body = 'this is all for Timer \n'                
    #mail(to, subject , body)  
    x=datetime.today()
    y=x.replace(day=x.day, hour=x.hour+3, minute=0, second=0, microsecond=0)
    delta_t=y-x

    body += str(y.day) + '/'+ str(y.hour)+'\n'
    mail(to, subject , body)    

    secs=delta_t.seconds+1
    s = Timer(secs, hello_world)
    s.start()



t = Timer(secs, hello_world)
t.start()
generate4EngStatesInformation()

@app.route('/')
def Welcome():
    return app.send_static_file('index.html')

@app.route('/myapp')
def WelcomeToMyapp():
    return 'Welcome again to my app running on Bluemix!!'

@app.route('/keyboard')
def Keyboard():    
    ItemList = {
        'type': 'buttons', 'buttons' : StateButtonList[initial_State]
    }    
    return jsonify(ItemList)

@app.route('/message', methods=['POST'])
def GetMessage():
    userRequest = json.loads(request.get_data()) 

    # if its a 1st message, you have to make instance
    if userRequest['user_key'] not in instance :
        instance[userRequest['user_key']] = { 'state' : state[initial_State] }
    # if its a sudden quit-and-reenter case, then make state initial
    if  instance[userRequest['user_key']]['state'] != state[initial_State] and \
        userRequest['content']  in  StateButtonList[initial_State] :
            instance[userRequest['user_key']]['state'] = state[initial_State]        

    #select initially 
    if instance[userRequest['user_key']]['state'] == state[ initial_State ] :        #state 1
        currentState = instance[userRequest['user_key']]['state']   
        if  userRequest['content']  ==  StateButtonList[ currentState ][0] :
            if  userRequest['user_key'] not in organization :
                return Arrow().make_Message_Button_change_State(currentState, nx_Child(currentState,1) ,userRequest)
            else :
                return Arrow().make_Message_Button_change_State(currentState, nx_Child(currentState,3) ,userRequest)
        elif userRequest['content']  ==  StateButtonList[ currentState ][1] :
            _textMessage = userRequest['content']+SelectString+u'\n'+u'Version: '+ VersionString +u'\n'+UnderConstructionString+u'\n'
            _textMessage += time.strftime('%X %x %Z') + u'\n'
            _textMessage += u'최종 접수 예정:' +u'\n'

            _UserRequestKey = userRequest['user_key'] 
            if _UserRequestKey in sum_instance and \
               _UserRequestKey in organization  :
                for i in range( len(sum_instance[_UserRequestKey]) ):
                    _textMessage += SummaryText()._generate(u'---------' + str(i+1) +  u'------------\n' , organization, sum_instance, _UserRequestKey, i)


                to = [ 'kws015@hanmail.net' ] 
                subject =  'My first email through python flask'
                body = 'this is all for you\n'
                body += str(organization[ _UserRequestKey ]['ID'])+'\n'


                try:
                    mail(to, subject , body)

                except smtplib.SMTPAuthenticationError : 
                    _textMessage += u'something went wrong1' 
                except smtplib.SMTPException : 
                    _textMessage += u'something went wrong2' 
                except :
                    _textMessage += u'something went wrong0'
            _textMessage += u'최종 접수 완료:' +u'\n'
            return Arrow()._make_Message_Button_change_State(True, _textMessage, True ,  currentState, currentState, userRequest)
        elif userRequest['content']  ==  StateButtonList[ currentState ][2] :             
            _textMessage = userRequest['content']+SelectString+u'\n'+UnderConstructionString
            _mButton = { "label": "link를 click해주세요", "url" : "https://www.youtube.com/watch?v=aj4VQmfiTBk" }
            return Arrow()._make_Messages_change_State(True, _textMessage, False , {} , True, _mButton, True,currentState, currentState , userRequest)
        elif userRequest['content']  ==  StateButtonList[ currentState ][3] :            
            return Arrow().make_Message_Button_change_State(currentState,    nx_Child_Sibling(currentState,1,3) , userRequest)
              
        else :
            _textMessage = userRequest['content']+SelectString+u'\n'+UnderConstructionString
            return Arrow()._make_Message_Button_change_State(True, _textMessage, True ,currentState , currentState, userRequest)

    elif   instance[userRequest['user_key']]['state'] \
        in [ nx_Child(initial_State,1) , first_Independent_IDInsert_State ]  :    #11, 141
        currentState = instance[userRequest['user_key']]['state']   
        try :
            if isValidID( int ( userRequest['content'] ) ) :
                temp_organization[userRequest['user_key']] = { 'ID' : int ( userRequest['content'] ) }                
                return Arrow().make_Message_Button_change_State( currentState, nx_Child( currentState, 1 )  , userRequest)
            elif  int ( userRequest['content'] ) == 0 : # return to prev menu
                return Arrow().make_Message_Button_change_State( currentState ,  prev_Parent(currentState,1)  , userRequest)
            else : 
                _textMessage = userRequest['content']+SelectString+u'\n' + InsertValidNumberString
                return Arrow()._make_Message_Button_change_State(True, _textMessage, False, currentState, currentState, userRequest)             
        except ValueError :
            _textMessage = userRequest['content']+SelectString+u'\n'+ InsertNumberString
            return Arrow()._make_Message_Button_change_State(True, _textMessage, False,currentState , currentState , userRequest)    

    #insert Name and prepare arrows
    elif   instance[userRequest['user_key']]['state']  \
        in [  nx_Child(initial_State,2),   nx_Child(first_Independent_IDInsert_State,1) ]  :               #111 , 1411
        currentState = instance[userRequest['user_key']]['state'] 
        if  userRequest['content']  == '0' :
            return Arrow().make_Message_Button_change_State(currentState, prev_Parent(currentState,1) , userRequest, request.url_root)   
        else :
            temp_organization[userRequest['user_key']]['Name'] = userRequest['content'] 
            if currentState == nx_Child(first_Independent_IDInsert_State,1) :
                _textMessage = userRequest['content']+SelectString+u'\n'+  LastYesNoString +u'\n'
                _textMessage += u'ID   :'+ str(temp_organization[userRequest['user_key']]['ID'])+u'\n'
                _textMessage += u'Name :'+ temp_organization[userRequest['user_key']]['Name']
                return Arrow()._make_Message_Button_change_State(True, _textMessage, True, currentState,  nx_Child( currentState ,1) , userRequest)             
            else :
                return Arrow().make_Message_Button_change_State(currentState, nx_Child(currentState,1) , userRequest ) 

    elif   instance[userRequest['user_key']]['state']  == nx_Child( first_Independent_IDInsert_State, 2 ) : #14111
        currentState = instance[userRequest['user_key']]['state']   
        if  userRequest['content']  ==  StateButtonList[ currentState ][0] :
            if  userRequest['user_key'] in temp_organization and \
                userRequest['user_key'] not in  organization :
                organization[userRequest['user_key']] = { 'ID' :  temp_organization[userRequest['user_key']]['ID']    }
                organization[userRequest['user_key']]['Name'] = temp_organization[userRequest['user_key']]['Name']   
                temp_organization.pop( userRequest['user_key'] ,  None)
            _textMessage = userRequest['content']+  u'\n' +SubmitString 
            instance[userRequest['user_key']] = { 'state' : state[initial_State] }            
            return  Arrow()._make_Message_Button_change_State(True, _textMessage, True, currentState, initial_State, userRequest)
        elif userRequest['content']  ==  StateButtonList[ currentState ][2] :
            return Arrow().make_Message_Button_change_State(currentState, prev_Parent(currentState,1) , userRequest)
        else : 
            _textMessage = userRequest['content']+ u'\n'+ CancelString 
            instance[userRequest['user_key']] = { 'state' : state[initial_State] }            
            return  Arrow()._make_Message_Button_change_State(True, _textMessage, True, currentState,initial_State, userRequest)

    #select location  
    elif instance[userRequest['user_key']]['state'] == nx_Child( initial_State ,3) :  #1111
        currentState = instance[userRequest['user_key']]['state']
        if  userRequest['content']  ==  StateButtonList[currentState][0] :
            instance[userRequest['user_key']]['location'] = userRequest['content']
            return Arrow().make_Message_Button_change_State(currentState, first_4work_State, userRequest, request.url_root  )
        elif userRequest['content']  ==  StateButtonList[currentState][1] :
            instance[userRequest['user_key']]['location'] = userRequest['content']
            return Arrow().make_Message_Button_change_State(currentState, first_4eng_State, userRequest, request.url_root  )
        elif userRequest['content']  ==  StateButtonList[currentState][2] :            
            return Arrow().make_Message_Button_change_State(currentState, nx_Child_Sibling(currentState,1,2) , userRequest )
        elif userRequest['content']  ==  StateButtonList[currentState][3] :
            instance[userRequest['user_key']]['location'] = userRequest['content']
            return Arrow().make_Message_Button_change_State(currentState, first_3com_State, userRequest, request.url_root )
        elif userRequest['content']  ==  StateButtonList[currentState][4] :
            _textMessage = userRequest['content']+SelectString+u'\n'+UnderConstructionString
            return Arrow()._make_Message_Button_change_State(True, _textMessage, True ,currentState, initial_State, userRequest)
        elif userRequest['content']  ==  StateButtonList[currentState][5] :  # return to prev menu
            if userRequest['user_key'] in organization :
              return Arrow().make_Message_Button_change_State( currentState , prev_Parent(currentState,3) , userRequest)
            else :
              return Arrow().make_Message_Button_change_State( currentState,  prev_Parent(currentState,1) , userRequest  )            
        else :
            _textMessage = userRequest['content']+SelectString+u'\n'+'(state:'+ str(instance[userRequest['user_key']]['state']) + ')'
            instance[userRequest['user_key']] = { 'state' : state[initial_State] }            
            return  Arrow()._make_Message_Button_change_State(True, _textMessage, True, currentState ,  initial_State, userRequest)

    #select memebership item and prepare arrows
    elif instance[userRequest['user_key']]['state'] == state[nx_Child_Sibling( initial_State ,1,3)] :
        currentState = instance[userRequest['user_key']]['state']
        if  userRequest['content']  ==  StateButtonList[currentState][0] :
            if  userRequest['user_key'] in organization :
                key = userRequest['user_key']
                _text_  = u'이미 입력된 ID와 Name이 있습니다.'
                _text_ += u'새로 입력하시려면 기존 ID와 Name을 먼저 삭제하고 입력해주세요.'+u'\n'
                _text_ += u'기존 ID   :'+ str(organization[key]['ID'])+u'\n'
                _text_ += u'기존 Name :'+ organization[key]['Name']+u'\n'
                return Arrow()._make_Message_Button_change_State(True, _text_, True, currentState, currentState , userRequest )            

                #fill this later. for one user multi device case
                #elif organization[key]['ID'] == temp_organization[userRequest['user_key']]['ID'] :
                    #_ItemList["message"]["text"] =  u'다른 device를 사용 중입니다.' +  u'\n'
                    #_ItemList["message"]["text"] += u'기존 ID   :'+ str(organization[key]['ID'])+u'\n'
                    #_ItemList["message"]["text"] += u'기존 Name :'+ organization[key]['Name']+u'\n'
                    #_ItemList["message"]["text"] += u'새로운 device를 사용하시겠습니까?.'
                    #_ItemList["keyboard"]["buttons"] =    StateButtonList[41111] 
                    #instance[userRequest['user_key']]['state'] = state[41111] 
                    #return jsonify(_ItemList)
            else :
                return Arrow().make_Message_Button_change_State(currentState, first_Independent_IDInsert_State , userRequest)

        elif  userRequest['content']  ==  StateButtonList[currentState][1] :
            if userRequest['user_key'] in organization:
                _text_ = userRequest['content']+SelectString + u'\n' + AskDeletionString+ u'\n'
                _text_ += u'ID   :'+ str(organization[userRequest['user_key']]['ID'])+u'\n'
                _text_ += u'Name :'+ organization[userRequest['user_key']]['Name']+u'\n'
                return Arrow()._make_Message_Button_change_State(True, _text_, True, currentState, nx_Child_Sibling(currentState,1,1) , userRequest )            
            else : 
                _text_ =  userRequest['content']+SelectString + u'\n' + u'등록된 ID와 Name이 없습니다.'           
                return Arrow()._make_Message_Button_change_State( True, _text_, True, currentState,  initial_State , userRequest )   
        elif  userRequest['content']  ==  StateButtonList[currentState][4] :  # return to prev menu
            return Arrow().make_Message_Button_change_State( currentState , prev_Parent(currentState,1) , userRequest )                        
        else : 
            _text_ = userRequest['content']+SelectString
            return Arrow()._make_Message_Button_change_State(True,  _text_, True, currentState,  initial_State , userRequest )                        
    elif   instance[userRequest['user_key']]['state']  in  \
    [ first_4work_State , first_3work_State , first_3handpiece_State,  first_3com_State, first_4eng_State ] :
        currentState = instance[userRequest['user_key']]['state']
        if  userRequest['content'].isdigit()  :
            currentContent  = userRequest['content']
            currentIntValue = int( userRequest['content'] ) 
            if  currentIntValue == 0 :
                return Arrow().make_Message_Button_change_State(currentState, prev_Parent(currentState,1) , userRequest)   
            elif instance[userRequest['user_key']]['state'] in [first_4work_State , first_3work_State, first_3handpiece_State] and \
                 currentIntValue  in range(1,96+1) :
                instance[userRequest['user_key']]['seat number'] = currentContent
                return Arrow().make_Message_Button_change_State(currentState, nx_Child(currentState,1) , userRequest, request.url_root)
            elif instance[userRequest['user_key']]['state'] in [first_3com_State] and \
                 currentIntValue  in range(1,88+1) :
                instance[userRequest['user_key']]['seat number'] = currentContent
                return Arrow().make_Message_Button_change_State(currentState, nx_Child(currentState,1) , userRequest, request.url_root)
            elif instance[userRequest['user_key']]['state'] in [first_4eng_State] and \
                 currentIntValue  in range(1, len_4eng_tables+1) :
                instance[userRequest['user_key']]['seat number'] = currentContent
                return Arrow().make_Message_Button_change_State(currentState, nx_Child_Sibling(currentState,1,currentIntValue-1) , userRequest, request.url_root)
            else :
                _textMessage = currentContent+SelectString+u'\n'+ InsertValidNumberString
                return Arrow()._make_Message_Button_change_State(True, _textMessage,  False, currentState,   currentState , userRequest)
        else : 
            _textMessage = userRequest['content']+SelectString+u'\n'+ InsertNumberString
            return Arrow()._make_Message_Button_change_State(True, _textMessage,  False, currentState, currentState , userRequest)

    elif   instance[userRequest['user_key']]['state'] in \
    [ nx_Child(first_4work_State,1) ,  nx_Child(first_3work_State,1) , nx_Child(first_3handpiece_State,1) , nx_Child(first_3com_State ,1) ] + \
    list( range( nx_Child(first_4eng_State,1) , nx_Child_Sibling(first_4eng_State,1,12-1)+1) ) :
        currentState = instance[userRequest['user_key']]['state']
        #if userRequest['content'] in  StateButtonList[nx_Child(first_4work_State,1)] :
        if userRequest['content'] in  StateButtonList[currentState] :
            #i = StateButtonList[nx_Child(first_4work_State,1)].index(userRequest['content'])
            i = StateButtonList[currentState].index(userRequest['content'])
            if i == len(StateButtonList[currentState]) -2 :
                return Arrow().make_Message_Button_change_State(currentState, nx_Child(currentState ,1), userRequest, request.url_root)
            elif i == len(StateButtonList[currentState]) -1 :
                return Arrow().make_Message_Button_change_State(currentState, prev_Parent(currentState,1) , userRequest, request.url_root  )   
            else :
                instance[userRequest['user_key']]['part'] = userRequest['content']
                return Arrow().make_Message_Button_change_State(currentState, nx_Child_Sibling(currentState,2,i) , userRequest )
        else : 
            _textMessage = userRequest['content']+SelectString+u'\n'+'(state:'+ str(instance[userRequest['user_key']]['state']) + ')'
            instance[userRequest['user_key']] = { 'state' : state[initial_State] }            
            return  Arrow()._make_Message_Button_change_State(True, _textMessage, True, currentState,   initial_State, userRequest)
    elif   instance[userRequest['user_key']]['state'] in \
     [ nx_Child(first_4work_State,2) , nx_Child(first_3work_State,2), nx_Child(first_3handpiece_State ,2) , nx_Child(first_3com_State ,2)] + \
     list( range(   nx_Child(nx_Child(first_4eng_State,1),1), nx_Child( nx_Child_Sibling(first_4eng_State,1,12-1), 1)+1 ,  0x10) ) :
        currentState = instance[userRequest['user_key']]['state']
        if  userRequest['content']  == '0' :
            return Arrow().make_Message_Button_change_State(currentState, prev_Parent(currentState,1) , userRequest, request.url_root)   
        instance[userRequest['user_key']]['part'] = userRequest['content']
        return Arrow().make_Message_Button_change_State(currentState, nx_Child(currentState,2), userRequest)

    elif  instance[userRequest['user_key']]['state'] in range(nx_Child(first_4work_State,3)+0, nx_Child(first_4work_State,3)+ len_4work_part-2 )   or  \
          instance[userRequest['user_key']]['state'] in range(nx_Child(first_3handpiece_State,3)+0, nx_Child(first_3handpiece_State,3)+ len_3handpiece_part-2 )  :
#          instance[userRequest['user_key']]['state'] in range(nx_Child(first_3com_State ,3)+1, nx_Child(first_3com_State ,3)+ len_3com_part-2 )  : 
#          instance[userRequest['user_key']]['state'] in range(nx_Child(first_3work_State,3)+0, nx_Child(first_3work_State ,3)+ len_3work_part-2 )  or  \
        currentState = instance[userRequest['user_key']]['state'] 
        if  userRequest['content'] in StateButtonList[ currentState ] :
            lastKeyIndex = len(StateButtonList[ currentState ])-1
            #direct describe case
            if  userRequest['content']  ==  StateButtonList[ currentState ][lastKeyIndex-1] :
                return Arrow().make_Message_Button_change_State(currentState,nx_Child(  determineSubGraph(currentState, True) ,4), userRequest )
            elif  userRequest['content']  ==  StateButtonList[ currentState ][lastKeyIndex] :
                return Arrow().make_Message_Button_change_State(currentState, prev_Parent(currentState,2) , userRequest, request.url_root)   
            else:
                instance[userRequest['user_key']]['symptom'] = userRequest['content']            
                # ID info in temp_organization 
                if userRequest['user_key'] not in organization:
                    _textMessage = SummaryText()._generate(LastYesNoString+u'\n' ,  temp_organization , instance , userRequest['user_key'])                
                    return Arrow()._make_Message_Button_change_State(True, _textMessage, True, currentState, nx_Child(  determineSubGraph(currentState, True) ,5) , userRequest)             
                #already ID info  in organization  
                else : 
                    _textMessage = SummaryText()._generate(LastYesNoString+u'\n' ,  organization , instance , userRequest['user_key'])                
                    return Arrow()._make_Message_Button_change_State(True, _textMessage, True, currentState, nx_Child(  determineSubGraph(currentState, True) ,5) , userRequest)                     
        else :
            _textMessage = userRequest['content']+SelectString+u'\n'
            instance[userRequest['user_key']] = { 'state' : state[initial_State] }            
            temp = Arrow()._make_Message_Button_change_State(True, _textMessage, True, currentState,  initial_State, userRequest)
            # have to enable and verify  below code
            ##instance.pop( userRequest['user_key'] ,  None)
            return temp
 
    elif    instance[userRequest['user_key']]['state'] in  \
            list(range(nx_Child(first_3com_State ,3)+0, nx_Child(first_3com_State ,3)+ len_3com_part-2 )) + \
            list(range(nx_Child(first_3work_State,3)+0, nx_Child(first_3work_State ,3)+ len_3work_part-2 )) + \
            _4EngSymptomStateList :   
        currentState = instance[userRequest['user_key']]['state'] 
        #instance[userRequest['user_key']]['symptom'] 
        _textMultiChoice = u'' 
        tokens =  userRequest['content'].split(",")   
        if  len(tokens) == 1 and \
            tokens[0].strip().isdigit() and \
            int ( tokens[0].strip() ) == 0 :
                return Arrow().make_Message_Button_change_State(currentState, prev_Parent(currentState,2) , userRequest, request.url_root)              
        for token in tokens :
            if token.strip().isdigit() : 
                if int(token.strip()) in range( 1, 1+len( StateMultiChoiceList[currentState] ) ) :
                    _textMultiChoice += StateMultiChoiceList[currentState][ int(token.strip())-1 ]                    
                else :
                    _textMessage = token.strip()+SelectString+u'\n'+ InsertValidNumberString
                    return Arrow()._make_Message_Button_change_State(True, _textMessage,  False, currentState,   currentState , userRequest)                  
            else :
                _textMultiChoice += token.strip()
            if  token != tokens[-1] :
                _textMultiChoice += u', '

        instance[userRequest['user_key']]['symptom'] = _textMultiChoice

        _UserRequestKey = userRequest['user_key']
        # ID info in temp_organization 
        if userRequest['user_key'] not in organization:
            _textMessage = SummaryText()._generate(LastYesNoString+u'\n' ,  temp_organization , instance , userRequest['user_key'])     
            #if  _UserRequestKey in sum_instance :
            #    _textMessage += u'\n\n'+u'다른 접수 내역(같은 자리만):' +u'\n'
            #    for i in range( len(sum_instance[_UserRequestKey]) ) :
            #        if   sum_instance[_UserRequestKey][i]['seat number'] == instance[_UserRequestKey]['seat number'] and \
            #             sum_instance[_UserRequestKey][i]['location'] == instance[_UserRequestKey]['location'] :
            #            _textMessage += SummaryText()._generate(u'---------' + str(i+1) +  u'------------\n' , temp_organization, sum_instance, _UserRequestKey, i, True)
            if  currentState not in _4EngSymptomStateList :
                return Arrow()._make_Message_Button_change_State(True, _textMessage, True, currentState, nx_Child(  determineSubGraph(currentState, True) ,5) , userRequest)             
            else  :
                return Arrow()._make_Message_Button_change_State(True, _textMessage, True, currentState, nx_Child(  determineSubGraph(currentState, True) ,4) , userRequest)                           
        #already ID info  in organization  
        else : 
            _textMessage = SummaryText()._generate(LastYesNoString+u'\n' ,  organization , instance , userRequest['user_key'])                
            #if  _UserRequestKey in sum_instance :
            #    _textMessage += u'\n\n'+u'다른 접수 내역(같은 자리만):' +u'\n'
            #    for i in range( len(sum_instance[_UserRequestKey]) ) :
            #        if   sum_instance[_UserRequestKey][i]['seat number'] == instance[_UserRequestKey]['seat number'] and \
            #             sum_instance[_UserRequestKey][i]['location'] == instance[_UserRequestKey]['location'] :
            #            _textMessage += SummaryText()._generate(u'---------' + str(i+1) +  u'------------\n' , organization, sum_instance, _UserRequestKey, i, True)
            if  currentState not in _4EngSymptomStateList :
                return Arrow()._make_Message_Button_change_State(True, _textMessage, True, currentState, nx_Child(  determineSubGraph(currentState, True) ,5) , userRequest)             
            else :
                return Arrow()._make_Message_Button_change_State(True, _textMessage, True, currentState, nx_Child(  determineSubGraph(currentState, True) ,4) , userRequest)             


    elif   instance[userRequest['user_key']]['state']  \
    in  [ nx_Child(first_4work_State,4) , nx_Child(first_3work_State,4) , nx_Child(first_3handpiece_State ,4) , nx_Child(first_3com_State ,4) ]  +  \
    list( range(   nx_Child(nx_Child(first_4eng_State,1),3), nx_Child( nx_Child_Sibling(first_4eng_State,1,12-1), 3)+1 ,  0x10) )   :
        currentState = instance[userRequest['user_key']]['state'] 

        if  userRequest['content']  == '0' :
            return Arrow().make_Message_Button_change_State(currentState, restore_prev_State( userRequest['user_key'] )  , userRequest, request.url_root)   
        instance[userRequest['user_key']]['symptom'] = userRequest['content']            
        # no ID info case
        if userRequest['user_key'] not in organization:
            _textMessage = SummaryText()._generate(LastYesNoString+u'\n' ,  temp_organization , instance , userRequest['user_key'])   
            if currentState not in  range(   nx_Child(nx_Child(first_4eng_State,1),3), nx_Child( nx_Child_Sibling(first_4eng_State,1,12-1), 3)+1 ,  0x10)  :            
                return Arrow()._make_Message_Button_change_State(True, _textMessage, True, currentState, nx_Child(  determineSubGraph(currentState, True) ,5) , userRequest)             
            else :
                return Arrow()._make_Message_Button_change_State(True, _textMessage, True, currentState, nx_Child(  determineSubGraph(currentState, True) ,4) , userRequest)                           
        # already have ID info   
        else : 
            _textMessage = SummaryText()._generate(LastYesNoString + u'\n' ,  organization , instance , userRequest['user_key'])                
            if currentState not in  range(   nx_Child(nx_Child(first_4eng_State,1),3), nx_Child( nx_Child_Sibling(first_4eng_State,1,12-1), 3)+1 ,  0x10)  :            
                return Arrow()._make_Message_Button_change_State(True, _textMessage, True, currentState, nx_Child(  determineSubGraph(currentState, True) ,5) , userRequest)             
            else :
                return Arrow()._make_Message_Button_change_State(True, _textMessage, True, currentState, nx_Child(  determineSubGraph(currentState, True) ,4) , userRequest)             

    elif   instance[userRequest['user_key']]['state']  \
    in [ nx_Child(first_4work_State,5)   ,nx_Child(first_3work_State ,5) , nx_Child(first_3handpiece_State ,5), nx_Child( first_3com_State,5) ] +\
        list( range(   nx_Child(nx_Child(first_4eng_State,1),4), nx_Child( nx_Child_Sibling(first_4eng_State,1,12-1), 4)+1 ,  0x10) ):
        currentState = instance[userRequest['user_key']]['state']   

        if  userRequest['content']  in [ StateButtonList[ currentState ][0] , StateButtonList[ currentState ][1] ] :

            if  userRequest['user_key'] in temp_organization and \
                userRequest['user_key'] not in  organization :
                organization[userRequest['user_key']] = { 'ID' :  temp_organization[userRequest['user_key']]['ID']    }
                organization[userRequest['user_key']]['Name'] = temp_organization[userRequest['user_key']]['Name']   
                temp_organization.pop( userRequest['user_key'] ,  None)

            _UserRequestKey = userRequest['user_key']
            _Time = time.strftime('%X %x %Z')
            if _UserRequestKey not in sum_instance    :
                sum_instance[_UserRequestKey] = []

            _copy_instance = { 'time':_Time }
            _copy_instance['location'] = instance[ _UserRequestKey ]['location']
            _copy_instance['seat number'] = instance[ _UserRequestKey ]['seat number']
            _copy_instance['part']  = instance[ _UserRequestKey ]['part']            
            _copy_instance['symptom'] = instance[ _UserRequestKey ]['symptom']
            sum_instance[_UserRequestKey].append(_copy_instance)

            if  userRequest['content']  ==  StateButtonList[ currentState ][0] :
                instance[userRequest['user_key']] = { 'state' : state[initial_State] }            
                return  Arrow().make_Message_Button_change_State(currentState, initial_State, userRequest)
            else  :
                if currentState not in  range(   nx_Child(nx_Child(first_4eng_State,1),4), nx_Child( nx_Child_Sibling(first_4eng_State,1,12-1), 4)+1 ,  0x10)  :
                    return Arrow().make_Message_Button_change_State(currentState, nx_Child( determineSubGraph(currentState, True),1)  , userRequest, request.url_root)
                else :
                    return Arrow().make_Message_Button_change_State(currentState, determineSubGraph(currentState, True)  , userRequest, request.url_root)                  
        elif userRequest['content']  ==  StateButtonList[ currentState ][3] :  # prev menu
            return Arrow().make_Message_Button_change_State(currentState, restore_prev_State(userRequest['user_key'])  , userRequest)
            #if  userRequest['user_key'] not in temp_organization and \
            #    userRequest['user_key'] in  organization :
            #    return Arrow().make_Message_Button_change_State(currentState, restore_prev_State(userRequest['user_key'])  , userRequest)
            #return Arrow().make_Message_Button_change_State(currentState ,  prev_Parent( currentState, 1 ) , userRequest)             
#            _textMessage = userRequest['content']+SelectString+u'\n'+ InsertNameString
#            return Arrow()._make_Message_Button_change_State(_textMessage, False, prev_Parent( currentState, 1 ) , userRequest)             

#        elif userRequest['content']  ==  StateButtonList[ currentState ][3] :
#            return Arrow().make_Message_Button_change_State(currentState, nx_Child( determineSubGraph(currentState, True),1)  , userRequest, request.url_root)

        else :   # No case
            _textMessage = userRequest['content']+ u'\n'+ CancelString 
            instance[userRequest['user_key']] = { 'state' : state[initial_State] }            
            return  Arrow()._make_Message_Button_change_State(True, _textMessage, True, currentState,initial_State, userRequest)

    #elif  instance[userRequest['user_key']]['state'] == 13 :
#    elif  instance[userRequest['user_key']]['state'] == nx_Child_Sibling(1,1,2) :        
    elif  instance[userRequest['user_key']]['state'] == nx_Child_Sibling( initial_State ,4,2) :        

        currentState = instance[userRequest['user_key']]['state']              
        if  userRequest['content']  ==  StateButtonList[ currentState ][0] :
            instance[userRequest['user_key']]['location'] = userRequest['content']
            return Arrow().make_Message_Button_change_State(currentState, nx_Child(currentState,1) , userRequest, request.url_root)
        elif  userRequest['content']  ==  StateButtonList[ currentState ][1] :
            instance[userRequest['user_key']]['location'] = userRequest['content']
            return Arrow().make_Message_Button_change_State(currentState, nx_Child_Sibling(currentState,1,1), userRequest, request.url_root)
        elif  userRequest['content']  ==  StateButtonList[ currentState ][2] :
            return Arrow().make_Message_Button_change_State(currentState, prev_Parent( currentState, 1 ) , userRequest)   
        else : 
            _textMessage = userRequest['content']+ u'\n'+ CancelString 
            instance[userRequest['user_key']] = { 'state' : state[initial_State] }            
            return  Arrow()._make_Message_Button_change_State(True, _textMessage, True,  currentState,initial_State, userRequest)

    #insert Yes of No for delete and prepare branches
#    elif  instance[userRequest['user_key']]['state'] == state[42] :
    elif  instance[userRequest['user_key']]['state'] == first_Independent_IDInsert_State+1  :
        currentState = instance[userRequest['user_key']]['state']              
        if  userRequest['content']  ==  StateButtonList[currentState][0] :
            organization.pop( userRequest['user_key'] ,  None)
            return Arrow().make_Message_Button_change_State(currentState, initial_State, userRequest)
        elif  userRequest['content']  ==  StateButtonList[currentState][1] :
            return Arrow().make_Message_Button_change_State(currentState, initial_State, userRequest)
        elif  userRequest['content']  ==  StateButtonList[currentState][2] :
            return Arrow().make_Message_Button_change_State(currentState,  prev_Parent(currentState,1) , userRequest)

    #else:     
    _text = '(state:'+ format(instance[userRequest['user_key']]['state'] , '#04x' ) + ')' + userRequest['content']
    text = "Valid command!"   
    text = text + "!! (" + _text + ")"  
    text = text + '(user_key:' + userRequest['user_key'] + ')'

    if userRequest['user_key'] not in instance :
        text = text + 'user_key is NOT in instance'
    else :
        text = text + 'user_key is in instance'
    textContent = {"text":text}
    textMessage = {"message":textContent}
    return jsonify(textMessage)

@app.errorhandler(404)
def page_not_found(e):
    text = "Invalid command!"
    textContent = {"text":text}
    errorMessage = {"message":textContent}
    return jsonify(errorMessage)

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
