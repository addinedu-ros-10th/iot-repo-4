#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flutter 앱 실행 스크립트
이 스크립트는 올바른 Flutter 프로젝트 경로에서 실행되도록 보장합니다.
크로스 플랫폼 지원 (Windows, macOS, Linux)
"""

import os
import sys
import subprocess
import platform
import argparse
from pathlib import Path

# 색상 정의 (ANSI 이스케이프 코드)
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

def print_colored(text, color):
    """색상이 있는 텍스트 출력"""
    print(f"{color}{text}{Colors.NC}")

def check_flutter_project():
    """현재 디렉토리가 Flutter 프로젝트인지 확인"""
    current_dir = Path.cwd()
    pubspec_file = current_dir / "pubspec.yaml"
    
    print_colored(f"현재 경로: {Colors.YELLOW}{current_dir}{Colors.NC}")
    
    if not pubspec_file.exists():
        print_colored("❌ 현재 디렉토리는 Flutter 프로젝트가 아닙니다!", Colors.RED)
        print_colored("올바른 Flutter 프로젝트 경로로 이동합니다...", Colors.YELLOW)
        
        # 프로젝트 루트에서 Flutter 프로젝트 찾기
        if platform.system() == "Windows":
            project_root = Path.home() / "Documents" / "AddInEdu" / "Project"
        else:
            project_root = Path.home() / "Documents" / "AddInEdu" / "Project"
        
        flutter_project = project_root / "apps" / "user_app"
        
        if flutter_project.exists():
            print_colored(f"✅ Flutter 프로젝트를 찾았습니다: {flutter_project}", Colors.GREEN)
            os.chdir(flutter_project)
            print_colored(f"✅ 경로를 변경했습니다: {Path.cwd()}", Colors.GREEN)
            return True
        else:
            print_colored("❌ Flutter 프로젝트를 찾을 수 없습니다!", Colors.RED)
            print_colored("수동으로 올바른 경로로 이동해주세요.", Colors.YELLOW)
            return False
    else:
        print_colored("✅ Flutter 프로젝트가 확인되었습니다.", Colors.GREEN)
        return True

def check_flutter_installation():
    """Flutter 설치 확인"""
    print_colored("\n🔍 Flutter 환경 확인 중...", Colors.BLUE)
    
    try:
        result = subprocess.run(["flutter", "--version"], 
                              capture_output=True, text=True, check=True)
        print_colored("✅ Flutter가 설치되어 있습니다.", Colors.GREEN)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_colored("❌ Flutter가 설치되지 않았습니다!", Colors.RED)
        print_colored("Flutter를 설치하거나 PATH에 추가해주세요.", Colors.YELLOW)
        return False

def run_flutter_doctor():
    """Flutter doctor 실행"""
    print_colored("\n🏥 Flutter Doctor 실행 중...", Colors.BLUE)
    try:
        subprocess.run(["flutter", "doctor"], check=True)
    except subprocess.CalledProcessError:
        print_colored("⚠️  Flutter doctor 실행 중 오류가 발생했습니다.", Colors.YELLOW)

def check_dependencies():
    """의존성 설치 확인"""
    print_colored("\n📦 의존성 설치 확인 중...", Colors.BLUE)
    
    dart_tool_dir = Path(".dart_tool")
    pubspec_lock = Path("pubspec.lock")
    
    if not dart_tool_dir.exists() or not pubspec_lock.exists():
        print_colored("⚠️  의존성이 설치되지 않았습니다. 설치를 시작합니다...", Colors.YELLOW)
        try:
            subprocess.run(["flutter", "pub", "get"], check=True)
            print_colored("✅ 의존성 설치가 완료되었습니다.", Colors.GREEN)
        except subprocess.CalledProcessError:
            print_colored("❌ 의존성 설치에 실패했습니다.", Colors.RED)
            return False
    else:
        print_colored("✅ 의존성이 이미 설치되어 있습니다.", Colors.GREEN)
    
    return True

def check_port_availability(port):
    """포트 사용 가능 여부 확인"""
    import socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            return True
    except OSError:
        return False

def run_flutter_app(port):
    """Flutter 앱 실행"""
    print_colored(f"\n🌐 포트 {port}에서 Chrome으로 실행합니다...", Colors.BLUE)
    
    # 포트 사용 중인지 확인
    if not check_port_availability(port):
        print_colored(f"⚠️  포트 {port}가 이미 사용 중입니다. 다른 포트를 시도합니다...", Colors.YELLOW)
        port += 1
        if not check_port_availability(port):
            port += 1
        print_colored(f"✅ 포트 {port}를 사용합니다.", Colors.GREEN)
    
    print_colored("\n🚀 Flutter 앱을 실행합니다...", Colors.GREEN)
    print_colored(f"명령어: flutter run -d chrome --web-port={port}", Colors.BLUE)
    print_colored("중단하려면 Ctrl+C를 누르세요.", Colors.YELLOW)
    print_colored("==================================", Colors.BLUE)
    
    try:
        subprocess.run(["flutter", "run", "-d", "chrome", f"--web-port={port}"], check=True)
    except subprocess.CalledProcessError as e:
        print_colored(f"❌ Flutter 앱 실행 중 오류가 발생했습니다: {e}", Colors.RED)
    except KeyboardInterrupt:
        print_colored("\n🛑 사용자에 의해 중단되었습니다.", Colors.YELLOW)

def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(description="Flutter 앱 실행 스크립트")
    parser.add_argument("--port", "-p", type=int, default=8084, 
                       help="사용할 포트 번호 (기본값: 8084)")
    args = parser.parse_args()
    
    print_colored("🚀 Flutter 앱 실행 스크립트", Colors.BLUE)
    print_colored("==================================", Colors.BLUE)
    
    # Flutter 프로젝트 확인
    if not check_flutter_project():
        sys.exit(1)
    
    # Flutter 설치 확인
    if not check_flutter_installation():
        sys.exit(1)
    
    # Flutter doctor 실행
    run_flutter_doctor()
    
    # 의존성 확인
    if not check_dependencies():
        sys.exit(1)
    
    # Flutter 앱 실행
    run_flutter_app(args.port)

if __name__ == "__main__":
    main()
