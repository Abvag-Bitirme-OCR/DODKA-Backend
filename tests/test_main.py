from fastapi.testclient import TestClient
from fastapi import status
import API
from API import main
client=TestClient(app=main.app)

base64_str = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAAAsSAAALEgHS3X78AAAC/klEQVRIx6VWSU8UQRQeZvFgYhgXFLcYEhwkYRwvJEzTMw3h5pYYJXrx6NGQePMPGIPxigHBBE92gWJEjStq4sF4U4zMwR+gZyMDiLTfN/WqqR5kHLGSL6/q1dvrVXXH8nk/xkFKdHUp0GoYvpaNzv0GMzcDvLjQWKgAJMBIwGCF6vUqYMTQNYZ0gCoHdFLGOA6N/+uQDBKS+U6snwMrcBBg/QHokL24rXQRjHHQIeCGDfDJGwG9AmwzQSHKHcBssfg0cJx7MD4RFApPAvDoJGWn2uI4dyubnvcy6Ol5DbyKgPy+vncwos5LQHuh99l1p8n7BoP9WF9gFnSGeWfMqt8hCCxCiZiQLG6CPyIYhsIo6HXwNwNp4FN3932JXE2L05P5/GRAQP6InUEGm8sQXMK8tVb9IZMGZl33IY2sOM5UwOyh/wD4Wiw+4znMVCtlgGUILGEzJ9EkwYvrNlSbhLcL+x9d9xGjpuxp7F9lFgSdgjcH7I4cMjPQDnxmkLU3wU+K8SYenhj5iXm/6B4HfrFckClh3lzdwlSuONBRqazwGLlxEjGO9RnhH4NcWcpVwt5+Cc60cC0HvrkwzeBVyoI5jPti3D8KlAuFx5WyMENxGt6tmg5AU+JgnH0O+gMKZ6ORV86CNW/iOQHnME8bRzVLBMEGeULeeN4LOrgs/BOQWbCM7xMbg729b5nNoF2mdR1IFFtoRJdBXYPSAOh3WdP4nlVZf1QHom6bLqzDgX+AHcKLwxvLHme5IFMyxkFNCw973gwzGKs7A7mxMKYWgS/Aezj07W7Bvuk0caBuyTrxlzY1XaS2A23gN0YvZ3hP6nFgXzSVMxfMOLHffyBFZTrQa11rvlnrOoBwmAGUDsY2MKA7JGfw5xLpd0jhCVCnQFtBs0BHHTgMtEBHSReNic1IBu38WPAt5wUCnQfK9cEn5qG3ILf6jthM2uk1QmCOT692NLkB8EMzxQAvRTKw/hS2Au08D+mqjP5O1IIKKfTapLRrv/XVvx3/O2zjvwEdrYsJZAdxTgAAAABJRU5ErkJggg=="


def test_index_returns_correct():

    response=client.get("/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == 'Redis connection is successfuly!'

    response2 = client.post(
        url="/file",
        params={"file_base_64": base64_str}
    )

    assert response2.status_code == status.HTTP_200_OK
    assert response2.json() == "Get File's base64 is successfuly!"

    response3 = client.post(
        url="/createQuery/deneme",
    )

    assert response3.status_code == status.HTTP_200_OK
    assert response3.json() == "Get query part 1 is successfuly!"

    response4 = client.post(
        url="/createQuery2",
        params={"query":"deneme"}
    )

    assert response4.status_code == status.HTTP_200_OK
    assert response4.json() == "Get quert part 2 is successfuly!"
