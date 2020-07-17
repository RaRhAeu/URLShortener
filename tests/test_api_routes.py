from tests import data


def test_shortcut(db_session, client):
    res = client.get("/nonexistingurl")
    assert res.status_code == 404
    res = client.post("/api/urls", json={"long_url": "http://google.com"})
    assert res.status_code == 200
    short_url = res.get_json()['short_url']
    res = client.get(f"/{short_url}")
    assert res.status_code == 302


def test_get_urls(db_session, client):
    res = client.get("/api/urls")
    assert res.status_code == 200


def test_create_url(db_session, client):
    res = client.post("/api/urls", json={"long_url": "http://google.com"})
    assert res.status_code == 200


def test_read_url(db_session, client):
    res = client.get("/api/urls/1")
    assert res.status_code == 404
    url = data.example_url()
    db_session.add(url)
    db_session.commit()
    url_id = url.id
    res = client.get(f"/api/urls/{url_id}")
    assert res.status_code == 200


def test_get_qr(db_session, client):
    url = data.example_url()
    db_session.add(url)
    db_session.commit()
    url_id = url.id
    res = client.get(f"/api/urls/{url_id}/get_qr")
    assert res.status_code == 200
    assert isinstance(res.data, bytes)
