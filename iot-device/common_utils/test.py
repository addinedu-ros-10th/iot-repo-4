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
            
            "time": "2025-08-21T17:48:16.777Z",
            "device_id": "string2",
            "accel_x": 0,
            "accel_y": 0,
            "accel_z": 0,
            "gyro_x": 0,
            "gyro_y": 0,
            "gyro_z": 0,
            "mag_x": 0,
            "mag_y": 0,
            "mag_z": 0,
            "temperature": 0,
            "raw_payload": {}

        }
        # res = await rt.get("/api/v1/list")
        res = await rt.post_json("/api/imu/create", payload)
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