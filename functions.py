import requests
from config import Config

config_instance = Config()
MAKE_URL = config_instance.MAKE_URL

config_instance = Config()
MAKE_URL = config_instance.MAKE_URL

# def save_answers(full_name, phone, email, street_name, zip_code, city,
#                  service_type, 
#                  ot1, ot2, ot3, ot4, ot5,  # responses for one-time cleaning -> 
#                  rc1, rc2, rc3, rc4, rc5,  # responses for regular cleaning
#                  pc1, pc2, pc3, pc4, pc5, pc6,  # responses for post-construction cleaning
#                  ww1, ww2, ww3, ww4, ww5,  # responses for window washing
#                  cc1, cc2, cc3, cc4,  # responses for carpet cleaning
#                  sc1, sc2, sc3, sc4  # responses for sofa cleaning
#                  ):
#     """
#     Saves the answers provided by the user for various cleaning service requests.

#     "full_name": {"type": "string", "description": "Full name of the user."},
#     "phone": {"type": "string", "description": "Phone number of the user."},
#     "email": {"type": "string", "description": "Email address of the user."},
#     "street_name": {"type": "string", "description": "Street name of the user's address."},
#     "zip_code": {"type": "string", "description": "Zip code of the user's location."},
#     "city": {"type": "string", "description": "City of the user's residence."},
#     "service_type": {"type": "string", "description": "Type of cleaning service, one of: 'One-time cleaning', 'Regular cleaning', 'Post-construction cleaning', 'Window washing', 'Carpet Cleaning', 'Sofa Cleaning'"},
#     "ot1": {"type": "string", "description": "Response for one-time cleaning question: 'Which standard cleaning tasks do you require? (required to have an answer)"},
#     "ot2": {"type": "string", "description": "Response for one-time cleaning question: 'What is the total square footage (m²) of the space that needs to be cleaned? (required to have an answer)'"},
#     "ot3": {"type": "string", "description": "Response for one-time cleaning question: 'Are there specific spots or details that need extra attention?'"},
#     "ot4": {"type": "string", "description": "Response for one-time cleaning question: 'Are there specific cleaning products we should use, for instance, for a certain type of floor?'"},
#     "ot5": {"type": "string", "description": "Response for one-time cleaning question: 'Do you also wish the windows to be washed?'"},
#     "rc1": {"type": "string", "description": "Response for regular cleaning question 1: 'Desired cleaning frequency (required to have an answer)'"},
#     "rc2": {"type": "string", "description": "Response for regular cleaning question 2: 'How often per week do you want cleaning to be done? (required to have an answer)'"},
#     "rc3": {"type": "string", "description": "Response for regular cleaning question 3: 'What is the total square footage (m²) of the space that needs to be cleaned? (required to have an answer)'"},
#     "rc4": {"type": "string", "description": "Response for regular cleaning question 4: 'What standard cleaning tasks do you expect from us?'"},
#     "rc5": {"type": "string", "description": "Response for regular cleaning question 5: 'Are there specific focus points or additional tasks you want to be executed?'"},
#     "pc1": {"type": "string", "description": "Response for post-construction cleaning question 1: 'Which standard cleaning tasks do you require?'"},
#     "pc2": {"type": "string", "description": "Response for post-construction cleaning question 2: 'What is the current condition of the spaces?'"},
#     "pc3": {"type": "string", "description": "Response for post-construction cleaning question 3: 'Are there specific spots or details that need extra attention?'"},
#     "pc4": {"type": "string", "description": "Response for post-construction cleaning question 4: 'What is the total square footage (m²) of the space that needs to be cleaned? (required to have an answer)'"},
#     "pc5": {"type": "string", "description": "Response for post-construction cleaning question 5: 'Are there specific cleaning products we should use, for instance, for a certain type of floor?'"},
#     "pc6": {"type": "string", "description": "Response for post-construction cleaning question 6: 'Are there any traces of cement grout haze?'"},
#     "ww1": {"type": "string", "description": "Response for window washing question 1: 'What is the total square footage (m²) of the space that needs to be cleaned? (required to have an answer)'"},
#     "ww2": {"type": "string", "description": "Response for window washing question 2: 'How many windows approximately need to be washed?'"},
#     "ww3": {"type": "string", "description": "Response for window washing question 3: 'How dirty are the windows currently?'"},
#     "ww4": {"type": "string", "description": "Response for window washing question 4: 'Are they mostly large or small windows?'"},
#     "ww5": {"type": "string", "description": "Response for window washing question 5: 'Are there specific cleaning products we should use for the windows?'"},
#     "cc1": {"type": "string", "description": "Response for carpet cleaning question 1: 'What is the width of the carpet you want to be cleaned? (in meters) (required to have an answer)'"},
#     "cc2": {"type": "string", "description": "Response for carpet cleaning question 2: 'What is the length of the carpet you want to be cleaned? (in meters) (required to have an answer)'"},
#     "cc3": {"type": "string", "description": "Response for carpet cleaning question 3: 'If you wish to have multiple carpets cleaned, please specify the total number of carpets to be cleaned here.'"},
#     "cc4": {"type": "string", "description": "Response for carpet cleaning question 4: 'If you have multiple carpets with different dimensions that need cleaning, please specify the dimensions of each carpet here.'"},
#     "sc1": {"type": "string", "description": "Response for sofa cleaning question 1: 'How many sofas do you want to be cleaned? (required to have an answer)'"},
#     "sc2": {"type": "string", "description": "Response for sofa cleaning question 2: 'How many seating places do the sofa(s) you want to be cleaned have? (required to have an answer)'"},
#     "sc3": {"type": "string", "description": "Response for sofa cleaning question 3: 'If you have multiple sofas with different seating arrangements to be cleaned, please specify the details of each sofa here.'"},
#     "sc4": {"type": "string", "description": "Response for sofa cleaning question 4: 'Is it a corner sofa?'"}

