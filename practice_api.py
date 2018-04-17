import requests, json

app_id = "be77c0cb"
app_key = "bf29b57815ffe51f465ca7069db9135c"
base_url="https://od-api.oxforddictionaries.com/api/v1/entries/en/"

def oxford_dict_request(app_id, app_key, base_url, word_id):
    base_url = base_url + word_id.lower()
    data = requests.get(base_url, headers={'app_id': app_id, 'app_key':app_key})
    return data.json()['results'][0]

#sample word queries
programming_dict = oxford_dict_request(app_id, app_key, base_url, "programming")
cool_dict = oxford_dict_request(app_id, app_key, base_url, "cool")
bark_dict = oxford_dict_request(app_id, app_key, base_url, "bark")

#ex of me using the data, using the programming word inforamtion dictionary:
word = programming_dict['word']
language = programming_dict['language']
phonetic_spelling = programming_dict['lexicalEntries'][0]['pronunciations'][0]['phoneticSpelling']
definitions = programming_dict['lexicalEntries'][0]['entries'][0]['senses']
definition_list = []
for d in definitions:
    definition_list.append(d['definitions'])

#this data will be used in my application to populate the contents of the different models in my database, for the Word, Definition, and PartOfSpeech models. Then this information will be displayed and populated in different ways throughout the app.

#based on a user's input to a form, this function will be invoked to get a dictionary of information about the user's entered word.
