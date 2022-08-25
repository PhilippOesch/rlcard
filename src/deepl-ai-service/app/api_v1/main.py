from tokenize import Triple
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.api_v1.plugins.ai_helper import handle_get_request, ActionPrediciton

main_url_part = '/api/v1'

app = FastAPI(
    title='DeepL-AI-Service',
    docs_url=main_url_part + '/docs',
    description='This AI use trained models to predict the next best move for the card game Cego',
    contact={
        'name': 'Philipp Oeschger',
        'url': 'https://philipp-oeschger.de',
        'email': 'kontakt@philipp-oeschger.de',
    },
)


@app.get(main_url_part+'/')
async def root():
    return RedirectResponse(url='/api/v1/docs')


@app.get(main_url_part+'/cego/', response_model=ActionPrediciton)
async def predict_cego(
    hand_cards: str = None,
    legage_cards: str = None,
    played_cards: str = None,
    trick_cards: str = None,
    current_player_id: int = None,
    round_starter_id: int = None,
    single_player_id: int = None
) -> ActionPrediciton:
    return handle_get_request('cego', hand_cards, legage_cards, played_cards,
                              trick_cards, current_player_id, round_starter_id, single_player_id)


@app.get(main_url_part+'/solo/', response_model=ActionPrediciton)
async def predict_solo(
    hand_cards: str = None,
    played_cards: str = None,
    trick_cards: str = None,
    current_player_id: int = None,
    round_starter_id: int = None,
    single_player_id: int = None
) -> ActionPrediciton:
    return handle_get_request('solo', hand_cards, None, played_cards,
                              trick_cards, current_player_id, round_starter_id, single_player_id)


@app.get(main_url_part+'/ultimo/', response_model=ActionPrediciton)
async def predict_ultimo(
    hand_cards: str = None,
    played_cards: str = None,
    trick_cards: str = None,
    current_player_id: int = None,
    round_starter_id: int = None,
    single_player_id: int = None
) -> ActionPrediciton:
    return handle_get_request('ultimo', hand_cards, None, played_cards,
                              trick_cards, current_player_id, round_starter_id, single_player_id)


@app.get(main_url_part+'/bettel/', response_model=ActionPrediciton)
async def predict_bettel(
    hand_cards: str = None,
    played_cards: str = None,
    trick_cards: str = None,
    current_player_id: int = None,
    round_starter_id: int = None,
    single_player_id: int = None
) -> ActionPrediciton:
    return handle_get_request('bettel', hand_cards, None, played_cards,
                              trick_cards, current_player_id, round_starter_id, single_player_id)


@app.get(main_url_part+'/piccolo/', response_model=ActionPrediciton)
async def predict_piccolo(
    hand_cards: str = None,
    played_cards: str = None,
    trick_cards: str = None,
    current_player_id: int = None,
    round_starter_id: int = None,
    single_player_id: int = None
) -> ActionPrediciton:
    return handle_get_request('piccolo', hand_cards, None, played_cards,
                              trick_cards, current_player_id, round_starter_id, single_player_id)


@app.get(main_url_part+'/raeuber/', response_model=ActionPrediciton)
async def predict_raeuber(
    hand_cards: str = None,
    played_cards: str = None,
    trick_cards: str = None,
    current_player_id: int = None,
    round_starter_id: int = None,
    raeuber_id: int = None
) -> ActionPrediciton:
    return handle_get_request('raeuber', hand_cards, None, played_cards,
                              trick_cards, current_player_id, round_starter_id, raeuber_id, True)
