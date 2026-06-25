from src.app import activities


def test_root_redirects_to_static_index(client):
    # Arrange
    # No special setup required for the root endpoint.

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_catalog(client):
    # Arrange
    # No special setup required for the activity listing endpoint.

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert "Chess Club" in response.json()
    assert response.json()["Chess Club"]["schedule"] == "Fridays, 3:30 PM - 5:00 PM"


def test_signup_for_activity_adds_participant(client):
    # Arrange
    email = "newstudent@mergington.edu"

    # Act
    response = client.post("/activities/Chess Club/signup?email=newstudent@mergington.edu")

    # Assert
    assert response.status_code == 200
    assert email in activities["Chess Club"]["participants"]
    assert response.json()["message"] == "Signed up newstudent@mergington.edu for Chess Club"


def test_signup_rejects_duplicate_email(client):
    # Arrange
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/Chess Club/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_returns_not_found_for_unknown_activity(client):
    # Arrange
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/Unknown Club/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_participant_removes_email(client):
    # Arrange
    activities["Chess Club"]["participants"] = ["michael@mergington.edu"]

    # Act
    response = client.delete("/activities/Chess Club/signup?email=michael@mergington.edu")

    # Assert
    assert response.status_code == 200
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
    assert response.json()["message"] == "Removed michael@mergington.edu from Chess Club"


def test_unregister_returns_not_found_for_unknown_email(client):
    # Arrange
    activities["Chess Club"]["participants"] = ["michael@mergington.edu"]

    # Act
    response = client.delete("/activities/Chess Club/signup?email=student@mergington.edu")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_returns_not_found_for_unknown_activity(client):
    # Arrange
    # No special setup required beyond the path itself.

    # Act
    response = client.delete("/activities/Unknown Club/signup?email=student@mergington.edu")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
