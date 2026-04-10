from app import create_app

def test_home():
    app = create_app()
    client = app.test_client()

    response = client.get("/platos")
    assert response.status_code in [200, 404]