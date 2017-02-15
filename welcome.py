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
      u'2.네트워크',
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

StateButtonList = { 0: _State0KeyList, 
                 1: _State1KeyList ,             4: _State4KeyList ,
                 13:  _State13KeyList,           42 : _YesorNoKeyList , 
                 111: _State111KeyList,          141: _State141KeyList,  
                 1311: _State1311KeyList ,       1321 : _State1321KeyList, 
                 4111: _YesorNoKeyList ,                 
                 11111: _LightSymptomKeyList  ,  11112: _MonitorSymptomKeyList ,    11113 : _GastorchSymptomKeyList , 
                 11114: _HandpieceengineSymptomKeyList ,11115: _AirinletSymptomKeyList ,    11116: _AiroutletSymptomKeyList ,
                 14111: _MonitorSymptomKeyList,  14112: _ComnetworkSymptomKeyList, 
                 41111: _YesorNoKeyList  ,   
                                                 131111: _DollSymtomKeyList ,        131112: _MonitorSymptomKeyList,
                                                 132111: _HighspeedSymtomKeyList,    132112: _LowspeedSymptomList,                
                 1111111: _YesorNoKeyList ,      1411111: _YesorNoKeyList, 
                 13111111: _YesorNoKeyList ,     13211111: _YesorNoKeyList ,  
                 1111111111: _YesorNoKeyList,    1411111111: _YesorNoKeyList,
                 13111111111: _YesorNoKeyList,   13211111111: _YesorNoKeyList                      
}

StatePhotoList = {  
                    11:   {"url": u'static/images/4work_seats.jpeg' , "width": 399, "height": 490 } ,
                    111:  {"url": u'static/images/4work_oneseat.png' ,"width": 200, "height": 283 } ,
                    131:  {"url": u'static/images/4work_seats.jpeg' ,"width": 399,"height": 490 }, 
                    1311: {"url": u'static/images/3work_oneseat.png' ,"width": 200, "height": 283 } ,
                    132:  {"url": u'static/images/3work_case.png' ,"width": 230,"height": 218}, 
                    1321: {"url": u'static/images/3work_caseopen.png' ,"width": 200,"height": 283 } ,
                    14:   {"url": u'static/images/3com_seats.png' ,   "width": 360,"height": 270 }, 
                    141:  {"url": u'static/images/3com_oneseat.png' ,"width": 363,"height": 616 }
#                    141:  {"url": request.url_root+u'static/images/3com_oneseat.png' ,"width": 363,"height": 616 }
}

SelectString = u' 선택하셨습니다.'
SubmitString = u'접수되었습니다.'
CancelString = u'취소되었습니다'
UnderConstructionString =u'-Under Construction-'
UnInsertedString = u'필수 항목인 학번(혹은 사번)이 입력되지 않았습니다.'

AskLocationString = u'위치가 어디신가요?'
AskSeatNumberString = u'자리가 어디신가요?\n0:이전 메뉴'
AskPartString = u'어떤 부분이 문제인가요?'
AskSymtomString = u'어떤 증상인가요?'
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

fromStateMessageList = {  0:SelectString ,
                          1:SelectString ,
                          4:SelectString+u'\n' ,                                        13:SelectString+u'\n' ,
                          11:SelectString+u'\n' ,      14:SelectString+u'\n' ,          131:SelectString+u'\n' ,       132:SelectString+u'\n' ,                                                 
                          111:SelectString+u'\n' ,     141:SelectString+u'\n' ,         1311:SelectString+u'\n' ,      1321:SelectString+u'\n' ,
                          1111:SelectString+u'\n' ,    1411:SelectString+u'\n' ,        13111:SelectString+u'\n' ,     13211:SelectString+u'\n' ,
                          11111:SelectString+u'\n' ,   14111:SelectString+u'\n' ,       131111:SelectString+u'\n' ,    132111:SelectString+u'\n' ,
                          11112:SelectString+u'\n' ,   14112:SelectString+u'\n' ,       131112:SelectString+u'\n' ,    132112:SelectString+u'\n' ,
                          11113:SelectString+u'\n' ,                                     
                          11114:SelectString+u'\n' ,
                          11115:SelectString+u'\n' ,
                          11116:SelectString+u'\n' ,
                          111111:SelectString+u'\n' ,    141111:SelectString+u'\n' ,    1311111:SelectString+u'\n' ,    1321111:SelectString+u'\n' ,     
                          1111111:SelectString+u'\n' ,   1411111:SelectString+u'\n' ,   13111111:SelectString+u'\n' ,   13211111:SelectString+u'\n' , 
                          11111111:SelectString+u'\n' ,  14111111:SelectString+u'\n' ,  131111111:SelectString+u'\n' ,  132111111:SelectString+u'\n' ,
                          111111111:SelectString+u'\n' , 141111111:SelectString+u'\n' , 1311111111:SelectString+u'\n' , 1321111111:SelectString+u'\n' ,
                          1111111111:SelectString+u'\n' ,1411111111:SelectString+u'\n' ,13111111111:SelectString+u'\n' ,13211111111:SelectString+u'\n' ,
                          41:SelectString+u'\n' ,
                          411:SelectString+ u'\n' , 
                          4111:SelectString+ u'\n'
}

