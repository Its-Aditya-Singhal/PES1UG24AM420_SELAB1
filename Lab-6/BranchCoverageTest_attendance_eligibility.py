import pytest
from attendance_eligibility import attendance_percent, exam_eligibility, attendance_warning


# ---------- attendance_percent ----------
def test_plain_percent():
    assert attendance_percent(30, 40, 0) == 75


def test_percent_zero_total_raises():
    with pytest.raises(ValueError, match="invalid total"):
        attendance_percent(0, 0, 0)


def test_percent_negative_total_raises():
    with pytest.raises(ValueError, match="invalid total"):
        attendance_percent(0, -5, 0)


def test_percent_negative_attended_raises():
    with pytest.raises(ValueError, match="invalid attended count"):
        attendance_percent(-1, 40, 0)


def test_percent_attended_more_than_total_raises():
    with pytest.raises(ValueError, match="invalid attended count"):
        attendance_percent(41, 40, 0)


def test_percent_attended_equals_total_is_valid():
    assert attendance_percent(40, 40, 0) == 100


def test_percent_medical_leave_capped_at_five():
    # 10 days of leave are capped to 5 -> (10 + 5) * 100 // 40
    assert attendance_percent(10, 40, 10) == 37


def test_percent_medical_leave_exactly_five_not_capped():
    assert attendance_percent(10, 40, 5) == 37


def test_percent_credited_capped_at_total():
    # 38 + 5 = 43 > 40, so credited is capped to 40
    assert attendance_percent(38, 40, 5) == 100


def test_percent_credited_equals_total_not_capped():
    assert attendance_percent(35, 40, 5) == 100


# ---------- exam_eligibility ----------
def test_fees_pending():
    assert exam_eligibility(90, True, False) == "fees pending"


def test_eligible():
    assert exam_eligibility(80, False, True) == "eligible"


def test_eligible_boundary_75():
    assert exam_eligibility(75, False, True) == "eligible"


def test_condonation_granted():
    assert exam_eligibility(70, True, True) == "eligible"


def test_condonation_required():
    assert exam_eligibility(70, False, True) == "condonation required"


def test_condonation_boundary_65():
    assert exam_eligibility(65, True, True) == "eligible"
    assert exam_eligibility(65, False, True) == "condonation required"


def test_detained():
    assert exam_eligibility(50, True, True) == "detained"


def test_detained_boundary_64():
    assert exam_eligibility(64, True, True) == "detained"


# ---------- attendance_warning ----------
def test_no_warning_for_high_attendance():
    assert attendance_warning(90, 10) is None


def test_no_warning_boundary_85():
    assert attendance_warning(85, 10) is None


def test_reminder_warning():
    assert attendance_warning(80, 10) == "reminder"


def test_reminder_boundary_75():
    assert attendance_warning(75, 1) == "reminder"


def test_critical_warning_many_weeks_left():
    assert attendance_warning(60, 10) == "critical"


def test_final_notice_few_weeks_left():
    assert attendance_warning(60, 2) == "final notice"


def test_final_notice_boundary_four_weeks():
    assert attendance_warning(74, 4) == "final notice"
    assert attendance_warning(74, 5) == "critical"
