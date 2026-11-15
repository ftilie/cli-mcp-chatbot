import unittest
from unittest.mock import AsyncMock, patch

from mcp.types import ListToolsResult, Tool

from core.tools import ToolManager
from mcp_client import MCPClient


class MCPClientTests(unittest.IsolatedAsyncioTestCase):
    async def test_list_tools_returns_tools_from_response(self):
        tool = Tool(name="read_doc_contents", inputSchema={"type": "object"})
        session = AsyncMock()
        session.list_tools.return_value = ListToolsResult(tools=[tool])
        client = MCPClient("unused", [])

        with patch.object(client, "session", return_value=session):
            self.assertEqual(await client.list_tools(), [tool])
            tools = await ToolManager.get_all_tools({"documents": client})
            self.assertEqual(tools[0]["name"], tool.name)
            self.assertIs(
                await ToolManager._find_client_with_tool([client], tool.name), client
            )


if __name__ == "__main__":
    unittest.main()