import json
import requests
import threading

class ApiData(object):
    def __init__(self, data):
	    self.__dict__ = json.loads(data)

average_failure = []

#perform checks
def check_notice():
    total = sum(average_failure)
    count = len(average_failure)
    if(count == 10):
        average_failure.clear()
    else:
        if (total/count > 30):
            print("High Traffic") #print notice could be refactored to do email instead
    
#function that makes api call every 5 minutes using Threading
def api_call():
    #Set thread for 5 minutes
    threading.Timer(300.0, api_call).start()
    #Make API get call
    response = requests.get('https://traf.nibss-plc.com.ng:7443/traf/ajax?command=website&action=detail&order=loadPOS&clientCode=NIBSS&txnSubCat=ALL')
    response = response.text
    #Deserialize Json to python object
    obj = ApiData(response).msg
    #Get property we are interested in
    val = obj['todayFailureRateOutward'][:-1]
    #Add to an Array for each call.
    average_failure.append(float(val))
    #Call method to check if traffic is high
    check_notice()

if __name__ == "__main__":
    #Program begins here
    api_call()

