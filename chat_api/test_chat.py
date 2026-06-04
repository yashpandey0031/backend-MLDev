from fastapi.testclient import TestClient
from main import app
from unittest.mock import AsyncMock
from routers.chat import manager

client = TestClient(app)

def test_Get_messages():
  response = client.get("/messages")
  assert response.status_code == 200
  assert isinstance(response.json(), list)
# checking if the instance is a list or not otherwise fail the test 

def test_upload_wrong_file_type():
  response = client.post(
    "/uploadfile",
    files = {"file":("test.exe",b"fake contet", "application/exe")}
  )

  assert response.status_code == 400

def test_pdf_file_upload():
  response = client.post("/uploadfile",files = {"file" : ("document.pdf",b"fakecontent","application/pdf")}
  )

  assert response.status_code == 200

def test_websocket_chat():
  with client.websocket_connect("chat/testuser") as websocket:
    websocket.send_text("hello")
    data=websocket.receive_text()
    assert data == "testuser: hello" #makes the changes directly to the database and checks if a message with that user is present or not 


def test_full_connection():
  with client.websocket_connect("chat/testuser2") as ws2:
    with client.websocket_connect("chat/testuser3") as ws3:
      ws2.send_text("hello from user1")

      data_ws2 = ws2.receive_text()
      data_ws3 = ws3.receive_text()
      assert data_ws2 == "testuser2: hello from user1"
      assert data_ws3 == "testuser2: hello from user1"
#created two instances to see they are both seeing the messages or not

def test_connection_manager():
    fake_websocket = AsyncMock() #creates a fake object that acts like real users
    
    import asyncio
    asyncio.run(manager.connect(fake_websocket))
    #connect the fake websocket into the functions 
    
    assert fake_websocket in manager.active_connections
    #if they are in the connection it is active connection 
    manager.disconnect(fake_websocket)
    #disconnect
    
    assert fake_websocket not in manager.active_connections

    #after diconnection , no connection should remain in active_connections we are assrting that here