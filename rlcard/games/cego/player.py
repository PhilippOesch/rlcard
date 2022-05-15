class CegoPlayer:
    ''' Represents a player

    Instance attributes:
        - np_random (numpy.random.RandomState): numpy random state
        - player_id (int): The id of the player
        - is_cego_player (bool): Whether the player is the cego player
        - hand (list): The cards in the hand
        - valued_cards (list): The cards layed asside and converted to points
    '''

    def __init__(self, player_id, np_random, is_single_player=False):
        ''' Initilize a player

        Parameters:
            - player_id (int): The id of the player
            - np_random (numpy.random.RandomState): numpy random state
            - is_cego_player (bool): Whether the player is the cego player
        '''
        self.np_random = np_random
        self.player_id: int = player_id
        self.is_single_player: bool = is_single_player
        self.hand: list = []
        self.valued_cards: list = []  # the cards that the cego player has layed aside

    def get_player_id(self) -> int:
        ''' Return the id of the player
        '''

        return self.player_id
