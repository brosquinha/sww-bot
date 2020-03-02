# Star Wars Wiki bot scripts

Repositório para scripts de automação do BB-08, bot da Star Wars Wiki em Português.

## Instalação

Note que esses scripts foram desenvolvidos com Python 3.6. Versões anteriores do Python, principalmente Python2, não devem funcionar corretamente.

Para instalar esse repositório de scripts do BB-08 na sua máquina, certifique-se de que tenha o git instalado e rode:

```sh
git clone https://github.com/brosquinha/sww-bot.git
cd sww-bot
```

Recomendo utilizar [virtualenv](https://virtualenv.pypa.io/en/latest/) para isolar as dependências desse projeto. Para criar um novo ambiente virtual:

```sh
virtualenv venv
```

Para ativá-lo e instalar as dependências:

```sh
source venv/bin/activate
pip3 install -r requirements.txt
```

## Uso

Para rodar um script do BB-08, basta rodar:

```sh
python3 run.py NOME_DO_SCRIPT
```

Exemplo com o general.py:

```sh
python3 run.py general
```

## TODO

Scripts a serem importados do RPi:

* [X] ~~aparicoes.py~~
* [X] ~~canon.py~~ (renomeado para links_canon.py)
* [ ] eras.py
* [ ] eras_canon.py
* [ ] estatisticas.py
* [X] ~~general.py~~
* [X] ~~icp.py~~
* [ ] legends.py
* [ ] legends_only_pages.py
* [X] ~~linha_do_tempo.py~~
* [X] ~~medalhas.py~~
* [X] ~~remover_predefs.py~~ (renomeado para emuso.py)
* [ ] sam.py
* [ ] temp.py
* [X] ~~traducaoSWW.py~~
* [X] ~~traducoes.py~~
* [ ] troca_padrao_links.py
* [ ] troca_padrao_mover.py
