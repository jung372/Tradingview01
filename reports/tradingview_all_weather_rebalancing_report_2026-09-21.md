# 미국 ETF All Weather형 포트폴리오와 TradingView 알고리즘 적용 보고서

> **후속 방향(2026-09-21):** 사용자가 SCHD·QQQM·IEF·IAUM을 명시했고, 최우선 목표를 **MDD 최소화**로 확정했다. 이 문서는 최초 전략 조사 기록이며, 현재 개발 기준과 대안 비중 검증안은 [MDD 우선 타이밍 안내 시스템 문서](mdd_first_rebalancing_timing_advisor_2026-09-21.md)를 따른다. 아래 티커 오타 추정 문단은 최초 입력의 해석 기록이다.

- 작성 기준일: 2026-09-21 (Asia/Seoul)
- 분석 목적: 1억 원 규모의 미국 ETF 포트폴리오에 적용할 리밸런싱 규칙과 TradingView 공개 스크립트 후보 선정
- 주의: 아래 내용은 정보 제공과 전략 설계를 위한 분석이며 수익을 보장하거나 매수·매도 주문을 권유하는 개인 맞춤 투자자문이 아니다.

## 1. 결론 요약

우선 **고정 목표비중 + 분기 점검 + ±5%p 허용밴드**를 *검증할 정책안*으로 제안한다. 아직 이 4자산 결합 규칙의 백테스트나 실계좌 검증을 마친 것은 아니다. TradingView의 인기 추세추종 알고리즘으로 기존 배분을 수시로 뒤집기보다는 다음처럼 역할을 분리하는 편이 전략 일관성과 검증 가능성이 높다. 공개 Pine 소스에서 확인한 정확한 적용 범위와 자동매매 가능성은 [후속 검토 보고서](tradingview_automation_feasibility_2026-09-21.md)에 정리했다.

