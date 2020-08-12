import time
import hmac
import base64
import json
import requests
import hashlib

def symptomClassifierFunc(symptomInput):
    #GET TOKEN TO AUTHORIZE OTHER CALL
    api_key = "ashwin.agnihotri@gmail.com"
    auth_url = "https://sandbox-authservice.priaid.ch/login"
    secret_key = "b7K6Qfe8E2Rcw5S9M"
    secret_key_bytes = secret_key.encode('utf-8')
    hmac_key = hmac.new(secret_key_bytes, msg=None, digestmod=hashlib.md5) 
    url_bytes = auth_url.encode('utf-8')
    hmac_key.update(url_bytes)
    comp_hash = hmac_key.digest()
    hashed_credentials = base64.b64encode(comp_hash)
    hashed_credentials = hashed_credentials.decode('utf-8')
    auth_parameters = {"api_key": api_key,
                       "secret_key": secret_key,
                       "hashed_credentials": hashed_credentials}

    auth_response = requests.post(auth_url,
                                  headers = {"Authorization":
                                             "Bearer " + api_key + ":" + hashed_credentials})
    output = auth_response.content.decode('utf-8')
    token_dict = json.loads(output)
    token = token_dict["Token"]

    ###
    #Input from users (via buttons)
    patient_gender = "male"
    birth_year = 1988
    #For each button clicked, append that symptom to list
    symptoms_input = symptomInput

    symptom_table = {}
    symptom_mappings = [{'ID': 10, 'Name': 'Abdominal pain'}, {'ID': 238, 'Name': 'Anxiety'}, {'ID': 104, 'Name': 'Back pain'}, {'ID': 75, 'Name': 'Burning eyes'}, {'ID': 46, 'Name': 'Burning in the throat'}, {'ID': 170, 'Name': 'Cheek swelling'}, {'ID': 17, 'Name': 'Chest pain'}, {'ID': 31, 'Name': 'Chest tightness'}, {'ID': 175, 'Name': 'Chills'}, {'ID': 139, 'Name': 'Cold sweats'}, {'ID': 15, 'Name': 'Cough'}, {'ID': 207, 'Name': 'Dizziness'}, {'ID': 244, 'Name': 'Drooping eyelid'}, {'ID': 273, 'Name': 'Dry eyes'}, {'ID': 87, 'Name': 'Earache'}, {'ID': 92, 'Name': 'Early satiety'}, {'ID': 287, 'Name': 'Eye pain'}, {'ID': 33, 'Name': 'Eye redness'}, {'ID': 153, 'Name': 'Fast, deepened breathing'}, {'ID': 76, 'Name': 'Feeling of foreign body in the eye'}, {'ID': 11, 'Name': 'Fever'}, {'ID': 57, 'Name': 'Going black before the eyes'}, {'ID': 9, 'Name': 'Headache'}, {'ID': 45, 'Name': 'Heartburn'}, {'ID': 122, 'Name': 'Hiccups'}, {'ID': 149, 'Name': 'Hot flushes'}, {'ID': 40, 'Name': 'Increased thirst'}, {'ID': 73, 'Name': 'Itching eyes'}, {'ID': 96, 'Name': 'Itching in the nose'}, {'ID': 35, 'Name': 'Lip swelling'}, {'ID': 235, 'Name': 'Memory gap'}, {'ID': 112, 'Name': 'Menstruation disorder'}, {'ID': 123, 'Name': 'Missed period'}, {'ID': 44, 'Name': 'Nausea'}, {'ID': 136, 'Name': 'Neck pain'}, {'ID': 114, 'Name': 'Nervousness'}, {'ID': 133, 'Name': 'Night cough'}, {'ID': 12, 'Name': 'Pain in the limbs'}, {'ID': 203, 'Name': 'Pain on swallowing'}, {'ID': 37, 'Name': 'Palpitations'}, {'ID': 140, 'Name': 'Paralysis'}, {'ID': 54, 'Name': 'Reduced appetite'}, {'ID': 14, 'Name': 'Runny nose'}, {'ID': 29, 'Name': 'Shortness of breath'}, {'ID': 124, 'Name': 'Skin rash'}, {'ID': 52, 'Name': 'Sleeplessness'}, {'ID': 95, 'Name': 'Sneezing'}, {'ID': 13, 'Name': 'Sore throat'}, {'ID': 64, 'Name': 'Sputum'}, {'ID': 179, 'Name': 'Stomach burning'}, {'ID': 28, 'Name': 'Stuffy nose'}, {'ID': 138, 'Name': 'Sweating'}, {'ID': 248, 'Name': 'Swollen glands in the armpits'}, {'ID': 169, 'Name': 'Swollen glands on the neck'}, {'ID': 211, 'Name': 'Tears'}, {'ID': 16, 'Name': 'Tiredness'}, {'ID': 115, 'Name': 'Tremor at rest'}, {'ID': 144, 'Name': 'Unconsciousness, short'}, {'ID': 101, 'Name': 'Vomiting'}, {'ID': 181, 'Name': 'Vomiting blood'}, {'ID': 56, 'Name': 'weakness'}, {'ID': 23, 'Name': 'Weight gain'}, {'ID': 30, 'Name': 'Wheezing'}]
    for symptom in symptom_mappings:
        symptom_table[symptom['Name']] = symptom['ID']

    symptom_ids = []
    for symptom in symptoms_input:
        if symptom in symptom_table:
            symptom_ids.append(symptom_table[symptom])

    parameters = {"token": token, "symptoms" : json.dumps(symptom_ids), 
                  "gender": patient_gender, "year_of_birth": birth_year, "language": "en-gb"}
    url = "https://sandbox-healthservice.priaid.ch/diagnosis"
    diagnoses = requests.get(url, params=parameters)
    diagnoses_str = diagnoses.content.decode('utf-8')
    diagnoses_json = json.loads(diagnoses_str)
    diag_dict = {}
    for i in range(len(diagnoses_json)):
        if diagnoses_json[i]['Issue']['Accuracy'] < 50:
            break
        specialist_string = ""
        for spec in diagnoses_json[i]['Specialisation']:
            specialist_string = specialist_string + spec['Name'] + ", "
        if len(specialist_string) >= 2:
            specialist_string = specialist_string[:-2]
        diag_dict[i] = {'Name': diagnoses_json[i]['Issue']['Name'],
                        'Professional Name': diagnoses_json[i]['Issue']['ProfName'],
                        'Confidence': "{:.1%}".format(diagnoses_json[i]['Issue']['Accuracy']/100),
                        'Specialists': specialist_string}

    #CHECK FOR RED FLAGS
    red_flag_url = "https://sandbox-healthservice.priaid.ch/redflag"
    red_flag_params = {"token": token, "symptomId": 0, "language": "en-gb"}
    warnings = 0
    for symptom in symptom_ids:
        red_flag_params["symptomId"] = symptom
        warning = requests.get(red_flag_url, params=red_flag_params)
        warning_str = warning.content.decode('utf-8')
        if len(warning_str) > 2:
            warnings += 1

    if len(diagnoses_json) > 0:
        main_diagnosis = diag_dict[0]
        return diagnoses_json, main_diagnosis, warnings
    else:
        return [], None, warnings

#FINAL OUTPUT VARIABLES
#Warnings variable has number of warnings: >0 means emergency
#diag_dict has the patient's diagnoses w/ specialists (>50% confidence)
#main_diagnosis has the patient's top diagnosis (for schedule display purposes)
    