from pyiqoptionapi import IQOption
import functions, AssetThread

# login to iqoption API
iq_option_api = IQOption("mail", "pass")
iq_option_api.connect()
print('current blance is: ' + str(iq_option_api.get_balance()) + ' ' + str(iq_option_api.get_currency()))

# get all opened binary assets
assets = functions.getOpenedBinaryAssets(iq_option_api)

# start all assets threads
for asset in assets:
    m = AssetThread.AssetThread(iq_option_api, asset)
    m.start()
