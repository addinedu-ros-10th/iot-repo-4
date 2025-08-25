# Flutter 프로젝트 관리 Makefile
# 사용법: make <target>

# 기본 설정
FLUTTER_PROJECT_DIR := $(shell pwd)
FLUTTER_CMD := flutter
DEFAULT_PORT := 8084

# 색상 정의
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[1;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

# 기본 타겟
.PHONY: help
help: ## 도움말 표시
	@echo "$(BLUE)🚀 Flutter 프로젝트 관리 명령어$(NC)"
	@echo "=================================="
	@echo "$(GREEN)사용법: make <target>$(NC)"
	@echo ""
	@echo "$(YELLOW)개발 명령어:$(NC)"
	@echo "  run        - Chrome에서 Flutter 앱 실행"
	@echo "  run-web    - 웹 브라우저에서 Flutter 앱 실행"
	@echo "  run-mobile - 모바일 디바이스에서 Flutter 앱 실행"
	@echo ""
	@echo "$(YELLOW)빌드 명령어:$(NC)"
	@echo "  build-web  - 웹용 빌드"
	@echo "  build-apk  - Android APK 빌드"
	@echo "  build-ios  - iOS 빌드"
	@echo ""
	@echo "$(YELLOW)유지보수 명령어:$(NC)"
	@echo "  clean      - 빌드 파일 정리"
	@echo "  get        - 의존성 설치"
	@echo "  doctor     - Flutter 환경 진단"
	@echo "  analyze    - 코드 분석"
	@echo "  test       - 테스트 실행"
	@echo ""
	@echo "$(YELLOW)경로 확인:$(NC)"
	@echo "  check-path - 현재 경로 및 Flutter 프로젝트 확인"
	@echo "  fix-path   - 경로 문제 자동 수정"

# 경로 확인
.PHONY: check-path
check-path: ## 현재 경로 및 Flutter 프로젝트 확인
	@echo "$(BLUE)🔍 경로 확인 중...$(NC)"
	@echo "현재 경로: $(YELLOW)$(FLUTTER_PROJECT_DIR)$(NC)"
	@if [ -f "pubspec.yaml" ]; then \
		echo "$(GREEN)✅ Flutter 프로젝트가 확인되었습니다.$(NC)"; \
	else \
		echo "$(RED)❌ 현재 디렉토리는 Flutter 프로젝트가 아닙니다!$(NC)"; \
		echo "$(YELLOW)올바른 Flutter 프로젝트 경로로 이동해주세요.$(NC)"; \
		exit 1; \
	fi

# 경로 자동 수정
.PHONY: fix-path
fix-path: ## 경로 문제 자동 수정
	@echo "$(BLUE)🔧 경로 문제 자동 수정 중...$(NC)"
	@if [ ! -f "pubspec.yaml" ]; then \
		echo "$(YELLOW)Flutter 프로젝트를 찾는 중...$(NC)"; \
		cd /Users/emotionalmachine/Documents/AddInEdu/Project/apps/user_app 2>/dev/null || \
		cd /Users/$(USER)/Documents/AddInEdu/Project/apps/user_app 2>/dev/null || \
		cd /home/$(USER)/Documents/AddInEdu/Project/apps/user_app 2>/dev/null || \
		(echo "$(RED)Flutter 프로젝트를 찾을 수 없습니다.$(NC)" && exit 1); \
		echo "$(GREEN)✅ 경로를 수정했습니다: $(shell pwd)$(NC)"; \
	fi

# 의존성 설치
.PHONY: get
get: check-path ## 의존성 설치
	@echo "$(BLUE)📦 의존성 설치 중...$(NC)"
	$(FLUTTER_CMD) pub get

# Flutter 환경 진단
.PHONY: doctor
doctor: check-path ## Flutter 환경 진단
	@echo "$(BLUE)🏥 Flutter 환경 진단 중...$(NC)"
	$(FLUTTER_CMD) doctor

# 코드 분석
.PHONY: analyze
analyze: check-path ## 코드 분석
	@echo "$(BLUE)🔍 코드 분석 중...$(NC)"
	$(FLUTTER_CMD) analyze

# 테스트 실행
.PHONY: test
test: check-path ## 테스트 실행
	@echo "$(BLUE)🧪 테스트 실행 중...$(NC)"
	$(FLUTTER_CMD) test

# 빌드 파일 정리
.PHONY: clean
clean: check-path ## 빌드 파일 정리
	@echo "$(BLUE)🧹 빌드 파일 정리 중...$(NC)"
	$(FLUTTER_CMD) clean

# Chrome에서 실행
.PHONY: run
run: check-path ## Chrome에서 Flutter 앱 실행
	@echo "$(BLUE)🌐 Chrome에서 Flutter 앱 실행 중...$(NC)"
	@echo "포트: $(DEFAULT_PORT)"
	@echo "$(YELLOW)중단하려면 Ctrl+C를 누르세요.$(NC)"
	$(FLUTTER_CMD) run -d chrome --web-port=$(DEFAULT_PORT)

# 웹에서 실행
.PHONY: run-web
run-web: check-path ## 웹 브라우저에서 Flutter 앱 실행
	@echo "$(BLUE)🌐 웹 브라우저에서 Flutter 앱 실행 중...$(NC)"
	@echo "포트: $(DEFAULT_PORT)"
	@echo "$(YELLOW)중단하려면 Ctrl+C를 누르세요.$(NC)"
	$(FLUTTER_CMD) run -d web-server --web-port=$(DEFAULT_PORT)

# 모바일에서 실행
.PHONY: run-mobile
run-mobile: check-path ## 모바일 디바이스에서 Flutter 앱 실행
	@echo "$(BLUE)📱 모바일 디바이스에서 Flutter 앱 실행 중...$(NC)"
	@echo "$(YELLOW)중단하려면 Ctrl+C를 누르세요.$(NC)"
	$(FLUTTER_CMD) run

# 웹용 빌드
.PHONY: build-web
build-web: check-path ## 웹용 빌드
	@echo "$(BLUE)🌐 웹용 빌드 중...$(NC)"
	$(FLUTTER_CMD) build web

# Android APK 빌드
.PHONY: build-apk
build-apk: check-path ## Android APK 빌드
	@echo "$(BLUE)🤖 Android APK 빌드 중...$(NC)"
	$(FLUTTER_CMD) build apk

# iOS 빌드
.PHONY: build-ios
build-ios: check-path ## iOS 빌드
	@echo "$(BLUE)🍎 iOS 빌드 중...$(NC)"
	$(FLUTTER_CMD) build ios

# 포트 확인
.PHONY: check-port
check-port: ## 포트 사용 상태 확인
	@echo "$(BLUE)🔍 포트 사용 상태 확인 중...$(NC)"
	@if lsof -Pi :$(DEFAULT_PORT) -sTCP:LISTEN -t >/dev/null 2>&1; then \
		echo "$(RED)❌ 포트 $(DEFAULT_PORT)가 이미 사용 중입니다.$(NC)"; \
		echo "$(YELLOW)사용 중인 프로세스:$(NC)"; \
		lsof -Pi :$(DEFAULT_PORT) -sTCP:LISTEN; \
	else \
		echo "$(GREEN)✅ 포트 $(DEFAULT_PORT)를 사용할 수 있습니다.$(NC)"; \
	fi

# 전체 설정
.PHONY: setup
setup: check-path get doctor ## 전체 설정 (의존성 설치 + 환경 진단)
	@echo "$(GREEN)✅ 설정이 완료되었습니다.$(NC)"

# 개발 시작
.PHONY: dev
dev: setup run ## 개발 시작 (설정 + 실행)
	@echo "$(GREEN)🚀 개발이 시작되었습니다.$(NC)"
