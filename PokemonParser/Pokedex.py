import json


class Pokedex:
    languages = ['de', 'en']

    def __init__(self):
        self.pokedex = {}
        for lang in Pokedex.languages:
            with open('data/' + lang + '.json') as file:
                self.pokedex[lang] = json.load(file)
        self.lang = 'en'

    def change_language(self, language):
        if language in Pokedex.languages:
            self.lang = language

    def get_pokemon_by_id(self, number, lang=None):
        lang = self.lang if lang is None else lang

        if number in range(1, len(self.pokedex[lang]), 1):
            return self.pokedex[lang][number-1]
        return -1

    def get_pokemon_id_by_name(self, name, lang=None):
        lang = self.lang if lang is None else lang

        try:
            return self.pokedex[lang].index(name) + 1
        except ValueError:
            return -1

    def get_pokemon_translated(self, name, lang_origin, lang_target=None):
        lang_target = self.lang if lang_target is None else lang_target

        ret = self.get_pokemon_id_by_name(name, lang_origin)
        return self.get_pokemon_by_id(ret, lang_target)
