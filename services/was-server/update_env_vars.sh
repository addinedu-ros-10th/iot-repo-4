#!/bin/bash
# update_env_vars.sh
# IoT Care Backend System 환경변수 자동 업데이트 스크립트
# Windows 환경 (Git Bash)에서 실행

echo "🔍 IoT Care Backend System 환경변수 자동 업데이트 시작..."
echo "📅 실행 시간: $(date)"
echo ""

# 현재 작업 디렉토리 확인
echo "📍 현재 작업 디렉토리: $(pwd)"

# .env.local 파일 존재 확인
if [ ! -f ".env.local" ]; then
    echo "❌ .env.local 파일을 찾을 수 없습니다."
    echo "💡 현재 디렉토리에 .env.local 파일이 있는지 확인하세요."
    exit 1
fi

echo "✅ .env.local 파일 발견"

# Windows 환경에서 IP 주소 추출
echo "🔍 현재 개발 머신 IP 주소 조사 중..."

# 방법 1: PowerShell을 사용한 IP 주소 추출 (권장)
CURRENT_IP=$(powershell -Command "Get-NetIPAddress | Where-Object {$_.AddressFamily -eq 'IPv4' -and $_.IPAddress -notlike '127.*' -and $_.IPAddress -notlike '169.*'} | Select-Object -First 1 -ExpandProperty IPAddress" | tr -d '\r')

# 방법 1이 실패한 경우 방법 2 시도
if [ -z "$CURRENT_IP" ]; then
    echo "⚠️  방법 1 실패, 대체 방법 시도 중..."
    CURRENT_IP=$(powershell -Command "ipconfig | findstr 'IPv4'" | head -1 | sed 's/.*: //' | tr -d '\r')
fi

# 방법 2도 실패한 경우 방법 3 시도
if [ -z "$CURRENT_IP" ]; then
    echo "⚠️  방법 2 실패, 대체 방법 시도 중..."
    CURRENT_IP=$(ipconfig | grep "IPv4" | head -1 | sed 's/.*: //' | tr -d '\r')
fi

if [ -z "$CURRENT_IP" ]; then
    echo "❌ IP 주소를 찾을 수 없습니다."
    echo "💡 수동으로 IP 주소를 확인하고 환경변수를 업데이트하세요."
    echo "💡 명령어: ipconfig 또는 powershell -Command 'ipconfig'"
    exit 1
fi

echo "✅ 현재 IP 주소: $CURRENT_IP"

# 현재 .env.local 파일의 IP 설정 확인
echo ""
echo "📋 현재 .env.local 파일의 IP 설정:"
grep -E "^(DB_HOST|CADDY_DOMAIN)=" .env.local || echo "⚠️  IP 관련 환경변수를 찾을 수 없습니다."

# 백업 파일 생성
BACKUP_FILE=".env.local.backup.$(date +%Y%m%d_%H%M%S)"
cp .env.local "$BACKUP_FILE"
echo "💾 백업 파일 생성: $BACKUP_FILE"

# 환경변수 업데이트
echo ""
echo "📝 .env.local 파일 업데이트 중..."

# DB_HOST 업데이트
if grep -q "DB_HOST=" .env.local; then
    sed -i "s/DB_HOST=.*/DB_HOST=$CURRENT_IP/g" .env.local
    echo "✅ DB_HOST 업데이트 완료: $CURRENT_IP"
else
    echo "⚠️  DB_HOST 환경변수가 .env.local 파일에 없습니다."
fi

# CADDY_DOMAIN 업데이트
if grep -q "CADDY_DOMAIN=" .env.local; then
    sed -i "s/CADDY_DOMAIN=.*/CADDY_DOMAIN=$CURRENT_IP/g" .env.local
    echo "✅ CADDY_DOMAIN 업데이트 완료: $CURRENT_IP"
else
    echo "⚠️  CADDY_DOMAIN 환경변수가 .env.local 파일에 없습니다."
fi

# 업데이트된 내용 확인
echo ""
echo "📋 업데이트된 환경변수:"
grep -E "^(DB_HOST|CADDY_DOMAIN)=" .env.local || echo "⚠️  업데이트된 환경변수를 찾을 수 없습니다."

echo ""
echo "🎯 다음 단계: Docker 환경 재시작"
echo "💡 명령어: docker-compose down && docker-compose up -d"
echo "💡 또는 이 스크립트를 --restart 옵션과 함께 실행하세요."

# --restart 옵션이 있는 경우 Docker 재시작
if [[ "$1" == "--restart" ]]; then
    echo ""
    echo "🚀 Docker 환경 자동 재시작 시작..."
    
    # Docker 컨테이너 중지
    echo "⏹️  Docker 컨테이너 중지 중..."
    docker-compose down --volumes --remove-orphans
    
    # Docker 시스템 정리
    echo "🧹 Docker 시스템 정리 중..."
    docker system prune -f
    
    # 프로젝트 재시작
    echo "🔄 프로젝트 재시작 중..."
    docker-compose up -d
    
    # 상태 확인
    echo ""
    echo "📊 Docker 컨테이너 상태:"
    docker-compose ps
    
    # API 서버 상태 확인
    echo ""
    echo "🔍 API 서버 상태 확인 중..."
    sleep 10  # 서버 시작 대기
    
    if curl -s http://localhost:8000/health > /dev/null; then
        echo "✅ API 서버 정상 동작"
    else
        echo "❌ API 서버 응답 없음"
        echo "💡 docker logs iot-care-app 명령으로 로그를 확인하세요."
    fi
    
    echo ""
    echo "🎉 환경변수 업데이트 및 Docker 재시작 완료!"
fi

echo ""
echo "✅ 환경변수 자동 업데이트 완료!"
echo "📅 완료 시간: $(date)"
