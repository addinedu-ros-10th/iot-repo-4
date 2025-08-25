@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM Flutter 앱 실행 배치 파일
REM 이 배치 파일은 올바른 Flutter 프로젝트 경로에서 실행되도록 보장합니다.

echo 🚀 Flutter 앱 실행 스크립트
echo ==================================

REM 현재 경로 확인
set CURRENT_DIR=%CD%
echo 현재 경로: %CURRENT_DIR%

REM Flutter 프로젝트인지 확인
if not exist "pubspec.yaml" (
    echo ❌ 현재 디렉토리는 Flutter 프로젝트가 아닙니다!
    echo 올바른 Flutter 프로젝트 경로로 이동합니다...
    
    REM 프로젝트 루트에서 Flutter 프로젝트 찾기
    set PROJECT_ROOT=C:\Users\%USERNAME%\Documents\AddInEdu\Project
    set FLUTTER_PROJECT=%PROJECT_ROOT%\apps\user_app
    
    if exist "%FLUTTER_PROJECT%" (
        echo ✅ Flutter 프로젝트를 찾았습니다: %FLUTTER_PROJECT%
        cd /d "%FLUTTER_PROJECT%"
        echo ✅ 경로를 변경했습니다: %CD%
    ) else (
        echo ❌ Flutter 프로젝트를 찾을 수 없습니다!
        echo 수동으로 올바른 경로로 이동해주세요.
        pause
        exit /b 1
    )
) else (
    echo ✅ Flutter 프로젝트가 확인되었습니다.
)

REM Flutter 환경 확인
echo.
echo 🔍 Flutter 환경 확인 중...
flutter --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Flutter가 설치되지 않았습니다!
    echo Flutter를 설치하거나 PATH에 추가해주세요.
    pause
    exit /b 1
)

REM Flutter doctor 실행
echo.
echo 🏥 Flutter Doctor 실행 중...
flutter doctor

REM 의존성 설치 확인
echo.
echo 📦 의존성 설치 확인 중...
if not exist ".dart_tool" if not exist "pubspec.lock" (
    echo ⚠️  의존성이 설치되지 않았습니다. 설치를 시작합니다...
    flutter pub get
)

REM 포트 확인 및 설정
set PORT=%1
if "%PORT%"=="" set PORT=8084
echo.
echo 🌐 포트 %PORT%에서 Chrome으로 실행합니다...

REM Flutter 앱 실행
echo.
echo 🚀 Flutter 앱을 실행합니다...
echo 명령어: flutter run -d chrome --web-port=%PORT%
echo 중단하려면 Ctrl+C를 누르세요.
echo ==================================

flutter run -d chrome --web-port=%PORT%

pause
