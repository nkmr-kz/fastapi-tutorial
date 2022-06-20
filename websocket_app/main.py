from typing import Union

from fastapi import Cookie, Depends, FastAPI, Query, WebSocket, status
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <label>Item ID: <input type="text" id="itemId" autocomplete="off" value="foo"/></label>
            <label>Token: <input type="text" id="token" autocomplete="off" value="some-key-token"/></label>
            <button onclick="connect(event)">Connect</button>
            <hr>
            <label>Message: <input type="text" id="messageText" autocomplete="off"/></label>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
        var ws = null;
            function connect(event) {
                var itemId = document.getElementById("itemId")
                var token = document.getElementById("token")
                ws = new WebSocket("ws://localhost:8000/items/" + itemId.value + "/ws?token=" + token.value);
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                };
                event.preventDefault()
            }
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
  return HTMLResponse(html)

async def get_token(
  websocket: WebSocket,
  token:Union[str,None]= Query(default=None)
):
  if token is None or token != "testToken":
    await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
  return token
  
@app.websocket("/items/{item_id}/ws")
async def websocket_endpoint(
  websocket: WebSocket,
  item_id: str,
  q: Union[int,None]=None,
  token:str = Depends(get_token)
  ):
  await websocket.accept()
  await websocket.send_text(f"Welcome to the chat room {item_id}")
  while True:
    data = await websocket.receive_text()
    print(data)
    await websocket.send_text(
      f"Session token value is: {token}"
    )
    if q is not None:
      await websocket.send_text(
        f"Query value is: {q}"
      )
    await websocket.send_text(
      f"Message is : {data}, for item ID :{item_id}"
    )
