#
# Copyright (c) 2022 Airbyte, Inc., all rights reserved.
#

from datetime import date, timedelta

from airbyte_cdk.sources.streams.http.auth import NoAuth
from source_mixpanel.source import Annotations


def test_date_slices():

    now = date.today()
    # Test with start_date now range
    stream_slices = Annotations(authenticator=NoAuth(), start_date=now, end_date=now, date_window_size=1, region="EU").stream_slices(
        sync_mode="any"
    )
    assert 1 == len(stream_slices)

    stream_slices = Annotations(
        authenticator=NoAuth(), start_date=now - timedelta(days=1), end_date=now, date_window_size=1, region="US"
    ).stream_slices(sync_mode="any")
    assert 2 == len(stream_slices)

    stream_slices = Annotations(authenticator=NoAuth(), start_date=now - timedelta(days=2), end_date=now, date_window_size=1).stream_slices(
        sync_mode="any"
    )
    assert 3 == len(stream_slices)

    stream_slices = Annotations(
        authenticator=NoAuth(), start_date=now - timedelta(days=2), end_date=now, date_window_size=10
    ).stream_slices(sync_mode="any")
    assert 1 == len(stream_slices)

    # test with attribution_window
    stream_slices = Annotations(
        authenticator=NoAuth(),
        start_date=now - timedelta(days=2),
        end_date=now,
        date_window_size=1,
        attribution_window=5,
        region="US",
    ).stream_slices(sync_mode="any")
    assert 8 == len(stream_slices)

    # Test with start_date end_date range
    stream_slices = Annotations(
        authenticator=NoAuth(),
        start_date=date.fromisoformat("2021-07-01"),
        end_date=date.fromisoformat("2021-07-01"),
        date_window_size=1,
        region="US",
    ).stream_slices(sync_mode="any")
    assert [{"start_date": "2021-07-01", "end_date": "2021-07-01"}] == stream_slices

    stream_slices = Annotations(
        authenticator=NoAuth(),
        start_date=date.fromisoformat("2021-07-01"),
        end_date=date.fromisoformat("2021-07-02"),
        date_window_size=1,
        region="EU",
    ).stream_slices(sync_mode="any")
    assert [{"start_date": "2021-07-01", "end_date": "2021-07-01"}, {"start_date": "2021-07-02", "end_date": "2021-07-02"}] == stream_slices

    stream_slices = Annotations(
        authenticator=NoAuth(),
        start_date=date.fromisoformat("2021-07-01"),
        end_date=date.fromisoformat("2021-07-03"),
        date_window_size=1,
        region="US",
    ).stream_slices(sync_mode="any")
    assert [
        {"start_date": "2021-07-01", "end_date": "2021-07-01"},
        {"start_date": "2021-07-02", "end_date": "2021-07-02"},
        {"start_date": "2021-07-03", "end_date": "2021-07-03"},
    ] == stream_slices

    stream_slices = Annotations(
        authenticator=NoAuth(),
        start_date=date.fromisoformat("2021-07-01"),
        end_date=date.fromisoformat("2021-07-03"),
        date_window_size=2,
        region="US",
    ).stream_slices(sync_mode="any")
    assert [{"start_date": "2021-07-01", "end_date": "2021-07-02"}, {"start_date": "2021-07-03", "end_date": "2021-07-03"}] == stream_slices

    # test with stream_state
    stream_slices = Annotations(
        authenticator=NoAuth(),
        start_date=date.fromisoformat("2021-07-01"),
        end_date=date.fromisoformat("2021-07-03"),
        date_window_size=1,
    ).stream_slices(sync_mode="any", stream_state={"date": "2021-07-02"})
    assert [{"start_date": "2021-07-02", "end_date": "2021-07-02"}, {"start_date": "2021-07-03", "end_date": "2021-07-03"}] == stream_slices
