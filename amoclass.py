import requests
import json
import time

class AMO:
    def __init__(self, amo_info):
        refresh_array = open("refresh.txt").read()
        refresh_array = refresh_array.split("x-amo-checker-info-amo;;;")
        refresh_time = refresh_array[0]
        self.amo_info = amo_info
        if float(refresh_time) > time.time():
            access_token = refresh_array[1]
        else:
            refresh_token = refresh_array[2]
            link = "https://" + amo_info['subdomain'] + ".amocrm.ru/oauth2/access_token"
            data = {
                'client_id': amo_info['client_id'],
                'client_secret': amo_info['client_secret'],
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token,
                'redirect_url': amo_info['redirect_url']
            }
            headers = {
                'User-Agent': 'amoCRM-oAuth-client/1.0',
                'Content-Type': 'application/json'
            }
            response = requests.post(link, data=json.dumps(data), headers=headers)
            response_data = response.json()
            access_token = response_data['access_token']
            refresh_token = response_data['refresh_token']
            expires_in = response_data['expires_in']
            info = str(time.time()) + str(expires_in) + "x-amo-checker-info-amo;;;" + access_token + "x-amo-checker-info-amo;;;" + refresh_token

            with open("refresh.txt", "w") as f:
                f.write(info)
        self.access_token = access_token

    def get_contact_info(self, query):
        method = "contacts"
        query = query.replace(" ", "")
        query = query.replace("(", "")
        query = query.replace(")", "")
        query = query.replace("-", "")
        request = self.get_request(method + '/?query=','')
        if request != 0:
            request = request['_embedded']['contacts']
            answer = request[0]['id']
        else:
            if query[0] == 8:
                query = 7
                request = self.get_request('?query=','') 
                if request != 0:
                    request = request['_embedded']['contacts']
                    answer = request[0]['id']
                else:
                    answer = 0
            elif query[0] == 7:
                query = 8
                request = self.get_request('?query=','') 
                if request != 0:
                    request = request['_embedded']['contacts']
                    answer = request[0]['id']
                else:
                    answer = 0
            time.sleep(1)
            return answer
    
    def get_request(self, method, query):
        link = "https://" + self.amo_info['subdomain'] + ".amocrm.ru/api/v4/" + method + query
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'User-Agent': 'amoCRM-oAuth-client/1.0'
        }

        try:
            response = requests.get(link, headers=headers)
            response.raise_for_status()
            data = response.json()

            if '_embedded' in data and method in data['_embedded']:
                return data['_embedded'][method]
            else:
                return data

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None
    
    def add_field(self, field, value, type, array):
        if array is None:
            array = [
            {
                field: value,
            },
        ]
        else:
            array[0][field] = value
        return array
    
    def add_tags(self, array, value):
        tags_array = {
            'name' : value
        }
        array[0]['_embedded']['tags'].append(tags_array)
        return array
    
    def add_customs(self, array, field, value, type, enum):
        if enum is None:
            custom_array = {
                'field_id' : field,
                'values' : [
                    {
                        'value' : value
                    }
                ]}
        else:
            custom_array = {
                'field_id': field,
                'values': [
                    {
                        'value': value,
                        'enum_id': enum,
                    }
                ]
            }
        array[0]['custom_fields_values'].append(custom_array)
        return array        
    
    def post_request(self, array, method, method_request=None):
        if method_request is None:
            method_request = "POST"
        
        url = "https://" + self.amo_info['subdomain'] + ".amocrm.ru/api/v4/" + method
        headers = {
            "Authorization": "Bearer " + self.access_token,
            "Content-Type": "application/json"
        }
        
        response = requests.request(method_request, url, headers=headers, json=array)
        response_json = response.json()

        if '_embedded' in response_json and method in response_json['_embedded']:
            return response_json['_embedded'][method][0]['id']
        else:
            return response_json
        