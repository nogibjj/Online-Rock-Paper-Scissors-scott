class Game:
    def __init__(self, id):
        self.p1Went = False
        self.p2Went = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0,0]
        self.ties = 0
        self.payout_done = False

    def get_player_move(self, p):
        """
        :param p: [0,1]
        :return: Move
        """
        return self.moves[p]

    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    def connected(self):
        return self.ready

    def bothWent(self):
        return self.p1Went and self.p2Went

    def winner(self):
        if self.payout_done:
            return -1, None, None, None  # return a placeholder value

        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]

        winner = -1
        # add winning conditions, grab winning address, post to blockchain
        if p1 == "R" and p2 == "S":
            winner = 0
            winner_uid = user1_uid
            loser_uid = user2_uid
        elif p1 == "S" and p2 == "R":
            winner = 1
            winner_uid = user2_uid
            loser_uid = user1_uid
        elif p1 == "P" and p2 == "R":
            winner = 0
            winner_uid = user1_uid
            loser_uid = user2_uid
        elif p1 == "R" and p2 == "P":
            winner = 1
            winner_uid = user2_uid
            loser_uid = user1_uid
        elif p1 == "S" and p2 == "P":
            winner = 0
            winner_uid = user1_uid
            loser_uid = user2_uid
        elif p1 == "P" and p2 == "S":
            winner = 1
            winner_uid = user2_uid
            loser_uid = user1_uid
        note = "Player 1 chose {0} and player 2 chose {1}.".format(p1,p2)
        return winner, winner_uid, loser_uid, note

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False

# define below user ids based on player 1 or player 2
user1_uid = "CEGWAX2saBV3bh0sNt5Q0yUxYH13" # test user uid 1 = player 1 
user2_uid = "4vqh7TmHNQSMxRkuzUuktNlHjeZ2" # test user uid 2 = player 2