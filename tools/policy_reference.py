"""Portable arithmetic/state specification, NOT a Pine runtime or a backtester."""
from dataclasses import dataclass
from datetime import datetime, timedelta
from math import isfinite

EPS = 1e-7


@dataclass(frozen=True)
class Review:
    state: str
    total: float = 0.0
    weights: tuple[float, ...] = ()
    gaps: tuple[float, ...] = ()
    drift: float = 0.0


def quarter_key(date: datetime) -> int:
    """Caller provides America/New_York calendar date, not Korean calendar date."""
    return date.year * 10 + (date.month - 1) // 3 + 1


def quarter_day(current: datetime, previous: datetime, previous_zero_based: int) -> int:
    """Consumes observed trading sessions; does not invent a weekday calendar."""
    return 1 if quarter_key(current) != quarter_key(previous) else previous_zero_based + 2


def evaluate(*, quantities, prices, cash, reserve, targets, now, checked_at,
             price_closes, unchanged=True, chart_ok=True, review_due=False,
             trend_ok=True, weekly_flip=False, band=5.0) -> Review:
    numeric = (*quantities, *prices, cash, reserve, *targets, band)
    if (len(quantities) != 4 or len(prices) != 4 or len(targets) != 4
            or len(price_closes) != 4 or not all(isfinite(x) for x in numeric)
            or not chart_ok or not unchanged or not 0 <= reserve <= cash
            or any(x < 0 for x in quantities) or any(x <= 0 for x in prices)
            or any(not 0 <= x <= 100 for x in targets)
            or abs(sum(targets) - 100) > EPS or band <= 0
            or len(set(price_closes)) != 1 or checked_at is None):
        return Review("DATA_CHECK")
    price_close = price_closes[0]
    if (not timedelta(0) <= now - price_close <= timedelta(days=7)
            or not timedelta(0) <= now - checked_at <= timedelta(days=7)
            or (review_due and checked_at < price_close)):
        return Review("DATA_CHECK")
    values = tuple(q * p for q, p in zip(quantities, prices))
    total = sum(values) + cash - reserve
    if total <= 0:
        return Review("DATA_CHECK")
    weights = tuple(100 * v / total for v in values)
    gaps = tuple(total * t / 100 - v for t, v in zip(targets, values))
    drift = max(abs(w - t) for w, t in zip(weights, targets))
    hit = drift + EPS >= band
    if sum(quantities) == 0:
        state = "INITIAL_ALLOCATION"
    elif review_due:
        state = "REBALANCE_REVIEW" if hit else "QUARTERLY_REVIEW"
    elif hit and trend_ok and weekly_flip:
        state = "EARLY_REVIEW_CANDIDATE"
    else:
        state = "DRIFT_WATCH" if hit else "ON_TRACK"
    return Review(state, total, weights, gaps, drift)


def vix_fix(closes, lows, *, length=22, band_length=20, band_mult=2.0,
            range_length=50, range_pct=0.85):
    """Williams Vix Fix with CM_Williams_Vix_Fix-style thresholds, per confirmed bar.

    Returns [(wvf, fear)] aligned with input; None during warm-up. Mirrors Pine
    ta.highest/ta.sma/ta.stdev (population stdev, Pine's default biased=True).
    """
    if len(closes) != len(lows):
        raise ValueError("closes and lows must align")
    wvf = [None] * len(closes)
    for i in range(length - 1, len(closes)):
        highest = max(closes[i - length + 1:i + 1])
        wvf[i] = 100 * (highest - lows[i]) / highest
    out = []
    for i, w in enumerate(wvf):
        band = wvf[max(0, i - band_length + 1):i + 1]
        rng = wvf[max(0, i - range_length + 1):i + 1]
        if w is None or len(band) < band_length or None in band or len(rng) < range_length or None in rng:
            out.append((w, None))
            continue
        mean = sum(band) / band_length
        std = (sum((x - mean) ** 2 for x in band) / band_length) ** 0.5
        upper = mean + band_mult * std
        range_high = range_pct * max(rng)
        out.append((w, w >= upper or w >= range_high))  # plain >= like Pine
    return out


def interpret(*, data_ok, actionable, trend_ok, difference, trend, fear):
    """Row reading from Pine f_row(). trend: 1 up / -1 down. Vix Fix refines only underweight+down."""
    if not trend_ok:
        return "추세 미확인"
    if not (data_ok and actionable):
        return "추세 " + ("상승" if trend == 1 else "하락") + " 참고"
    if difference > 0:
        return "하락: 축소 검토 우선" if trend == -1 else "상승: 초과분만 검토"
    if trend == 1:
        return "상승: 보충 검토 우호"
    return "하락+공포: 1차 분할 보충 검토" if fear else "하락: 분할·재확인"


class AlertGate:
    """Runtime-scoped deduplication; recreating a TradingView alert resets it."""
    def __init__(self):
        self.notified = None
        self.reminded = None

    def event(self, quarter, *, enabled, due, realtime, confirmed, valid):
        if not (enabled and due and realtime and confirmed):
            return None
        if not valid and self.reminded != quarter:
            self.reminded = quarter
            return "DATA_CHECK"
        if valid and self.notified != quarter:
            self.notified = quarter
            return "REVIEW"
        return None
