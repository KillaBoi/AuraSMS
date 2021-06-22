###############################################
##   AuraSMS Wrapper for OzekiNG SMS Gateway ##
###############################################

import urllib.parse as urllib
import urllib.request as urllib_request
from bs4 import BeautifulSoup
import time
from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime


###############################################
###          Ozeki NG Authentication        ###
###############################################
loop = True
while loop == True:

    host = ""
    user_name = ""
    user_password = ""
    folder = ""
    after_download = ""

###############################################
###       HTTP Request to obtain SMS        ###
###############################################

    http_req = host
    http_req += "api?action=receivemessage&username="
    http_req += urllib.quote(user_name)
    http_req += "&password="
    http_req += urllib.quote(user_password)
    http_req += "&folder="
    http_req += urllib.quote(folder)
    http_req += "&afterdownload="
    http_req += urllib.quote(after_download)

################################################
###               Check for SMS              ###
################################################
    get = urllib_request.urlopen(http_req)
    req = get.read()
    y = BeautifulSoup(req, features="lxml")
    get.close()

################################################
###           Prepare Variables UwU          ###
################################################

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    time_string = now.strftime("%H:%M:%S")
    aura_response = y.response
    aura_action = y.response.action.text
    aura_data = aura_response.data
    try:
        aura_messageid = aura_data.messageid.text
        aura_originator = aura_data.originator.text
        aura_recipient = aura_data.recipient.text
        aura_messagetype = aura_data.messagetype.text
        aura_messagedata = aura_data.messagedata.text
        aura_senttime = aura_data.senttime.text
        aura_receivedtime = aura_data.receivedtime.text
    except AttributeError as x:
        print("[AURA] - " + str(time_string) + " - Checking for SMSs")
        time.sleep(3)

################################################
###            Verifying the response        ###
################################################
# if aura_action == "receivemessage":
###        print("[ACTION] AURA_RECEIVE_SMS")
# elif aura_action == "sendmessage":
###        print("[ACTION] AURA_SEND_SMS")
# else:
###        print("[ACTION] AURA_UNKNOWN_ACTION")
################################################

    try:
        if aura_originator is None:
            print("[AURA] - " + str(time_string) + " - No New SMSs Found")
            time.sleep(3)
        else:
            print("-"*10)
            print("[AURA] - " + str(time_string) + " - SMS Received From: " + str(aura_originator))
            print("[AURA] - " + str(time_string) + " - SMS Message Type: " + str(aura_messagetype))
            print("[AURA] - " + str(time_string) + " - SMS Contents: " + str(aura_messagedata))
            print("[AURA] - " + str(time_string) + " - SMS Received Time: " + str(aura_receivedtime))
            print("-"*10)
            print("\n")
            webhook = DiscordWebhook(
                url='')
            embed = DiscordEmbed(
                title='New SMS Detected', color='03b2f8')
            embed.set_footer(text='Aura v1.1.3 ')
            embed.set_timestamp()
            embed.add_embed_field(name='SMS Received From',
                                  value=str(aura_originator))
            embed.add_embed_field(name='SMS Contents',
                                  value=str(aura_messagedata))
            webhook.add_embed(embed)
            response = webhook.execute()
            aura_messageid = None
            aura_originator = None
            aura_recipient = None
            aura_messagetype = None
            aura_messagedata = None
            aura_senttime = None
            aura_receivedtime = None
            time.sleep(1)
    except:
        print("[AURA] - " + str(time_string) + " - No New SMSs Found")
        time.sleep(3)
