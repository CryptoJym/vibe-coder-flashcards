from datetime import date

from packages.core.spaced_repetition import sm2, Card, schedule_cards, due_cards


def test_sm2_known_example():
    rep, interval, ef = sm2(0, 0, 2.5, 5)
    assert rep == 1
    assert interval == 1
    assert round(ef, 2) == 2.6

    rep, interval, ef = sm2(rep, interval, ef, 5)
    assert rep == 2
    assert interval == 6
    assert round(ef, 2) == 2.7

    rep, interval, ef = sm2(rep, interval, ef, 5)
    assert rep == 3
    assert interval == round(6 * 2.7)
    assert round(ef, 2) == 2.8

    # failure resets repetition and interval but keeps ef
    rep, interval, ef = sm2(rep, interval, ef, 2)
    assert rep == 0
    assert interval == 1
    assert round(ef, 2) == 2.8


def test_daily_scheduling_and_deck():
    today = date(2024, 1, 1)
    cards = [
        Card(id=1, question="q1", answer="a1", repetition=2, interval=6, ease_factor=2.5, next_review=today, grade=5),
        Card(id=2, question="q2", answer="a2", repetition=1, interval=1, ease_factor=2.5, next_review=today, grade=2),
        Card(id=3, question="q3", answer="a3", repetition=0, interval=0, ease_factor=2.5, next_review=today, grade=None),
    ]

    schedule_cards(cards, today)

    # card1 graded 5 -> rep3 interval round(6*2.5)=15, ef>2.5
    c1 = cards[0]
    assert c1.repetition == 3
    assert c1.interval == 15
    assert round(c1.ease_factor, 2) > 2.5
    assert c1.next_review == date(2024, 1, 16)
    assert c1.grade is None

    # card2 graded 2 -> reset
    c2 = cards[1]
    assert c2.repetition == 0
    assert c2.interval == 1
    assert c2.next_review == date(2024, 1, 2)

    # due cards for today after scheduling
    due = due_cards(cards, today)
    # only card3 remained due because others moved to future
    assert [c.id for c in due] == [3]
