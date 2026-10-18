"""YouTube Reader as an MCP server (for Claude Desktop, Cursor, etc.).

Install once:   .venv/bin/pip install fastmcp
Run:            .venv/bin/python mcp_server.py
"""
from fastmcp import FastMCP

from yt import read_video

mcp = FastMCP("youtube-reader")


@mcp.tool()
def youtube_reader(url: str) -> dict:
    """Read a YouTube video as text.

    Give a YouTube link and get back the title, channel, and the full
    spoken transcript with timestamps. For AI agents that cannot watch video.
    """
    return read_video(url)


if __name__ == "__main__":
    import sys
    if "--http" in sys.argv:
        # Remote mode: serves MCP over streamable HTTP (for Railway + registry)
        # Run: .venv/bin/python mcp_server.py --http   (listens on 0.0.0.0:8081)
        mcp.run(transport="streamable-http", host="0.0.0.0", port=8081)
    else:
        mcp.run()
