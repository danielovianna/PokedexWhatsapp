from fastapi import FastAPI, Form, Response
import requests
from twilio.twiml.messaging_response import MessagingResponse

app = FastAPI()

#search and return all the pokemon data needed in the pokeapi
def get_pokemon_data(pokemon_name_or_number):

    basic_api = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name_or_number}'
    res_basic_api = requests.get(basic_api)
    if(res_basic_api.status_code == 404 or res_basic_api.status_code == 400):
        return 'Invalid Pokemon'

    pokemon_data = res_basic_api.json()
    pokemon = dict()
    pokemon['id'] = pokemon_data['id']
    pokemon['name'] = pokemon_data['species']['name'].capitalize()
    pokemon['image'] = pokemon_data['sprites']['other']['official-artwork']['front_default']
    pokemon['hp'] = pokemon_data['stats'][0]['base_stat']
    pokemon['attack'] = pokemon_data['stats'][1]['base_stat']
    pokemon['defense'] = pokemon_data['stats'][2]['base_stat']
    pokemon['speed'] = pokemon_data['stats'][5]['base_stat']

    #the way the pokeapi saves height and weight is really weird so this is necessary to make it look good
    pokemon['height'] = str(pokemon_data['height'])[:-1] + ',' + str(pokemon_data['height'])[-1:] + 'm'
    pokemon['weight'] = str(pokemon_data['weight'])[:-1] + ',' + str(pokemon_data['weight'])[-1:] + 'Kg'
    if(pokemon['height'][:1] == ','):
        pokemon['height'] = '0' + pokemon['height']
    if(pokemon['weight'][:1] == ','):
        pokemon['weight'] = '0' + pokemon['weight']

    #getting the pokemon types and special abilities
    pokemon['type'] = ''
    for i in pokemon_data['types']:
        pokemon['type'] += i['type']['name'].capitalize() + ' '
    pokemon['ability'] = ''
    for i in pokemon_data['abilities']:
        pokemon['ability'] += i['ability']['name'].title() + ', '
    pokemon['ability'] = pokemon['ability'][:-2]

    #getting and formatting the description and habitat
    species_api = pokemon_data['species']['url']
    res_species_api = requests.get(species_api)
    species_data = res_species_api.json()
    pokemon['description'] = species_data['flavor_text_entries'][1]['flavor_text']
    pokemon['description'] = pokemon['description'].replace('\n',' ')
    pokemon['description'] = pokemon['description'].replace('\x0c',' ')
    pokemon['description'] = pokemon['description'].replace('\r','')
    pokemon['description'] = pokemon['description'].replace('\f','')
    pokemon['description'] = pokemon['description'].replace('\t','')
    if (species_data['habitat'] is None): 
        pokemon['habitat'] = 'Unknown'
    elif(species_data['habitat']['name'] == 'rare'):
        pokemon['habitat'] = species_data['pal_park_encounters'][0]['area']['name'].title() + f' ({species_data["habitat"]["name"]})'
    else:
        pokemon['habitat'] = species_data['habitat']['name'].title()

    return pokemon

@app.get('/')
async def root():
    return 'Welcome to the Pokedex!'

@app.post('/pokedex')
async def pokedex(Body: str = Form(...)):
    response = MessagingResponse() 
    incoming_msg = Body.lower().strip()
    outcoming_msg = response.message()

    if 'hello' in incoming_msg or 'test' in incoming_msg:
        text = 'Hello! Welcome to the Pokedex.\nPlease type a pokemon name or number:'
    elif 'thank' in incoming_msg:
        text = "You are welcome! Thank you for using the Pokedex. And don't forget:\n *_Gotta Catch 'Em All!_*"
    else:  
        pokemon = get_pokemon_data(incoming_msg)
        if (pokemon == 'Invalid Pokemon'):
            text = "Sorry! We didn't find this pokemon in the Pokedex Database. Please try again."
        else:
            outcoming_msg.media(pokemon['image'])
            text = f'ID #{pokemon["id"]}  *{pokemon["name"]}*\n'
            text+= f'Type: {pokemon["type"]}\n'
            text+= f'_"{pokemon["description"]}"_\n'
            text+= f'Height: {pokemon["height"]}\n'
            text+= f'Weight: {pokemon["weight"]}\n'
            text+= f'Habitat: {pokemon["habitat"]}\n'
            text+= f'Abilities: {pokemon["ability"]}\n'
            text+= f'Base Stats:\nHP          {pokemon["hp"]}\nSpeed    {pokemon["speed"]}\nAttack    {pokemon["attack"]}\nDefense {pokemon["defense"]}'
        
    outcoming_msg.body(text)
    return Response(content=str(response), media_type="application/xml")