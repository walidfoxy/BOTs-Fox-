#Cmd 
# ?lvl
# /des
# /lag
# /back
# /2-4-5
# /ca
# /spy
# 3sby+id
# fox



invite  = None
invite2  = None
s = False
gameplayed= 0
x =1
listt =[]
serversocket =None
C =None
istarted = False
start =None
stop =b'\x03\x15\x00\x00\x00\x10\t\x1e\xb7N\xef9\xb7WN5\x96\x02\xb0g\x0c\xa8'
runscript = 0
import re 
isconn = False

increase =False

back=False
ca=False
socktion =None

def str2hex(s:str):
    return ''.join([hex(ord(c))[2:].zfill(2) for c in s])

def get_info(user_id):
	global ff_player_region,requests,json
	import requests,json

	id = user_id
	cookies = {

        '_ga': 'GA1.1.2123120599.1674510784',
        '_fbp': 'fb.1.1674510785537.363500115',
        '_ga_7JZFJ14B0B': 'GS1.1.1674510784.1.1.1674510789.0.0.0',
        'source': 'mb',
        'region': 'MA',
        'language': 'ar',
        '_ga_TVZ1LG7BEB': 'GS1.1.1674930050.3.1.1674930171.0.0.0',
        'datadome': '6h5F5cx_GpbuNtAkftMpDjsbLcL3op_5W5Z-npxeT_qcEe_7pvil2EuJ6l~JlYDxEALeyvKTz3~LyC1opQgdP~7~UDJ0jYcP5p20IQlT3aBEIKDYLH~cqdfXnnR6FAL0',
        'session_key': 'efwfzwesi9ui8drux4pmqix4cosane0y',
    }

	headers = {
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        # 'Cookie': '_ga=GA1.1.2123120599.1674510784; _fbp=fb.1.1674510785537.363500115; _ga_7JZFJ14B0B=GS1.1.1674510784.1.1.1674510789.0.0.0; source=mb; region=MA; language=ar; _ga_TVZ1LG7BEB=GS1.1.1674930050.3.1.1674930171.0.0.0; datadome=6h5F5cx_GpbuNtAkftMpDjsbLcL3op_5W5Z-npxeT_qcEe_7pvil2EuJ6l~JlYDxEALeyvKTz3~LyC1opQgdP~7~UDJ0jYcP5p20IQlT3aBEIKDYLH~cqdfXnnR6FAL0; session_key=efwfzwesi9ui8drux4pmqix4cosane0y',
        'Origin': 'https://shop2game.com',
        'Referer': 'https://shop2game.com/app/100067/idlogin',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Redmi Note 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
        'accept': 'application/json',
        'content-type': 'application/json',
        'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'x-datadome-clientid': '6h5F5cx_GpbuNtAkftMpDjsbLcL3op_5W5Z-npxeT_qcEe_7pvil2EuJ6l~JlYDxEALeyvKTz3~LyC1opQgdP~7~UDJ0jYcP5p20IQlT3aBEIKDYLH~cqdfXnnR6FAL0',
    }

	json_data = {
        'app_id': 100067,
        'login_id': f'{id}',
        'app_server_id': 0,
    }

	res = requests.post('https://shop2game.com/api/auth/player_id_login', cookies=cookies, headers=headers, json=json_data)
	response = json.loads(res.text)
	try :
		name=response['nickname']
		region = response["region"]
		name = [name,region]
		ff_player_region =name[1]
	except:
		pass
	return name[0]
def convert_to_bytes(input_string):
    # replace non-hexadecimal character with empty string
    cleaned_string = input_string[:231] + input_string[232:]
    # convert cleaned string to bytes
    output_bytes = bytes.fromhex(cleaned_string)
    return output_bytes
def gen_packet(data : str):
    PacketLenght = data[7:10]
    PacketHedar1= data[10:32]
    PayLoad= data[32:34]
    NameLenghtAndName=re.findall('1b12(.*)1a02' , data)[0]
    Name = NameLenghtAndName[2:]
    NameLenght = NameLenghtAndName[:2]

    NewName="5b46463030305d4d6f64652042792040594b5a205445414d"
    NewNameLenght = len(NewName)//2

    NewPyloadLenght=int(int('0x'+PayLoad , 16) - int("0x"+NameLenght , 16))+int(NewNameLenght)
    NewPacketLenght = (int('0x'+PacketLenght , 16)-int('0x'+PayLoad , 16)) + NewPyloadLenght

    packet = data.replace(Name , str((NewName)))
    packet = packet.replace(str('1b12'+NameLenght) , '1b12'+str(hex(NewNameLenght)[2:]))
    packet = packet.replace(PayLoad , str(hex(NewPyloadLenght)[2:]))
    packet = packet.replace(PacketLenght[0] , str(hex(NewPacketLenght)[2:]) )
    
    return packet
