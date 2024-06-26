from config import *
from amoclass import *

array = [
    {
        "name": "zxcqwe123",
        "created_by": 0,
        "price": 20000,
        "custom_fields_values": [
            {
                "field_id": 1538091,
                "values": [
                    {
                        "value": "Наш первый клиент"
                    }
                ]
            }
        ]
    }
]

tags_array = [
    {
        "id": 7887833,
        "_embedded": {
            "tags": [
                {
                    "name": "Тег 1" 
                }
            ]
        }
    },
    {
        "id": 7887833,
        "_embedded": {
            "tags": [
                {
                    "name": "Тег 2"
                }
            ]
        }
    }
]

array1 = {
        "id": 8168973,
        "pipeline_id": 7941858,
        "status_id": 141,
        "tags_to_add": [
            {
                "name": "Первый тег"
            }
        ],
        "_embedded": {
         "contacts":[
            {
               "first_name":"Пиджак",
               "custom_fields_values":[
                  {
                     "field_id":1538079,
                     "values":[
                        {
                           "value":"example"
                        }
                     ]
                  }
               ]
            }
         ]
    }
}

array2 = [{
      "name": "Название сделкиklll",
      "price": 10000,
      "tags_to_add": [
            {
                "name": 'pudge'
            }
        ],
      "_embedded": {
         "contacts":[
            {
               "first_name":"Пиджак",
               "custom_fields_values":[
                  {
                     "field_id":1538079,
                     "values":[
                        {
                           "value":"example"
                        }
                     ]
                  }
               ]
            }
         ],
         "companies":[
            {
               "name":"ООО Рога и Копыта"
            }
         ],
      }
   }]

leadtag = '/8168973'

# print(AMO(AMOINFO).get_request('leads/pipelines' + leadtag,''))    
# print(AMO(AMOINFO).add_tags(tags_array,leadtag))    
# AMO(AMOINFO)
#print(AMO(AMOINFO).post_request(array1,f'leads{leadtag}','PATCH'))
# print(AMO(AMOINFO).get_contact_info('+79999999999'))
print(AMO(AMOINFO).post_request(array2,'leads/complex'), 'POST')