# 주식·AI 투자에서 TradingView를 활용하는 실제 사례 조사

조사 기준: 2026-11-02. 공개 사용자 스크립트는 **제작자가 제시한 사용법**의 사례다. 실제 거래 성과나 제3자의 사용 규모를 입증하지 않는다. 기능과 요금 조건은 TradingView 공식 설명을 기준으로 확인했다. 개인 계좌의 실제 수익·잔고는 조사 대상에 포함하지 않았다.

## 먼저 결론

TradingView의 실용적인 역할은 세 가지다. (1) 많은 종목을 빠르게 좁히는 탐색 화면, (2) 투자 규칙을 눈으로 확인하고 가상으로 시험하는 실험실, (3) 가격·이벤트 감시 화면이다. 실제 거래·배당 원장, 환전, 세금, 체결 후 수량은 별도의 원장으로 관리하는 편이 사용자님의 현재 구조와 맞는다. AI는 TradingView 자료를 읽고 후보를 정리하거나 Pine 초안을 만드는 데 쓸 수 있다. AI 출력만으로 거래를 확정하지 않는다.

| 사용 목적 | 다른 투자자의 공개 활용 사례 | 사용자님에게 적합도 | 시작 비용 |
|---|---|---|---|
| 장기 ETF 배분 비교 | 다자산 포트폴리오 시뮬레이터 | 높음 | 무료 화면부터 시험 |
| 리밸런싱 기준 시각화 | 비중 이탈·낙폭 지표 | 높음 | 수동 확인은 무료, 스크립트 알림은 유료 |
| 개별 주식 후보 발굴 | 스크리너→관심목록→차트 | 중간 | 기본 스크리너부터 시험 |
| 실적 발표 후 단기 매매 | 실적 갭·거래량 지표 | 낮음~중간 | 화면 확인은 무료, 지표 알림은 유료 |
| 상대강도 순위·자산 교체 | 자산군 순위 지표 | 연구용 | 수동 비교부터 시험 |
| AI에게 화면 작업 요청 | AI Screener, AI Copilot, MCP | 현재 낮음 | 유료 기능 포함 |
| 실계좌 원장 복제 | TradingView Portfolios CSV | 낮음 | 중복 관리 비용 발생 |

## 사례 1. 장기 투자자가 배분안을 차트로 비교

