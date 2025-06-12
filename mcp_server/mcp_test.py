from typing import Any

import httpx
from fastmcp import FastMCP

mcp = FastMCP("alapi tools")

# Constants
WEATHER_API_BASE = "http://v3.alapi.cn/api/tianqi"
ZAOBAO_API_BASE = "http://v3.alapi.cn/api/zaobao"
API_TOKEN = "api_token"
USER_AGENT = "weather-app/1.0"

async def make_weather_request(city: str) -> dict[str, Any] | None:
    """Make a request to the weather API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }
    url = f"{WEATHER_API_BASE}?token={API_TOKEN}&city={city}"
    print(f"url:{url}")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching weather data: {e}")
            return None

@mcp.tool()
async def stream_weather(city: str):
    """Stream weather updates using SSE.
    
    Args:
        city: 城市名称
    """
    print("hello")
    weather_data = await make_weather_request(city)
    print(weather_data)
    return weather_data


async def make_zaobao_request() -> dict[str, Any] | None:
    """Make a request to the zaobao API with proper error handling."""
    headers = {
        "Accept": "application/json"
    }
    url = f"{ZAOBAO_API_BASE}?token={API_TOKEN}&format=json"
    print(f"url:{url}")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching weather data: {e}")
            return None

@mcp.tool()
async def stream_zaobao():
    """Stream zaobao updates using SSE.
    
    """
    print("hello")
    zaobao_data = await make_zaobao_request()
    print(zaobao_data)
    return zaobao_data


if __name__ == "__main__":
    print("Starting mcp server...")
    print(f"Server will be available at: http://0.0.0.0:10030")
    try:
        print("Initializing MCP server...")
        # Run the MCP server with SSE transport
        print("Calling mcp.run()...")
        mcp.run(transport="sse", host="0.0.0.0", port=10030)
        print("Server started successfully!")
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc()
