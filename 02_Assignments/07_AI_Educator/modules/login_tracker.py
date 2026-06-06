import json
from datetime import datetime, timedelta, date
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
LOGIN_FILE = DATA_DIR / "login_tracker.json"


def _load_logins() -> dict:
    DATA_DIR.mkdir(exist_ok=True)
    if LOGIN_FILE.exists():
        with open(LOGIN_FILE, "r") as f:
            return json.load(f)
    return {"logins": []}


def _save_logins(data: dict):
    DATA_DIR.mkdir(exist_ok=True)
    with open(LOGIN_FILE, "w") as f:
        json.dump(data, f, indent=2)


def record_login():
    data = _load_logins()
    now = datetime.now()
    data["logins"].append({
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "datetime": now.isoformat(),
    })
    _save_logins(data)


def get_unique_login_dates() -> set:
    return {entry["date"] for entry in _load_logins()["logins"]}


def get_current_streak(login_dates: set) -> int:
    streak = 0
    check = date.today()
    while check.strftime("%Y-%m-%d") in login_dates:
        streak += 1
        check -= timedelta(days=1)
    return streak


def get_longest_streak(login_dates: set) -> int:
    if not login_dates:
        return 0
    sorted_dates = sorted(
        datetime.strptime(d, "%Y-%m-%d").date() for d in login_dates
    )
    longest = current = 1
    for i in range(1, len(sorted_dates)):
        if (sorted_dates[i] - sorted_dates[i - 1]).days == 1:
            current += 1
            longest = max(longest, current)
        else:
            current = 1
    return longest


def get_missed_dates_last_n(login_dates: set, n: int = 30) -> list[str]:
    today = date.today()
    return [
        (today - timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range(1, n + 1)
        if (today - timedelta(days=i)).strftime("%Y-%m-%d") not in login_dates
    ]


def get_dashboard_data() -> dict:
    data = _load_logins()
    login_dates = get_unique_login_dates()
    missed = get_missed_dates_last_n(login_dates, 30)

    return {
        "total_sessions":  len(data["logins"]),
        "total_days":      len(login_dates),
        "current_streak":  get_current_streak(login_dates),
        "longest_streak":  get_longest_streak(login_dates),
        "missed_last_30":  len(missed),
        "missed_dates":    missed,
        "login_dates":     login_dates,
        "all_logins":      data["logins"],
    }
