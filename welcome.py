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
      u'5.공기 흡입구(Suction)',
      u'6.공기 방출구' ,
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
      u'1.토마스',
      u'2.모니터',
      u'5.직접 입력'  ,    
      u'이전 메뉴'              
]
len_3work_part = len( _State1311KeyList)


_State1321KeyList = [
      u'1.하이스피드',
      u'2.로우스피드',
      u'5.직접 입력'  ,    
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
      u'Hand/Foot 조절 안 됨',      
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
      u'몸체 회전 안 됨' ,
      u'목 셕션 안 됨' , 
      u'증상 직접 입력',
      u'이전 메뉴'        
]

#_LightSymptomKeyList = _YesorNoKeyList 
#_State11111111KeyList = _YesorNoKeyList 

_HighspeedSymtomKeyList = [
      u'회전 안 됨' , 
      u'증상 직접 입력', 
      u'이전 메뉴'       
]

_LowspeedSymptomList = _HighspeedSymtomKeyList

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



StateMultiChoiceList = {
                11114111: _MonitorSymptomMultiChoiceList ,  11114112:_CombodySymptomMultiChoiceList ,  11114113:_ComnetworkSymptomMultiChoiceList 
}

StateButtonList = { 1: _State0KeyList, 
                  14: _State4KeyList ,
                  142 : _YesorNoKeyList ,
                 1111: _State1KeyList ,             
                 11113:  _State13KeyList,            
                 111111: _State111KeyList,          111141: _State141KeyList,  
                 1111311: _State1311KeyList ,       1111321 : _State1321KeyList, 
                 14111: _YesorNoKeyList ,                 
                 11111111: _LightSymptomKeyList  ,  11111112: _MonitorSymptomKeyList ,    11111113 : _GastorchSymptomKeyList , 
                 11111114: _HandpieceengineSymptomKeyList ,11111115: _AirinletSymptomKeyList ,    11111116: _AiroutletSymptomKeyList ,
                 #11114111: _MonitorSymptomKeyList,  
                 #11114112: _ComnetworkSymptomKeyList, 
                 141111: _YesorNoKeyList  ,   
                                                 111131111: _DollSymtomKeyList ,        111131112: _MonitorSymptomKeyList,
                                                 111132111: _HighspeedSymtomKeyList,    111132112: _LowspeedSymptomList,                
                 1111111111: _YesorNoKeyList,    1111411111: _YesorNoKeyList,
                 11113111111: _YesorNoKeyList,   11113211111: _YesorNoKeyList                      
}

