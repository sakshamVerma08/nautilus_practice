from decimal import Decimal
from nautilus_trader.trading.strategy import Strategy
from nautilus_trader.config import StrategyConfig, BacktestEngineConfig
from nautilus_trader.model.data import Bar, BarType
from nautilus_trader.model import InstrumentId
from nautilus_trader.backtest.engine import BacktestEngine

class EMACross_Config(StrategyConfig):
        instrument_id: InstrumentId
        bar_type: BarType = ""
        fast_ema_period: int = 10
        slow_ema_period: int = 20 
        trade_size: Decimal
        order_id_tag: str 


class EMACross(Strategy):
    def __init__(self, config: EMACross_Config):
        super().__init__(config)
        self.time_started = None
        self.count_of_processed_bars: int = 0

    def on_start(self):
        self.time_started = self.clock.utc_now()
        self.subscribe_bars(self.config.bar_type)

    def on_bar(self):
        self.count_of_processed_bars+=1

    def on_stop(self):
        print("Strategy started to run at :", self.time_started)
        print(f"Strategy processed {self.count_of_processed_bars} bars")
    


config = EMACross_Config(
     bar_type = BarType.from_str("ETHUSDT-PERP.BINANCE-15-MINUTES-LAST-EXTERNAL"),
     trade_size = Decimal(1),
     order_id_tag = "001",

)

strategy = EMACross(config)

        

engine = BacktestEngine(BacktestEngineConfig())


engine.add_venue(
     venue="BINANCE",
     oms_type = "HEDGING",
     account_type = "CASH"
)

