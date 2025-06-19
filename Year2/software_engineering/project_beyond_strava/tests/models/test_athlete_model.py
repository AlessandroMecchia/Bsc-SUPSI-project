import pytest
from mongoengine import ValidationError
from web_service.models.athlete import Athlete 

class TestAthleteModel:

    def test_valid_athlete(self):
        athlete = Athlete(
            athlete_id=1,
            username="runner123",
            firstname="Alice",
            lastname="Smith",
            sex="F",
            weight=60.5,
            city="Paris",
            country="France"
        )
        # Should pass validation without error
        athlete.validate()

    def test_missing_required_fields(self):
        with pytest.raises(ValidationError):
            athlete = Athlete(athlete_id=123)
            athlete.validate()

    def test_invalid_sex_choice(self):
        with pytest.raises(ValidationError):
            athlete = Athlete(
                athlete_id=2,
                username="testuser",
                firstname="Jane",
                lastname="Doe",
                sex="X"  # Invalid choice
            )
            athlete.validate()

    def test_negative_weight(self):
        with pytest.raises(ValidationError):
            athlete = Athlete(
                athlete_id=3,
                username="badweight",
                firstname="Bob",
                lastname="Builder",
                weight=-10.0
            )
            athlete.validate()

    def test_default_values(self):
        athlete = Athlete(
            athlete_id=4,
            username="defaultuser",
            firstname="Default",
            lastname="User"
        )
        assert athlete.weight == 0.0
        assert athlete.city == ""
        assert athlete.state == ""
        assert athlete.country == ""
        assert athlete.sex == "O"  # Default

