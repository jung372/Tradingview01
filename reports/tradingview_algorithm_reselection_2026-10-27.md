# TradingView 인기 알고리즘 전면 재검토 — 무엇을 차용할 것인가

- 작성·조회일: 2026-10-27, Asia/Seoul
- 대상: 해외2 4-ETF(SCHD·QQQM·IEF·IAUM) 분기 리밸런싱, MDD 우선, 읽기 전용, 현금 전액 포함
- 이전 판단: [Pine 설명서 §2](quarterly_etf_pine_guide_2026-10-26.md) — Chandelier Exit 채택, SuperTrend 비교 표시
- 성격: 지표 선정 근거 문서. 어떤 지표도 이 포트폴리오에서 성과가 입증되지 않았음

## 0. 결론

| 역할 | 이전 (10-26) | **재검토 결과 (10-27)** |
|---|---|---|
| 핵심 규칙 | 분기 점검 + ±5%p | **유지** |
| 추세 지표 | Chandelier Exit(29.7K) 주, SuperTrend **STRATEGY판**(25.1K) 비교 | **SuperTrend 원조 지표판(84.3K) 하나만** 사용 |
| 공포·저점 지표 | 없음 | **CM_Williams_Vix_Fix(66K) 신규 차용** |
| 백테스트 비교군 | — | Chandelier Exit, 40주 이동평균(학술 근거, TradingView 내장) |
| 검증 도구 | Portfolio Simulator 참고 | 유지 (Boost 772로 작아 **신호가 아닌 교차검증용**임을 명시) |

**이유를 한 줄로 정리하면** 이렇습니다. 이전 안은 *비슷한 성격의 추세선 두 개*를 겹쳐 쓰고 있었습니다. 새 안은 **"추세가 꺾였나"(SuperTrend)**와 **"지금 공포 구간인가"(Vix Fix)**라는 *서로 다른 두 질문*에 하나씩 답하는 구성입니다.

## 1. 이전 검토에서 부족했던 점

1. **인기 상위 스크립트가 빠졌다.** Smart Money Concepts(176.6K), Squeeze Momentum(117.6K), SuperTrend 지표판(84.3K), Williams Vix Fix(66K), WaveTrend(61.3K)가 비교표에 없었다.
2. **SuperTrend의 판(版)을 잘못 골랐다.** 같은 제작자(KivancOzbilgic)의 *지표판*은 84.3K인데, 롱·숏 가상매매용 *STRATEGY판*(25.1K)을 인용했다. 그 결과 Chandelier(29.7K)가 더 인기 있는 것처럼 보였다.
3. **포트폴리오 도구의 인기를 적지 않았다.** Portfolio Simulator는 772, BackQuant는 77이다. 둘 다 "좋아요를 많이 받은 기법"에는 해당하지 않는다.
4. **같은 계열 지표 두 개를 "확인"으로 썼다.** Chandelier와 SuperTrend는 둘 다 ATR 추적선이다. 둘의 일치는 독립적인 근거가 아니다(이전 문서도 이 점은 인정했다).

## 2. 평가 기준

중학생 비유로는 "**우리 집 상황(분기마다 바구니 크기를 점검하는 장기 투자)에 맞는 도구인가**"를 묻는 기준입니다. 인기가 높아도 단타용 도구라면 맞지 않습니다.

| # | 기준 | 왜 필요한가 |
|---|---|---|
| C1 | **목적 적합성** | "부족분을 채울까/초과분을 줄일까"를 판단하는 데 쓸 수 있는가 |
| C2 | **주봉 적합성** | 분 단위나 4시간 단위 매매용으로 설계됐다면 분기 점검에 맞지 않음 |
| C3 | **리페인트 없음** | 지나간 신호가 나중에 바뀌면 검증이 불가능함 |
| C4 | **설명 가능성** | 사용자가 이유를 이해할 수 있어야 직접 판단할 수 있음 |
| C5 | **역할 중복 없음** | 같은 정보를 두 번 보면 확신만 커지고 근거는 늘지 않음 |
| C6 | **재현성** | 오픈소스이거나 Pine 내장 함수여서 계산을 똑같이 재현할 수 있는가 |
| C7 | **인기(Boost)** | 많이 쓰이고 검토됐다는 1차 필터. **성과의 증거는 아님** |

