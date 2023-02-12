from enum import Enum


class Institution(str, Enum):
    MIDMARKET = "mid-market"

    VISA = "visa"
    MASTERCARD = "mastercard"


class StatPeriod(str, Enum):
    ONE_DAY = "1d"
    ONE_WEEK = "1wk"
    ONE_MONTH = "1mo"
    THREE_MONTHS = "3mo"
    SIX_MONTHS = "6mo"
    ONE_YEAR = "1y"
    TWO_YEARS = "2y"
    FIVE_YEARS = "5y"
    TEN_YEARS = ("10y",)
    MAX_PERIOD = "max"

    def from_str(period: str):
        for stat_period in StatPeriod:
            if period.upper() == stat_period.name or period == stat_period.value:
                return stat_period

        raise NotImplementedError


class StatInterval(str, Enum):
    ONE_DAY = "1d"
    ONE_WEEK = "1wk"
    ONE_MONTH = "1mo"

    def from_str(interval: str):
        for stat_interval in StatInterval:
            if (
                interval.upper() == stat_interval.name
                or interval == stat_interval.value
            ):
                return stat_interval

        raise NotImplementedError


class StatColumns(str, Enum):
    DATE = "Date"
    OPEN = "Open"
    HIGH = "High"
    LOW = "Low"
    CLOSE = "Close"
    ADJ_CLOSE = "Adj Close"
    VOLUME = "Volume"
