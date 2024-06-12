class Action:

    def __init__(self, action, stock, investmentVolume):

        self.action = {
            "action": action,
            "stock": stock,
            "volume": investmentVolume
        }

    def get_action(self):

        if self.action == 'buy' or self.action == 'sell':
            print(self.action["action"] + " " + str(self.action["volume"]) + " worth of " + self.action["stock"].name)
        else:
            print('WAIT FOR IT!')
