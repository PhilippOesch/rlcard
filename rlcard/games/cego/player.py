class CegoPlayer:
    def __init__(self, player_id, np_random, is_cego_player=False):
        ''' Initilize a player.

        Args:
            player_id (int): The id of the player
        '''
        self.np_random = np_random
        self.player_id = player_id
        self.is_cego_player = is_cego_player
        self.hand = []
        self.valued_cards = []  # the cards that the cego player has layed aside

    def get_player_id(self):
        ''' Return the id of the player
        '''

        return self.player_id
