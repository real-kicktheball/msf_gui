🛡️ Kali Linux MSF Control Center
Metasploit Framework GUI Wrapper for Payload Building & Listening > 본 도구는 Kali Linux 환경에서 msfvenom 페이로드 생성과 msfconsole 리스너 구동을 하나의 GUI 인터페이스에서 관리할 수 있도록 설계된 Python 기반 애플리케이션입니다.

🚀 핵심 기능
GUI 기반 페이로드 생성: 명령어를 외울 필요 없이 LHOST, LPORT, 페이로드 타입, 포맷을 선택하여 즉시 msfvenom 명령 실행.

멀티 플랫폼 지원: Windows, Linux, Android, PHP 등 주요 환경에 맞는 다양한 페이로드 프리셋 제공.

원클릭 리스너 실행: 설정된 정보를 바탕으로 새 터미널에서 msfconsole 핸들러(exploit/multi/handler) 자동 실행.

실시간 로그 모니터링: 내부 텍스트 박스를 통해 페이로드 생성 과정을 실시간으로 확인 가능.

사용자 친화적 인터페이스: CustomTkinter를 활용한 모던한 다크 모드 UI 적용.

🛠 설치 및 요구 사항
1. 시스템 요구 사항
OS: Kali Linux (또는 Metasploit이 설치된 Linux 환경)

Terminal: qterminal (코드 내 기본 설정) 또는 x-terminal-emulator

2. 파이썬 라이브러리 설치
프로그램 실행을 위해 아래 라이브러리가 필요합니다.

Bash
pip install customtkinter
3. 실행 방법
Bash
python msf_control_center.py
📖 사용 방법
Network Setting: 공격자의 IP(LHOST)와 수신 대기할 포트(LPORT)를 입력합니다.

Option Setting: 타겟 시스템에 맞는 페이로드 종류와 파일 포맷(exe, apk, elf 등)을 선택합니다.

Save Path: Browse 버튼을 눌러 페이로드 파일이 저장될 위치와 이름을 지정합니다.

Generate: GENERATE PAYLOAD 버튼을 클릭하여 파일을 생성합니다.

Listen: 생성이 완료되면 START LISTENER를 눌러 세션 연결을 대기하는 터미널을 실행합니다.

⚠️ 법적 고지 (Legal Disclaimer)
본 도구는 교육적 목적 및 승인된 환경에서의 모의 침투 테스트를 위해 제작되었습니다.

허가되지 않은 시스템에 대한 접근이나 공격은 엄격히 금지됩니다.

본 소프트웨어의 오남용으로 인해 발생하는 모든 법적 책임은 사용자에게 있습니다.

📄 라이선스
이 프로젝트는 MIT 라이선스를 따릅니다. 개인적인 커스터마이징 및 배포가 자유롭습니다.
