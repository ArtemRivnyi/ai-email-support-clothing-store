"""
End-to-end test string requires manual Gmail setup.
Skipped to allow other tests to run.
"""
import pytest

@pytest.mark.skip(reason="Requires manual Gmail credential setup and valid mock services")
@pytest.mark.e2e
def test_full_email_flow():
    pass
