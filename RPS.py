import numpy as np

win = {"P": "S", "R": "P", "S": "R"}
moves = ["R"]
hist = []
strategy = [0, 0, 0, 0]
pred = ["", "", "", ""]
selfpred = ["", "", "", ""]
oplays = {}
plays = {}

def reset():
    global moves, hist, strategy, pred, selfpred, oplays, plays
    moves = ["R"]
    hist.clear()
    strategy = [0, 0, 0, 0]
    pred = ["", "", "", ""]
    selfpred = ["", "", "", ""]
    oplays = {}
    plays = {}

def player(prev):
    if prev in ["R", "P", "S"]:
        hist.append(prev)
        for i in range(0, 4):
            if pred[i] == prev:
                strategy[i] += 1
    else:
        reset()

    prev10 = moves[-10:]
    if len(prev10) > 0:
        freq = max(set(prev10), key=prev10.count)
        pred[0] = win[freq]
        selfpred[0] = win[pred[0]]

    if len(moves) > 0:
        last = moves[-1]
        pred[1] = win[last]
        selfpred[1] = win[pred[1]]

    if len(hist) >= 3:
        pred[2] = predict_move(hist, 3, oplays)
        selfpred[2] = win[pred[2]]

    if len(moves) >= 2:
        pred[3] = win[predict_move(moves, 2, plays)]
        selfpred[3] = win[pred[3]]

    best = np.argmax(strategy)
    guess = selfpred[best]
    if guess == "":
        guess = "S"
    moves.append(guess)
    return guess


def predict_move(hist, n, plays):
    if "".join(hist[-n:]) in plays.keys():
        plays["".join(hist[-n:])] += 1
    else:
        plays["".join(hist[-n:])] = 1
    possible = ["".join(hist[-(n - 1) :]) + k for k in ["R", "P", "S"]]
    for pm in possible:
        if not pm in plays.keys():
            plays[pm] = 0
    predict = max(possible, key=lambda key: plays[key])
    return predict[-1]




