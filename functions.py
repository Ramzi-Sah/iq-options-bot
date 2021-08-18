def getOpenedBinaryAssets(iq_option_api):
    # get list of all assets
    ALL_Asset = iq_option_api.get_all_open_time()
    
    # filter only binary opened assets
    opened_binary_assets = []
    for type_name, data in ALL_Asset.items():
        for Asset,value in data.items():
            if type_name == "binary" and value["open"]:
                opened_binary_assets.append(Asset)
    
    return opened_binary_assets

def buyMood(iq_option_api, ACTIVES, Money, MoodTreshold):
    # configs
    buy_time = 4 # buy time (before last chance)
    expirations_mode = 1 # api refresh time

    # returned vars
    call_status = False # buy status
    call_id = 0 # buy request id

    # loop until 
    while True:
        remaning_time = iq_option_api.get_remaning(expirations_mode)

        purchase_time = remaning_time-30
        if purchase_time < buy_time:
            # get mood value
            mood = iq_option_api.get_traders_mood(ACTIVES)

            # decide what to do
            ACTION = ""
            if mood >= MoodTreshold:
                ACTION = "call"
            elif mood < 1 - MoodTreshold:
                ACTION = "put"

            # if action decided, buy
            if ACTION != "":
                call_status, call_id = iq_option_api.buy(Money, ACTIVES, ACTION, expirations_mode)

                # if didn't work, add a notice
                msg = ""
                if not call_status:
                    msg = "[WARNING] Action Failed: "
                
                # print status
                print(msg + ACTION + " " + str(Money) + str(iq_option_api.get_currency()) + " on \"" + ACTIVES + "\"" + " |  mood was at " + str(mood) + " Higher.")
            
            break
    
    return call_status, call_id

def watchAssetCall(iq_option_api, assetCallId):
    # will loop until win, returns benefit value
    return iq_option_api.check_win_v3(assetCallId)






############################################################
# optional

def buy(iq_option_api, ACTIVES, Money, ACTION):
    expirations_mode = 1

    print(Money, ACTIVES, ACTION, expirations_mode)
    while True:
        remaning_time = iq_option_api.get_remaning(expirations_mode)
        purchase_time = remaning_time-30
        if purchase_time < 4: # buy the binary option at purchase_time<4
            iq_option_api.buy(Money, ACTIVES, ACTION, expirations_mode)
            break
    print("done.")

def getMood(iq_option_api, goal):
    print("getting mood " + goal)   
    iq_option_api.start_mood_stream(goal)
    mood = iq_option_api.get_traders_mood(goal)
    iq_option_api.stop_mood_stream(goal)
    print(mood)
    return mood

def printAllAssets(iq_option_api):
    ALL_Asset = iq_option_api.get_all_open_time()
    # check if open or not

    ## print(ALL_Asset["forex"]["EURUSD"]["open"]) 
    print(ALL_Asset["cfd"]["FACEBOOK"]["open"])#Stock,Commodities,ETFs
    print(ALL_Asset["crypto"]["BTCUSD-L"]["open"])
    print(ALL_Asset["digital"]["EURUSD-OTC"]["open"])

    ## Binary have two diffenence type:"turbo","binary"
    print(ALL_Asset["turbo"]["EURUSD-OTC"]["open"])
    print(ALL_Asset["binary"]["EURUSD-OTC"]["open"])

    ##!!!! exception ""
    print(ALL_Asset["binary"]["not exist asset"]["open"])#it will return "{}" a None of the dict

    #!!!!print all!!!!
    for type_name, data in ALL_Asset.items():
        for Asset,value in data.items():
            print(type_name, Asset, value["open"])

