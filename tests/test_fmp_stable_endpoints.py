from ModifiedModule.fmpsdk import company_valuation


def _capture_stable_request(monkeypatch):
    captured = {}

    def fake_request(path, query_vars):
        captured.update(path=path, query_vars=query_vars)
        return []

    monkeypatch.setattr(company_valuation, "__return_json_stable", fake_request)
    return captured


def test_company_profile_uses_stable_endpoint(monkeypatch):
    captured = _capture_stable_request(monkeypatch)

    company_valuation.company_profile("secret", "AAPL")

    assert captured == {
        "path": "profile",
        "query_vars": {"apikey": "secret", "symbol": "AAPL"},
    }


def test_financial_statements_use_stable_endpoint(monkeypatch):
    captured = _capture_stable_request(monkeypatch)

    company_valuation.balance_sheet_statement("secret", "AAPL", period="quarter", limit=20)

    assert captured["path"] == "balance-sheet-statement"
    assert captured["query_vars"] == {
        "apikey": "secret",
        "limit": 20,
        "period": "quarter",
        "symbol": "AAPL",
    }


def test_ratios_use_stable_endpoint(monkeypatch):
    captured = _capture_stable_request(monkeypatch)

    company_valuation.financial_ratios("secret", "AAPL", period="annual", limit=10)

    assert captured["path"] == "ratios"
    assert captured["query_vars"]["symbol"] == "AAPL"
