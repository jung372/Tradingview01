# 해외2 계정용 ETF 구현 결과

새 계정용 스크립트는 [quarterly_etf_account.pine](../pine/quarterly_etf_account.pine)이다. 기존 전략 검토용 `quarterly_etf_review.pine`과 구분한다.

Stock_Trading_Log의 전용 Balance, 실제 원장 기반 스냅샷, 분기 판단·수량 계산, 웹훅 검증·수신, 동기화 순서 제어를 구현했다. 세부 설치와 검증 기록은 별도 로컬 저장소 `Stock_Trading_Log/docs/etf-tradingview.md`에 있다. 해당 파일은 이 GitHub 저장소의 push에 포함되지 않는다.

현재는 **로컬 코드 및 차트 컴파일 검증 단계**다. 실제 TradingView 무인 화면 어댑터는 아직 구현하지 않았으며 잔고 자료가 자동 전송되지 않는다. Basic 계정의 기술적 알림 및 새 스크립트 저장 제한을 확인했고, 사용자 결정에 따라 업그레이드와 실알림 시험을 뒤로 미뤘다. 업그레이드 후 G0 버전 교체 시험, 화면 어댑터 구현·연결, HTTPS relay 배포와 실제 수신 검증이 남아 있다.

후보 A 기본 설정: SCHD 10% / QQQM 45% / IEF 25% / IAUM 20%, 절대 이탈폭 5%p. 매매 필요 조건에서만 운영 신호를 발생시킨다. 분기 마지막 정규장 종가를 다음 분기 첫 거래일의 60분 확정 봉에서 판단하며, 실제 주문을 자동 제출하지 않는다. 실거래는 수기로 원장에 기록한다.
