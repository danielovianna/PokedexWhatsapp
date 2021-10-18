# Pokedex Whatsapp

A "Pokedex Whatsapp" é um aplicativo que gera um chatbot para whatsapp responsável em ser uma pokeagenda (enciclopédia pokemon). Foi desenvolvido como uma rest API em Python usando FastApi, Twilio, documentação Swagger e consumindo a [pokeapi](https://pokeapi.co).

## Antes de Instalar

Verifique se sua máquina possui o instalador de pacotes [pip](https://pypi.org/help/). É necessário também ter uma conta no [Twilio](https://www.twilio.com/) com sandbox configurada com o endereço gerado com o [ngrok](https://ngrok.com) na máquina para testes local.

Eu fiz o deploy dessa api no [Heroku](https://heroku.com/) no endereço [https://pokedexwhatsapp.herokuapp.com/](https://pokedexwhatsapp.herokuapp.com/) e [https://pokedexwhatsapp.herokuapp.com/docs](https://pokedexwhatsapp.herokuapp.com/docs) para que fique sempre online e funcionando. Mas como a minha conta do Twilio é gratuita, somente os números de telefone que cadastrei na sandbox vão funcionar para testes. Caso queira que eu cadastre o seu número para teste mande uma mensagem pedindo para 21 98442-5722.

## Instalação
Não esqueça de iniciar o seu venv (virtual environment) antes.
```bash
# Instalando todos os requirementos:
pip install -r requeriments.txt

# Iniciando o programa:
uvicorn app:app --reload
```


Você pode verificar no seu browser no endereço http://localhost:8000 e testar pela documentação Swagger gerada em [http://localhost:8000/docs](http://localhost:8000/docs)

## Funcionamento

A API gera um chatbot no whatsapp com o qual você pode interagir. No meu caso, o número fornecido pelo Twilio para o bot é +1 (415) 523-8886. Esse bot tem a tarefa de ser uma enciclopédia pokemon (pokedex) fornecendo dados dos pokemon requisitados. Para usar basta mandar uma mensagem whatsapp para esse número com o nome ou número do pokemon e o programa retornará o uma imagem do pokemon e dados como nome, descrição, tipo, habilidades, habitat e etc. O programa também responde a mensagens básicas como "Hello" e "Thank you".


##### Nota: Toda a programação e comentários foram feitos em inglês.

## Demonstração
Uma rápida demonstração pode ser vista nesse [gif animado](https://drive.google.com/file/d/1aYRS7OrY3YLlSNi4DZRkGWmPdUErNzZm/view) e o funcionamento do aplicativo pode ser vista nesse [video](https://youtu.be/LKEt-0KD3K4).

## Autor
Daniel de Oliveira Vianna
