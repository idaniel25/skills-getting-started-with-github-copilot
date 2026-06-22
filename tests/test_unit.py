def test_activities_data_structure(client):
    """Test that activities have the correct data structure"""
    # Arrange
    expected_fields = ["description", "schedule", "max_participants", "participants"]
    expected_types = {
        "description": str,
        "schedule": str,
        "max_participants": int,
        "participants": list,
    }
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert response.status_code == 200
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_name, str)
        for field in expected_fields:
            assert field in activity_data
            assert isinstance(activity_data[field], expected_types[field])


def test_participant_count_consistency(client):
    """Test that participant count doesn't exceed max_participants"""
    # Arrange
    # (activities loaded from fixture)
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name, activity_data in activities.items():
        participant_count = len(activity_data["participants"])
        max_participants = activity_data["max_participants"]
        
        assert participant_count <= max_participants, \
            f"{activity_name} has {participant_count} participants but max is {max_participants}"


def test_max_participants_is_positive(client):
    """Test that all activities have a positive max_participants value"""
    # Arrange
    min_allowed = 1
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name, activity_data in activities.items():
        assert activity_data["max_participants"] > min_allowed, \
            f"{activity_name} has invalid max_participants value"


def test_participants_are_email_strings(client):
    """Test that all participants are email strings"""
    # Arrange
    email_domain = "@mergington.edu"
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name, activity_data in activities.items():
        for participant in activity_data["participants"]:
            assert isinstance(participant, str)
            assert email_domain in participant