def gen_msgv2(packet  , replay):
    
    replay  = replay.encode('utf-8')
    replay = replay.hex()
    

    hedar = packet[0:8]
    packetLength = packet[8:10] #
    paketBody = packet[10:32]
    pyloadbodyLength = packet[32:34]#
    pyloadbody2= packet[34:60]
    
    pyloadlength = packet[60:62]#
    pyloadtext  = re.findall(r'{}(.*?)28'.format(pyloadlength) , packet[50:])[0]
    pyloadTile = packet[int(int(len(pyloadtext))+62):]
    
    
    NewTextLength = (hex((int(f'0x{pyloadlength}', 16) - int(len(pyloadtext)//2) ) + int(len(replay)//2))[2:])
    if len(NewTextLength) ==1:
        NewTextLength = "0"+str(NewTextLength)
        
    NewpaketLength = hex(((int(f'0x{packetLength}', 16) - int((len(pyloadtext))//2) ) ) + int(len(replay)//2) )[2:]
    NewPyloadLength = hex(((int(f'0x{pyloadbodyLength}', 16) - int(len(pyloadtext)//2))  )+ int(len(replay)//2) )[2:]

    finallyPacket = hedar + NewpaketLength +paketBody + NewPyloadLength +pyloadbody2+NewTextLength+ replay + pyloadTile
    
    return str(finallyPacket)

def check_information(uid,abbr):
	player_uid = uid

	servers_name_db = {
	"bd": "بنغلاديش",
	"br": "البرازيل",
	"eu": "اروبا",
	"hk": "هونج كونج",
	"id": "أندونوسيا",
	"in": "الهند",
	"me": "الشرق الأوسط و أفريقيا",
	"mo": "ماكوي",
	"my": "ماليسيا",
	"ph": "فليبينيس",
	"pk": "باكيستان",
	"ru": "روسيا",
	"sa": "لاتين الأمم المتحدة",
	"sg": "سنغفورة",
	"th": "التيلاند",
	"tw": "الطيوان",
	"vn": "فيتنام",
	"ind" : "الهند"
	}
	def get_server_name(abbr):
		short_name = abbr.lower()
		return servers_name_db[short_name]
	try:
		player_server = get_server_name(abbr)
	except:
		player_server = abbr
	def check_if_banned(uid):
		response_bol = None
		request_url = f"https://ff.garena.com/api/antihack/check_banned?lang=en&uid={uid}"
		req_server = requests.get(request_url)
		req_response = req_server.text
		req_response = json.loads(req_response)
		if req_response["status"]=="success":
			formula = req_response["data"]["is_banned"]
			if formula==1:
				response_bol=True
			elif formula==0:
				response_bol=False
		return response_bol
	def return_result(res_bol):
		if res_bol:
		#ban
			return "[FF0000][b][c]تم تعليقه !"
		elif res_bol==False:
		#clear
			return "[00FF00][b][c]متصل !"
	msg = return_result(check_if_banned(uid))
	return (player_server,msg)

def getinfobyid(packet , user_id , client):
    player_name = get_info(user_id)
    player_region = ff_player_region
    received_data = check_information(user_id,player_region)
    final_info_region = received_data[0]
    final_ban_msg = received_data[1]
    #player_name
    #final_info_region
    #
#--------------------------------------------------

    pyload_3 = gen_msgv2_clan(packet , f"""[00FFFF][b][c]معلومات الاعب ! """)
    client.send(bytes.fromhex(pyload_3))
    pyload_3 = gen_msgv2(packet , f"""[00FFFF][b][c]معلومات الاعب !  """)
    client.send(bytes.fromhex(pyload_3))
    client.send(bytes.fromhex(pyload_3))
        
#id plyaer
    time.sleep(4.0)
    pyload_3 = gen_msgv2_clan(packet , f"""[00FFFF][b][c]أيدي الاعب : [FFA500]""")
    client.send(bytes.fromhex(pyload_3))
    pyload_3 = gen_msgv2(packet , f"""[00FFFF][b][c]أيدي الاعب : [FFA500]""")
    client.send(bytes.fromhex(pyload_3))
    pyload_3 = gen_msgv2_clan(packet , f"""[00FF00][b][c]{user_id}""")
    client.send(bytes.fromhex(pyload_3))
    pyload_3 = gen_msgv2(packet , f"""[00FF00][b][c]{user_id}""")
    client.send(bytes.fromhex(pyload_3))
    #splach
    pyload_3 = gen_msgv2_clan(packet , f"""[ffd319][b][c]جاري تحميل . . .""")
    client.send(bytes.fromhex(pyload_3))
    pyload_3 = gen_msgv2(packet , f"""[ffd319][b][c]جاري تحميل . . .""")
    client.send(bytes.fromhex(pyload_3))
        #name
        
        
    time.sleep(2.0)
    pyload_3 = gen_msgv2_clan(packet , f"""[00FFFF][b][c]إسم لاعب : [FFA500]""")
    client.send(bytes.fromhex(pyload_3))
    pyload_3 = gen_msgv2(packet , f"""[00FFFF][b][c]إسم لاعب : [FFA500]""")
    client.send(bytes.fromhex(pyload_3))
    pyload_3 = gen_msgv2_clan(packet , f"""[00FF00][b][c]{player_name}""")
    client.send(bytes.fromhex(pyload_3))
    pyload_3 = gen_msgv2(packet , f"""[00FF00][b][c]{player_name}""")
    client.send(bytes.fromhex(pyload_3))
        
        
        #splach1
    pyload_3 = gen_msgv2_clan(packet , f"""[ffd319][b][c]جاري تحميل . . .""")
    client.send(bytes.fromhex(pyload_3))
    pyload_3 = gen_msgv2(packet , f"""[ffd319][b][c]جاري تحميل . . .""")
    client.send(bytes.fromhex(pyload_3))
        
        
        #region
    time.sleep(2.0)
    pyload_3 = gen_msgv2_clan(packet , f"""[00FFFF][b][c]المنطقة : [FFA500]""")
    client.send(bytes.fromhex(pyload_3))
    pyload_3 = gen_msgv2(packet , f"""[00FFFF][b][c]المنطقة : [FFA500]""")
    client.send(bytes.fromhex(pyload_3))
    pyload_3 = gen_msgv2_clan(packet , f"""[00FF00][b][c]{final_info_region}""")
    client.send(bytes.fromhex(pyload_3))
    pyload_3 = gen_msgv2(packet , f"""[00FF00][b][c]{final_info_region}""")
    client.send(bytes.fromhex(pyload_3))
        
        ##
#splach2

    pyload_3 = gen_msgv2_clan(packet , f"""[ffd319][b][c]جاري تحميل . . .""")
    client.send(bytes.fromhex(pyload_3))
    pyload_3 = gen_msgv2(packet , f"""[ffd319][b][c]جاري تحميل . . .""")
    client.send(bytes.fromhex(pyload_3))
        
        
        #ban check
    time.sleep(2.0)
    pyload_3 = gen_msgv2_clan(packet , f"""[00FFFF][b][c]حالة الاعب : """)
    client.send(bytes.fromhex(pyload_3))
    pyload_3 = gen_msgv2(packet , f"""[00FFFF][b][c]حالة الاعب : """)
    client.send(bytes.fromhex(pyload_3))
    client.send(bytes.fromhex(pyload_3))
        
        
        
        #
    
    pyload_3 = gen_msgv2_clan(packet , f"""[00FF00][b][c]{final_ban_msg}""")
    client.send(bytes.fromhex(pyload_3))
    pyload_3 = gen_msgv2(packet , f"""[00FF00][b][c]{final_ban_msg}""")
    client.send(bytes.fromhex(pyload_3))
    client.send(bytes.fromhex(pyload_3))


        



def gen_msgv2_clan(packet  , replay):
    
    replay  = replay.encode('utf-8')
    replay = replay.hex()

    hedar = packet[0:8]
    packetLength = packet[8:10] #
    paketBody = packet[10:32]
    pyloadbodyLength = packet[32:34]#
    pyloadbody2= packet[34:64]
    pyloadlength = packet[64:66]#
    pyloadtext  = re.findall(r'{}(.*?)28'.format(pyloadlength) , packet[50:])[0]
    pyloadTile = packet[int(int(len(pyloadtext))+66):]
    

    NewTextLength = (hex((int(f'0x{pyloadlength}', 16) - int(len(pyloadtext)//2) ) + int(len(replay)//2))[2:])
    if len(NewTextLength) ==1:
        NewTextLength = "0"+str(NewTextLength)
    NewpaketLength = hex(((int(f'0x{packetLength}', 16) - int(len(pyloadtext)//2) ) - int(len(pyloadlength))) + int(len(replay)//2) + int(len(NewTextLength)))[2:]
    NewPyloadLength = hex(((int(f'0x{pyloadbodyLength}', 16) - int(len(pyloadtext)//2)) -int(len(pyloadlength)) )+ int(len(replay)//2) + int(len(NewTextLength)))[2:]
    
    
    finallyPacket = hedar + NewpaketLength +paketBody + NewPyloadLength +pyloadbody2+NewTextLength+ replay + pyloadTile

    return finallyPacket
invite= None




spams = False

spampacket= b''
recordmode= False

sendpackt=False
global vares
vares = 0
spy = False
inviteD=False
inviteE=False
op = None
global statues
statues= True
SOCKS_VERSION = 5
packet =b''
spaming =True
full=False
import os
import sys


def spam(server,packet):
    while True:


        time.sleep(0.015)


        server.send(packet)
        if   recordmode ==False:

            break

def destroy(remote,dataC):
    
    var= 0
    for i in range(50):
        
        var= var+1
       
        time.sleep(0.010)
        for i in range(10):
            
            remote.send(dataC)
    time.sleep(0.5)



def timesleep():
    time.sleep(60)
    #print(istarted)
    if istarted == True:
        serversocket.send(start)


def enter_game_and_RM():
    global listt
    for data in listt:
        
        C.send(data)
        listt.remove(data)
    time.sleep(15)

    print("start the game ....")

    istarted =False
    serversocket.send(start)

    t = threading.Thread(target=timesleep, args=())
    t.start()
def break_the_matchmaking(server):
    global is_start
    global isrun

    server.send(stop)


    server.send(stop)

    server.send(stop)
    print('sending stop')
    is_start =True

    t = threading.Thread(target=enter_game_and_RM, args=())
    t.start()


import time

import socket
import threading
import select
SOCKS_VERSION= 5


class Proxy:



    def __init__(self):
        self.username = "username"
        self.password = "username"
        self.packet = b''
        self.sendmode = 'client-0-'
        self.spam_level=False
        self.spam_foxy=False


    def handle_client(self, connection):



        version, nmethods = connection.recv(2)
        methods = self.get_available_methods(nmethods, connection)



        if 2   in set(methods):
            if 2 in set(methods):

                connection.sendall(bytes([SOCKS_VERSION, 2]))
            else:
                connection.sendall(bytes([SOCKS_VERSION, 0]))





        if not self.verify_credentials(connection,methods):
            return
        version, cmd, _, address_type = connection.recv(4)



        if address_type == 1:
            address = socket.inet_ntoa(connection.recv(4))
        elif address_type == 3:
            domain_length = connection.recv(1)[0]
            address = connection.recv(domain_length)
            address = socket.gethostbyname(address)
            name= socket.gethostname()



        port = int.from_bytes(connection.recv(2), 'big', signed=False)
        port2 = port
        try:





            remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote.connect((address, port))
            #print(" connect to {} \n \n \n ".format(address))
            bind_address = remote.getsockname()

            addr = int.from_bytes(socket.inet_aton(
                bind_address[0]), 'big', signed=False)
            port = bind_address[1]

            reply = b''.join([
                SOCKS_VERSION.to_bytes(1, 'big'),
                int(0).to_bytes(1, 'big'),
                int(0).to_bytes(1, 'big'),
                int(1).to_bytes(1, 'big'),
                addr.to_bytes(4, 'big'),
                port.to_bytes(2, 'big')

            ])
        except Exception as e:

            reply = self.generate_failed_reply(address_type, 5)


        connection.sendall(reply)


        self.botdev(connection, remote,port2)


    def generate_failed_reply(self, address_type, error_number):
        return b''.join([
            SOCKS_VERSION.to_bytes(1, 'big'),
            error_number.to_bytes(1, 'big'),
            int(0).to_bytes(1, 'big'),
            address_type.to_bytes(1, 'big'),
            int(0).to_bytes(4, 'big'),
            int(0).to_bytes(4, 'big')
        ])

    def verify_credentials(self, connection,methods):

        if 2 in methods:


            version = ord(connection.recv(1))


            username_len = ord(connection.recv(1))
            username = connection.recv(username_len).decode('utf-8')

            password_len = ord(connection.recv(1))
            password = connection.recv(password_len).decode('utf-8')
            #   print(username,password)
            if username == self.username and password == self.password:

                response = bytes([version, 0])
                connection.sendall(response)


                return True

            response = bytes([version, 0])
            connection.sendall(response)

            return True

        else:


            version =1
            response = bytes([version, 0])
            connection.sendall(response)


            return True

    def get_available_methods(self, nmethods, connection):
        methods = []
        for i in range(nmethods):
            methods.append(ord(connection.recv(1)))
        return methods

    def runs(self, host, port):
        try:
            var =  0







            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port))
            s.listen()



            while True:
                var =var+1


                conn, addr = s.accept()
                running = False

                t = threading.Thread(target=self.handle_client, args=(conn,))
                t.start()
        except Exception as e:
            print("Created")
            










    #connect
    def botdev(self, client, remote, port):
        
            while True:
                r, w, e = select.select([client, remote], [], [])

                od= b''
                global start
                if client in r or remote in r:
                    global invite
                    global invite2
                    global s
                    global x
                    global ca
                    global hidr
                    global cliee
                    global serversocket
                    global isconn ,inviteD ,back
                    if client in r:



                        dataC = client.recv(999999)


                        if port ==39801 or port ==39699:
                            isconn=True
                        if  "39699" in str(remote) :
                            self.op = remote
                
                        if '0515' in dataC.hex()[0:4] and len(dataC.hex()) >= 141  :                  
                            self.data_join=dataC

                            
                        
                        if '0515' in dataC.hex()[0:4] and len(dataC.hex()) <50  :  
                            print(remote)                
                            self.data_back=dataC

                        if  port ==39699:
                            #print(" catch a socket sir ")
                            #  print(f"{dataC}\n")
                            invite= remote
                        global hide
                        hide =False
                        global recordmode
                        #laaaaaag
                        if '1215' in dataC.hex()[0:4] and recordmode ==True:

                            global spampacket
                            spampacket =dataC

                            #recordmode=False
                            global statues
                            statues= True
                            time.sleep(5)

                            b = threading.Thread(target=spam, args=(remote,spampacket))
                            b.start()


                                    #invite_D
                        if '0515' in dataC.hex()[0:4] and len(dataC.hex()) >=900 and inviteD==True and hide ==False :
                            var = 0
                            m = threading.Thread(target=destroy, args=(remote,dataC))
                            m.start()
                            global spams
                            spams =True

                        if '0515' in dataC.hex()[0:4] and len(dataC.hex()) >= 141:

                            hide = True


                            global benfit
                            benfit = False


                                    #lvl_UP
                        if '0315' in dataC.hex()[0:4]:
                            if len(dataC.hex()) >=300:
                                start = dataC
                                print(dataC)
                            is_start =False

                            serversocket =remote
                            print("socket is defined suucesfuly !..")
                            t = threading.Thread(target=timesleep, args=())
                            t.start()
                            #level_PRO++
                        if "0315" in dataC.hex()[0:4] and len(dataC.hex())>820 and self.spam_level==True:
                            self.start_game=dataC
                            print("packet >>"+dataC.hex())
                            threading.Thread(target=self.level_up ).start()
                            #level_low
                        if "0315" in dataC.hex()[0:4] and len(dataC.hex())>820 and self.spam_foxy==True:
                            self.start_walid=dataC
                            print("packet >>"+dataC.hex())
                            threading.Thread(target=self.foxy_up ).start()



         





#mizaaaaat


                        if remote.send(dataC) <= 0:
                            break
                    if remote in r:

                        global opb
                        global listt
                        global C
                        global istarted
                        global gameplayed
                        global packet
                        global socktion
                        global ca
                        global increase ,back
                        dataS = remote.recv(999999)
                        
                        
                        if '1809' in dataS.hex()[26:30] or "1802" in dataS.hex()[26:30] or "1808" in dataS.hex()[26:30]:
                          #  ca=False
                            print(dataC.hex()[0:4])
                            print('  the team ')
                            #hackg.send(hackw
                        

                        if '0300' in dataS.hex()[0:4] :
                            #print('yes')
                            C = client
                            print(dataS)
                            socketsender =client

                            if b'Ranked Mode' in dataS:
                                #print("w")
                                client.send(dataS)
                            else:



                                if b'catbarq' in dataS:
                                    vdsf=3
                                else:
                                    #
                                    hackw= dataS
                                    hackg= client

                                    if len(dataS.hex()) <= 100:
                                        e=2
                                    #  print("anti detect !")


                                    else:
                                        if increase ==True:

                                            print("Enter game packet founded")
                                            #      start = dataC
                                            #      print(dataC)
                                            gameplayed =gameplayed+1
                                            istarted = True
                                            #      print(f"{dataS} \n")
                                            listt.append(dataS)
                                            #rint(listt)
                                            t = threading.Thread(target=break_the_matchmaking, args=(serversocket,))
                                            t.start()
                                        else:
                                            client.send(dataS)

                        else:
                            #  if '0000' !in dataS.hex()[:4] and '1200' !in dataS.hex()[:4] and '1700' !in dataS.hex()[:4]:
                            #  print(dataS.hex(),"\n")
                            if '0500' in dataS.hex()[:4] and b'\x05\x15\x00\x00\x00\x10Z\xca\xf5&T;\x0cA\x01\x16\xe0\x05\xb2\xea\xe4\x0b' in dataC:
                                f=2
                                #serversocket.send(b'\x05\x15\x00\x00\x00\x10\x9b@x\xd7\x15\x9e\x0f\xfaZ+\x88\xe5\xac\x18\x9fw')

                            else:
                                #spam_invite
                                if '1200' in dataS.hex()[0:4] and '2f646573' in dataS.hex()[0:900] : 
                                    inviteD =True
                                    client.send(bytes.fromhex(gen_msgv2(dataS.hex() ,"[00FFFF][b][c]تدمير سكواد <<-- [00ff00][b][c] م")))
                                    client.send(bytes.fromhex(str(gen_msgv2_clan(dataS.hex() ,"[00FFFF][b][c]تدمير سكواد <<-- [00ff00][b][c] مفعل"))))

                                    time.sleep(3.5)
                                    
                                    
                                    
                                    client.send(bytes.fromhex(gen_msgv2(dataS.hex() ,"[00FF00][b][c]The Foxy Official [FFC800][b][c]Ⓥ")))
                                    client.send(bytes.fromhex(str(gen_msgv2_clan(dataS.hex() ,"[00FF00][b][c]The Foxy Official [FFC800][b][c]Ⓥ"))))
                                    
                                    
                                    client.send(bytes.fromhex(gen_msgv2(dataS.hex() ,"[1200000002-12]")))
                                    client.send(bytes.fromhex(str(gen_msgv2_clan(dataS.hex() ,"[1200000002-12]"))))
                                    
                                    

                                    
                                    
                                    
                                    #Follow_Us
                                if '1200' in dataS.hex()[0:4] and '666f7879' in dataS.hex()[0:900] :
                                    
                                    
                                    client.send(bytes.fromhex(str(gen_msgv2_clan(dataS.hex() ,"[00FF00][b][c]Instagram : [FFC800][b][c]@the_foxy999"))))
                                    #Youtube
                                    client.send(bytes.fromhex(gen_msgv2(dataS.hex() ,"[00FF00][b][c]Youtube : [FFC800][b][c] The Foxy Ⓥ")))
                                    client.send(bytes.fromhex(str(gen_msgv2_clan(dataS.hex() ,"[00FF00][b][c]Youtube : [FFC800][b][c]The Foxy Ⓥ"))))
                                    
                                    client.send(bytes.fromhex(gen_msgv2(dataS.hex() ,"[1200000002-03]")))
                                    client.send(bytes.fromhex(str(gen_msgv2_clan(dataS.hex() ,"[1200000002-03]"))))
                                    
                                    
                                    #Follow_Us2
                                if '1200' in dataS.hex()[0:4] and '466f7879' in dataS.hex()[0:900] :
                                    
                                    
                                    client.send(bytes.fromhex(str(gen_msgv2_clan(dataS.hex() ,"[00FF00][b][c]Instagram : [FFC800][b][c]@the_foxy999"))))
                                    #Youtube
                                    client.send(bytes.fromhex(gen_msgv2(dataS.hex() ,"[00FF00][b][c]Youtube : [FFC800][b][c] The Foxy Ⓥ")))
                                    client.send(bytes.fromhex(str(gen_msgv2_clan(dataS.hex() ,"[00FF00][b][c]Youtube : [FFC800][b][c]The Foxy Ⓥ"))))
                                    
                                    
                                    client.send(bytes.fromhex(gen_msgv2(dataS.hex() ,"[1200000002-03]")))
                                    client.send(bytes.fromhex(str(gen_msgv2_clan(dataS.hex() ,"[1200000002-03]"))))
                                    
                                    
                                    #invite_spam OFF
                                if '1200' in dataS.hex()[0:4] and '2f2d646573' in dataS.hex()[0:900] :
                                    inviteD =False
                                    client.send(bytes.fromhex(gen_msgv2(dataS.hex() ,"[FF0000][b][c]توقفت !")))
                                    client.send(bytes.fromhex(str(gen_msgv2_clan(dataS.hex() ,"[FF0000][b][c]توقفت ! "))))                       
                                    
                                    
                                        #level_ON       PRO++
                                                                     
                                if '1200' in dataS.hex()[0:4] and '3f6c766c' in dataS.hex()[0:900] :
                                    

                                    
                                    client.send(bytes.fromhex(gen_msgv2(dataS.hex() ,"[00FF00][b][c]زيادة لفل مفعل !!")))
                                    client.send(bytes.fromhex(str(gen_msgv2_clan(dataS.hex() ,"[00FF00][b][c]زيادة لفل مفعل  !! "))))
                                    
                                    time.sleep(2.0)
                                    client.send(bytes.fromhex(gen_msgv2(dataS.hex() ,"[00FF00][b][c]المود : [171dcd][b][c] ذئب وحيد")))
                                    client.send(bytes.fromhex(str(gen_msgv2_clan(dataS.hex() ,"[00FF00][b][c]المود : [171dcd][b][c] ذئب وحيد"))))
                                    
                                    time.sleep(3.5)
                                    
                                    self.spam_level=True
                                    
                                    
                                    
                                    client.send(bytes.fromhex(gen_msgv2(dataS.hex() ,"[00FF00][b][c]The Foxy Official [FFC800][b][c]Ⓥ")))
                                    client.send(bytes.fromhex(str(gen_msgv2_clan(dataS.hex() ,"[00FF00][b][c]The Foxy Official [FFC800][b][c]Ⓥ"))))
                                    
                                    client.send(bytes.fromhex(gen_msgv2(dataS.hex() ,"[1200000002-07]")))
                                    client.send(bytes.fromhex(str(gen_msgv2_clan(dataS.hex() ,"[1200000002-07]"))))
                                    
                                    
                                    
                                    
                                    
                                    
                                #level_OFF
                                if '1200' in dataS.hex()[0:4] and '3f2d6c766c' in dataS.hex()[0:900] :
                                

                                    client.send(bytes.fromhex(gen_msgv2(dataS.hex() ,"[FF0000][b][c]توقفت !")))
                                    client.send(bytes.fromhex(str(gen_msgv2_clan(dataS.hex() ,"[FF0000][b][c]توقفت !"))))
                                    
                                    self.spam_level=False
                                    
                                    
                                    
                                    
                                    
                                        #level_ON       Low
                                                                     
                                if '1200' in dataS.hex()[0:4] and '3F6C766C31' in dataS.hex()[0:900] :
                                    

                                    
                                    client.send(bytes.fromhex(gen_msgv2(dataS.hex() ,"[00FF00][b][c]زيادة لفل مفعلة للأجهزة البطيئة !!")))
                                    client.send(bytes.fromhex(str(gen_msgv2_clan(dataS.hex() ,"[00FF00][b][c]زيادة لفل مغعلة للأجهزة البطيئة  !! "))))
                                    
                                    time.sleep(2.0)
                                    client.send(bytes.fromhex(gen_msgv2(dataS.hex() ,"[00FF00][b][c]المود : [171dcd][b][c] ذئب وحيد")))
                                    client.send(bytes.fromhex(str(gen_msgv2_clan(dataS.hex() ,"[00FF00][b][c]المود : [171dcd][b][c] ذئب وحيد"))))
                                    
                                    time.sleep(3.5)
                                    
                                    self.spam_foxy=True
                                    
                                    
                                    
                                    client.send(bytes.fromhex(gen_msgv2(dataS.hex() ,"[00FF00][b][c]The Foxy Official [FFC800][b][c]Ⓥ")))
                                    client.send(bytes.fromhex(str(gen_msgv2_clan(dataS.hex() ,"[00FF00][b][c]The Foxy Official [FFC800][b][c]Ⓥ"))))
                                    
                                    client.send(bytes.fromhex(gen_msgv2(dataS.hex() ,"[1200000002-07]")))
                                    client.send(bytes.fromhex(str(gen_msgv2_clan(dataS.hex() ,"[1200000002-07]"))))
                                    
                                    
                                    
                                    
                                    
                                    
                                #level_OFF
                                if '1200' in dataS.hex()[0:4] and '3F2D6C766C31' in dataS.hex()[0:900] :
                                

                                    client.send(bytes.fromhex(gen_msgv2(dataS.hex() ,"[FF0000][b][c]توقفت !")))
                                    client.send(bytes.fromhex(str(gen_msgv2_clan(dataS.hex() ,"[FF0000][b][c]توقفت !"))))
                                    
                                    self.spam_foxy=False
                                    
                                   #end
                                    
                                    
                                    
                                   
                                   

                                   
                                #spy_last_sqoud
                                if '1200' in dataS.hex()[0:4] and '2f737079' in dataS.hex()[0:900] :

                                    client.send(bytes.fromhex(gen_msgv2(dataS.hex() ,"[00FF00][b][c]اصمت أنت فوضع التجسس !")))
                                    client.send(bytes.fromhex(str(gen_msgv2_clan(dataS.hex() ,"[00FF00][b][c]أصمت أنت فوضع التجسس !"))))
                                    socktion.send(packet)
                                    
                                    time.sleep(3.5)
                                    
                                    
                                    
                                    client.send(bytes.fromhex(gen_msgv2(dataS.hex() ,"[00FF00][b][c]The Foxy Official [FFC800][b][c]Ⓥ")))
                                    client.send(bytes.fromhex(str(gen_msgv2_clan(dataS.hex() ,"[00FF00][b][c]The Foxy Official [FFC800][b][c]Ⓥ"))))
                                    
                                    client.send(bytes.fromhex(gen_msgv2(dataS.hex() ,"[1200000002-11]")))
                                    client.send(bytes.fromhex(str(gen_msgv2_clan(dataS.hex() ,"[1200000002-11]"))))
                                    
                                    
                                    
#           /                          5
                                if '1200' in dataS.hex()[0:4] and '2f35' in dataS.hex()[0:900]:
                                    client.send(bytes.fromhex(gen_msgv2(dataS.hex() ,"[00FFFF][b][c]تحويل وضع سكواد 5 ")))
                                    client.send(bytes.fromhex(str(gen_msgv2_clan(dataS.hex() ,"[00FFFF][b][c]تحويل وضع سكواد 5 "))))
                                    client.send(bytes.fromhex(gen_msgv2(dataS.hex() ,"[1200000002-08]")))
                                    client.send(bytes.fromhex(str(gen_msgv2_clan(dataS.hex() ,"[1200000002-08]"))))
                                    
                                    
                                    

                                    invite.send(bytes.fromhex("0503000001d01fb578313150905babcef51dd24ed75fd0a24b024bd1429646114bc22e604afd35a96fbc48710b2d9cfec4378287ec829e33a78608fd2dd138d4d24a19c00fbfdc9f15c77ff86d638b34de95bd886e3075e82d3f4a3888f9b6943463022c43fb90e229f0eaf8a788f6f766d891d99eb2c37b277144923212810b3c80d1c521790154ed270f5241adc136f2a22816e0bc84fcaf79386b27559de966aa788c184d35bbbfaa03a5f08746f8db0e73b2c91ec4515d61f689a0cad30a7cbd6c325151e879dabc43d506b3240abe41bc0d6b4416c18f68ef4af2d04c381be6bf586f6b25727c0c85c03a579137e4a6c602ef6d833dabdab3eba3a5266e5a4731fbfb1720b60f124cd8fd4fa26cc7a9fb6e0a218d8809f57b204d22fa97520aeb99007c7b71c709e53ecc688c9963e0786909152fa93f06dc93085468dae34e1609f33f7dee228fb058c6efd6846b50ac54db0aebb8f5bc2f6751f9e2886dbab41cbaf5a1d8cd88e6c13a2a2a56b613a2d32179dc3f781493a5027322ac0cb1a2d3c79d49fb12ed26230e1561df43d315a27be17b5debdba757803305252b5443f3d77cd319dde9c49a72c636d93d02bdd9597168f378aa6e41d0fd545abf8bc0883f3dac11ea27166683c7111a0f329bf6b6a5"))

#           /4
    
                               
                                if '1200' in dataS.hex()[0:4] and '2f34' in dataS.hex()[0:900]:
                                    client.send(bytes.fromhex(gen_msgv2(dataS.hex() ,"[00FFFF][b][c] تحويل وضع سكواد 4 ")))
                                    client.send(bytes.fromhex(str(gen_msgv2_clan(dataS.hex() ,"[00FFFF][b][c]تحويل وضع سكواد 4 "))))
                                    
                                    client.send(bytes.fromhex(gen_msgv2(dataS.hex() ,"[1200000002-06]")))
                                    client.send(bytes.fromhex(str(gen_msgv2_clan(dataS.hex() ,"[1200000002-06]"))))
                                    
                                    

                                    invite.send(bytes.fromhex("0515000001c07906415ee12e4a169ec5633b54581771e13cd08077f10f76e5b7d2706c90b2b8bb5167a9832b2b4179e50f4dc8e20c3ac72ac7e2fd3bc9f9c21148d6b8107c8ed0c6377d23d0f2f3f7635c4a2ee5db6f544f8a6b9e5ca136a5d0678ab752e42380d10428c3fdaf4abc66d58456f6a67960fcb1e4b2bcb80721c6bb3c56698dc5a0944e4fff46bb57030590106b45520169c9ca422f2d1f04e067d4b0b3ddfa162c5dc3156ff11a5df872133ee1f9fd332f1a9df55edba27eebe0ae48de1a97893304765ebe4637be65b82df04ba8180681e68bc905347613bdf200e8435aeafcb1bdbcbc2c5b8a210f05907226b797f336fc9ee7df553e2edaa8d15682828304b922b1913890e4eb273d0550438bc227a35b0d76e28cacc14fb4aee6ad831f8d132610644152be8f0b5a3b9816ae65a004ddb64980ac36403ade91afd383a85930c8e153d7da457ccc4988047a63277a378e34defd3741b38cd34c133bcb1cb836ee79ae0c4da968d6453bb31edb8d083ed3f2b309cdbf96c0eb5f849f9ef9ac4bbeb6f43631b637fe86a6e2ba5c5ec75013535b473d3028a62a5f27614ac3b0ae60774c60acbf6b7006b89f90d5331075391cde7da017d088cfb470aab95d2b"))
                                    
                                    
             
            
                                    
                                    
                                    
#           /2

                               
                                if '1200' in dataS.hex()[0:4] and '2f32' in dataS.hex()[0:900]:
                                    client.send(bytes.fromhex(gen_msgv2(dataS.hex() ,"[00FFFF][b][c] تحويل وضع سكواد 2")))
                                    client.send(bytes.fromhex(str(gen_msgv2_clan(dataS.hex() ,"[00FFFF][b][c]تحويل وضع سكواد 2"))))
                                    
                                    client.send(bytes.fromhex(gen_msgv2(dataS.hex() ,"[1200000002-01]")))
                                    client.send(bytes.fromhex(str(gen_msgv2_clan(dataS.hex() ,"[1200000002-01]"))))
                                    
                                    

                                    invite.send(bytes.fromhex("0515000001c041b8f4aed5883a2ccdc22f2549c3751974a8f2bcacace88c156ee69911475b14104d4e09027a0d296458125320915cf6512c040d648d8f4c59c57d1e6ba5e098545c39bb37ea0be6e5b3a288d974acb2afbc1836f83061d4e5e291c683bb44911e08860e700c7be5d40578712805a8e99b3317d4d06cf42573ad9094f1091bf30f4238afd51a4989d5dc4efbe5d447b079fd3e8ea08e7942baea11f449068c89826a4928abfcdaf55aa99bdda35f8d61c2277156df051c123e3571e2fd2356b574195bd2b28f03480b3cdb1712bebec6029546faf87e816fdc688c67c1264f06b8513145f75132edb7d811300541fdccbdc3161f2dba96eff6640293e35e6c44ed3334ef785b0d3808073f393981bc572da04223a217cc68af8c9b5a0df472aa16e2c449973727236e990936fc86bdc9acec5efc5af6b31ee36a15e0e09aff0f8ef239e5e9affc7d589d1c3b08dd13f6b9b2f44a7163dbef02643945af4cb201b31530bb3fef1c7bb55a44cb7cd04fd9bb5a76f9625eccc733f7513cd5541632ffb5a8753fb6e0dea1b77b51c828835276fa8668a7a0bb0e584a021e2ea5610747b38b1c3eaf17d918b7f848487aee5ee41517dadfc587f5f21cd996d440f23e"))






                                if '1200' in dataS.hex()[0:4] and '2f6c6167' in dataS.hex()[0:900] and spaming:
                                    client.send(bytes.fromhex(gen_msgv2(dataS.hex() ,"[00FFFF][b][c]تكرار رسالتك : <--")))
                                    client.send(bytes.fromhex(str(gen_msgv2_clan(dataS.hex() ,"[00FFFF][b][c]تكرار رسالتك : <--"))))

                                    
                                    
                                    
                                    recordmode = True
     
                                if '1200' in dataS.hex()[0:4] and '2f2d6c6167' in dataS.hex()[0:900]:
                                    recordmode=False
                                    client.send(bytes.fromhex(gen_msgv2(dataS.hex() ,"[FF0000][b][c]توقفت !")))
                                    client.send(bytes.fromhex(str(gen_msgv2_clan(dataS.hex() ,"[FF0000][b][c]توقفت !"))))
                                    
                                    #back_one_time
                                if '1200' in dataS.hex()[0:4]:
                                    if b"/back" in dataS:
                                        back=True
                                        threading.Thread(target=self.foxy , args=(self.data_join,)).start()
                                        client.send(bytes.fromhex(gen_msgv2(dataS.hex() ,"[00FF00][b][c]تم إسترجاعك ")))
                                        client.send(bytes.fromhex(str(gen_msgv2_clan(dataS.hex() ,"[00FF00][b][c]تم إسترجاعك "))))
                                        client.send(bytes.fromhex(gen_msgv2(dataS.hex() ,"[1200000002-05]")))
                                        client.send(bytes.fromhex(str(gen_msgv2_clan(dataS.hex() ,"[1200000002-05]"))))
                                    
                                    
                                    


                                    statues= False
                                    

                                    
                                    
                                 #back_spam
                                 
                                if '1200' in dataS.hex()[0:4]:
                                    if b"/ca" in dataS:
                                        ca=True
                                        threading.Thread(target=self.walid , args=(self.data_join,)).start()
                                        client.send(bytes.fromhex(gen_msgv2(dataS.hex() ,"[00FF00][b][c]اللعب الإجباري ")))
                                        client.send(bytes.fromhex(str(gen_msgv2_clan(dataS.hex() ,"[00FF00][b][c]اللعب الإجباري "))))
                                        client.send(bytes.fromhex(gen_msgv2(dataS.hex() ,"[00FF00][b][c]The Foxy Official [FFC800][b][c]Ⓥ")))
                                        client.send(bytes.fromhex(str(gen_msgv2_clan(dataS.hex() ,"[00FF00][b][c]The Foxy Official [FFC800][b][c]Ⓥ"))))

                                    statues= False
                                    

                                   
                                    
                                    #false
                                if '1200' in dataS.hex()[0:4]:
                                    if b"/-ca" in dataS:
                                        ca=False

                                        client.send(bytes.fromhex(gen_msgv2(dataS.hex() ,"[00FF00][b][c]توقفت !")))
                                        client.send(bytes.fromhex(str(gen_msgv2_clan(dataS.hex() ,"[00FF00][b][c]توقفت !"))))
                                        client.send(bytes.fromhex(gen_msgv2(dataS.hex() ,"[00FF00][b][c]The Foxy Official [FFC800][b][c]Ⓥ")))
                                        client.send(bytes.fromhex(str(gen_msgv2_clan(dataS.hex() ,"[00FF00][b][c]The Foxy Official [FFC800][b][c]Ⓥ"))))

                                    statues= False
                                    

                                 #test
                                if '1200' in dataS.hex()[0:4]:
                                    if b"/ca" in dataS:
                                        time.sleep(30.0)
                                        ca=False

                                        client.send(bytes.fromhex(gen_msgv2(dataS.hex() ,"[00FF00][b][c]توقفت تلقائيا ! !")))
                                        client.send(bytes.fromhex(str(gen_msgv2_clan(dataS.hex() ,"[00FF00][b][c]توقفت تلقائيا !!"))))
                                 
                                 #uid


                                if "1200" in dataS.hex()[0:4]:
                        
                                    if b"3sby" in dataS:
                                        print(dataS.hex())
                                        try:
                                            user_id= (bytes.fromhex(re.findall(r'33736279(.*?)28' , dataS.hex()[50:])[0])).decode("utf-8")
                                            print(user_id)
                                            threading.Thread(target=getinfobyid , args=(dataS.hex() , user_id , client)).start()  
                                        except:
                                            pass

                                if  '0500' in dataS.hex()[0:4] and hide == True  :
                                    socktion =client


                                    if len(dataS.hex())<=30:

                                        hide =True
                                    if len(dataS.hex())>=31:
                                        packet = dataS

                                        hide = False

                                 #جلب
                                if '0500' in dataS.hex()[0:4] and len(dataS.hex())>= 1000:
                                    hidr = dataS
                                    cliee = client
                                    print("Catch Packet Sucess !")
                                    print("paket--->",dataS.hex())
                                if '1200' in dataS.hex()[0:4] and '2F77616C6964' in dataS.hex() :
                                    client.send(bytes.fromhex(gen_msgv2(dataS.hex() ,"[00FFFF][b][c] تم سترجاعه للمجموعة !")))
                                    client.send(bytes.fromhex(str(gen_msgv2_clan(dataS.hex() ,"[00FFFF][b][c]تم سترجاعه للمجموعة ! "))))
                                    
                                    client.send(bytes.fromhex(gen_msgv2(dataS.hex() ,"[1200000002-11]")))
                                    client.send(bytes.fromhex(str(gen_msgv2_clan(dataS.hex() ,"[1200000002-11]"))))
                                    
                                    cliee.send(hidr)
                                    print("DONE ! ")




                                if client.send(dataS) <= 0:
                                    break
                                    
                                    
        

                                
        
        
        
    def foxy( self , data_join):
        global back
        print(data_join)
        
        while back==True:
            try:
                self.op.send(data_join)
                time.sleep(9999.0)
               
                #                           0515000000104903408b9e91774e75b990038dddee49
            except Exception as e:
                
                pass
                
    
                
               
    def walid( self , data_join):
        global ca
        print(data_join)
        
        while ca==True:
            try:
                self.op.send(data_join)
                time.sleep(1.0)
                self.op.send(self.data_back)
                #                           0515000000104903408b9e91774e75b990038dddee49
            except Exception as e:
                
                pass
                
                #level UP
    def level_up(self ):
    
        time.sleep(3)
        print("start")
        self.op.send(bytes.fromhex("031500000010091eb74eef39b7574e359602b0670ca8"))
        self.op.send(bytes.fromhex("031500000010091eb74eef39b7574e359602b0670ca8"))
        self.op.send(bytes.fromhex("031500000010091eb74eef39b7574e359602b0670ca8"))
           
        while self.spam_level==True :
            
            
            
            self.op.send(self.start_game)
            

            self.op.send(bytes.fromhex("031500000010091eb74eef39b7574e359602b0670ca8"))
            self.op.send(bytes.fromhex("031500000010091eb74eef39b7574e359602b0670ca8"))
            self.op.send(bytes.fromhex("031500000010091eb74eef39b7574e359602b0670ca8"))
            
            
            time.sleep(3)
            
            #device_low
            
    def foxy_up(self ):
    
        time.sleep(10)
        print("start")
        self.op.send(bytes.fromhex("031500000010091eb74eef39b7574e359602b0670ca8"))
        self.op.send(bytes.fromhex("031500000010091eb74eef39b7574e359602b0670ca8"))
        self.op.send(bytes.fromhex("031500000010091eb74eef39b7574e359602b0670ca8"))
            
        while self.spam_foxy==True :
            
            
            
            self.op.send(self.start_walid)
            

            self.op.send(bytes.fromhex("031500000010091eb74eef39b7574e359602b0670ca8"))
            self.op.send(bytes.fromhex("031500000010091eb74eef39b7574e359602b0670ca8"))
            self.op.send(bytes.fromhex("031500000010091eb74eef39b7574e359602b0670ca8"))
            
            
            time.sleep(10)




def start_bot():
    try :
        Proxy().runs('127.0.0.1',3000)
    except Exception as e:
        sea=2


