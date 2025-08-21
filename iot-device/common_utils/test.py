from rest_transport import RestTransport

class TestRestTransport:
    """
    RestTransport의 단위 테스트를 위한 클래스
    """
    async def test_post_json(self):
        rt = RestTransport()
        payload = {
            # "device_id": "device-001",
            # "sensors": {
            #     "fall_detected": False,
            #     "gas_ppm": 223.4,
            #     "activity_level": 0.62
            # },
            # "ts": 1724212345
            
            "user_name": "테스트1 사용자",
            "email": "test1@example.com",
            "phone_number": "01012345678",
            "user_role": "user"

        }
        # res = await rt.get("/api/v1/list")
        res = await rt.post_json("/api/v1/", payload)
        print(f"Response: {res.text}")
        assert res.status_code == 200
    
    async def test_get(self):
        rt = RestTransport()

if __name__ == "__main__":
    import asyncio
    from rest_transport import RestTransport

    async def main():
        test = TestRestTransport()
        await test.test_post_json()

    asyncio.run(main())