# TradingView_01

## 대화 이력

- [1차: 알고리즘 초안과 설계 근거 (2026-10-26)](reports/overseas2_algorithm_conversation_history_2026-10-26.md)
- [2차: 현금 정책 확정과 지표 재선정 (2026-10-27)](reports/overseas2_algorithm_conversation_history_2026-10-27.md)
- [3차: 기존 결정 확인과 GitHub 보관 (2026-11-01)](reports/overseas2_algorithm_conversation_history_2026-11-01.md)

## 2026-10-27 v0.3

- 지표 재선정: 추세 지표는 SuperTrend 지표판(KivancOzbilgic, 84.3K) 하나만 쓰고, 공포 지표로 CM_Williams_Vix_Fix(66K)를 추가했다. Chandelier는 백테스트 비교군으로 돌렸다. 근거: [재선정 보고서](reports/tradingview_algorithm_reselection_2026-10-27.md)
- 해외2 현금 정책: **전액 투자 재원 포함**(별도 현금 0). 0이 아닌 값을 넣으면 화면에 경고가 뜬다.
- 계획: [구축 계획안](reports/overseas2_algorithm_build_plan_2026-10-27.md)
- 검증: `python -m unittest discover -s tests -v` — 22개 통과. Pine 컴파일·실차트·알림·성과는 여전히 미검증.

## 2026-10-26 Pine Script 초안

- [Pine v6 스크립트](pine/quarterly_etf_review.pine): 네 ETF 비중·분기 점검·확정 주봉 Chandelier·SuperTrend 비교. 수량/현금은 직접 입력하며 자동주문 기능은 없다.
- [초보자용 원리·매수/매도 검토·설치 설명서](reports/quarterly_etf_pine_guide_2026-10-26.md)
- [해외2 화면 확인 기록 — 개인 금융정보 포함](reports/overseas2_snapshot_2026-10-26.md)
- 검증: `python -m unittest discover -s tests -v` — 17개 통과. Python 참조 규격·정적 소스 검사이며 **Pine 컴파일·실차트·알림 수신·투자 성과는 미검증**. TradingView 차트 추가 시 로그인 요구를 확인했다.

현재 구현은 PRD의 읽기 전용 화면에 해당하는 부분 초안이다. MDD 연구·성과 승인·조기 알림 출시 게이트를 통과한 운영 버전은 아니다. 현금 포함 여부에 따라 판단이 달라지므로 실제 사용 전 설정을 확인한다.

현재 목표는 **SCHD 25% / QQQM 25% / IEF 30% / IAUM 20%** 포트폴리오의 **MDD를 우선**하여 리밸런싱 *검토 시점*을 안내하는 시스템이다. 주문 실행·증권사 주문 API·자동매매는 범위에 포함하지 않는다.

개발의 기준 문서는 [PRD](PRD.md)다. [선행 개발 방향](reports/mdd_first_rebalancing_timing_advisor_2026-09-21.md)을 기능·데이터·알고리즘·검증·출시 게이트로 구체화했다. 사용자 후속 요청으로 티커와 MDD 우선 목표가 확정되었다. 방어형 대안 비중은 **미검증 가설**이며, 데이터 검증 전에는 최적 비중이나 실거래 권고로 취급하지 않는다.

이전 [전략 조사 보고서](reports/tradingview_all_weather_rebalancing_report_2026-09-21.md)와 [자동매매 가능성 검토](reports/tradingview_automation_feasibility_2026-09-21.md)는 조사 이력이다. 구현 시에는 현재 기준 문서의 범위와 검증 조건을 따른다.
