class Lookup:

    def __init__(self,
                 mahavyutpatti=True,
                 tony_duff=True,
                 erik_pema_kunsang=True,
                 ives_waldo=True,
                 jeffrey_hopkins=True,
                 lobsang_monlam=True,
                 tibetan_multi=True,
                 tibetan_medicine=True,
                 verb_lexicon=True):

        from tibetan_lookup.build_dictionary import BuildDictionary

        self.dictionaries = BuildDictionary(mahavyutpatti=mahavyutpatti,
                                            tony_duff=tony_duff,
                                            erik_pema_kunsang=erik_pema_kunsang,
                                            ives_waldo=ives_waldo,
                                            jeffrey_hopkins=jeffrey_hopkins,
                                            lobsang_monlam=lobsang_monlam,
                                            tibetan_multi=tibetan_multi,
                                            tibetan_medicine=tibetan_medicine,
                                            verb_lexicon=verb_lexicon)
        
        self.sources = ['mahavyutpatti',
                        'tony_duff',
                        'erik_pema_kunsang',
                        'ives_waldo',
                        'jeffrey_hopkins',
                        'lobsang_monlam',
                        'tibetan_multi',
                        'tibetan_medicine',
                        'verb_lexicon']


    def lookup(self, string, sources=None):

        '''Lookup Tibetan words from one or more dictionaries.
        
        string | str | the Tibetan string to be looked up
        sources | list or None | a list with one or more dictionary names

        NOTE: `string` must end in tsek.'''
        
        string = self._check_wylie(string).replace(' ', '')
        
        out = []
        
        for source in self.sources:
            out.append([source, self.dictionaries.query(string, source)])
            
        return out

    def _wylie_to_tibetan(self, wylie_string):
        
        '''Takes in string, and converts to Tibetan following Wylie rules.
        Adds Tsek between syllables and after the last syllable.'''

        from tibetan_lookup.wylie import Wylie

        warn = []
        
        return (Wylie().fromWylie(wylie_string, warn)) + '་'


    def _check_wylie(self, string):
        
        '''Unless string is Tibetan Unicode, assume it is Wylie and
        perform conversion to Tibetan. 

        string | str | some text

        Example:
        
            check_wylie('thabs')
        '''

        import re
        
        if len(re.findall(r'[\u0f00-\u0fff]+', string)) > 0:
            return string
        else:
            return self._wylie_to_tibetan(string)