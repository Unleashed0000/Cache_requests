from fastapi import  APIRouter, WebSocket, WebSocketDisconnect

socket = APIRouter()

# A dictionary to store connected clients
# client - это cardschannel или sbp channel
connected_clients = {}


@socket.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await websocket.accept()

    # Add the client to the dictionary
    connected_clients[client_id] = websocket

    try:
        while True:
            # Receive ISO 8583 message
            iso8583_message = await websocket.receive_text()

            # Process ISO 8583 message (you need to implement this)
            response_message = process_iso8583(iso8583_message)

            # Send the response back to the client
            await websocket.send_text(response_message)

    except WebSocketDisconnect:
        # Remove the client from the dictionary when disconnected
        del connected_clients[client_id]


def process_iso8583(iso8583_message: str) -> str:
    """В этой функции парсим строку в отдельные json, xml или другой формат и повторяем логику функции make_request"""

    return iso8583_message
