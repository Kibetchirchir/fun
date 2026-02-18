from django.test import TestCase

# Create your tests here.
from django.core.exceptions import ValidationError
from users.validators import validate_nid, validate_phone_number

class ValidatorTests(TestCase):
    # NID Validator Tests
    def test_valid_nid(self):
        valid_nid = "1234567890123456"
        self.assertEqual(validate_nid(valid_nid), valid_nid)

    def test_nid_too_short(self):
        short_nid = "12345678"
        with self.assertRaises(ValidationError):
            validate_nid(short_nid)

    def test_nid_too_long(self):
        long_nid = "12345678901234567890"
        with self.assertRaises(ValidationError):
            validate_nid(long_nid)

    def test_nid_non_digit(self):
        invalid_nid = "12345678901234ab"
        with self.assertRaises(ValidationError):
            validate_nid(invalid_nid)

    # Phone Number Validator Tests
    def test_valid_phone_number(self):
        valid_phone = "123456789012"
        self.assertEqual(validate_phone_number(valid_phone), valid_phone)

    def test_phone_number_too_short(self):
        short_phone = "12345"
        with self.assertRaises(ValidationError):
            validate_phone_number(short_phone)

    def test_phone_number_too_long(self):
        long_phone = "1234567890123456"
        with self.assertRaises(ValidationError):
            validate_phone_number(long_phone)

    def test_phone_number_non_digit(self):
        invalid_phone = "12345abc9012"
        with self.assertRaises(ValidationError):
            validate_phone_number(invalid_phone)

    def test_phone_number_starts_with_250(self):
        phone_with_250 = "250123456789"
        with self.assertRaises(ValidationError):
            validate_phone_number(phone_with_250)