from decimal import Decimal
from unittest.mock import MagicMock, patch

import pytest

from src.external_api import _get_exchange_rates, convert_transaction_to_rubles


class TestGetExchangeRates:
    @patch("src.external_api.requests.get")
    def test_success_response(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.raise_for_status.return_value = None
        mock_resp.json.return_value = {
            "Valute": {
                "USD": {"CharCode": "USD", "Value": 90.55},
                "EUR": {"CharCode": "EUR", "Value": 98.32},
                "JPY": {"CharCode": "JPY", "Value": 65.1},
            }
        }
        mock_get.return_value = mock_resp

        rates = _get_exchange_rates()

        assert rates is not None
        assert "USD" in rates
        assert "EUR" in rates
        assert "JPY" not in rates
        assert isinstance(rates["USD"], Decimal)
        assert float(rates["USD"]) == 90.55

    @patch("src.external_api.requests.get")
    def test_request_failure(self, mock_get):
        # Важно: side_effect выбрасывает исключение, функция его ловит и возвращает None
        mock_get.side_effect = Exception("Network error")
        rates = _get_exchange_rates()
        assert rates is None

    @patch("src.external_api.requests.get")
    def test_invalid_json(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.raise_for_status.return_value = None
        mock_resp.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_resp

        rates = _get_exchange_rates()
        assert rates is None


class TestConvertTransactionToRubles:
    @patch("src.external_api._get_exchange_rates")
    def test_convert_usd_to_rub(self, mock_get_rates):
        mock_get_rates.return_value = {"USD": Decimal("90.5")}

        transaction = {
            "id": 123,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "100.00",
                "currency": {"name": "US Dollar", "code": "USD"}
            }
        }

        result = convert_transaction_to_rubles(transaction)
        assert result == 9050.0

    @patch("src.external_api._get_exchange_rates")
    def test_convert_eur_to_rub(self, mock_get_rates):
        mock_get_rates.return_value = {"EUR": Decimal("98.2")}

        transaction = {
            "id": 456,
            "state": "EXECUTED",
            "date": "2018-07-01T10:15:20.123456",
            "operationAmount": {
                "amount": 50.75,
                "currency": {"name": "Euro", "code": "EUR"}
            }
        }

        result = convert_transaction_to_rubles(transaction)
        expected = 50.75 * 98.2
        assert abs(result - expected) < 0.01

    def test_rub_amount_no_conversion(self):
        transaction = {
            "id": 789,
            "state": "EXECUTED",
            "date": "2018-07-02T11:20:30.654321",
            "operationAmount": {
                "amount": "1234.56",
                "currency": {"name": "Russian Ruble", "code": "RUB"}
            }
        }

        result = convert_transaction_to_rubles(transaction)
        assert result == 1234.56

    @patch("src.external_api._get_exchange_rates")
    def test_rates_unavailable(self, mock_get_rates):
        mock_get_rates.return_value = None

        transaction = {
            "id": 101,
            "state": "EXECUTED",
            "date": "2018-07-03T12:25:40.111222",
            "operationAmount": {
                "amount": "200.00",
                "currency": {"name": "Dollar", "code": "USD"}
            }
        }

        with pytest.raises(RuntimeError, match="Не удалось получить курсы валют"):
            convert_transaction_to_rubles(transaction)

    @patch("src.external_api._get_exchange_rates")
    def test_missing_rate_for_currency(self, mock_get_rates):
        mock_get_rates.return_value = {"EUR": Decimal("98.2")}

        transaction = {
            "id": 202,
            "state": "EXECUTED",
            "date": "2018-07-04T13:30:50.333444",
            "operationAmount": {
                "amount": "300.00",
                "currency": {"name": "Dollar", "code": "USD"}
            }
        }

        with pytest.raises(RuntimeError, match="Курс для валюты USD не найден"):
            convert_transaction_to_rubles(transaction)

    def test_invalid_operation_amount(self):
        transaction = {
            "id": 303,
            "state": "EXECUTED",
            "date": "2018-07-05T14:35:00.555666",
        }

        with pytest.raises(ValueError, match="отсутствует или неверно заполнено поле 'operationAmount'"):
            convert_transaction_to_rubles(transaction)

    def test_invalid_currency_field(self):
        transaction = {
            "id": 404,
            "state": "EXECUTED",
            "date": "2018-07-06T15:40:10.777888",
            "operationAmount": {
                "amount": "400.00",
                "currency": "USD"
            }
        }

        with pytest.raises(ValueError, match="неверно заполнено поле 'currency'"):
            convert_transaction_to_rubles(transaction)

    def test_unsupported_currency(self):
        transaction = {
            "id": 505,
            "state": "EXECUTED",
            "date": "2018-07-07T16:45:20.999000",
            "operationAmount": {
                "amount": "500.00",
                "currency": {"name": "Bitcoin", "code": "BTC"}
            }
        }

        with pytest.raises(ValueError, match="Неподдерживаемая валюта"):
            convert_transaction_to_rubles(transaction)

    def test_amount_not_numeric(self):
        transaction = {
            "id": 606,
            "state": "EXECUTED",
            "date": "2018-07-08T17:50:30.123456",
            "operationAmount": {
                "amount": "not_a_number",
                "currency": {"name": "Dollar", "code": "USD"}
            }
        }

        with pytest.raises(ValueError, match="Поле 'amount' не может быть преобразовано в число"):
            convert_transaction_to_rubles(transaction)
