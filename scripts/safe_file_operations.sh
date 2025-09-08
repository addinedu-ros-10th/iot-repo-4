#!/bin/bash

# 안전한 파일/폴더 작업 스크립트
# 사용법: ./safe_file_operations.sh [명령] [소스] [대상]

set -e  # 오류 발생 시 스크립트 중단

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 로그 함수
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 현재 위치 및 프로젝트 루트 확인
check_environment() {
    log_info "현재 작업 디렉토리 확인 중..."
    CURRENT_DIR=$(pwd)
    log_info "현재 디렉토리: $CURRENT_DIR"
    
    # Git 저장소인지 확인
    if [ ! -d ".git" ]; then
        log_error "현재 디렉토리는 Git 저장소가 아닙니다!"
        log_info "프로젝트 루트 디렉토리로 이동해주세요."
        exit 1
    fi
    
    # 프로젝트 루트 확인
    PROJECT_ROOT=$(git rev-parse --show-toplevel)
    log_info "프로젝트 루트: $PROJECT_ROOT"
    
    # 프로젝트 루트가 아닌 경우 경고
    if [ "$CURRENT_DIR" != "$PROJECT_ROOT" ]; then
        log_warning "현재 디렉토리가 프로젝트 루트가 아닙니다!"
        log_info "프로젝트 루트로 이동하는 것을 권장합니다: cd $PROJECT_ROOT"
        read -p "계속 진행하시겠습니까? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            log_info "작업을 중단합니다."
            exit 0
        fi
    fi
}

# 파일/폴더 존재 확인
check_source_exists() {
    local source="$1"
    if [ ! -e "$source" ]; then
        log_error "소스 '$source'가 존재하지 않습니다!"
        exit 1
    fi
    log_success "소스 확인 완료: $source"
}

# 대상 경로 확인 및 생성
check_target_path() {
    local target="$1"
    local target_dir=$(dirname "$target")
    
    if [ ! -d "$target_dir" ]; then
        log_info "대상 디렉토리 생성 중: $target_dir"
        mkdir -p "$target_dir"
        log_success "대상 디렉토리 생성 완료"
    fi
}

# 중복 파일 확인
check_duplicates() {
    local filename=$(basename "$1")
    local duplicates=$(find . -name "$filename" -type f 2>/dev/null | wc -l)
    
    if [ "$duplicates" -gt 1 ]; then
        log_warning "중복 파일 발견: $filename ($duplicates개)"
        find . -name "$filename" -type f 2>/dev/null
        read -p "중복 파일을 정리하시겠습니까? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            cleanup_duplicates "$filename"
        fi
    fi
}

# 중복 파일 정리
cleanup_duplicates() {
    local filename="$1"
    local duplicates=$(find . -name "$filename" -type f 2>/dev/null)
    local count=0
    
    log_info "중복 파일 정리 중..."
    
    for file in $duplicates; do
        if [ "$count" -eq 0 ]; then
            log_info "유지할 파일: $file"
            ((count++))
        else
            log_info "삭제할 파일: $file"
            rm "$file"
            log_success "삭제 완료: $file"
        fi
    done
    
    log_success "중복 파일 정리 완료"
}

# 안전한 이동
safe_move() {
    local source="$1"
    local target="$2"
    
    log_info "파일 이동 작업 시작..."
    log_info "소스: $source"
    log_info "대상: $target"
    
    # 환경 확인
    check_environment
    
    # 소스 존재 확인
    check_source_exists "$source"
    
    # 대상 경로 확인 및 생성
    check_target_path "$target"
    
    # 중복 파일 확인
    check_duplicates "$source"
    
    # 백업 생성
    local backup_dir="./backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"
    cp -r "$source" "$backup_dir/"
    log_success "백업 생성 완료: $backup_dir"
    
    # 파일 이동
    log_info "파일 이동 중..."
    mv "$source" "$target"
    
    # 이동 확인
    if [ -e "$target" ]; then
        log_success "파일 이동 완료!"
        log_info "대상 위치: $target"
        log_info "백업 위치: $backup_dir"
    else
        log_error "파일 이동 실패!"
        log_info "백업에서 복원 중..."
        cp -r "$backup_dir/$(basename "$source")" "$(dirname "$source")/"
        exit 1
    fi
}

# 안전한 복사
safe_copy() {
    local source="$1"
    local target="$2"
    
    log_info "파일 복사 작업 시작..."
    log_info "소스: $source"
    log_info "대상: $target"
    
    # 환경 확인
    check_environment
    
    # 소스 존재 확인
    check_source_exists "$source"
    
    # 대상 경로 확인 및 생성
    check_target_path "$target"
    
    # 파일 복사
    log_info "파일 복사 중..."
    cp -r "$source" "$target"
    
    # 복사 확인
    if [ -e "$target" ]; then
        log_success "파일 복사 완료!"
        log_info "대상 위치: $target"
    else
        log_error "파일 복사 실패!"
        exit 1
    fi
}

# 안전한 삭제
safe_delete() {
    local target="$1"
    
    log_info "파일 삭제 작업 시작..."
    log_info "대상: $target"
    
    # 환경 확인
    check_environment
    
    # 대상 존재 확인
    if [ ! -e "$target" ]; then
        log_error "삭제할 대상 '$target'가 존재하지 않습니다!"
        exit 1
    fi
    
    # 백업 생성
    local backup_dir="./backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"
    cp -r "$target" "$backup_dir/"
    log_success "백업 생성 완료: $backup_dir"
    
    # 삭제 확인
    read -p "정말로 '$target'를 삭제하시겠습니까? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "삭제 작업을 중단합니다."
        exit 0
    fi
    
    # 파일 삭제
    log_info "파일 삭제 중..."
    rm -rf "$target"
    
    # 삭제 확인
    if [ ! -e "$target" ]; then
        log_success "파일 삭제 완료!"
        log_info "백업 위치: $backup_dir"
    else
        log_error "파일 삭제 실패!"
        exit 1
    fi
}

# 사용법 출력
show_usage() {
    echo "안전한 파일/폴더 작업 스크립트"
    echo ""
    echo "사용법:"
    echo "  $0 move <소스> <대상>    - 파일/폴더 이동"
    echo "  $0 copy <소스> <대상>    - 파일/폴더 복사"
    echo "  $0 delete <대상>         - 파일/폴더 삭제"
    echo "  $0 check                 - 현재 환경 확인"
    echo ""
    echo "예시:"
    echo "  $0 move app.py apps/new_folder/"
    echo "  $0 copy config/ backup/config/"
    echo "  $0 delete old_file.txt"
    echo "  $0 check"
}

# 메인 로직
main() {
    case "$1" in
        "move")
            if [ $# -ne 3 ]; then
                log_error "이동 명령은 소스와 대상이 필요합니다."
                show_usage
                exit 1
            fi
            safe_move "$2" "$3"
            ;;
        "copy")
            if [ $# -ne 3 ]; then
                log_error "복사 명령은 소스와 대상이 필요합니다."
                show_usage
                exit 1
            fi
            safe_copy "$2" "$3"
            ;;
        "delete")
            if [ $# -ne 2 ]; then
                log_error "삭제 명령은 대상이 필요합니다."
                show_usage
                exit 1
            fi
            safe_delete "$2"
            ;;
        "check")
            check_environment
            log_success "환경 확인 완료"
            ;;
        *)
            show_usage
            exit 1
            ;;
    esac
}

# 스크립트 실행
main "$@"
