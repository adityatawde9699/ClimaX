#!/usr/bin/env python3
"""Non-mutating production HTTP and WebSocket smoke validation."""

import asyncio
import json
import os

import httpx
import websockets


async def main() -> None:
    base_url = os.environ["CLIMAX_PRODUCTION_URL"].rstrip("/")
    token = os.environ["CLIMAX_SMOKE_TOKEN"]
    api_url = f"{base_url}/api/v1"
    headers = {"Authorization": f"Bearer {token}"}
    checks = [
        "/sensors/?limit=1",
        "/environment/latest?limit=1",
        "/reports/",
        "/incidents/",
        "/alerts/?active=true",
        "/interventions/",
        "/analytics/summary",
        "/risk/hotspots",
    ]
    async with httpx.AsyncClient(timeout=15) as client:
        health = await client.get(f"{base_url}/health")
        health.raise_for_status()
        for path in checks:
            response = await client.get(f"{api_url}{path}", headers=headers)
            response.raise_for_status()

        ws_url = base_url.replace("https://", "wss://").replace("http://", "ws://")
        async with websockets.connect(f"{ws_url}/ws/events?token={token}") as socket:
            probe = await client.post(f"{base_url}/health/realtime-probe", headers=headers)
            probe.raise_for_status()
            probe_id = probe.json()["probe_id"]
            async with asyncio.timeout(10):
                while True:
                    event = json.loads(await socket.recv())
                    if event.get("event") == "system.realtime_probe":
                        if event.get("data", {}).get("id") != probe_id:
                            raise RuntimeError("Realtime probe ID mismatch")
                        break
    print("Production HTTP and WebSocket validation passed.")


if __name__ == "__main__":
    asyncio.run(main())