StatePhotoList = {  
                    11111:   {"url": u'static/images/4work_seats.jpeg' , "width": 399, "height": 490 } ,
                    111111:  {"url": u'static/images/4work_oneseat.png' ,"width": 200, "height": 283 } ,
                    111131:  {"url": u'static/images/4work_seats.jpeg' ,"width": 399,"height": 490 }, 
                    1111311: {"url": u'static/images/3work_oneseat.png' ,"width": 200, "height": 283 } ,
                    111132:  {"url": u'static/images/3work_case.png' ,"width": 230,"height": 218}, 
                    1111321: {"url": u'static/images/3work_caseopen.png' ,"width": 200,"height": 283 } ,
                    11114:   {"url": u'static/images/3com_seats.png' ,   "width": 360,"height": 270 }, 
                    111141:  {"url": u'static/images/3com_oneseat.png' ,"width": 363,"height": 616 }
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
AskPartString = u'어떤 부분이 문제인가요?'
AskSymtomString = u'어떤 증상인가요?'
AskMultiSymtomString = u'어떤 증상인가요?(복수, 직접 입력 가능)\nex) 1,3,나사 빠짐\n\n0:이전 메뉴로 돌아가기'
InsertIDString = u'학번(혹은 사번)을 입력해주세요 ex)2011740011\n0:이전 메뉴'
InsertNameString = u'이름을 입력해주세요 ex)오승환, 강정호a, HyunsooKim\n0:이전 메뉴'
ReInsertString = u'다시 입력해 주세요'
InsertYesNoString = u'입력하시겠습니까?'
LastYesNoString = u'최종 접수하시겠습니까'
DirectInsertSymptomString = u'직접 증상을 입력해주세요\n0:이전 메뉴'
DirectInsertPartString = u'직접 고장난 부분을 입력해주세요\n0:이전 메뉴'

InsertValidNumberString = u'범위 내의 숫자를 입력해주세요'
InsertNumberString = u'숫자를 입력해주세요'
InsertCaseNumberString = u'Case의 번호를 입력해주세요\n0:이전 메뉴'

AskSeatHandpieceString = u'실습실 자리 문제인가요? 핸드피스 문제인가요?'
AskDeletionString = u'삭제하시겠습니까?'

fromStateMessageList = {  1:SelectString+u'\n' ,
                          11:SelectString+u'\n' ,
                          14:SelectString+u'\n' ,          111:SelectString+u'\n' ,          
                          1111:SelectString+u'\n' ,
                          11113:SelectString+u'\n' ,
                          11111:InsertedString+u'\n' ,    11114:SelectString+u'\n' ,          111131:SelectString+u'\n' ,       111132:SelectString+u'\n' ,                                                 
                          111111:InsertedString+u'\n' ,   111141:SelectString+u'\n' ,         1111311:SelectString+u'\n' ,      1111321:SelectString+u'\n' ,
                          1111111:SelectString+u'\n' ,    1111411:SelectString+u'\n' ,        11113111:SelectString+u'\n' ,     11113211:SelectString+u'\n' ,
                          11111111:SelectString+u'\n' ,   11114111:SelectString+u'\n' ,       111131111:SelectString+u'\n' ,    111132111:SelectString+u'\n' ,
                          11111112:SelectString+u'\n' ,   11114112:SelectString+u'\n' ,       111131112:SelectString+u'\n' ,    111132112:SelectString+u'\n' ,
                          11111113:SelectString+u'\n' ,   11114113:SelectString+u'\n' ,                                  
                          11111114:SelectString+u'\n' ,
                          11111115:SelectString+u'\n' ,
                          11111116:SelectString+u'\n' ,
                          111111111:SelectString+u'\n' ,    111141111:SelectString+u'\n' ,    1111311111:SelectString+u'\n' ,    1111321111:SelectString+u'\n' ,     
                                                                                              #13111111:SelectString+u'\n' ,   13211111:SelectString+u'\n' , 
                                                                                              #131111111:SelectString+u'\n' ,  132111111:SelectString+u'\n' ,
                                                                                              #1311111111:SelectString+u'\n' , 1321111111:SelectString+u'\n' ,
                          1111111111:SelectString+SubmitString+u'\n' ,1111411111:SelectString+SubmitString+u'\n' ,11113111111:SelectString+u'\n' ,11113211111:SelectString+u'\n' ,
                          141:SelectString+u'\n' ,   142:SelectString+u'\n' ,  
                          1411:SelectString+ u'\n' , 
                          14111:SelectString+ u'\n'
}

toStateMessageList = {    1:u'',
                          
                          1111:AskLocationString,
                          11113:AskSeatHandpieceString,                                                    
                          11111:AskSeatNumberString,       11114:AskSeatNumberString,                 111131:AskSeatNumberString,       111132:InsertCaseNumberString,                          
                          111111:AskPartString,            111141:AskPartString,                      1111311:AskPartString,            1111321:AskPartString,       
                          1111111:DirectInsertPartString,  1111411:DirectInsertPartString,            11113111:DirectInsertPartString,  11113211:DirectInsertPartString,
                          11111111:AskSymtomString ,       
                          11114111:AskMultiSymtomString+u'\n'+ _MonitorSymptomJoinString ,                  
                          11114112:AskMultiSymtomString+u'\n'+ _CombodySymptomJoinString ,                                            
                          11114113:AskMultiSymtomString+u'\n'+ _ComnetworkSymptomJoinString ,
                          111131111:AskSymtomString,       111132111:AskSymtomString,
                          11111112:AskSymtomString ,                                                   111131112:AskSymtomString,        111132112:AskSymtomString, 
                          11111113:AskSymtomString ,
                          11111114:AskSymtomString ,
                          11111115:AskSymtomString ,
                          11111116:AskSymtomString ,
                          111111111:DirectInsertSymptomString,  111141111:DirectInsertSymptomString,                1111311111:DirectInsertPartString,  1111321111:DirectInsertPartString,
                                                                #1111411111:UnInsertedString+'\n'+InsertYesNoString, 11113111111:UnInsertedString+'\n'+InsertYesNoString,  13211111:UnInsertedString+'\n'+InsertYesNoString,
                                                                #11114111111:InsertIDString,                         111131111111:InsertIDString,  132111111:InsertIDString, 
                                                                #111141111111:InsertNameString,                      1111311111111:InsertNameString,  1321111111:InsertNameString, 
                          14:u'',
                          11:InsertIDString,                     141:InsertIDString,                  142:AskDeletionString,
                          111:InsertNameString,                  1411:InsertNameString,                
}

push_StateList = {
                  1111111:True, 11111111:True, 11111112:True, 11111113:True, 11111114:True, 11111115:True, 11111116:True, 111111111:True,
                  1111411:True, 11114111:True, 11114112:True, 11114113:True,                                              111141111:True,
                  11113111:True,111131111:True,111131112:True,                                                            1111311111:True,
                  11113211:True,111132111:True,111132112:True,                                                            1111321111:True,
}

pop_pushedStateList = {
                       111111111:True , 111141111:True , 1111311111:True ,  1111321111:True     
}   

initial_State          = 1
first_4work_State      = 11111
first_3work_State      = 111131
first_3handpiece_State = 111132
first_3com_State       = 11114
#last_4work_Light_State = 1111
last_4work_Light_State      = 111111111
last_3work_Doll_State       = 1111311111
last_3handpiece_High_State  = 1111321111
last_3com_State             = 111141111

first_Independent_IDInsert_State = 141


state = { 1:1 , 
          11:11,                     2:2,                     3:3,                    14:14 , 
          111:111,
          1111:1111,
          11111:11111 ,                  11114:11114,                   11113:11113,                  141:141,                   142:142, 
          111111:111111 ,                111131:111131,                 111132:111132,                111141:111141,             1411:1411,
          1111111:1111111 ,              1111311:1111311,               1111321:1111321,              1111411:1111411,           14111:14111 , 
          11111111:11111111 ,            11111112:11111112,             11111113:11111113,            11111114:11111114 ,        11111115:11111115,
          11111116:11111116,             11111117:11111117 ,             
          11113111:11113111,             11113211:11113211,    
          11114111:11114111,             11114112:11114112,
          141111:141111 ,     
          111111111:111111111,           111141111:111141111,       
          111131111:111131111  ,         111131112:111131112 ,          111131113:111131113 , 
          111132111:111132111  ,         111132112:111132112 ,          111132113:111132113 ,           
                                         1111311111:1111311111 ,        1111321111:1111321111 ,         
                                    #13111111:13111111,       13211111:13211111,               
                                    #131111111:131111111,     132111111:132111111,           
          1111111111:1111111111,         1111311111:1111311111,   1111321111:1111321111,    1111411111:1111411111,    
                                         11113111111:11113111111, 11113211111:11113211111             
}

Error_NoInt     = 9
Error_NoSubTree = 8
def determineSubGraph( _State , _wantInfo ) :
    if type( _State ) is not int :
        return  Error_NoInt
    else :
        num_str = str(_State)
        if len(num_str) < len(str(first_4work_State)) :
            return Error_NoSubTree
        else :
            if    num_str[:len(str(first_4work_State))] ==  str(first_4work_State) :
                if _wantInfo == True :
                    return first_4work_State
                else :
                    return last_4work_Light_State
            elif  num_str[:len(str(first_3com_State))] == str(first_3com_State) :
                if _wantInfo == True :
                    return first_3com_State 
                else :
                    return last_3com_State
            elif  num_str[:len(str(first_3work_State))] == str(first_3work_State ) :
                if _wantInfo == True :
                    return first_3work_State
                else :
                    return last_3work_Doll_State  
            elif  num_str[:len(str(first_3handpiece_State))] == str(first_3handpiece_State ) :
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
        return _nx_Child(stage_num * 10 +1 , score-1)

def  nx_Child( stage_num , score ) :
    num = _nx_Child(stage_num, score)
    if _isValidState(num) :
        return num
    else :
        return  num*100 

def nx_Child_Sibling(stage_num , child_score, sibling_score) :
    num = nx_Child(stage_num, child_score) + sibling_score
    if _isValidState(num) :
        return num
    else :
        return  num*100 

def _prev_Parent(stage_num, score) :
    if score == 0 :
        return stage_num 
    else :
        return _prev_Parent( stage_num/10  , score-1)    

def prev_Parent(stage_num, score) :
    num = _prev_Parent(stage_num, score)
    if _isValidState(num) :
        return num
    else :
        return num * 100

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
    
    def  _generate(self, _TextMessage,_organization,_instance, _UserRequestKey, _key1=None) :
        self.mText += _TextMessage
        self.mText += u'ID         :' + str(_organization[ _UserRequestKey ]['ID'])+u'\n'
        self.mText += u'Name       :' + _organization[ _UserRequestKey ]['Name']+u'\n'
        if _key1 is None :
            self.mText += u'location   :' + _instance[ _UserRequestKey ]['location']+u'\n'
            self.mText += u'seat number:' + _instance[ _UserRequestKey ]['seat number']+u'\n'
            self.mText += u'part       :' + _instance[ _UserRequestKey ]['part']+u'\n'
            self.mText += u'symptom    :' + _instance[ _UserRequestKey ]['symptom']
        else : 
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
            _textMessage = userRequest['content']+SelectString+u'\n'+UnderConstructionString+u'\n'
            _textMessage += time.strftime('%X %x %Z') + u'\n'
            _textMessage += u'접수 예정:' +u'\n'

            _UserRequestKey = userRequest['user_key'] 
            if _UserRequestKey in sum_instance and \
               _UserRequestKey in organization  :
                for key in sum_instance[_UserRequestKey] :
                    _textMessage += SummaryText()._generate(u'---------' + key +  u'------------\n' , organization, sum_instance, _UserRequestKey, key)


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


            _textMessage += u'접수 완료:' +u'\n'
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
            _textMessage = userRequest['content']+SelectString+u'\n'+UnderConstructionString
            return Arrow()._make_Message_Button_change_State(True, _textMessage, True ,currentState , initial_State, userRequest)
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
    [ first_4work_State , first_3work_State , first_3handpiece_State,  first_3com_State ] :
        currentState = instance[userRequest['user_key']]['state']
        try : 
            # valid for seat and handpiece case?  
            if int ( userRequest['content'] )  in range(1,96+1) :
                instance[userRequest['user_key']]['seat number'] = userRequest['content']
                return Arrow().make_Message_Button_change_State(currentState, nx_Child(currentState,1) , userRequest, request.url_root)
            elif  int ( userRequest['content'] ) == 0 :
                return Arrow().make_Message_Button_change_State(currentState, prev_Parent(currentState,1) , userRequest)   

            else :
                _textMessage = userRequest['content']+SelectString+u'\n'+ InsertValidNumberString
                return Arrow()._make_Message_Button_change_State(True, _textMessage,  False, currentState,   currentState , userRequest)
        except ValueError : 
            _textMessage = userRequest['content']+SelectString+u'\n'+ InsertNumberString
            return Arrow()._make_Message_Button_change_State(True, _textMessage,  False, currentState, currentState , userRequest)

    elif   instance[userRequest['user_key']]['state'] in \
    [ nx_Child(first_4work_State,1) ,  nx_Child(first_3work_State,1) , nx_Child(first_3handpiece_State,1) , nx_Child(first_3com_State ,1) ]  :
        currentState = instance[userRequest['user_key']]['state']
        #if userRequest['content'] in  StateButtonList[nx_Child(first_4work_State,1)] :
        if userRequest['content'] in  StateButtonList[currentState] :
            #i = StateButtonList[nx_Child(first_4work_State,1)].index(userRequest['content'])
            i = StateButtonList[currentState].index(userRequest['content'])
            if i == len(StateButtonList[currentState]) -2 :
                _textMessage  = userRequest['content']+SelectString+u'\n'+ DirectInsertPartString
                return Arrow()._make_Message_Button_change_State( True, _textMessage , False , currentState,  nx_Child(currentState ,1) , userRequest )                        
            elif i == len(StateButtonList[currentState]) -1 :
                return Arrow().make_Message_Button_change_State(currentState, prev_Parent(currentState,1) , userRequest, request.url_root  )   
            else :
                instance[userRequest['user_key']]['part'] = userRequest['content']
                return Arrow().make_Message_Button_change_State(currentState, nx_Child(currentState,2)+i , userRequest )
        else : 
            _textMessage = userRequest['content']+SelectString+u'\n'+'(state:'+ str(instance[userRequest['user_key']]['state']) + ')'
            instance[userRequest['user_key']] = { 'state' : state[initial_State] }            
            return  Arrow()._make_Message_Button_change_State(True, _textMessage, True, currentState,   initial_State, userRequest)

    elif   instance[userRequest['user_key']]['state'] in \
     [ nx_Child(first_4work_State,2) , nx_Child(first_3work_State,2), nx_Child(first_3handpiece_State ,2) , nx_Child(first_3com_State ,2)]  :
        currentState = instance[userRequest['user_key']]['state']

        if  userRequest['content']  == '0' :
            return Arrow().make_Message_Button_change_State(currentState, prev_Parent(currentState,1) , userRequest, request.url_root)   
        instance[userRequest['user_key']]['part'] = userRequest['content']
        return Arrow().make_Message_Button_change_State(currentState, nx_Child(currentState,2), userRequest)

    elif  instance[userRequest['user_key']]['state'] in range(nx_Child(first_4work_State,3)+0, nx_Child(first_4work_State,3)+ len_4work_part-2 )   or  \
          instance[userRequest['user_key']]['state'] in range(nx_Child(first_3work_State,3)+0, nx_Child(first_3work_State ,3)+ len_3work_part-2 )  or  \
          instance[userRequest['user_key']]['state'] in range(nx_Child(first_3handpiece_State,3)+0, nx_Child(first_3handpiece_State,3)+ len_3handpiece_part-2 )  :
#          instance[userRequest['user_key']]['state'] in range(nx_Child(first_3com_State ,3)+1, nx_Child(first_3com_State ,3)+ len_3com_part-2 )  : 

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
    elif   instance[userRequest['user_key']]['state'] in  \
           range(nx_Child(first_3com_State ,3)+0, nx_Child(first_3com_State ,3)+ len_3com_part-2 ) :
#          [ nx_Child(first_3com_State ,3), nx_Child(first_3com_State ,3)+1  ] :
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
        # ID info in temp_organization 
        if userRequest['user_key'] not in organization:
            _textMessage = SummaryText()._generate(LastYesNoString+u'\n' ,  temp_organization , instance , userRequest['user_key'])                
            return Arrow()._make_Message_Button_change_State(True, _textMessage, True, currentState, nx_Child(  determineSubGraph(currentState, True) ,5) , userRequest)             
        #already ID info  in organization  
        else : 
            _textMessage = SummaryText()._generate(LastYesNoString+u'\n' ,  organization , instance , userRequest['user_key'])                
            return Arrow()._make_Message_Button_change_State(True, _textMessage, True, currentState, nx_Child(  determineSubGraph(currentState, True) ,5) , userRequest)             

                     



    elif   instance[userRequest['user_key']]['state']  \
    in  [ nx_Child(first_4work_State,4) , nx_Child(first_3work_State,4) , nx_Child(first_3handpiece_State ,4) , nx_Child(first_3com_State ,4) ]  :
        currentState = instance[userRequest['user_key']]['state'] 

        if  userRequest['content']  == '0' :
            return Arrow().make_Message_Button_change_State(currentState, restore_prev_State( userRequest['user_key'] )  , userRequest, request.url_root)   
        instance[userRequest['user_key']]['symptom'] = userRequest['content']            
        # no ID info case
        if userRequest['user_key'] not in organization:
            _textMessage = SummaryText()._generate(LastYesNoString+u'\n' ,  temp_organization , instance , userRequest['user_key'])                
            return Arrow()._make_Message_Button_change_State(True, _textMessage, True, currentState, nx_Child(  determineSubGraph(currentState, True) ,5) , userRequest)             
        # already have ID info   
        else : 
            _textMessage = SummaryText()._generate(LastYesNoString + u'\n' ,  organization , instance , userRequest['user_key'])                
            return Arrow()._make_Message_Button_change_State(True, _textMessage, True, currentState, nx_Child(  determineSubGraph(currentState, True) ,5) , userRequest)             
    elif   instance[userRequest['user_key']]['state']  \
    in [ nx_Child(first_4work_State,5)   ,nx_Child(first_3work_State ,5) , nx_Child(first_3handpiece_State ,5), nx_Child( first_3com_State,5) ] :
        currentState = instance[userRequest['user_key']]['state']   
        if  userRequest['content']  ==  StateButtonList[ currentState ][0] :
            if  userRequest['user_key'] in temp_organization and \
                userRequest['user_key'] not in  organization :
                organization[userRequest['user_key']] = { 'ID' :  temp_organization[userRequest['user_key']]['ID']    }
                organization[userRequest['user_key']]['Name'] = temp_organization[userRequest['user_key']]['Name']   
                temp_organization.pop( userRequest['user_key'] ,  None)

            _UserRequestKey = userRequest['user_key']
            _Time = time.strftime('%X %x %Z')
            if _UserRequestKey not in sum_instance    :
                sum_instance[_UserRequestKey] = {}
            if _Time not in sum_instance[_UserRequestKey] :
                sum_instance[_UserRequestKey][ _Time ] = {}

            sum_instance[_UserRequestKey][_Time]['location'] = instance[ _UserRequestKey ]['location']
            sum_instance[_UserRequestKey][_Time]['seat number'] = instance[ _UserRequestKey ]['seat number']
            sum_instance[_UserRequestKey][_Time]['part']  = instance[ _UserRequestKey ]['part']            
            sum_instance[_UserRequestKey][_Time]['symptom'] = instance[ _UserRequestKey ]['symptom']

            #_textMessage = userRequest['content']+  u'\n' +SubmitString 
            instance[userRequest['user_key']] = { 'state' : state[initial_State] }            
            #return  Arrow()._make_Message_Button_change_State(True, _textMessage, True, currentState, initial_State, userRequest)
            return  Arrow().make_Message_Button_change_State(currentState, initial_State, userRequest)
        elif userRequest['content']  ==  StateButtonList[ currentState ][2] :
            return Arrow().make_Message_Button_change_State(currentState, restore_prev_State(userRequest['user_key'])  , userRequest)
            #if  userRequest['user_key'] not in temp_organization and \
            #    userRequest['user_key'] in  organization :
            #    return Arrow().make_Message_Button_change_State(currentState, restore_prev_State(userRequest['user_key'])  , userRequest)
            #return Arrow().make_Message_Button_change_State(currentState ,  prev_Parent( currentState, 1 ) , userRequest)             
#            _textMessage = userRequest['content']+SelectString+u'\n'+ InsertNameString
#            return Arrow()._make_Message_Button_change_State(_textMessage, False, prev_Parent( currentState, 1 ) , userRequest)             


        else : 
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
    _text = '(state:'+ str(instance[userRequest['user_key']]['state']) + ')' + userRequest['content']
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
