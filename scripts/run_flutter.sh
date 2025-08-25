#!/bin/bash

# Flutter 앱 실행 스크립트
# 이 스크립트는 올바른 Flutter 프로젝트 경로에서 실행되도록 보장합니다.

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Flutter 앱 실행 스크립트${NC}"
echo "=================================="

# 현재 경로 확인
CURRENT_DIR=$(pwd)
echo -e "현재 경로: ${YELLOW}$CURRENT_DIR${NC}"

# Flutter 프로젝트인지 확인
if [ ! -f "pubspec.yaml" ]; then
    echo -e "${RED}❌ 현재 디렉토리는 Flutter 프로젝트가 아닙니다!${NC}"
    echo -e "${YELLOW}올바른 Flutter 프로젝트 경로로 이동합니다...${NC}"
    
    # 프로젝트 루트에서 Flutter 프로젝트 찾기
    PROJECT_ROOT="/Users/emotionalmachine/Documents/AddInEdu/Project"
    FLUTTER_PROJECT="$PROJECT_ROOT/apps/user_app"
    
    if [ -d "$FLUTTER_PROJECT" ]; then
        echo -e "${GREEN}✅ Flutter 프로젝트를 찾았습니다: $FLUTTER_PROJECT${NC}"
        cd "$FLUTTER_PROJECT"
        echo -e "${GREEN}✅ 경로를 변경했습니다: $(pwd)${NC}"
    else
        echo -e "${RED}❌ Flutter 프로젝트를 찾을 수 없습니다!${NC}"
        echo -e "${YELLOW}수동으로 올바른 경로로 이동해주세요.${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ Flutter 프로젝트가 확인되었습니다.${NC}"
fi

# Flutter 환경 확인
echo -e "\n${BLUE}🔍 Flutter 환경 확인 중...${NC}"
if ! command -v flutter &> /dev/null; then
    echo -e "${RED}❌ Flutter가 설치되지 않았습니다!${NC}"
    echo -e "${YELLOW}Flutter를 설치하거나 PATH에 추가해주세요.${NC}"
    exit 1
fi

# Flutter doctor 실행
echo -e "\n${BLUE}🏥 Flutter Doctor 실행 중...${NC}"
flutter doctor

# 의존성 설치 확인
echo -e "\n${BLUE}📦 의존성 설치 확인 중...${NC}"
if [ ! -d ".dart_tool" ] || [ ! -f "pubspec.lock" ]; then
    echo -e "${YELLOW}⚠️  의존성이 설치되지 않았습니다. 설치를 시작합니다...${NC}"
    flutter pub get
fi

# 포트 확인 및 설정
PORT=${1:-8084}
echo -e "\n${BLUE}🌐 포트 $PORT에서 Chrome으로 실행합니다...${NC}"

# 포트 사용 중인지 확인
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
    echo -e "${YELLOW}⚠️  포트 $PORT가 이미 사용 중입니다. 다른 포트를 시도합니다...${NC}"
    PORT=$((PORT + 1))
    echo -e "${GREEN}✅ 포트 $PORT를 사용합니다.${NC}"
fi

# Flutter 앱 실행
echo -e "\n${GREEN}🚀 Flutter 앱을 실행합니다...${NC}"
echo -e "${BLUE}명령어: flutter run -d chrome --web-port=$PORT${NC}"
echo -e "${YELLOW}중단하려면 Ctrl+C를 누르세요.${NC}"
echo "=================================="

flutter run -d chrome --web-port=$PORT
