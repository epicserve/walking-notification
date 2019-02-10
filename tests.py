import walking_notification


def test_get_message():
    message = walking_notification.get_message(
        location='66535',
        client_key=walking_notification.get_env_var('YAHOO_CLIENT_KEY'),
        client_secret=walking_notification.get_env_var('YAHOO_CLIENT_SECRET'),
    )
    assert len(message) > 15
