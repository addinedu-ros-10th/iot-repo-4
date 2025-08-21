# file: rest_transport.py
# -*- coding: utf-8 -*-
"""
단일 책임(REST 전송 전용):
- HTTP(S) 기반 REST API 요청(POST/GET)만 처리
- 재시도/백오프, 타임아웃, JWT 헤더 지원
- 네트워크 외의 책임(센서, 직렬통신, 큐 저장 등)은 포함하지 않음

포트폴리오 포인트:
- 사회적 의미 데이터 예시를 테스트에 활용할 수 있도록, 예제 payload에 'fall_detected', 'gas_ppm' 등의 필드명을 제안
"""

from __future__ import annotations
import os
from typing import Any, Dict, Optional
import asyncio
import httpx
import logging
from pydantic import BaseModel, Field

log = logging.getLogger("rest_transport")
if not log.handlers:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")

class RestSettings(BaseModel):
    """
    REST 통신에 필요한 설정 값만 가짐
    """
    base_url: str = Field(default=os.getenv("API_BASE_URL", "http://localhost"))
    timeout_sec: float = Field(default=float(os.getenv("HTTP_TIMEOUT_SEC", "10")))
    max_retries: int = Field(default=int(os.getenv("HTTP_MAX_RETRIES", "4")))
    backoff_factor: float = Field(default=float(os.getenv("HTTP_BACKOFF_FACTOR", "0.7")))
    jwt_token: Optional[str] = Field(default=os.getenv("JWT_TOKEN"))

class RestTransport:
    """
    - 단일 책임: REST API 호출만 수행
    - 외부에서 settings를 주입받아 동작
    - httpx.AsyncClient를 내부에서 관리
    """
    def __init__(self, settings: Optional[RestSettings] = None):
        self.settings = settings or RestSettings()
        headers = {"Content-Type": "application/json"}
        if self.settings.jwt_token:
            headers["Authorization"] = f"Bearer {self.settings.jwt_token}"
        self._client = httpx.AsyncClient(
            base_url=self.settings.base_url,
            headers=headers,
            timeout=self.settings.timeout_sec,
        )

    async def close(self):
        await self._client.aclose()

    async def post_json(self, path: str, json_payload: Dict[str, Any]) -> httpx.Response:
        """
        - 단일 기능: JSON POST 요청 전송
        - 재시도/백오프 내장
        """
        retries = 0
        while True:
            try:
                resp = await self._client.post(path, json=json_payload)
                resp.raise_for_status()
                return resp
            except Exception as e:
                retries += 1
                if retries > self.settings.max_retries:
                    log.error(f"[POST] 최대 재시도 초과: {e}")
                    raise
                # 기하급수 백오프(최대 8초 캡 등은 호출자가 결정)
                sleep = min(8.0, (self.settings.backoff_factor ** retries) * 2.0)
                log.warning(f"[POST] 실패 → {sleep:.2f}s 후 재시도({retries}/{self.settings.max_retries}): {e}")
                await asyncio.sleep(sleep)

    async def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> httpx.Response:
        """
        - 단일 기능: GET 요청
        - 재시도/백오프 내장
        """
        retries = 0
        while True:
            try:
                resp = await self._client.get(path, params=params)
                resp.raise_for_status()
                return resp
            except Exception as e:
                retries += 1
                if retries > self.settings.max_retries:
                    log.error(f"[GET] 최대 재시도 초과: {e}")
                    raise
                sleep = min(8.0, (self.settings.backoff_factor ** retries) * 2.0)
                log.warning(f"[GET] 실패 → {sleep:.2f}s 후 재시도({retries}/{self.settings.max_retries}): {e}")
                await asyncio.sleep(sleep)

# -------- 사용 예시(예제 실행 전용): python rest_transport.py --------
# 아래 코드는 모듈의 사용법을 보여주는 예시이며, 실제 애플리케이션에서는
# 다른 레이어(예: 센서 수집기, 직렬브릿지 등)에서 이 RestTransport를 호출하세요.
if __name__ == "__main__":
    async def _demo():
        rt = RestTransport()
        try:
            # 사회적 의미 예시 payload (낙상/가스/활동)
            payload = {
                "device_id": "device-001",
                "sensors": {
                    "fall_detected": False,
                    "gas_ppm": 223.4,
                    "activity_level": 0.62
                },
                "ts": 1724212345
            }
            res = await rt.post_json("/api/v1/iot/data", payload)
            print("POST status:", res.status_code, res.text)
        finally:
            await rt.close()
    asyncio.run(_demo())
