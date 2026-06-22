def test_root_redirect(client):
    """Test that root redirects to /static/index.html"""
    # Arrange
    # (no setup needed - testing default behavior)
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307


def test_get_activities(client):
    """Test getting all activities"""
    # Arrange
    expected_activities = ["Chess Club", "Programming Class", "Gym Class"]
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert response.status_code == 200
    for activity in expected_activities:
        assert activity in activities
    assert len(activities) >= 3


def test_get_activity_details(client):
    """Test activity contains required fields"""
    # Arrange
    required_fields = ["description", "schedule", "max_participants", "participants"]
    activity_name = "Chess Club"
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    chess_club = activities[activity_name]
    
    # Assert
    assert response.status_code == 200
    for field in required_fields:
        assert field in chess_club
    assert isinstance(chess_club["participants"], list)
    assert len(chess_club["participants"]) == 2


def test_signup_for_activity(client):
    """Test signing up a new student for an activity"""
    # Arrange
    activity_name = "Chess Club"
    new_email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={new_email}"
    )
    
    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    
    # Verify the participant was actually added
    response = client.get("/activities")
    activities = response.json()
    assert new_email in activities[activity_name]["participants"]


def test_signup_duplicate_student(client):
    """Test that a student cannot sign up twice for the same activity"""
    # Arrange
    activity_name = "Chess Club"
    duplicate_email = "duplicate@mergington.edu"
    
    # Act - First signup (should succeed)
    response_first = client.post(
        f"/activities/{activity_name}/signup?email={duplicate_email}"
    )
    
    # Assert first signup
    assert response_first.status_code == 200
    
    # Act - Second signup (should fail)
    response_second = client.post(
        f"/activities/{activity_name}/signup?email={duplicate_email}"
    )
    
    # Assert second signup fails
    assert response_second.status_code == 400
    assert "already signed up" in response_second.json()["detail"]


def test_signup_nonexistent_activity(client):
    """Test signing up for an activity that doesn't exist"""
    # Arrange
    nonexistent_activity = "Nonexistent Club"
    email = "test@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{nonexistent_activity}/signup?email={email}"
    )
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_remove_participant(client):
    """Test removing a participant from an activity"""
    # Arrange
    activity_name = "Chess Club"
    email_to_remove = "michael@mergington.edu"
    
    # Act - Remove the participant
    response = client.delete(
        f"/activities/{activity_name}/participants?email={email_to_remove}"
    )
    
    # Assert deletion was successful
    assert response.status_code == 200
    assert "Removed" in response.json()["message"]
    
    # Verify the participant was actually removed
    response = client.get("/activities")
    activities = response.json()
    assert email_to_remove not in activities[activity_name]["participants"]


def test_remove_nonexistent_participant(client):
    """Test removing a participant that's not in the activity"""
    # Arrange
    activity_name = "Chess Club"
    nonexistent_email = "notinactivity@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants?email={nonexistent_email}"
    )
    
    # Assert
    assert response.status_code == 404
    assert "Student not found" in response.json()["detail"]


def test_remove_from_nonexistent_activity(client):
    """Test removing from an activity that doesn't exist"""
    # Arrange
    nonexistent_activity = "Nonexistent Club"
    email = "test@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{nonexistent_activity}/participants?email={email}"
    )
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
