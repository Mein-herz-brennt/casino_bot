from random import randint


class Win_or_lose_money:
    def __init__(self, rate):
        self.rate = int(rate)

    def give_cash(self):
        if self.rate == 1 or 1 < self.rate < 5:
            win = randint(1, self.rate)
        elif 5 <= self.rate <= 10:
            win = randint(self.rate, self.rate+5)
        elif 10 < self.rate <= 50:
            win = randint(self.rate, self.rate+10)
        elif 50 < self.rate <= 250:
            win = randint(self.rate, self.rate+30)
        elif 250 < self.rate <= 1000:
            win = randint(self.rate, self.rate+150)
        elif 1000 < self.rate <= 5000:
            win = randint(self.rate, self.rate+500)
        elif 5000 < self.rate <= 10000:
            win = randint(self.rate, self.rate+1000)
        elif self.rate == 0:
            win = 0
        else:
            win = randint(self.rate, self.rate+5000)

        return win