toStateMessageList = {    0:u'',
                          1:AskLocationString,                                                  13:AskSeatHandpieceString,  
                          11:AskSeatNumberString,       14:AskSeatNumberString,                 131:AskSeatNumberString,       132:InsertCaseNumberString,                          
                          111:AskPartString,            141:AskPartString,                      1311:AskPartString,            1321:AskPartString,       
                          1111:DirectInsertPartString,  1411:DirectInsertPartString,            13111:DirectInsertPartString,  13211:DirectInsertPartString,
                          11111:AskSymtomString ,       14111:AskSymtomString,                  131111:AskSymtomString,        132111:AskSymtomString,
                          11112:AskSymtomString ,       14112:AskSymtomString,                  131112:AskSymtomString,        132112:AskSymtomString, 
                          11113:AskSymtomString ,
                          11114:AskSymtomString ,
                          11115:AskSymtomString ,
                          11116:AskSymtomString ,
                          111111:DirectInsertSymptomString,   141111:DirectInsertPartString,                   1311111:DirectInsertPartString,  1321111:DirectInsertPartString,
                          1111111:UnInsertedString+'\n'+InsertYesNoString,  1411111:UnInsertedString+'\n'+InsertYesNoString,  13111111:UnInsertedString+'\n'+InsertYesNoString,  13211111:UnInsertedString+'\n'+InsertYesNoString,
                          11111111:InsertIDString,            14111111:InsertIDString,                         131111111:InsertIDString,  132111111:InsertIDString, 
                          111111111:InsertNameString,         141111111:InsertNameString,                      1311111111:InsertNameString,  1321111111:InsertNameString, 
                          4:u'',
                          41:InsertIDString,                  42:AskDeletionString,
                          411:InsertNameString,                
}

push_StateList = {
                  1111:True, 11111:True, 11112:True, 11113:True, 11114:True, 11115:True, 11116:True, 111111:True,
                  1411:True, 14111:True, 14112:True,                                                 141111:True,
                  13111:True,131111:True,131112:True,                                                1311111:True,
                  13211:True,132111:True,132112:True,                                                1321111:True,
}

pop_pushedStateList = {
                       111111:True , 141111:True , 1311111:True ,  1321111:True     
}   

initial_State          = 0
first_4work_State      = 11
first_3work_State      = 131
first_3handpiece_State = 132
first_3com_State       = 14
#last_4work_Light_State = 1111
last_4work_Light_State      = 111111
last_3work_Doll_State       = 1311111
last_3handpiece_High_State  = 1321111
last_3com_State             = 141111

first_Independent_IDInsert_State = 41


state = { 0:0 , 
          1:1,                     2:2,                     3:3,                    4:4 , 
          11:11 ,                  14:14,                   13:13,                  41:41,               42:42, 
          111:111 ,                131:131,                 132:132,                141:141,             411:411,
          1111:1111 ,              1311:1311,               1321:1321,              1411:1411,           4111:4111 , 
          11111:11111 ,            11112:11112,             11113:11113,            11114:11114 ,        11115:11115,
          11116:11116,             11117:11117 ,             
          13111:13111,             13211:13211,    
          14111:14111,             14112:14112,
          41111:41111 ,     
          111111:111111,                  
          131111:131111  ,         131112:131112 ,          131113:131113 , 
          132111:132111  ,         132112:132112 ,          132113:132113 ,          141111:141111, 
          1111111:1111111 ,        1311111:1311111 ,        1321111:1321111 ,        1411111:1411111, 
          11111111:11111111,       13111111:13111111,       13211111:13211111,       14111111:14111111,        
          111111111:111111111 ,    131111111:131111111,     132111111:132111111,     141111111:141111111,      
          1111111111:1111111111,   1311111111:1311111111,   1321111111:1321111111,   1411111111:1411111111,    
                                   13111111111:13111111111, 13211111111:13211111111             
}

