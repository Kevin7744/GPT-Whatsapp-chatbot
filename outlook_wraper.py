import requests
from datetime import datetime, timedelta
from config import Config

class OutlookWraper:
    def __init__(self):
        self.create_event_url = Config.CREATE_OUTLOOK_EVENT_MAKE_URL
        self.recurrent_event_url = Config.CREATE_RECURING_OUTLOOK_EVENT_MAKE_URL
    
    
    def create_event(self, name, start, end):
        resp = requests.get(self.create_event_url, 
                            data = {
                                'name': name, 
                                'start_datetime': start, 
                                'end_datetime': end
                            })

        return resp.status_code == 200
        
    
    def create_recurring_event(self, name, days_of_week, start_time, end_time, start_date, end_date, num_occurences):
        #event that repeats every week
        resp = requests.get(self.recurrent_event_url, 
                            data = {
                                'name': name, 
                                'days_of_week': days_of_week, 
                                'start_time': start_time, 
                                'end_time': end_time, 
                                'start_date': start_date,
                                'end_date': end_date, 
                                'num_occurences': num_occurences
                            })

        return resp.status_code == 200




if __name__ == '__main__':
    wraper = OutlookWraper()
    now = datetime.now()
    end = datetime.now() + timedelta(hours = 1)
    # wraper.create_event('', '', '')
    
    wraper.create_recurring_event('test', '["thursday"]', '11:00:00', '14:00:00', '24/03/2024', '28/04/2024', 4)