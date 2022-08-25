from fastapi.testclient import TestClient

from app.api_v1.main import app, main_url_part

client = TestClient(app)


def test_cego_no_info():
    response = client.get(main_url_part + '/cego/')
    assert response.status_code == 400
    assert response.json() == {
        'detail': 'please provide information about the hand cards'}


def test_cego_no_current_player():
    response = client.get(main_url_part + '/cego/', params={
        'hand_cards': '18-trump,15-trump,13-trump,r-d,r-c,b-h,3-h,20-trump,17-trump'
    })
    assert response.status_code == 400
    assert response.json() == {
        'detail': 'please provide current_player_id'}


def test_cego_no_start_player():
    response = client.get(main_url_part + '/cego/', params={
        'hand_cards': '18-trump,15-trump,13-trump,r-d,r-c,b-h,3-h,20-trump,17-trump',
        'current_player_id': '0'
    })
    assert response.status_code == 400
    assert response.json() == {
        'detail': 'please provide start_player_id'}


def test_cego_no_single_starter():
    response = client.get(main_url_part + '/cego/', params={
        'hand_cards': '18-trump,15-trump,13-trump,r-d,r-c,b-h,3-h,20-trump,17-trump',
        'current_player_id': '0',
        'round_starter_id': '1',
    })
    assert response.status_code == 400
    assert response.json() == {
        'detail': 'please provide single_player_id'}


def test_cego_valid():
    response = client.get(main_url_part + '/cego/', params={
        'hand_cards': '18-trump,15-trump,13-trump,r-d,r-c,b-h,3-h,20-trump,17-trump',
        'played_cards': 'r-h,16-trump,4-h,2-h,21-trump,6-trump,9-trump,10-trump',
        'trick_cards': '8-s,r-s,k-s',
        'legage_cards': '11-trump,7-trump,1-trump,k-h,k-d,d-h,2-d,4-d,7-s,3-d',
        'current_player_id': '0',
        'round_starter_id': '1',
        'single_player_id': '0'
    })
    assert response.status_code == 200


def test_cego_valid_just_hand_cards():
    response = client.get(main_url_part + '/cego/', params={
        'hand_cards': '18-trump,15-trump,13-trump,r-d,r-c,b-h,3-h,20-trump,17-trump',
        'current_player_id': '0',
        'round_starter_id': '1',
        'single_player_id': '0'
    })
    assert response.status_code == 200


def test_to_many_hand_cards():
    response = client.get(main_url_part + '/cego/', params={
        'hand_cards': '18-trump,15-trump,13-trump,r-d,r-c,b-h,3-h,20-trump,17-trump,1-trump,7-c,16-trump',
        'current_player_id': '0',
        'round_starter_id': '1',
        'single_player_id': '0'
    })
    assert response.status_code == 400
    assert response.json() == {
        'detail': 'hand card deck is to large (has more than 11 cards)'}


def test_valid_solo():
    response = client.get(main_url_part + '/solo/', params={
        'hand_cards': '18-trump,15-trump,13-trump,r-d,r-c,b-h,3-h,20-trump,17-trump',
        'played_cards': 'r-h,16-trump,4-h,2-h,21-trump,6-trump,9-trump,10-trump',
        'trick_cards': '8-s,r-s,k-s',
        'current_player_id': '0',
        'round_starter_id': '1',
        'single_player_id': '0'
    })
    assert response.status_code == 200


def test_valid_ultimo():
    response = client.get(main_url_part + '/ultimo/', params={
        'hand_cards': '18-trump,15-trump,13-trump,r-d,r-c,b-h,3-h,20-trump,17-trump,1-trump',
        'played_cards': 'r-h,16-trump,4-h,2-h,21-trump,6-trump,9-trump,10-trump',
        'trick_cards': '8-s,r-s,k-s',
        'current_player_id': '0',
        'round_starter_id': '1',
        'single_player_id': '0'
    })
    assert response.status_code == 200


def test_invalid_ultimo():
    response = client.get(main_url_part + '/ultimo/', params={
        'hand_cards': '18-trump,15-trump,13-trump,r-d,r-c,b-h,3-h,20-trump,17-trump',
        'played_cards': 'r-h,16-trump,4-h,2-h,21-trump,6-trump,9-trump,10-trump',
        'trick_cards': '8-s,r-s,k-s',
        'current_player_id': '0',
        'round_starter_id': '1',
        'single_player_id': '0'
    })
    assert response.status_code == 400
    assert response.json() == {
        'detail': 'ultimo deck does not provide 1-trump card'}


def test_bettel():
    response = client.get(main_url_part + '/bettel/', params={
        'hand_cards': '18-trump,15-trump,13-trump,r-d,r-c,b-h,3-h,20-trump,17-trump',
        'played_cards': 'r-h,16-trump,4-h,2-h,21-trump,6-trump,9-trump,10-trump',
        'trick_cards': '8-s,r-s,k-s',
        'current_player_id': '0',
        'round_starter_id': '1',
        'single_player_id': '0'
    })
    assert response.status_code == 200


def test_piccolo():
    response = client.get(main_url_part + '/piccolo/', params={
        'hand_cards': '18-trump,15-trump,13-trump,r-d, r-c  , b-h , 3-h, 20-trump,17-trump',
        'played_cards': 'r-h,16-trump,4-h,2-h,21-trump,6-trump,9-trump,10-trump',
        'trick_cards': '8-s,r-s,k-s',
        'current_player_id': '0',
        'round_starter_id': '1',
        'single_player_id': '0'
    })
    assert response.status_code == 200


def test_card_invalidity():
    response = client.get(main_url_part + '/cego/', params={
        'hand_cards': '18-trump,15-trump,13-trump,r-d,r-c ,b-h, 10-h , 20-trump,17-trump ',
        'played_cards': 'r-h,16-trump,4-h,2-h,21-trump,6-trump,9-trump,25-trump',
        'trick_cards': '8-s,r-s,k-s',
        'current_player_id': '0',
        'round_starter_id': '1',
        'single_player_id': '0'
    })
    assert response.status_code == 400
    assert response.json() == {
        'detail': 'Not all card codes provided are valid'}


def test_raeuber_invalid():
    response = client.get(main_url_part + '/raeuber/', params={
        'hand_cards': '18-trump,15-trump,13-trump,r-d,r-c,b-h,3-h,20-trump,17-trump',
        'played_cards': 'r-h,16-trump,4-h,2-h,21-trump,6-trump,9-trump,25-trump',
        'trick_cards': '8-s,r-s,k-s',
        'current_player_id': '0',
        'round_starter_id': '1',
        'single_player_id': '0'
    })
    assert response.status_code == 400
    assert response.json() == {
        'detail': 'please provide raeuber_id (The player who called raeuber)'}


def test_raeuber():
    response = client.get(main_url_part + '/raeuber/', params={
        'hand_cards': '18-trump,15-trump,13-trump,r-d, r-c,  b-h ,3-h ,20-trump ,17-trump',
        'played_cards': 'r-h,16-trump,4-h,2-h,21-trump,6-trump,9-trump,10-trump',
        'trick_cards': '8-s,r-s,k-s',
        'current_player_id': '0',
        'round_starter_id': '1',
        'raeuber_id': '0'
    })
    assert response.status_code == 200