공개 지표 [Portfolio Simulator & Backtester](https://www.tradingview.com/script/kbaODuIz-Portfolio-Simulator-Backtester/)의 제작자는 최대 5개 자산의 비중을 입력하고, 적립식 투자·월/분기/연 리밸런싱·거래비용을 바꿔 보며 CAGR와 최대낙폭 등을 비교하도록 설계했다. 또 다른 [Portfolio Backtester](https://www.tradingview.com/script/GDaKbVW2-Portfolio-Backtester-MS/)는 여러 배분을 차트 한 화면에 겹쳐 비교하는 사용법을 소개한다.

사용자님에게 적용하면 SCHD·QQQM·IEF·IAUM의 후보 A와 B/C/D를 같은 시작일, 같은 비용, 같은 현금흐름으로 겹쳐 볼 수 있다. “QQQM 45%가 40%보다 언제 더 위험했는가”, “분기와 연간 조정의 거래 횟수 차이는 얼마인가”처럼 PPT의 숫자가 발생한 기간을 눈으로 찾는 용도다. 다만 위 첫 번째 제작자의 지표 설명은 기능 소개이며 검증된 미래 수익이 아니다. 두 번째 지표는 제작자가 배당·수수료 등을 계산하지 않는다고 명시한다. 사용자님의 원장과 과거 검토 계산이 성과 판단의 기준이어야 한다.

## 사례 2. 비중 이탈을 차트에서 감시

[Institutional Portfolio Timeline Suite](https://www.tradingview.com/script/qA0GV6U8-Institutional-Portfolio-Timeline-Suite-JOAT/) 제작자는 목표 비중에서 벗어난 종목이 있을 때 리밸런싱 신호를 내고, 낙폭 경계도 표시하는 사용법을 공개했다. [Smart Rebalance](https://www.tradingview.com/script/mBiy1SMv-Smart-Rebalance/)는 가격 변화와 목표 배분을 입력해 조정이 발생하는 모습을 보여주는 또 다른 사례다.

이 접근은 사용자님의 ±5%p 규칙을 설명하는 시각 자료로 유용하다. 다만 차트 지표의 가상 수량과 실제 증권사 체결 수량은 다를 수 있다. 배당, 수수료, 환전도 실제 원장에서 맞춰야 한다. **현재 Basic에는 Pine 지표를 조건으로 하는 기술적 알림이 없으므로**, 무료 계정에서는 화면 확인·연구용으로만 활용하는 것이 현실적이다. [공식 요금표](https://www.tradingview.com/pricing/)

## 사례 3. 실적 발표 후 주식을 선별하는 투자자

[Power Earnings Gap & HVE](https://www.tradingview.com/script/pjwCxbrn-Power-Earnings-Gap-PEG-HVE/) 제작자는 실적 발표 후 큰 상승 갭, 평소보다 많은 거래량, 200일 이동평균 위 가격, 종가 위치를 묶어 관심종목을 찾는다. 스크립트에는 새로운 실적 갭이나 최고 거래량을 알리는 조건도 있다. TradingView의 [주식 스크리너](https://www.tradingview.com/support/solutions/43000718866-tradingview-stock-screener-trade-smarter-not-harder/)는 시가총액·상대 거래량·실적 관련 지표로 넓은 후보를 좁힐 수 있다.

실제 활용 흐름은 “실적 발표 예정 종목 목록 → 실적 발표 → 거래량·갭 조건 충족 종목 확인 → 공시와 사업 내용을 별도 검토”다. 사용자님이 장기 ETF만 운용한다면 이 사례의 직접 효용은 낮다. 향후 개별 성장주나 국내 가치주를 별도 계정에서 발굴한다면 유용할 수 있다. 거래량 급증 자체가 좋은 기업이나 좋은 매수가를 뜻하지는 않는다.

실제 이용자가 공개한 [INTC 실적 갭 분석 흐름](https://www.reddit.com/r/TradingView/comments/1sypdof/how_i_use_tradingview_to_frame_postearnings_gap/)은 더 구체적이다. 작성자는 일봉에서 실적 갭과 과거 저항선을 보고, 1시간봉에서 갭이 유지되는지 확인한 뒤, 5분봉으로 진입 시점을 살핀다. 별도 화면에는 반도체 ETF와 동종주를 함께 띄우고, 갭 지지선 아래로 떨어질 때 알림을 받는다고 설명한다. 이는 **작성자의 자기보고 사례**이며 실제 성과는 확인되지 않았다. 사용자님처럼 분기 ETF를 보유하는 투자자에게 5분 진입 화면은 오히려 불필요할 수 있다.

## 사례 4. 상대강도로 자산을 돌려 보유하는 연구자

공개 지표 [Custom Portfolio](https://www.tradingview.com/script/O4HO54TJ-Custom-Portfolio-BackQuant/) 제작자는 여러 자산의 상대강도를 순위화하고 강한 종목으로 가상 배분하는 방식을 소개한다. 다른 [Momentum Portfolio Rotation](https://www.tradingview.com/script/2HzGUS1E/)은 정해진 자산군의 과거 모멘텀을 비교해 상위 자산을 선택하고 정해진 시점에 교체한다.

사용자님에게는 후보 A를 바로 교체하기보다 “고정 비중 대비 추세 필터를 추가하면 낙폭·회전율이 어떻게 바뀌는가”를 연구하는 용도가 적합하다. 종목 수, 관찰기간, 신호 지연, 거래비용을 바꾸면 결과가 크게 달라질 수 있다. 모멘텀 상위 종목을 매일 갈아타는 전략은 분기 4 ETF 목표 배분과 다른 의사결정이므로 별도 실험으로 분리해야 한다.

## 사례 5. 스크리너와 관심목록을 조사 노트처럼 사용

공식 [주식 스크리너](https://www.tradingview.com/support/solutions/43000718866-tradingview-stock-screener-trade-smarter-not-harder/)는 시장·유동성·재무·기술 지표를 조합해 후보를 좁힌다. [ETF 스크리너](https://www.tradingview.com/support/solutions/43000718743-tradingview-etf-screener-your-shortcut-to-top-funds/)는 운용자산, 자금 유출입, 배당, NAV 성과, 위험 지표를 비교할 수 있다. [관심목록 고급 화면](https://www.tradingview.com/support/solutions/43000745825-mastering-the-tradingview-watchlists/)에는 종목별 실적 일정·배당 일정·뉴스와 개인 메모가 있다.

예를 들어 QQQM 대체 후보 ETF를 조사할 때 유사 지수 추종 ETF를 먼저 모은 뒤 규모·유동성·배당·위험 지표를 비교하고, 최종 후보만 차트에 겹쳐 보는 식이다. 주식 발굴에서는 “현금흐름과 성장률이 좋은 후보”를 거른 뒤 기존 Stock_Data_Evaluation의 원천·연결 재무제표 검증을 붙일 수 있다. 화면 수치는 출처와 기준일을 확인하고, 최종 기업평가는 기존 분석 DB에서 재현하는 것이 안전하다.

## 사례 6. AI로 탐색 조건을 만들고 검증

TradingView [AI Screener](https://www.tradingview.com/support/solutions/43000785770-how-to-use-the-ai-screener/)는 “일정 시장에서 50일선이 200일선을 상향 돌파한 종목” 같은 문장을 실제 스크리너 필터·열·정렬로 바꾼다. 결과 화면에서 AI가 적용한 조건을 확인하고 바꿀 수 있다. 공식 설명상 공개 베타이며 유료 플랜에서 요청 횟수 제한이 있다. 따라서 AI가 찾아준 종목을 그대로 매수하는 기능이라기보다 **필터 설정을 빨리 만드는 도구**다.

[AI Copilot](https://www.tradingview.com/support/solutions/43000795131-getting-started-with-ai-copilot/)은 현재 차트의 시세·지표·재무·뉴스를 읽고 질문에 답하거나 차트 작업을 수행한다. 다만 기본 유료 플랜 위에 **별도 월 구독 추가 기능**이며, 공식 설명도 답변 오류·자료 지연 가능성을 명시한다. [공식 MCP](https://www.tradingview.com/mcp/docs)는 Essential 이상에서 AI 도구가 TradingView 데이터·관심목록·단순 가격 알림을 다루게 하지만, Pine 지표 알림이나 웹훅 알림 생성은 지원하지 않는다. 사용자님이 이 서비스를 거의 쓰지 않는 현재에는 세 AI 기능 모두 구독 이유가 약하다.

유료 기능 없이도 AI와 TradingView를 함께 쓸 수 있다. 사용자가 무료 스크리너에서 만든 후보표나 차트 정보를 AI에게 주고, AI가 후보별 투자 가설·반대 증거·확인할 공시를 정리하게 하는 방식이다. 화면 데이터가 AI에게 자동 전달되는 것은 아니며, 숫자와 날짜는 원천에서 확인해야 한다.

## 사례 7. 실거래와 별도로 모의 전략을 검증

TradingView [전략 테스트](https://www.tradingview.com/support/solutions/43000562362-what-are-strategies-backtesting-and-forward-testing/)는 Pine 규칙으로 가상 매매를 실행해 거래 목록과 성과를 보여준다. 실제 투자자는 200일선 이탈 시 위험 노출을 줄이는 규칙, 특정 종목 진입·청산 규칙 등을 과거와 이후 데이터에서 비교할 수 있다. 사용자의 4 ETF 배분도 “분기말 전체 조정”과 “연간 조정”의 가상 비교를 차트에서 볼 수 있다.

단, 이 결과는 증권사 체결 기록이 아니다. TradingView는 [미래 데이터가 과거에 새어 들어가는 문제](https://www.tradingview.com/support/solutions/43000614705-strategy-produces-unrealistically-good-results-by-peeking-into-the-future/)와 비표준 차트의 비현실적인 체결 결과를 경고한다. 비용·미끄러짐·배당·환율·세금, 대체 ETF의 상장 전 자료를 명시하지 않으면 사용자님의 PPT 연구 결과와 같은 수치가 나오지 않는다.

한 [개인 전략 제작자](https://www.reddit.com/r/TradingView/comments/1jdyi67/a_strategy_i_built_for_myself_just_shows_when_the/)는 AI/GPT로 상승 추세를 찾는 규칙을 만들고 Pine 전략으로 거래 시점을 시험한다고 소개했다. 같은 글에서 횡보 구간의 과도한 거래와 Heikin Ashi 차트의 체결 왜곡을 논의한다. 이 사례의 핵심은 AI가 만든 규칙을 바로 신뢰하지 않고, 원시 가격·비용·실시간 성능을 다시 확인해야 한다는 점이다. 글 속 성과 숫자는 검증되지 않아 보고서의 성과 근거로 사용하지 않았다.

## TradingView Portfolios는 원장 대체보다 비교 화면

[TradingView Portfolios](https://www.tradingview.com/support/solutions/43000760937-tradingview-portfolios-track-your-assets-know-your-trades/)는 보유·거래·수익률·위험 지표와 벤치마크 비교를 제공한다. [CSV 가져오기](https://www.tradingview.com/support/solutions/43000756010-how-to-create-a-portfolio-via-transaction-import/)에는 매매뿐 아니라 배당·분할·현금 입출금 형식도 있다. 따라서 Stock_Trading_Log에서 CSV를 만들어 **읽기 전용 비교본**을 만드는 것은 가능하다. 다만 공식 가져오기는 업로드 작업이며 자동 양방향 원장 동기화로 설명되지 않는다. 사용자의 수기 원장을 두 군데에서 수정하면 차이가 생긴다.

## 사용자님에게 권하는 무료 시험 순서

1. 현재 4 ETF만 관심목록에 두고 주간 차트와 ETF 스크리너에서 가격, 배당, 자금 유출입, 변동성을 비교한다. 매매 판단은 아직 바꾸지 않는다.
2. 공개 포트폴리오 시뮬레이터를 후보 A와 비교안으로 **연구용**으로 돌린다. 기존 PPT의 동일 기간·비용·배당 조건과 일치하는지 확인한다. 일치하지 않으면 원인을 기록한다.
3. 4주간 TradingView에서 새로 발견한 정보가 실제 의사결정을 바꿨는지 메모한다. 예: “QQQM 변동성 체감”, “SCHD 배당 일정”, “IEF 금리 이벤트”. 이 기간에는 구독이나 자동 알림 구축을 추가하지 않는다.
4. 실계좌 관리는 Stock_Trading_Log의 해외2 거래·배당 원장에 유지한다. 리밸런싱 필요 알림은 원장 계산 결과에서 직접 보내는 방향이 더 간단하다.

4주 후 판단 기준은 단순하다. 차트·스크리너만 가끔 본다면 무료 사용을 유지한다. 매주 여러 종목에 커스텀 지표 알림을 반복적으로 쓰거나 AI Screener/MCP가 실제 분석 시간을 줄인다는 증거가 있으면 그때 플랜을 다시 비교한다. Essential 가입만으로 원장 자동 연결이 완성되지는 않는다.

## 근거의 범위

공개 스크립트 설명과 공식 기능 문서는 **무슨 작업을 할 수 있는지** 보여준다. 이 조사에는 사용자별 실제 수익률, 전략의 위험조정 초과성과, AI 추천의 정확도를 입증하는 자료가 없다. 그러므로 특정 공개 지표의 백테스트나 제작자 표현을 투자 성과 증거로 사용하지 않았다. 가격·플랜·기능 지원 여부는 변경될 수 있으므로 실제 구독 직전에 [공식 요금표](https://www.tradingview.com/pricing/)를 다시 확인한다.
