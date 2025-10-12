from h800.punchcard import Deck, PunchCard


def test_punchcard_basic():
    line = " 0981   BACKUP     TS           S ZERO        COMMON        SET UP GPB     C    COMMUNICATION FLAG FOR END."
    card = PunchCard(line)

    # Raw line preservation
    assert card.line == line

    # Layout: list of (start_column, width)
    assert card.layout == [
        (1, 1),
        (2, 6),
        (8, 1),
        (9, 11),
        (20, 13),
        (33, 14),
        (47, 14),
        (61, 15),
        (76, 5),
        (81, 40),
    ]

    # Raw fields (sliced with original spacing)
    assert card.fields == [
        " ",
        "0981  ",
        " ",
        "BACKUP     ",
        "TS           ",
        "S ZERO        ",
        "COMMON        ",
        "SET UP GPB     ",
        "C    ",
        "COMMUNICATION FLAG FOR END.",
    ]

    # Stripped fields (None for empty/blank)
    assert card.stripped_fields == [
        None,
        "0981",
        None,
        "BACKUP",
        "TS",
        "S ZERO",
        "COMMON",
        "SET UP GPB",
        "C",
        "COMMUNICATION FLAG FOR END.",
    ]

    # Record dictionary
    assert card.record == {
        "column1": None,
        "lognum": "0981",
        "column8": None,
        "label": "BACKUP",
        "operation": "TS",
        "operand1": "S ZERO",
        "operand2": "COMMON",
        "operand3": "SET UP GPB",
        "misc": "C",
        "remarks": "COMMUNICATION FLAG FOR END.",
    }

    # Comment detection
    assert card.is_comment is False
    assert card.comment is None


def test_punchcard_comment_line():
    comment_line = "# This is a comment line"
    card = PunchCard(comment_line)
    assert card.line == comment_line
    assert card.is_comment is True
    assert card.comment == comment_line
    # No fields should be parsed for comment cards
    assert card.fields == []
    assert card.stripped_fields == []
    assert card.record == {}


def test_deck_basic():
    lines = [
        "# Header comment",
        " 0981   BACKUP     TS           S ZERO        COMMON        SET UP GPB     C    COMMUNICATION FLAG FOR END.",
        " 0983              TS           Z,SC,4        N,SH          MON WAKE       C",
        "# Another comment",
    ]
    deck = Deck(lines=lines)

    # Deck fields
    assert len(deck.cards) == 2  # Only non-comment lines become cards
    assert deck.lines == lines
    assert len(deck.records) == 2

    # Check first card record matches previous test
    rec0 = deck.records[0]
    assert rec0["label"] == "BACKUP"
    assert rec0["operation"] == "TS"
    assert rec0["operand1"] == "S ZERO"

    # Ensure snake_case attribute access works
    assert deck.stripped_fields[0][1] == "0981"  # lognum stripped
    # Ensure second card has expected operand field mapping
    rec1 = deck.records[1]
    assert rec1["operation"] == "TS"
    assert rec1["operand1"] == "Z,SC,4"
    assert rec1["operand2"] == "N,SH"


def test_deck_no_input_error():
    # Expect system exit if neither lines nor file provided.
    import sys

    import pytest

    class ExitInterceptError(Exception):
        pass

    def fake_exit(msg):
        raise ExitInterceptError(msg)

    # Monkeypatch sys.exit
    original_exit = sys.exit
    sys.exit = fake_exit
    try:
        with pytest.raises(ExitInterceptError):
            Deck()  # type: ignore
    finally:
        sys.exit = original_exit
