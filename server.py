import socket
from _thread import *
import pickle
from game import Game
import threading

server = "localhost"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0

# Add this global variable at the beginning of your script
executed_payouts = {}

def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)

                    # start server change
                    if game.bothWent():
                        winner, winner_uid, loser_uid, note = game.winner()
                        if winner != -1 and not game.payout_done:
                            lock = threading.Lock()
                            lock.acquire()
                            try:
                                if gameId not in executed_payouts:
                                    payout_winner(loser_uid, winner_uid, note)
                                    executed_payouts[gameId] = True  # mark that payout has been done for this game
                            finally:
                                lock.release()
                    # end server change


                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        if gameId in executed_payouts:  # remove the game id from executed_payouts when game is closed
            del executed_payouts[gameId]
        print("Closing Game", gameId)
    except:
        pass

# [ Start DropChain API Integrations ]
def payout_winner(loser_uid, winner_uid, note): 
    # get the game instance
    game = games.get(gameId, None)
    if game is None or game.payout_done:
        return  # exit the function if the game does not exist or the payout has already been done
    
    game.payout_done = True  # set the payout_done flag to True
    
    import requests, json 
    app_id = "BNCYKR4B39XimiWcS4UvgeGu" # app_id 

    url = "https://api.dropchain.network/v1/send_algo_testnet"

    payload = {
    "app_id": app_id,
        "user1_uid": loser_uid,
        "receiver1_uid": winner_uid,
        "asset1_amount_int": "100000", # this amount can be changed based on the wager for the game
        "transaction1_note": note
    }
    headers = {
        "content-type": "application/json",
        "X-API-Key": "7096410e-6d70-4846-9082-b0a242f29b1b", # taken from your DropChain API dashboard
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    response = json.loads(response.text)
    print(response)
    return response
# [ End DropChain API Integrations ]


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        p = 1


    start_new_thread(threaded_client, (conn, p, gameId))