Error_NoInt     = 9
Error_NoSubTree = 8
def determineSubGraph( _State , _wantInfo ) :
    if type( _State ) is not int :
        return  Error_NoInt
    else :
        num_str = str(_State)
        if len(num_str) < 2 :
            return Error_NoSubTree
        else :
            if    num_str[:2] ==  str(first_4work_State) :
                if _wantInfo == True :
                    return first_4work_State
                else :
                    return last_4work_Light_State
            elif  num_str[:2] == str(first_3com_State) :
                if _wantInfo == True :
                    return first_3com_State 
                else :
                    return last_3com_State
            elif  num_str[:3] == str(first_3work_State ) :
                if _wantInfo == True :
                    return first_3work_State
                else :
                    return last_3work_Doll_State  
            elif  num_str[:3] == str(first_3handpiece_State ) :
                if _wantInfo == True :
                    return first_3handpiece_State
                else :
                    return last_3handpiece_High_State 
            else :
                return Error_NoSubTree

sum_instance = { 'init' :  {} }

instance = { 'temp': {'state':state[0], 
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

        #return self._make_Messages_change_State(_textMessage , False , {}  , False , {} , _ButtonFlag , _toState, _userRequest)
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
    if number % 10000 in range(01, 80+1)  and \
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




@app.route('/')
def Welcome():
    return app.send_static_file('index.html')

@app.route('/myapp')
def WelcomeToMyapp():
    return 'Welcome again to my app running on Bluemix!!'

@app.route('/keyboard')
def Keyboard():    
    ItemList = {
        'type': 'buttons', 'buttons' : StateButtonList[0]
    }    
    return jsonify(ItemList)

@app.route('/message', methods=['POST'])
def GetMessage():
    userRequest = json.loads(request.get_data()) 

    # if its a 1st message, you have to make instance
    if userRequest['user_key'] not in instance :
        instance[userRequest['user_key']] = { 'state' : state[0] }
    # if its a sudden quit-and-reenter case, then make state initial
    if  instance[userRequest['user_key']]['state'] != state[0] and \
        userRequest['content']  in  StateButtonList[0] :
            instance[userRequest['user_key']]['state'] = state[0]        

    #select initially 
    if instance[userRequest['user_key']]['state'] == state[0] :        
        if  userRequest['content']  ==  StateButtonList[0][0] :
#            _textMessage = userRequest['content']+SelectString+u'\n'+AskLocationString
#            return Arrow()._make_Message_Button_change_State(True, _textMessage, True ,0,  1, userRequest)
            return Arrow().make_Message_Button_change_State(0,1,userRequest)
        elif userRequest['content']  ==  StateButtonList[0][1] :
            _textMessage = userRequest['content']+SelectString+u'\n'+UnderConstructionString+u'\n'
            _textMessage += time.strftime('%X %x %Z') + u'\n'
            _textMessage += u'접수 예정:' +u'\n'

            _UserRequestKey = userRequest['user_key'] 
            if _UserRequestKey in sum_instance and \
               _UserRequestKey in organization  :
                for key in sum_instance[_UserRequestKey] :
                    #_textMessage += u'-------------------------------\n'
                    #_textMessage += key + u'\n'
                    #_textMessage += str(organization[ _UserRequestKey ]['ID']) +u'\n'
                    #_textMessage += organization[ _UserRequestKey ]['Name'] + u'\n'
                    #_textMessage += sum_instance[_UserRequestKey][key]['location'] + u'\n'
                    #_textMessage += sum_instance[_UserRequestKey][key]['seat number'] + u'\n'
                    #_textMessage += sum_instance[_UserRequestKey][key]['part'] + u'\n'
                    #_textMessage += sum_instance[_UserRequestKey][key]['symptom'] + u'\n'

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
            return Arrow()._make_Message_Button_change_State(True, _textMessage, True , 0, 0, userRequest)
        elif userRequest['content']  ==  StateButtonList[0][2] :             
            _textMessage = userRequest['content']+SelectString+u'\n'+UnderConstructionString
            _mButton = { "label": "link를 click해주세요", "url" : "https://www.youtube.com/watch?v=aj4VQmfiTBk" }
            return Arrow()._make_Messages_change_State(True, _textMessage, False , {} , True, _mButton, True,0, 0 , userRequest)
        elif userRequest['content']  ==  StateButtonList[0][3] :            
            return Arrow().make_Message_Button_change_State(0, 4, userRequest)
              
        else :
            _textMessage = userRequest['content']+SelectString+u'\n'+UnderConstructionString
            return Arrow()._make_Message_Button_change_State(True, _textMessage, True ,0, 0, userRequest)

    #select location  
    elif instance[userRequest['user_key']]['state'] == 1 :
        currentState = instance[userRequest['user_key']]['state']
        if  userRequest['content']  ==  StateButtonList[1][0] :
            instance[userRequest['user_key']]['location'] = userRequest['content']
            return Arrow().make_Message_Button_change_State(currentState, first_4work_State, userRequest, request.url_root  )  
        elif userRequest['content']  ==  StateButtonList[1][1] :
            _textMessage = userRequest['content']+SelectString+u'\n'+UnderConstructionString
            return Arrow()._make_Message_Button_change_State(True, _textMessage, True ,1, 0, userRequest)
        elif userRequest['content']  ==  StateButtonList[1][2] :            
            return Arrow().make_Message_Button_change_State(currentState, nx_Child_Sibling(1,1,2) , userRequest )
        elif userRequest['content']  ==  StateButtonList[1][3] :
            instance[userRequest['user_key']]['location'] = userRequest['content']
            return Arrow().make_Message_Button_change_State(currentState, first_3com_State, userRequest, request.url_root )
        elif userRequest['content']  ==  StateButtonList[1][4] :
            _textMessage = userRequest['content']+SelectString+u'\n'+UnderConstructionString
            return Arrow()._make_Message_Button_change_State(True, _textMessage, True ,1, 0, userRequest)
        elif userRequest['content']  ==  StateButtonList[1][5] :  # return to prev menu
            return Arrow().make_Message_Button_change_State( 1, 0, userRequest)            
        else :
            _textMessage = userRequest['content']+SelectString+u'\n'+'(state:'+ str(instance[userRequest['user_key']]['state']) + ')'
            instance[userRequest['user_key']] = { 'state' : state[0] }            
            return  Arrow()._make_Message_Button_change_State(True, _textMessage, True, 1, 0, userRequest)

    #select memebership item and prepare arrows
    elif instance[userRequest['user_key']]['state'] == state[4] :
        currentState = instance[userRequest['user_key']]['state']
        if  userRequest['content']  ==  StateButtonList[4][0] :
            if  userRequest['user_key'] in organization :
                key = userRequest['user_key']
                _text_  = u'이미 입력된 ID와 Name이 있습니다.'
                _text_ += u'새로 입력하시려면 기존 ID와 Name을 먼저 삭제하고 입력해주세요.'+u'\n'
                _text_ += u'기존 ID   :'+ str(organization[key]['ID'])+u'\n'
                _text_ += u'기존 Name :'+ organization[key]['Name']+u'\n'
                return Arrow()._make_Message_Button_change_State(True, _text_, True, currentState, currentState , userRequest )            
#                return Arrow()._make_Message_Button_change_State( _text_, True, 4 , userRequest )            

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
#                _text_ = userRequest['content']+SelectString +u'\n' + InsertIDString                         
#                return Arrow()._make_Message_Button_change_State(True, _text_, False ,currentState, first_Independent_IDInsert_State , userRequest )            
#                return Arrow()._make_Message_Button_change_State( _text_, False , 41 , userRequest )            
                return Arrow().make_Message_Button_change_State(currentState, first_Independent_IDInsert_State , userRequest)

        elif  userRequest['content']  ==  StateButtonList[4][1] :
            if userRequest['user_key'] in organization:
                _text_ = userRequest['content']+SelectString + u'\n' + AskDeletionString+ u'\n'
                _text_ += u'ID   :'+ str(organization[userRequest['user_key']]['ID'])+u'\n'
                _text_ += u'Name :'+ organization[userRequest['user_key']]['Name']+u'\n'
                return Arrow()._make_Message_Button_change_State(True, _text_, True, currentState, nx_Child_Sibling(currentState,1,1) , userRequest )            
#                return Arrow()._make_Message_Button_change_State( _text_, True, 42 , userRequest )            
            else : 
                _text_ =  userRequest['content']+SelectString + u'\n' + u'등록된 ID와 Name이 없습니다.'           
                return Arrow()._make_Message_Button_change_State( True, _text_, True, currentState,  0 , userRequest )   
        elif  userRequest['content']  ==  StateButtonList[4][4] :  # return to prev menu
            return Arrow().make_Message_Button_change_State( 4 , 0 , userRequest )                        
#            _text_ = userRequest['content']+SelectString
#            return Arrow()._make_Message_Button_change_State(  _text_, True, 0 , userRequest )                        
        else : 
            _text_ = userRequest['content']+SelectString
            return Arrow()._make_Message_Button_change_State(True,  _text_, True, currentState,  0 , userRequest )                        
    elif   instance[userRequest['user_key']]['state']  in  \
    [ first_4work_State , first_3work_State , first_3handpiece_State,  first_3com_State ] :
        currentState = instance[userRequest['user_key']]['state']
        try : 
            # valid for seat and handpiece case?  
            if int ( userRequest['content'] )  in range(1,96+1) :
                _textMessage = userRequest['content']+SelectString+u'\n'+ AskPartString
                if currentState == first_4work_State :
                    _photo = {
                        "url": request.url_root+u'static/images/4work_oneseat.png' ,
                        "width": 200,
                         "height": 283
                    }
                elif  currentState == first_3work_State :
                    _photo = {
                        "url": request.url_root+u'static/images/3work_oneseat.png' ,
                        "width": 200,
                        "height": 283
                    }
                elif  currentState == first_3handpiece_State : 
                    _photo = {
                        "url": request.url_root+u'static/images/3work_caseopen.png' ,
                        "width": 200,
                        "height": 283
                    }
                else :  #currentState == first_3com_State
                    _photo = {
                        "url": request.url_root+u'static/images/3com_oneseat.png' ,
                        "width": 363,
                        "height": 616
                    }
                instance[userRequest['user_key']]['seat number'] = userRequest['content']
#                return Arrow()._make_Messages_change_State(True, _textMessage, True , _photo , False, {}, True,currentState, nx_Child(currentState,1) , userRequest)
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
                _textMessage = userRequest['content']+SelectString+u'\n'+ AskSymtomString
                return Arrow()._make_Message_Button_change_State( True, _textMessage , True, currentState, nx_Child(currentState,2)+i , userRequest )                        
        else : 
            _textMessage = userRequest['content']+SelectString+u'\n'+'(state:'+ str(instance[userRequest['user_key']]['state']) + ')'
            instance[userRequest['user_key']] = { 'state' : state[0] }            
            return  Arrow()._make_Message_Button_change_State(True, _textMessage, True, currentState,   0, userRequest)

    elif   instance[userRequest['user_key']]['state'] in \
     [ nx_Child(first_4work_State,2) , nx_Child(first_3work_State,2), nx_Child(first_3handpiece_State ,2) , nx_Child(first_3com_State ,2)]  :
        currentState = instance[userRequest['user_key']]['state']

        if  userRequest['content']  == '0' :
            return Arrow().make_Message_Button_change_State(currentState, prev_Parent(currentState,1) , userRequest, request.url_root)   
        instance[userRequest['user_key']]['part'] = userRequest['content']
        _textMessage = userRequest['content']+SelectString+u'\n'+ DirectInsertSymptomString
        return Arrow()._make_Message_Button_change_State(True, _textMessage , False , currentState, nx_Child(currentState,2) , userRequest)

    elif  instance[userRequest['user_key']]['state'] in range(nx_Child(first_4work_State,3)+0, nx_Child(first_4work_State,3)+ len_4work_part )   or  \
          instance[userRequest['user_key']]['state'] in range(nx_Child(first_3work_State,3)+0, nx_Child(first_3work_State ,3)+ len_3work_part )  or  \
          instance[userRequest['user_key']]['state'] in range(nx_Child(first_3handpiece_State,3)+0, nx_Child(first_3handpiece_State,3)+ len_3handpiece_part )  or \
          instance[userRequest['user_key']]['state'] in range(nx_Child(first_3com_State ,3)+0, nx_Child(first_3com_State ,3)+ len_3com_part )  : 

        currentState = instance[userRequest['user_key']]['state'] 
        if  userRequest['content'] in StateButtonList[ currentState ] :
            lastKeyIndex = len(StateButtonList[ currentState ])-1
            #direct describe case
            if  userRequest['content']  ==  StateButtonList[ currentState ][lastKeyIndex-1] :
                _textMessage = DirectInsertSymptomString
                return Arrow()._make_Message_Button_change_State(True, _textMessage, False, currentState, nx_Child(  determineSubGraph(currentState, True) ,4) , userRequest)             
            elif  userRequest['content']  ==  StateButtonList[ currentState ][lastKeyIndex] :
                return Arrow().make_Message_Button_change_State(currentState, prev_Parent(currentState,2) , userRequest, request.url_root)   
            else:
                instance[userRequest['user_key']]['symptom'] = userRequest['content']            
                # no ID info case
                if userRequest['user_key'] not in organization:
                    #_textMessage = u'학번(혹은 사번)이 입력되지 않았습니다.\n입력하시겠습니까?\n'
                    _textMessage =  UnInsertedString + '\n' +  InsertYesNoString 
                    return Arrow()._make_Message_Button_change_State(True, _textMessage, True, currentState, nx_Child(  determineSubGraph(currentState, False) ,1) , userRequest)             
                # already ID info case  
                else : 
                    _textMessage = SummaryText()._generate(LastYesNoString+u'\n' ,  organization , instance , userRequest['user_key'])                
                    return Arrow()._make_Message_Button_change_State(True, _textMessage, True, currentState, nx_Child(  determineSubGraph(currentState, False) ,4) , userRequest)             
        else :
            _textMessage = userRequest['content']+SelectString+u'\n'
            instance[userRequest['user_key']] = { 'state' : state[0] }            
            temp = Arrow()._make_Message_Button_change_State(True, _textMessage, True, currentState,  0, userRequest)
            # have to enable and verify  below code
            ##instance.pop( userRequest['user_key'] ,  None)
            return temp

    elif   instance[userRequest['user_key']]['state']  \
    in  [ nx_Child(first_4work_State,4) , nx_Child(first_3work_State,4) , nx_Child(first_3handpiece_State ,4) , nx_Child(first_3com_State ,4) ]  :
        currentState = instance[userRequest['user_key']]['state'] 

        if  userRequest['content']  == '0' :
            return Arrow().make_Message_Button_change_State(currentState, restore_prev_State( userRequest['user_key'] )  , userRequest, request.url_root)   


        instance[userRequest['user_key']]['symptom'] = userRequest['content']            
                # no ID info case
        if userRequest['user_key'] not in organization:
            _textMessage =  UnInsertedString + '\n' +  InsertYesNoString
            return Arrow()._make_Message_Button_change_State(True, _textMessage, True, currentState, nx_Child(  determineSubGraph(currentState, False) ,1) , userRequest)             
        # already have ID info   
        else : 
            _textMessage = SummaryText()._generate(LastYesNoString + u'\n' ,  organization , instance , userRequest['user_key'])                
            return Arrow()._make_Message_Button_change_State(True, _textMessage, True, currentState, nx_Child(  determineSubGraph(currentState, False) ,4) , userRequest)             
    elif  instance[userRequest['user_key']]['state']  \
    in  [ nx_Child(last_4work_Light_State,1), nx_Child(last_3work_Doll_State,1), nx_Child(last_3handpiece_High_State ,1) , nx_Child(last_3com_State,1) ]  : 
        currentState = instance[userRequest['user_key']]['state'] 
        #if  userRequest['content']  ==  StateButtonList[nx_Child(last_4work_Light_State,1)][0] :
        if  userRequest['content']  ==  StateButtonList[ currentState ][0] :
            _textMessage = userRequest['content']+SelectString +u'\n' + InsertIDString
            return Arrow()._make_Message_Button_change_State(True, _textMessage, False, currentState, nx_Child( currentState ,1) , userRequest)             
#            return Arrow()._make_Message_Button_change_State(_textMessage, False, nx_Child(  determineSubGraph(currentState, False) ,2) , userRequest)      
        elif  userRequest['content']  ==  StateButtonList[ currentState ][2] :
            return Arrow().make_Message_Button_change_State(currentState, restore_prev_State( userRequest['user_key'] )  , userRequest, request.url_root)   
        else : 
            _textMessage = userRequest['content']+ u'\n'+ CancelString +u'\n'
            instance[userRequest['user_key']] = { 'state' : state[0] }            
            return  Arrow()._make_Message_Button_change_State(True, _textMessage, True, currentState, 0, userRequest)
    #insert ID
    elif   instance[userRequest['user_key']]['state'] \
    in [ nx_Child(last_4work_Light_State,2), nx_Child(last_3work_Doll_State,2), nx_Child(last_3handpiece_High_State ,2) , nx_Child(last_3com_State,2), first_Independent_IDInsert_State] : 
        currentState = instance[userRequest['user_key']]['state']   
        try :
            if isValidID( int ( userRequest['content'] ) ) :
                temp_organization[userRequest['user_key']] = { 'ID' : int ( userRequest['content'] ) }                
                _textMessage = userRequest['content']+SelectString+u'\n'+ InsertNameString
                return Arrow()._make_Message_Button_change_State(True, _textMessage, False, currentState, nx_Child( currentState, 1 ) , userRequest)             
            elif  int ( userRequest['content'] ) == 0 : # return to prev menu
                return Arrow().make_Message_Button_change_State( currentState ,  prev_Parent(currentState, 1)  , userRequest)
#                _textMessage = userRequest['content']+SelectString
#                return Arrow()._make_Message_Button_change_State(_textMessage, True , prev_Parent(currentState, 1)  , userRequest)
            else : 
                _textMessage = userRequest['content']+SelectString+u'\n' + InsertValidNumberString
                return Arrow()._make_Message_Button_change_State(True, _textMessage, False, currentState, currentState, userRequest)             
        except ValueError :
            _textMessage = userRequest['content']+SelectString+u'\n'+ InsertNumberString
            return Arrow()._make_Message_Button_change_State(True, _textMessage, False,currentState , currentState , userRequest)                                     
    #insert Name and prepare arrows
    elif   instance[userRequest['user_key']]['state']  \
    in [ nx_Child(last_4work_Light_State,3) ,nx_Child(last_3work_Doll_State,3) , nx_Child(last_3handpiece_High_State,3), nx_Child(last_3com_State,3) , nx_Child( first_Independent_IDInsert_State , 1 ) ] :
        currentState = instance[userRequest['user_key']]['state'] 

        if  userRequest['content']  == '0' :
            return Arrow().make_Message_Button_change_State(currentState, prev_Parent(currentState,1) , userRequest, request.url_root)   

        temp_organization[userRequest['user_key']]['Name'] = userRequest['content'] 
        currentState = instance[userRequest['user_key']]['state']   
        if currentState != nx_Child( first_Independent_IDInsert_State , 1 )  :
            _textMessage = SummaryText()._generate(LastYesNoString + u'\n' ,  temp_organization , instance , userRequest['user_key'])                
            return Arrow()._make_Message_Button_change_State(True,_textMessage, True, currentState,nx_Child( currentState ,1) , userRequest)             
        else :
            _textMessage = userRequest['content']+SelectString+u'\n'+  LastYesNoString +u'\n'
            _textMessage += u'ID   :'+ str(temp_organization[userRequest['user_key']]['ID'])+u'\n'
            _textMessage += u'Name :'+ temp_organization[userRequest['user_key']]['Name']
            return Arrow()._make_Message_Button_change_State(True, _textMessage, True, currentState,  nx_Child( currentState ,1) , userRequest)             
    elif   instance[userRequest['user_key']]['state']  \
    in [ nx_Child(last_4work_Light_State,4) ,nx_Child(last_3work_Doll_State,4) , nx_Child(last_3handpiece_High_State,4), nx_Child(last_3com_State,4), nx_Child( first_Independent_IDInsert_State , 2 ) ] :
        currentState = instance[userRequest['user_key']]['state']   
        if  userRequest['content']  ==  StateButtonList[ currentState ][0] :
            if  userRequest['user_key'] in temp_organization and \
                userRequest['user_key'] not in  organization :
                organization[userRequest['user_key']] = { 'ID' :  temp_organization[userRequest['user_key']]['ID']    }
                organization[userRequest['user_key']]['Name'] = temp_organization[userRequest['user_key']]['Name']   
                temp_organization.pop( userRequest['user_key'] ,  None)
            if currentState != nx_Child( first_Independent_IDInsert_State , 2 )  :
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

            _textMessage = userRequest['content']+  u'\n' +SubmitString 
            instance[userRequest['user_key']] = { 'state' : state[0] }            
            return  Arrow()._make_Message_Button_change_State(True, _textMessage, True, currentState, 0, userRequest)
        elif userRequest['content']  ==  StateButtonList[ currentState ][2] :
            if  userRequest['user_key'] not in temp_organization and \
                userRequest['user_key'] in  organization :
                return Arrow().make_Message_Button_change_State(currentState, restore_prev_State(userRequest['user_key'])  , userRequest)
            return Arrow().make_Message_Button_change_State(currentState ,  prev_Parent( currentState, 1 ) , userRequest)             
#            _textMessage = userRequest['content']+SelectString+u'\n'+ InsertNameString
#            return Arrow()._make_Message_Button_change_State(_textMessage, False, prev_Parent( currentState, 1 ) , userRequest)             


        else : 
            _textMessage = userRequest['content']+ u'\n'+ CancelString 
            instance[userRequest['user_key']] = { 'state' : state[0] }            
            return  Arrow()._make_Message_Button_change_State(True, _textMessage, True, currentState,0, userRequest)

    #elif  instance[userRequest['user_key']]['state'] == 13 :
    elif  instance[userRequest['user_key']]['state'] == nx_Child_Sibling(1,1,2) :        
        currentState = instance[userRequest['user_key']]['state']              
        if  userRequest['content']  ==  StateButtonList[ currentState ][0] :
            _textMessage = userRequest['content']+SelectString+u'\n'+ AskLocationString
            _photo = {
                "url": request.url_root+u'static/images/4work_seats.jpeg' ,
                "width": 399,
                "height": 490
            } 
            instance[userRequest['user_key']]['location'] = userRequest['content']
            return Arrow().make_Message_Button_change_State(currentState, nx_Child(currentState,1) , userRequest, request.url_root)
#            return Arrow()._make_Messages_change_State(True, _textMessage, True , _photo , False, {}, False,currentState, nx_Child(currentState,1) , userRequest)
#            return Arrow()._make_Messages_change_State(_textMessage, True , _photo , False, {}, False, first_3work_State , userRequest)
        elif  userRequest['content']  ==  StateButtonList[ currentState ][1] :
            _textMessage = userRequest['content']+SelectString+u'\n'+ InsertCaseNumberString
            _photo = {
                "url": request.url_root+u'static/images/3work_case.png' ,
                "width": 230,
                "height": 218
            } 
            instance[userRequest['user_key']]['location'] = userRequest['content']
            return Arrow().make_Message_Button_change_State(currentState, nx_Child_Sibling(currentState,1,1), userRequest, request.url_root)
#            return Arrow()._make_Messages_change_State(True, _textMessage, True , _photo , False, {}, False, currentState,nx_Child(currentState,1)+1   , userRequest)
#            return Arrow()._make_Messages_change_State(_textMessage, True , _photo , False, {}, False, 132 , userRequest)
        elif  userRequest['content']  ==  StateButtonList[ currentState ][2] :
            return Arrow().make_Message_Button_change_State(currentState, prev_Parent( currentState, 1 ) , userRequest)   


        else : 
            _textMessage = userRequest['content']+ u'\n'+ CancelString 
            instance[userRequest['user_key']] = { 'state' : state[0] }            
            return  Arrow()._make_Message_Button_change_State(True, _textMessage, True,  currentState,0, userRequest)

    #insert Yes of No for delete and prepare branches
#    elif  instance[userRequest['user_key']]['state'] == state[42] :
    elif  instance[userRequest['user_key']]['state'] == state[ nx_Child_Sibling(4,1,1) ] :
        currentState = instance[userRequest['user_key']]['state']              
        if  userRequest['content']  ==  StateButtonList[currentState][0] :
            organization.pop( userRequest['user_key'] ,  None)
        _textMessage = userRequest['content']+SelectString
        return  Arrow()._make_Message_Button_change_State(True,_textMessage, True, currentState,0, userRequest)

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
