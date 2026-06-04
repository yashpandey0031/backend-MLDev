from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_Get_messages():
  response = client.get("/messages")
  assert response.status_code == 200
  assert isinstance(response.json(), list)


def test_upload_wrong_file_type():
  response = client.post(
    "/uploadfile",
    files = {"file":("test.exe",b"fake contet", "application/exe")}
  )

  assert response.status_code == 400