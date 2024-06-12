

class Test:

    __params = (
        ('min_profit_limit', 0.05),
        ('max_profit_limit', 0.20),
        ('loss_limit', 0.05),
        ('days_forecasted', 14)
    )


    @classmethod
    def get_params(cls):
        return cls.__params

