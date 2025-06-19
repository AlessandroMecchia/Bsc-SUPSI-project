import pytest
from datetime import datetime
from mongoengine import ValidationError
from web_service.models.activity import Activity
from web_service.models.athlete import Athlete 
from unittest.mock import Mock

class TestActivityModel:

    def setup_method(self):
        self.mock_athlete = Mock(spec=Athlete)

    def test_valid_activity(self):
        activity = Activity(
            _id=1,
            athlete=self.mock_athlete,
            name="Morning Run",
            start_date=datetime.utcnow(),
            elapsed_time=3600,
            distance=10.0
        )
        activity.validate()  # Should not raise

    def test_missing_required_fields(self):
        with pytest.raises(ValidationError):
            activity = Activity()
            activity.validate()

    def test_invalid_resource_state(self):
        with pytest.raises(ValidationError):
            activity = Activity(
                _id=2,
                athlete=self.mock_athlete,
                name="Invalid Resource State",
                start_date=datetime.utcnow(),
                resource_state=99  # Invalid choice
            )
            activity.validate()

    def test_pointfield_accepts_valid_data(self):
        activity = Activity(
            _id=3,
            athlete=self.mock_athlete,
            name="Geo Test",
            start_date=datetime.utcnow(),
            start_latlng=[12.34, 56.78],
            end_latlng=[87.65, 43.21]
        )
        activity.validate()

    def test_negative_elapsed_time_allowed(self):
        # If you want to prevent this, you'd need to add a custom clean() method.
        activity = Activity(
            _id=4,
            athlete=self.mock_athlete,
            name="Test",
            start_date=datetime.utcnow(),
            elapsed_time=-100
        )
        activity.validate()  # Passes unless you add custom validation

    def test_missing_athlete(self):
        with pytest.raises(ValidationError):
            activity = Activity(
                _id=5,
                name="No Athlete",
                start_date=datetime.utcnow()
            )
            activity.validate()

    def test_max_field_lengths(self):
        activity = Activity(
            _id=6,
            athlete=self.mock_athlete,
            name="a" * 200,  # Max allowed
            start_date=datetime.utcnow()
        )
        activity.validate()
        
        with pytest.raises(ValidationError):
            activity = Activity(
                _id=7,
                athlete=self.mock_athlete,
                name="a" * 201,  # Too long
                start_date=datetime.utcnow()
            )
            activity.validate()
