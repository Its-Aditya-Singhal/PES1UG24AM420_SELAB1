import pytest
from attendance_eligibility import attendance_percent, exam_eligibility, attendance_warning


# ---------- attendance_percent ----------
def test_plain_percent():
    assert attendance_percent(30, 40, 0) == 75


def test_percent_zero_total_raises():
    with pytest.raises(ValueError):
        attendance_percent(0, 0, 0)


def test_percent_negative_attended_raises():
    with pytest.raises(ValueError):
        attendance_percent(-1, 40, 0)


def test_percent_attended_more_than_total_raises():
    with pytest.raises(ValueError):
        attendance_percent(41, 40, 0)


def test_percent_medical_leave_capped_at_five():
    # 10 days of leave are capped to 5 -> (10 + 5) * 100 // 40
    assert attendance_percent(10, 40, 10) == 37


# ---------- exam_eligibility ----------
def test_eligible():
    assert exam_eligibility(80, False, True) == "eligible"


def test_fees_pending():
    assert exam_eligibility(90, True, False) == "fees pending"


def test_condonation_granted():
    assert exam_eligibility(70, True, True) == "eligible"


def test_condonation_required():
    assert exam_eligibility(70, False, True) == "condonation required"


def test_detained():
    assert exam_eligibility(50, True, True) == "detained"


# ---------- attendance_warning ----------
def test_no_warning_for_high_attendance():
    assert attendance_warning(90, 10) is None


def test_critical_warning():
    assert attendance_warning(60, 10) == "critical"


def test_reminder_warning():
    assert attendance_warning(80, 10) == "reminder"
