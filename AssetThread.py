import threading
import functions

class AssetThread (threading.Thread):
    def __init__(self, iq_option_api, asset):
        # init thread
        threading.Thread.__init__(self)

        # init thread attributes
        self.iq_option_api = iq_option_api
        self.asset = asset

    def run(self):
        # handle thread errors
        try:
            # start monitoring asset mood
            self.iq_option_api.start_mood_stream(self.asset)

            print("asset \"" + self.asset + "\" thread started.")

            # main thread loop
            while True:
                    # check mood and call or put
                    call_status, call_id = functions.buyMood(self.iq_option_api, self.asset, 1, 0.8) # never put lower then 0.51

                    # watch call status
                    benefits = 0
                    if call_status:
                        benefits = functions.watchAssetCall(self.iq_option_api, call_id)
                    
        except Exception as e:
            print("[ERROR] Thread \"" + self.asset + "\": " + str(e))
