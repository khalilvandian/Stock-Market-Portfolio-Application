import Recommender as recom
from Action import Action


class Account:

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password
        self.recommender = recom.RecommenderBt(self.name, 'Bama', 10)
        self.recommender.get_analysis()


    def get_plan(self):
        act = self.recommender.plan()
        for x in act:
            print(x.getAction())

    # TODO: account specific data specially portfolio is loaded by this function
    def load_user_data(self):
        return dict

    def get_machine_plan(self):
        print('System\'s recommendation is: ')
        self.recommender.get_actions()