1. **핵심 백테스트 도구:** [Portfolio Simulator & Backtester](https://www.tradingview.com/script/kbaODuIz-Portfolio-Simulator-Backtester/) — 4개 ETF의 목표비중, 배당 재투자, 거래비용, 월·분기·연 리밸런싱을 한 번에 비교한다.
2. **허용밴드 아이디어 참고:** [Performance Metrics With Bracketed Rebalancing](https://www.tradingview.com/script/uTzHDFX6-Performance-Metrics-With-Bracketed-Rebalacing-BackQuant/) — 공개 소스의 임계값 트리거 개념만 참고한다. 원본은 3자산·33/33/34 고정이며 `최대 현재비중 > 40%` 방식이다. 4자산·25/25/30/20·목표 대비 ±5%p 정책을 원본에서 직접 검증하거나 실행할 수 없다.
3. **보조 위험 신호:** [Chandelier Exit](https://www.tradingview.com/script/AqXxNS7j-Chandelier-Exit-everget/) 또는 [SuperTrend STRATEGY](https://www.tradingview.com/script/P5Gu6F8k/) — 주봉 추세 상태를 대시보드와 알림에만 사용한다. 코어 자산을 자동 청산하는 규칙으로 바로 사용하지 않는다.
4. **별도 실험 후보:** [Dual Momentum Strategy](https://www.tradingview.com/script/wFRnnlQr/) — 실계좌 적용 전 모의운용과 아웃오브샘플 검증이 필요한 전술형 전략이다. 코어 포트폴리오 전체에 적용하면 원래의 All Weather형 철학을 크게 변경한다.

핵심 이유는 간단하다. TradingView의 Boost 수는 이용자 관심도를 보여줄 뿐 미래 수익률이나 견고성을 증명하지 않는다. 반면 포트폴리오의 목적은 시장 방향을 맞히는 것이 아니라 목표 위험구조를 유지하는 것이다. Vanguard도 리밸런싱의 목적을 시장 타이밍이 아닌 위험 관리로 설명하고, 달력과 허용밴드를 결합하는 방법을 제시한다. [Vanguard 리밸런싱 안내](https://investor.vanguard.com/investor-resources-education/portfolio-management/rebalancing-your-portfolio)

## 2. 입력 티커와 포트폴리오 해석

사용자 입력에는 티커 오타 가능성이 있다.

- `SHCD`는 **SCHD**로 가정했다.
- `AUM`은 금 가격 노출 상품인 **IAUM**으로 가정했다.
- `AUM`이 `IAU` 또는 전혀 다른 상품을 뜻한다면 모든 TradingView 입력과 분석을 수정해야 한다. 티커 확정 전에는 이 보고서를 실제 주문 수량 산정에 사용하면 안 된다.

| 자산 | 가정한 티커 | 목표비중 | 1억 원 기준 최초 배분 | 전략상 역할 |
|---|---:|---:|---:|---|
| Schwab U.S. Dividend Equity ETF | SCHD | 25% | 2,500만 원 | 미국 배당·퀄리티·가치주 성격의 성장 자산 |
| Invesco NASDAQ 100 ETF | QQQM | 25% | 2,500만 원 | 미국 대형 성장주·기술주 중심의 성장 자산 |
| iShares 7–10 Year Treasury Bond ETF | IEF | 30% | 3,000만 원 | 중기 미국 국채, 성장 둔화·디스인플레이션 방어 역할 |
| iShares Gold Trust Micro | IAUM | 20% | 2,000만 원 | 금 가격 노출, 인플레이션·통화 불확실성 완충 역할 |

상품 성격은 각 운용사의 공식 자료로 확인했다. SCHD는 Dow Jones U.S. Dividend 100 Index를 추종하고, QQQM은 Nasdaq-100 지수에 노출되며, IEF는 잔존만기 7~10년 미국 국채, IAUM은 금 현물 가격 반영을 목표로 한다. [SCHD 공식 페이지](https://www.schwabassetmanagement.com/products/schd), [QQQM 공식 자료](https://www.invesco.com/us-rest/contentdetail?contentId=3bb2c37291215710VgnVCM1000006e36b50aRCRD&dnsName=us), [IEF 공식 페이지](https://www.ishares.com/us/products/239456/ishares-710-year-treasury-bond-etf), [IAUM 공식 페이지](https://www.ishares.com/us/products/306979/ishares-gold-trust-micro)

### All Weather 관점의 진단

이 배분은 **All Weather에서 영감을 받은 정적 자산배분**으로 보는 것이 정확하다. Bridgewater의 원래 개념은 성장과 인플레이션의 서로 다른 환경에 대한 노출을 자산 금액이 아니라 위험 기여도 관점에서 균형화하는 데 있다. [Bridgewater, The All Weather Story](https://www.bridgewater.com/research-and-insights/the-all-weather-story)

현재 안은 다음 특징이 있으므로 정통 Risk Parity 또는 Bridgewater의 All Weather와 동일하지 않다.

- SCHD와 QQQM을 합친 주식 명목비중이 50%이며 두 상품 모두 미국 대형주 노출이므로, 실제 위험은 주식과 미국 시장에 더 집중될 가능성이 있다.
- IEF는 중기 국채다. Bridgewater가 설명한 디플레이션 방어에는 장기채의 위험 기여가 중요한데, IEF만으로 같은 민감도를 재현한다고 볼 수 없다.
- IAUM은 금 노출을 제공하지만 광범위 원자재, 물가연동채, 해외주식이 없다.
- 원화 투자자의 성과에는 USD/KRW 환율이 크게 작용한다. TradingView의 달러 표시 ETF 백테스트만 보면 원화 기준 손익과 변동성이 누락된다.

따라서 이번 보고서의 목표는 “All Weather라는 이름을 입증”하는 것이 아니라, 사용자가 정한 25/25/30/20 정책을 일관되게 유지하고 검증하는 것이다.

## 3. TradingView 후보 조사 결과

TradingView는 현재 공개 인기 수치를 `Boost`로 표시한다. 아래 수치는 2026-09-21 직접 조회값이며 계속 변할 수 있다. 공개 소스, 다중자산 적합성, 거래빈도, 리페인트·백테스트 위험, 기존 정책과의 충돌 여부를 함께 평가했다.

| 우선순위 | 스크립트 | Boost | 공개 여부 | 적합성 판단 | 활용 결정 |
|---:|---|---:|---|---|---|
| 1 | [Portfolio Simulator & Backtester](https://www.tradingview.com/script/kbaODuIz-Portfolio-Simulator-Backtester/) | 75 | Open source | 최대 5개 자산, 목표비중, DCA, 월·분기·연 리밸런싱, 비용, DRIP, CAGR·MDD·Sharpe·Sortino 비교가 가능해 현재 포트폴리오와 가장 직접적으로 맞는다. | **채택: 기준 백테스터** |
| 2 | [Performance Metrics With Bracketed Rebalancing](https://www.tradingview.com/script/uTzHDFX6-Performance-Metrics-With-Bracketed-Rebalacing-BackQuant/) | 76 | Open source | 원본은 3자산·33/33/34 고정, `최대 현재비중 > 40%`를 재조정 트리거로 사용한다. 목표 대비 개별 ±5%p와 분기 점검을 지원하지 않아 이 포트폴리오의 백테스트로 직접 사용할 수 없다. | **개념만 참고; 별도 구현 필요** |
| 3 | [Dual Momentum Strategy](https://www.tradingview.com/script/wFRnnlQr/) | 109 | Open source | 월 단위 12개월 절대·상대 모멘텀으로 위험자산과 안전자산을 전환한다. 논리가 단순하고 검증 가능하지만 기본 SPY/TLT 구조를 현재 4자산에 그대로 대입할 수 없다. | **모의운용 후보** |
| 4 | [Chandelier Exit, everget](https://www.tradingview.com/script/AqXxNS7j-Chandelier-Exit-everget/) | 29,103 | Open source | ATR 기반 추적 손절과 확정봉 알림을 제공한다. 인기는 매우 높지만 단일 자산의 추세 청산 도구이지 포트폴리오 리밸런서가 아니다. | **주봉 보조 신호만** |
| 5 | [SuperTrend STRATEGY, KivancOzbilgic](https://www.tradingview.com/script/P5Gu6F8k/) | 25,185 | Open source | ATR 기간·배수를 이용한 단순 추세 전환 전략으로 소스 검토와 Strategy Tester가 가능하다. 제작자도 횡보장에서 약하다고 명시한다. | **주봉 비교 실험만** |
| 6 | [Chandelier Exit Strategy with 200 EMA Filter](https://www.tradingview.com/script/T7c4n0Qu/) | 약 1.1K | Open source | Chandelier에 200 EMA 방향 필터를 결합했지만 롱·숏 거래와 개별 트레이드 위험관리가 중심이라 코어 자산배분과 충돌한다. | **미채택** |
| 7 | [Risk Parity Allocations](https://www.tradingview.com/script/2WMwliNs-Risk-Parity-Allocations/) | 3 | Protected | 역변동성만 사용하고 상관·공분산을 반영하지 않아 완전한 Risk Parity가 아니며, 14봉 기본값은 장기 자산배분에 지나치게 민감하다. 소스도 비공개다. | **미채택** |

### 인기 상위 알고리즘을 핵심 규칙으로 선택하지 않은 이유

Chandelier Exit과 SuperTrend는 각각 2만 회 이상의 Boost를 받아 인기가 높지만, 그 인기는 다음 문제를 해결하지 않는다.

- SCHD·QQQM·IEF·IAUM 네 자산의 합계 비중이 항상 100%가 되도록 조정하지 않는다.
- 개별 자산 신호를 동시에 적용하면 여러 자산이 현금화되어 원래의 분산 구조가 사라질 수 있다.
- ATR 기반 신호는 횡보장에서 잦은 반전과 거래비용을 만들 수 있다.
- 일봉 최적화 결과를 주봉·월봉 장기투자에 그대로 옮기면 과최적화 위험이 크다.

TradingView 공식 문서도 전략 테스트는 시뮬레이션이며 미래 성과를 보장하지 않고, 다른 시간대 데이터·리페인트 변수·체결 가정에 따라 과거 데이터에 미래 정보가 누출될 수 있다고 설명한다. [TradingView 전략 문서](https://www.tradingview.com/pine-script-docs/concepts/strategies/)

## 4. 권고 리밸런싱 정책

### 4.1 정책 규칙

1. 목표비중은 SCHD 25%, QQQM 25%, IEF 30%, IAUM 20%로 유지한다.
2. 미국 시장의 3·6·9·12월 마지막 거래일 종가 기준으로 비중을 점검한다.
3. 어느 한 자산이라도 목표에서 **±5%p**를 벗어날 때만 네 자산 전체를 목표비중으로 되돌린다.
4. 밴드 안이면 거래하지 않는다. 연말에는 목표·위험수용도·현금흐름을 검토하되, 밴드 안이라는 이유만으로 반드시 매매하지는 않는다.
5. 신규 납입금, 배당, 이자를 저비중 자산에 우선 배분하는 것은 **별도 제안 규칙**이다. Portfolio Simulator의 DCA는 목표비중대로 분배하므로 이 정책을 시험하려면 별도 계산기가 필요하다. 매도는 현금흐름만으로 복원이 안 되는 차액에 한정한다.
6. 실제 주문 전에는 세금, 환전비용, 스프레드, 최소 주문단위와 계좌 유형을 확인한다.

### 4.2 허용범위

밴드는 금액이 아니라 **당시 총 평가액 대비 비중**으로 계산한다.

| 자산 | 목표 | 거래를 하지 않는 범위 | 1억 원일 때의 예시 범위 |
|---|---:|---:|---:|
| SCHD | 25% | 20%~30% | 2,000만~3,000만 원 |
| QQQM | 25% | 20%~30% | 2,000만~3,000만 원 |
| IEF | 30% | 25%~35% | 2,500만~3,500만 원 |
| IAUM | 20% | 15%~25% | 1,500만~2,500만 원 |

현재 총 평가액을 `V`, 자산 `i`의 평가액을 `M_i`, 목표비중을 `t_i`라고 하면 다음 수식을 사용한다.

```text
현재비중 w_i = M_i / V
리밸런싱 차액 Δ_i = (t_i × V) - M_i
실행 조건 = |w_i - t_i| ≥ 0.05
```

예를 들어 총 평가액이 1억 2천만 원이면 SCHD 목표금액은 3천만 원이다. 최초 1억 원 기준 금액을 계속 고정해서는 안 된다.

### 4.3 추세 신호의 제한적 반영

Chandelier Exit 또는 SuperTrend는 **매매 명령이 아니라 위험 점검 알림**으로만 반영한다.

- 차트 시간대: 주봉
- 신호 확정: 주간 종가 확정 후
- 적용 대상: 우선 SCHD와 QQQM
- 행동: 두 주식 ETF가 동시에 약세로 전환하면 다음 분기 점검을 앞당겨 현재 비중, 최대낙폭, 환율, 투자기간을 검토한다.
- 금지: 약세 신호 하나만으로 IEF·IAUM을 포함한 코어 배분을 현금화하거나, 신호에 맞춰 목표비중 자체를 변경하지 않는다.

이는 인기 알고리즘의 정보는 활용하되, 정적 분산 포트폴리오를 단기 추세 전략으로 바꾸지 않기 위한 경계다.

## 5. TradingView 적용 절차

### 5.1 기준 백테스트

1. TradingView에서 가장 긴 공통 이력을 가진 자산 또는 SPY의 일봉 차트를 연다.
2. `Portfolio Simulator & Backtester`를 추가한다.
3. 자산을 `AMEX:SCHD 25`, `NASDAQ:QQQM 25`, `NASDAQ:IEF 30`, `AMEX:IAUM 20`으로 설정한다. 거래소 접두사는 TradingView 검색 결과의 실제 심볼을 다시 확인한다.
4. `Reinvest Dividends`를 켠다.
5. 거래비용은 실제 증권사 수수료·스프레드·환전비용을 반영한다. 최소한 편도 0.05%, 0.10%, 0.25%의 세 시나리오를 비교한다.
6. `None`, `Quarterly`, `Yearly`를 각각 실행해 CAGR뿐 아니라 MDD, Sortino, Calmar, 변동성, 거래 횟수를 기록한다.
7. 같은 기간의 SPY와 비교하되, 목표는 SPY 초과수익이 아니라 낙폭과 위험조정성과의 개선 여부로 둔다.

이 스크립트는 현재 세금과 슬리피지를 완전히 모델링하지 않는다고 명시한다. 결과표를 세후 실현성과로 해석하면 안 된다.

### 5.2 허용밴드 검증

1. `Performance Metrics With Bracketed Rebalancing`을 별도 레이아웃에 추가한다.
2. 원본 설정에서 3개 자산·33/33/34 고정, 절대비중 기준 기본 40% 트리거를 확인한다. 이를 4개 자산·목표 대비 ±5%p로 입력할 수 있다고 해석하지 않는다.
3. 25/25/30/20의 분기 점검 + ±5%p 방식은 별도 백테스터/계산기에 재구현해 `None`, 무조건 `Quarterly`, 밴드 결합 정책을 같은 데이터·비용으로 비교한다.
4. 별도 구현의 밴드 결합 정책이 무조건 분기 또는 연간 리밸런싱보다 거래 횟수만 늘리고 위험지표를 개선하지 못하면 더 단순한 정책을 검토한다.

### 5.3 알림 설정

- Chandelier Exit: `wait for bar confirmation`을 사용하고 주봉 종가에서만 알림을 발생시킨다.
- SuperTrend: ATR 10, 배수 3은 출발점일 뿐 고정된 정답이 아니다. 8~14와 2.5~4.0의 인접 구간에서 결과가 급변하면 사용하지 않는다.
- 알림명에는 자산·시간대·확정 조건을 포함한다. 예: `QQQM | 1W | confirmed trend-down`.
- 알림 수신 후 당일 자동 주문을 연결하지 않는다. 다음 영업일에 데이터와 포트폴리오 비중을 수동 확인한다.

## 6. 백테스트 설계와 통과 기준

정확한 현재 상품을 그대로 사용하면 공통 이력이 IAUM의 설정일인 2021-06-15 이후로 제한된다. QQQM은 2020-10-13, IAUM은 2021-06-15에 설정되어 금리 급등과 인플레이션 국면을 포함하지만 여러 경기순환을 검증하기에는 짧다. [QQQM 공식 자료](https://www.invesco.com/us-rest/contentdetail?contentId=3bb2c37291215710VgnVCM1000006e36b50aRCRD&dnsName=us), [IAUM 공식 페이지](https://www.ishares.com/us/products/306979/ishares-gold-trust-micro)

따라서 두 종류의 검증을 병행한다.

| 검증 | 심볼 | 시작 가능 시점 | 목적 |
|---|---|---|---|
| 정확 상품 검증 | SCHD / QQQM / IEF / IAUM | 2021-06-15 이후 | 실제 상품·비용·배당 데이터에 가까운 결과 |
| 장기 프록시 검증 | SCHD / QQQ / IEF / IAU | SCHD 설정 이후인 2011년 | 성장주와 금 노출의 더 긴 국면 비교. 단, 동일 상품 결과로 단정하지 않음 |

반드시 다음을 확인한다.

- 표준 캔들만 사용하고 Heikin Ashi·Renko 같은 합성 차트는 사용하지 않는다.
- 미래 데이터 누출, `lookahead_on`, 미확정봉 신호, 리페인트가 없는지 소스를 확인한다.
- 전체기간 최적화 후 같은 기간에서 성과를 주장하지 않는다. 학습구간과 검증구간을 분리하고 롤링 구간을 비교한다.
- 10년 이상의 백테스트가 나오더라도 프록시·지수·배당 처리 차이를 명시한다.
- USD 성과와 함께 `ETF 가격 × USDKRW`로 환산한 원화 기준 CAGR·변동성·MDD를 별도로 계산한다.
- 평가 우선순위는 `최대낙폭 → 목표비중 이탈 → 회전율/비용 → Sortino/Calmar → CAGR` 순으로 둔다.

전략 채택 조건은 특정 최고수익 조합이 아니라 다음의 견고성이다.

1. 인접 파라미터에서도 결론이 유지된다.
2. 정확 상품과 장기 프록시 검증의 방향이 크게 모순되지 않는다.
3. 비용을 높여도 상대적 장점이 사라지지 않는다.
4. 아웃오브샘플 구간에서 최대낙폭이나 위험조정성과가 악화되지 않는다.
5. 사용자가 실제로 지킬 수 있는 거래빈도와 절차다.

## 7. 선택하지 않은 대안과 향후 확장

### Dual Momentum

12개월 모멘텀으로 위험자산과 안전자산을 전환하는 논리는 검증하기 쉽지만, 네 자산을 계속 보유하는 현재 철학과 다르다. 시험하려면 코어 포트폴리오와 분리된 모의계정에서 월말에만 평가한다. 실계좌 도입을 검토하더라도 처음부터 전체 자산에 적용하지 말고, 별도의 소규모 전술 슬리브로 정의한 뒤 목표비중 변경을 정책서에 기록해야 한다.

### 역변동성 또는 Risk Parity

단순 역변동성은 변동성이 낮은 IEF의 비중을 크게 늘릴 수 있지만, 자산 간 상관관계를 무시하므로 동일 위험기여를 보장하지 않는다. 진정한 위험균형을 원한다면 TradingView의 비공개 단순 스크립트보다 일별 총수익률, 공분산, 최소·최대 비중, 거래비용을 포함한 Equal Risk Contribution 모델을 별도 분석 환경에서 구현하는 편이 낫다. 이는 기존 25/25/30/20 정책을 바꾸는 별도 의사결정이므로 이번 권고안에는 포함하지 않았다.

## 8. 실행 체크리스트

- [ ] `SHCD`가 `SCHD`인지 확인
- [ ] `AUM`이 `IAUM`인지, `IAU`인지 확인
- [ ] 네 상품의 실제 보유수량·평가액·계좌 유형 확인
- [ ] 목표비중과 ±5%p 밴드를 투자정책서에 기록
- [ ] Portfolio Simulator에서 None/Quarterly/Yearly 비교
- [ ] 4자산·개별 ±5%p 규칙을 별도 구현한 뒤 분기·연간 정책과 비교
- [ ] USD 기준과 KRW 기준 결과를 분리
- [ ] 수수료·스프레드·환전·세금 시나리오 반영
- [ ] 주봉 Chandelier 또는 SuperTrend는 알림 전용으로 3~12개월 관찰
- [ ] 실계좌 자동주문 연결 전 모의운용 및 아웃오브샘플 검증

## 9. 최종 권고

현재 단계에서는 **SCHD 25% / QQQM 25% / IEF 30% / IAUM 20%를 코어로 유지하고, 분기 말 점검 + ±5%p 이탈 시 목표비중 복원**을 *검증할 기본 정책안*으로 둔다. TradingView Portfolio Simulator는 무조건 분기·연간 리밸런싱의 기준 시뮬레이터이며, BackQuant 원본은 허용밴드 발상의 참고 자료일 뿐 이 정책의 검증 도구가 아니다.

Chandelier Exit과 SuperTrend는 높은 인기 때문에 검토 가치가 있지만, 이 포트폴리오에서는 “추세 하락 시 전량 매도”가 아니라 “위험 점검을 앞당기는 주봉 알림”으로만 반영한다. Dual Momentum은 코어와 분리된 모의 전술 전략으로 취급한다. 이렇게 해야 인기 알고리즘을 활용하면서도 All Weather형 자산배분의 핵심인 장기 분산과 규칙 기반 리밸런싱을 훼손하지 않는다.

## 출처 및 조회 메모

- TradingView 스크립트의 Boost·공개 여부·설명: 각 원문 페이지, 2026-09-21 조회
- TradingView 백테스트 한계: [Pine Script Strategies](https://www.tradingview.com/pine-script-docs/concepts/strategies/), 2026-09-21 조회
- TradingView 다중 심볼 요청 한도: [Pine Script Limitations](https://www.tradingview.com/pine-script-docs/writing/limitations/), 2026-09-21 조회
- All Weather 개념: [Bridgewater, The All Weather Story](https://www.bridgewater.com/research-and-insights/the-all-weather-story), 2026-09-21 조회
- 리밸런싱 원칙: [Vanguard, Rebalancing your portfolio](https://investor.vanguard.com/investor-resources-education/portfolio-management/rebalancing-your-portfolio), 2026-09-21 조회
- ETF의 목적·설정일·비용: 각 운용사 공식 상품 페이지, 2026-09-21 조회
