import requests
import config

MAKE_URL = config.MAKE_URL


def save_answers(full_name, phone, email, street_name, zip_code, city,
                 service_type, 
                 ot1, ot2, ot3, ot4, ot5,  # responses for one-time cleaning
                 rc1, rc2, rc3, rc4, rc5,  # responses for regular cleaning
                 pc1, pc2, pc3, pc4, pc5, pc6,  # responses for post-construction cleaning
                 ww1, ww2, ww3, ww4, ww5,  # responses for window washing
                 cc1, cc2, cc3, cc4,  # responses for carpet cleaning
                 sc1, sc2, sc3, sc4  # responses for sofa cleaning
                 ):
    """
    Saves the answers provided by the user for various cleaning service requests.

    Parameters:
    - full_name: User's full name
    - phone: User's phone number
    - email: User's email address
    - street_name: Street name of the service location
    - zip_code: Zip code of the service location
    - city: City of the service location
    - service_type: Type of cleaning service requested (e.g., one-time, regular, post-construction)
    - ot1 to ot5: Responses to one-time cleaning questions
    - rc1 to rc5: Responses to regular cleaning questions
    - pc1 to pc6: Responses to post-construction cleaning questions, including:
        - pc1: Standard cleaning tasks required
        - pc2: Current condition of the spaces ('good', 'average', 'poor')
        - pc3: Specific spots needing extra attention ('at the center and corners')
        - pc4: Total square footage (e.g., '400 m²')
        - pc5: Specific cleaning products to use ('omo and extra soap')
        - pc6: Presence of cement grout haze ('yes' or 'no')
    - ww1 to ww5: Responses to window washing questions
    - cc1 to cc4: Responses to carpet cleaning questions
    - sc1 to sc4: Responses to sofa cleaning questions
    """

    resp = requests.get(MAKE_URL, data={
        'full_name': full_name,
        'street_name': street_name,
        'zip_code': zip_code,
        'phone': phone,
        'email': email,
        'city': city,
        'service_type': service_type, 
        'ot1': ot1,
        'ot2': ot2,
        'ot3': ot3,
        'ot4': ot4,
        'ot5': ot5,
        'rc1': rc1,
        'rc2': rc2,
        'rc3': rc3,
        'rc4': rc4,
        'rc5': rc5,
        'pc1': pc1,
        'pc2': pc2,
        'pc3': pc3,
        'pc4': pc4,
        'pc5': pc5,
        'pc6': pc6,
        'ww1': ww1,
        'ww2': ww2,
        'ww3': ww3,
        'ww4': ww4,
        'ww5': ww5,
        'cc1': cc1,
        'cc2': cc2,
        'cc3': cc3,
        'cc4': cc4,
        'sc1': sc1,
        'sc2': sc2,
        'sc3': sc3,
        'sc4': sc4
    })

    if resp.ok:
        print('Saved answers successfully')
        return resp.text
    else:
        print('Failed to save responses')
        return ''