# -*- coding: utf-8  -*-

fixes['obras'] = {
    'regex': True,
    'msg': {
        '_default':u'([[User:Thales César|Thales]]) Varredura padrão: obras',
    },
    'replacements': [
		### AUXILIARES ###
        (r'\(novel\)', u'(romance)'),
        (r'\(film\)', u'(filme)'),
        (r'\(episode\)', u'(episódio)'),
        (r'\(short story\)', u'(conto)'),
        (r'\bPart\b', u'Parte'),
        #(r'\b\b', u''),
		
		### CÂNON ###
        (r'\bLost Stars\b', u'Estrelas Perdidas'),
        (r'\bAftermath\b', u'Marcas da Guerra'),
        (r'\bMarcas da Guerra: Life Debt\b', u'Marcas da Guerra: Dívida de Honra'),
        (r'\bMarcas da Guerra: Empire\'s End\b', u'Marcas da Guerra: Fim do Império'),
        (r'\bSkywalker Strikes\b', u'Skywalker Ataca'),
        (r'\bMoving Target: A Princess Leia Adventure\b', u'Alvo em Movimento: Uma Aventura da Princesa Leia'),
        (r'\bPrincess Leia\b', u'Princesa Leia'),
        (r'\bThe Weapon of a Jedi: A Luke Skywalker Adventure\b', u'A Arma de um Jedi: Uma Aventura de Luke Skywalker'),
        (r'\bSmuggler\'s Run: A Han Solo & Chewbacca Adventure\b', u'A Missão do Contrabandista: Uma Aventura de Han Solo e Chewbacca'),
        (r'\bA New Dawn\b', u'Um Novo Amanhecer'),
        (r'\bLords of the Sith\b', u'Lordes dos Sith'),
        (r'\bTarkin (novel)\b', u'Tarkin (romance)'),
        (r'\bHeir to the Jedi\b', u'Herdeiro do Jedi'),
        (r'\[\[Bloodline \(romance\)\|Bloodline\]\]', u'[[Legado de Sangue]]'),
        (r'Bloodline \(romance\)', u'Legado de Sangue'),
        (r'\bThe Making of Um Novo Amanhecer\b', u'The Making of A New Dawn'),
        (r'\bShattered Empire\b', u'Império Despedaçado'),
        (r'\bThe Inquisitor\'s Trap\b', u'A Armadilha do Inquisidor'),
        (r'\bStar Wars Rebels: Spark of Rebellion\b', u'Star Wars Rebels: A Fagulha de Uma Rebelião'),
        (r'\bDoctor Aphra ([1-9]): Book I\b', r'Doutora Aphra \1: Livro I'),
        (r'\bDoctor Aphra\b', u'Doutora Aphra'),
        (r'\bStar Wars: Uprising\b', u'Star Wars: A Rebelião'),
        (r'\bBattlefront: Twilight Company\b', u'Battlefront: Companhia do Crepúsculo'),
        (r'\bResistance Reborn\b', u'A Resistência Renasce'),
        #(r'\b\b', u''),
		
		### FILMES ###
        (r'\[\[Star Wars: Episode I The Phantom Menace\|\'\'Star Wars\'\': Episode I \'\'The Phantom Menace\'\'\]\]', u'{{Filme|I}}'),
        (r'\[\[Star Wars: Episode II Attack of the Clones\|\'\'Star Wars\'\': Episode II \'\'Attack of the Clones\'\'\]\]', u'{{Filme|II}}'),
        (r'\[\[Star Wars: Episode III Revenge of the Sith\|\'\'Star Wars\'\': Episode III \'\'Revenge of the Sith\'\'\]\]', u'{{Filme|III}}'),
        (r'\[\[Star Wars: Episode IV A New Hope\|\'\'Star Wars\'\': Episode IV \'\'A New Hope\'\'\]\]', u'{{Filme|IV}}'),
        (r'\[\[Star Wars: Episode V The Empire Strikes Back\|\'\'Star Wars\'\': Episode V \'\'The Empire Strikes Back\'\'\]\]', u'{{Filme|V}}'),
        (r'\[\[Star Wars: Episode VI Return of the Jedi\|\'\'Star Wars\'\': Episode VI \'\'Return of the Jedi\'\'\]\]', u'{{Filme|VI}}'),
        (r'\[\[Star Wars: Episode VII The Force Awakens\|\'\'Star Wars\'\': Episode VII \'\'The Force Awakens\'\'\]\]', u'{{Filme|VII}}'),
        (r'\[\[Rogue One: A Star Wars Story\]\]', u'[[Rogue One: Uma História Star Wars]]'),
        (r'\[\[Star Wars: Episode VIII The Last Jedi\|\'\'Star Wars\'\': Episode VIII \'\'The Last Jedi\'\'\]\]', u'{{Filme|VIII}}'),
        (r'\[\[Star Wars: Episode IX The Rise of Skywalker\|\'\'Star Wars\'\': Episode IX \'\'The Rise of Skywalker\'\'\]\]', u'{{Filme|IX}}'),
        (r'\[\[Solo: A Star Wars Story\]\]', u'[[Han Solo: Uma História Star Wars]]'),
        #(r'\b\b', u''),
		
		### EPISÓDIOS DE TV ###
        (r'Blue Shadow Virus \(episódio\)', u'Blue Shadow Virus'),
        (r'Bounty Hunters \(episódio\)', u'Bounty Hunters'),
        (r'Assassin \(episódio\)', u'Assassin'),
        (r'Altar of Mortis \(episódio\)', u'Altar of Mortis'),
        (r'Bounty \(episódio\)', u'Bounty'),
        (r'Revenge \(episódio\)', u'Revenge'),
        (r'The Gathering \(episódio\)', u'The Gathering'),
        (r'Revival \(episódio\)', u'Revival'),
        (r'Eminence \(episódio\)', u'Eminence'),
        (r'Sabotage \(episódio\)', u'Sabotage'),
        (r'Destiny \(episódio\)', u'Destiny'),
        (r'Empire Day \(episódio\)', u'Empire Day'),
        (r'Idiot\'s Array \(episódio\)', u'Idiot\'s Array'),
        (r'Legacy \(episódio\)', u'Legacy'),
        #(r'\b\b', u''),
		
		### LEGENDS ###
        (r'\bThe Paradise Snare\b', u'A Armadilha do Paraíso'),
        (r'\bDarth Vader and the Cry of Shadows\b', u'Darth Vader: O Clamor das Sombras'),
        #(r'\b\b', u''),
    ]
}