#     """

#     resp = requests.get(MAKE_URL, data={
#         'full_name': full_name,
#         'street_name': street_name,
#         'zip_code': zip_code,
#         'phone': phone,
#         'email': email,
#         'city': city,
#         'service_type': service_type, 
#         'ot1': ot1,
#         'ot2': ot2,
#         'ot3': ot3,
#         'ot4': ot4,
#         'ot5': ot5,
#         'rc1': rc1,
#         'rc2': rc2,
#         'rc3': rc3,
#         'rc4': rc4,
#         'rc5': rc5,
#         'pc1': pc1,
#         'pc2': pc2,
#         'pc3': pc3,
#         'pc4': pc4,
#         'pc5': pc5,
#         'pc6': pc6,
#         'ww1': ww1,
#         'ww2': ww2,
#         'ww3': ww3,
#         'ww4': ww4,
#         'ww5': ww5,
#         'cc1': cc1,
#         'cc2': cc2,
#         'cc3': cc3,
#         'cc4': cc4,
#         'sc1': sc1,
#         'sc2': sc2,
#         'sc3': sc3,
#         'sc4': sc4
#     })

#     if resp.ok:
#         print('Saved answers successfully')
#         return resp.text
#     else:
#         print('Failed to save responses')
#         return ''

def save_answers(full_name, phone, email, street_name, zip_code, city, service_type, **kwargs):
    """
    Saves the answers provided by the user for various cleaning service requests.

    "full_name": {"type": "string", "description": "Full name of the user."},
    "phone": {"type": "string", "description": "Phone number of the user."},
    "email": {"type": "string", "description": "Email address of the user."},
    "street_name": {"type": "string", "description": "Street name of the user's address."},
    "zip_code": {"type": "string", "description": "Zip code of the user's location."},
    "city": {"type": "string", "description": "City of the user's residence."},
    "service_type": {"type": "string", "description": "Type of cleaning service, one of: 'One-time cleaning', 'Regular cleaning', 'Post-construction cleaning', 'Window washing', 'Carpet Cleaning', 'Sofa Cleaning'"},
    """
    resp = requests.get(MAKE_URL, data={
        'full_name': full_name,
        'street_name': street_name,
        'zip_code': zip_code,
        'phone': phone,
        'email': email,
        'city': city,
        'service_type': service_type,
        **kwargs
    })

    if resp.ok:
        print('Saved answers successfully')
        return resp.text
    else:
        print('Failed to save responses')
        return ''