import pytest
from dash.testing.application_runners import import_app


@pytest.fixture
def app(dash_duo):
    application = import_app("app")
    dash_duo.start_server(application)
    return dash_duo


def test_header_present(app):
    """The page header should be visible."""
    header = app.find_element("#header")
    assert header.is_displayed()
    assert header.text == "Pink Morsel Sales Visualiser"


def test_chart_present(app):
    """The sales line chart should be rendered on the page."""
    # Wait for the Plotly graph to finish rendering inside the dcc.Graph container
    chart = app.wait_for_element("#sales-chart .js-plotly-plot")
    assert chart.is_displayed()


def test_region_picker_present(app):
    """The region filter radio group should be present with all five options."""
    picker = app.find_element("#region-filter")
    assert picker.is_displayed()

    options = app.find_elements("#region-filter input[type='radio']")
    assert len(options) == 5