## 3. 후보 15개 평가

Boost는 2026-10-27에 각 원문 페이지 상단에서 확인한 첫 번째 숫자다. 페이지에 라벨이 없어 Boost로 **추정**했다. 근거는 Chandelier의 수치가 10-26 조회값(29.1K)과 이어지는 29.7K라는 점이다.

| 스크립트 (제작자) | Boost | 계열 | C1 목적 | C2 주봉 | C3 리페인트 | 판정 |
|---|---:|---|---|---|---|---|
| [Smart Money Concepts](https://www.tradingview.com/script/CnB3fSph-Smart-Money-Concepts-SMC-LuxAlgo/) (LuxAlgo) | 176.6K | 시장구조·오더블록 | ✗ 단기 진입 자리 찾기 | △ | ○ | **제외** — 분기 리밸런싱과 무관한 단기 매매 도구 |
| [Squeeze Momentum](https://www.tradingview.com/script/nqQ1DT5a-Squeeze-Momentum-Indicator-LazyBear/) (LazyBear) | 117.6K | 변동성 수축 후 돌파 | ✗ 방향 중립, 돌파 시점용 | △ 주봉 신호 드묾 | ○ | **제외** — "채울까/줄일까"에 답하지 않음 |
| [SuperTrend](https://www.tradingview.com/script/r6dAP7yi/) (KivancOzbilgic) | **84.3K** | ATR 추적선 | ○ 추세 꺾임 | ○ | ○ 확정봉 사용 시 | **채택: 추세 지표** |
| [CM_Williams_Vix_Fix](https://www.tradingview.com/script/og7JPrRA-CM-Williams-Vix-Fix-Finds-Market-Bottoms/) (ChrisMoody) | **66K** | 공포(변동성) 급등 | ○ 하락 중 보충 판단 | ○ 원문은 일봉 설계, 주봉 검증 필요 | ○ | **채택: 공포 지표** |
| [WaveTrend](https://www.tradingview.com/script/2KE8wTuF-Indicator-WaveTrend-Oscillator-WT/) (LazyBear) | 61.3K | 과매수·과매도 | △ | △ | ○ | **제외** — 강한 추세에서 과열 신호가 계속 뜸. 과매도 역할은 Vix Fix가 더 직접적 |
| [UT Bot Alerts](https://www.tradingview.com/script/n8ss8BID-UT-Bot-Alerts/) (QuantNomad) | 61K | ATR 추적선 | ○ | ○ | ○ | **제외** — SuperTrend와 같은 계열(C5). 원본 전략의 알림 포장판 |
| [Lorentzian Classification](https://www.tradingview.com/script/WhBzgfDu-Machine-Learning-Lorentzian-Classification/) (jdehorty) | 37.2K | 머신러닝 분류 | △ | ✗ 4H~12H 최적화 | ○ | **제외** — 블랙박스(C4), 과최적화 위험 |
| [Nadaraya-Watson Envelope](https://www.tradingview.com/script/Iko0E2kL-Nadaraya-Watson-Envelope-LuxAlgo/) (LuxAlgo) | 35.3K | 커널 회귀 밴드 | △ | △ | ✗ 기본값이 리페인트 | **제외** (C3) |
| [Chandelier Exit](https://www.tradingview.com/script/AqXxNS7j-Chandelier-Exit-everget/) (everget) | 29.7K | ATR 추적선 | ○ | ○ | ○ | **백테스트 비교군으로 강등** |
| [Pivot Point SuperTrend](https://www.tradingview.com/script/L0AIiLvH-Pivot-Point-Supertrend/) (LonesomeTheBlue) | 29.5K | 피벗 + ATR | ○ | △ 피벗 확정 지연 | ○ | **제외** — SuperTrend 변형(C5) |
| [AlphaTrend](https://www.tradingview.com/script/o50NYLAZ-AlphaTrend/) (KivancOzbilgic) | 29.5K | ATR + RSI/MFI 혼합 | ○ | ○ | △ 장중 알림 옵션 | **제외** — 구성 요소가 많아 설명이 어려움(C4) |
| [Hull Suite](https://www.tradingview.com/script/hg92pFwS-Hull-Suite/) (InSilico) | 22.6K | 저지연 이동평균 | ○ | ○ | ○ | **제외** — 빠른 대신 잦은 방향 전환, 분기 운용에는 불리 |
| [QQE MOD](https://www.tradingview.com/script/TpUW4muw-QQE-MOD/) (Mihkel00) | 14K | RSI 변형 오실레이터 | △ | △ | ○ | **제외** — 단기 오실레이터 |
| [Portfolio Simulator](https://www.tradingview.com/script/kbaODuIz-Portfolio-Simulator-Backtester/) (HenriqueCentieiro) | 772 | 다자산 리밸런싱 백테스트 | ○ 직접 적합 | ○ | ○ | **검증 도구로 유지** — 인기 기법은 아님 |
| [Bracketed Rebalancing](https://www.tradingview.com/script/uTzHDFX6-Performance-Metrics-With-Bracketed-Rebalacing-BackQuant/) (BackQuant) | 77 | 임계값 리밸런싱 | ○ 아이디어 | ○ | ○ | **아이디어만 참고** (±5%p 밴드의 발상) |

**참고 (TradingView 커뮤니티 밖):** 40주(≈10개월) 이동평균 추세 필터. Faber의 *A Quantitative Approach to Tactical Asset Allocation*(2007, SSRN)에서 자산군별 낙폭을 줄이는 근거로 제시됐다. TradingView에 내장된 `ta.sma`로 바로 재현할 수 있다. Boost가 없는 대신 **학술 근거**가 있어 백테스트 비교군에 넣는다. 논문의 구체적 수치는 이번에 다시 확인하지 않았다(**검증 필요**).

## 4. 채택 지표 설명 (중학생 눈높이)

### 4.1 SuperTrend — "추세의 방향 표지판"

- **원리:** 가격 아래(상승 중) 또는 위(하락 중)에 "평소 흔들림(ATR)의 3배" 거리만큼 떨어진 선을 긋습니다. 종가가 그 선을 뚫고 반대로 넘어가면 방향이 바뀌었다고 봅니다.
- **설정:** 주봉, ATR 10주, 배수 3, 원문 기본 가격 `hl2`. 확정된 주봉만 사용합니다.
- **Chandelier 대신 이것을 고른 이유:**
  1. 같은 계열에서 인기가 가장 높습니다(84.3K 대 29.7K).
  2. Pine 내장 함수 `ta.supertrend()`와 계산이 같아서 **원본과 똑같이 재현하기 쉽습니다**(C6). 2단계의 "원본 대조" 작업이 단순해집니다.
  3. 이미 현재 Pine 코드에 들어 있어 바꿀 양이 적습니다.
- **한계:** 주봉 기준이라 느립니다. 이미 꽤 떨어진 뒤에야 "하락"으로 바뀔 수 있습니다.

### 4.2 Williams Vix Fix — "시장의 비명 측정기"

- **원리:** "최근 22기간 최고 종가에서 이번 저가까지 몇 % 떨어졌나"를 매번 계산합니다. 이 값이 평소보다 비정상적으로 커지면(볼린저 상단 또는 최근 최고치의 85% 이상) **공포 구간**으로 표시합니다.

  ```text
  WVF = (최근 22기간 최고 종가 − 이번 저가) ÷ 최근 22기간 최고 종가 × 100
  공포 구간 = WVF ≥ (WVF 20기간 평균 + 2 × 표준편차)  또는  WVF ≥ 최근 50기간 WVF 최고치 × 0.85
  ```
  위 식은 ChrisMoody 원문의 기본값(22/20/2.0/50/0.85)으로 알려진 값이며, **원문 소스와 다시 대조해야 합니다(검증 필요)**.
- **이것을 넣은 이유:** SuperTrend 같은 추세 지표는 바닥 근처에서 가장 늦습니다. 리밸런싱에서 가장 어려운 순간은 "**부족한 종목이 계속 떨어질 때 채울 것인가**"입니다. Vix Fix는 바로 그 상황에 "지금이 평범한 하락인가, 공포성 급락인가"라는 *다른 정보*를 줍니다(C5).
- **한계:** "바닥"을 맞히는 도구가 아닙니다. 공포 구간이 몇 주씩 이어지거나 더 깊어질 수 있습니다. 원문은 일봉용 설계이므로 주봉 적용은 백테스트로 확인해야 합니다. IEF(채권)와 IAUM(금)에서도 의미가 있는지는 미검증입니다.

## 5. 바뀌는 매수·매도 해석표 (제안, 미구현)

추세 지표가 하나로 줄어 "두 지표 엇갈림" 칸이 없어집니다. Vix Fix는 **부족한 종목이 하락 추세일 때만** 추가 정보로 씁니다.

| 비중 | SuperTrend (확정 주봉) | Vix Fix | 표시 | 의미 |
|---|---|---|---|---|
| 부족 | 상승 | — | 보충 검토 우호 | 채우는 방향과 추세가 같음 |
| 부족 | 하락 | 공포 구간 | **공포 구간 — 1차 분할 보충 검토** | 급락 중이므로 일부만 먼저 채우는 안을 검토 (가설) |
| 부족 | 하락 | 평상 | 분할·재확인 | 서서히 빠지는 중. 한 번에 채우지 않음 |
| 초과 | 하락 | — | 축소 검토 우선 | 초과분 축소와 추세가 같음 (전량 매도 아님) |
| 초과 | 상승 | — | 초과분만 검토 | 상승 중이어도 쏠림 위험 |
| 어느 쪽이든 | 자료 부족 | — | 추세 미확인 | 비중 판단만 사용 |

**지켜야 할 점:** Vix Fix는 목표비중을 바꾸지 않습니다. 매도 쪽 판단에도 쓰지 않습니다. 해외2는 현재 네 종목이 모두 부족한 상태(현금 전액 포함 기준)라서, 다음 분기에는 Vix Fix가 실제로 쓰일 가능성이 있습니다.

## 6. 백테스트에서 확인할 것 (계획안 Phase 3 반영)

| 비교 | 질문 |
|---|---|
| SuperTrend vs Chandelier vs 40주 SMA | 같은 분기+밴드 규칙에서 어느 추세 지표가 MDD·회전율 면에서 나은가. **SuperTrend가 지면 교체한다** |
| Vix Fix 공포 구간 1차 분할 vs 그냥 분할 vs 즉시 전액 | 공포 구간 정보가 하락 중 보충의 낙폭·회복기간을 실제로 개선하는가 |
| Vix Fix 주봉 vs 일봉 | 원문 설계(일봉)와 주봉 적용의 차이 |
| 자산별 Vix Fix | 주식(SCHD·QQQM)에서만 의미가 있는가, 채권·금에도 쓸 수 있는가 |

결과가 기준선(분기+밴드, 추세 미사용)보다 낫지 않으면 **지표를 화면 참고용으로만 두는 것이 정상 결론**입니다.

## 7. 반영 상태 (2026-10-27 사용자 승인 후 구현)

1. ✅ Pine v0.3: Chandelier 계산·표시 제거, SuperTrend 주 지표화(조기 점검 후보의 주봉 전환도 SuperTrend 기준), Vix Fix 공포 구간 열과 §5 해석 문구 추가, 현금 정책 경고 추가
2. ✅ Python 참조 규격 `vix_fix()`, `interpret()` 추가. 테스트 17개에서 22개로 늘었고 모두 통과
3. ✅ 설명서·README·PRD·계획안 갱신
4. ⬜ Chandelier 비교는 Phase 3 백테스트(Python)에서 구현한다. Pine에는 남기지 않았다.
5. ⬜ Pine 컴파일과 원본 지표 대조는 TradingView 로그인이 필요하다.

**테스트에서 확인한 Vix Fix의 성질:** 기준이 "최근 50기간과의 상대 비교"라서, 변동이 거의 없는 시기에는 작은 하락도 공포 구간으로 판정될 수 있다. 원문 설계에서 나오는 성질이며, 주봉 백테스트에서 오탐 빈도를 확인해야 한다.

## 출처

모든 TradingView 페이지는 2026-10-27에 조회했다. Boost는 페이지 상단의 라벨 없는 첫 숫자를 추정한 값이며, 이후 바뀔 수 있다.

- 표 §3의 각 링크 (TradingView 스크립트 원문)
- Faber, M. (2007). *A Quantitative Approach to Tactical Asset Allocation*. SSRN — 이번에 재조회하지 않음 (**검증 필요**)
- 이전 판단: [Pine 설명서](quarterly_etf_pine_guide_2026-10-26.md), [PRD §3](../PRD.md)
