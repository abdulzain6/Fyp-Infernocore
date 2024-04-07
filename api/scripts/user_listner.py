import asyncio
import websockets
import base64

async def listen_to_ws(base_url: str, target_id: str, command_id: str, auth_token: str):
    # Construct the WebSocket URL
    url = f"{base_url}/ws/listen?target_id={target_id}&command_id={command_id}&auth_token={auth_token}"
    print(url)
    # Prepare the authentication heade

    # Use the low-level API of websockets to connect with custom headers
    async with websockets.connect(url, extra_headers={}) as websocket:
        print("Connected to WebSocket server")

        # Listen for messages
        try:
            async for message in websocket:
                print("Received message:", message)
        except websockets.ConnectionClosed as e:
            print(f"Connection closed with error code {e.code}, reason: {e.reason}")

# Example usage
async def main():
    base_url = "ws://localhost:8000/io-attacker"  # Update with the actual base URL of your server
    target_id = "2cf6271f-acfe-4bad-83e4-ecf099b6237f"
    command_id = "c646e7c5-e131-46c4-b106-51f4bbe7e8bb"
    auth_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjUzZWFiMDBhNzc5MTk3Yzc0MWQ2NjJmY2EzODE1OGJkN2JlNGEyY2MiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vaW5mZXJub2NvcmUtNjcyMWMiLCJhdWQiOiJpbmZlcm5vY29yZS02NzIxYyIsImF1dGhfdGltZSI6MTcwNzUwMTgzNywidXNlcl9pZCI6ImZSWWsybXdlbzdUWXcxZ0FIcHBORXBPTzUxQzMiLCJzdWIiOiJmUllrMm13ZW83VFl3MWdBSHBwTkVwT081MUMzIiwiaWF0IjoxNzA3NTAxODM3LCJleHAiOjE3MDc1MDU0MzcsImVtYWlsIjoidGVzdEBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsidGVzdEBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.anhKp2u0knsybaBYuKcj3UBRkmgUy4DSfFF5a8STs8DCCiQwOOX_gun9IMUvYL8NP0F2KM2QP3gzblehX-wg-kh2VVygj0LjkBMqCXU-0KaZ2kt6TMaFowocXDVIo8G1pLIksl5sOQXthuxCjn1_nEIn-6tpEEYqo1tU3StG73o1INX8t0Bx40kn3la4xN6ku-nHD7kmYghyF8jXrufiVJfefEE0IXEAqRYXdHWoCwAzbdta-8XZcPXMhPVcL__Je-r8R4zqeXXtTPjmd-P68prad_D4bhc1SNboZq0iu0Gb4VTWjOicuamNccXpx5CgrOPoESvnsc45lkNl88VDSw"  # Your authentication token

    await listen_to_ws(base_url, target_id, command_id, auth_token)

if __name__ == "__main__":
    asyncio.run(main())
