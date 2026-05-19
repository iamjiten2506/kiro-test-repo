import unittest

from login_form import validate_email, validate_login_form, validate_password


class TestValidateEmail(unittest.TestCase):
    """Tests for validate_email function."""

    def test_valid_email_simple(self):
        result = validate_email("user@example.com")
        self.assertTrue(result["valid"])
        self.assertEqual(result["errors"], [])

    def test_valid_email_with_dots(self):
        result = validate_email("first.last@example.com")
        self.assertTrue(result["valid"])
        self.assertEqual(result["errors"], [])

    def test_valid_email_with_plus(self):
        result = validate_email("user+tag@example.com")
        self.assertTrue(result["valid"])
        self.assertEqual(result["errors"], [])

    def test_valid_email_starting_with_plus(self):
        result = validate_email("+user@example.com")
        self.assertTrue(result["valid"])
        self.assertEqual(result["errors"], [])

    def test_valid_email_subdomain(self):
        result = validate_email("user@mail.example.co.uk")
        self.assertTrue(result["valid"])
        self.assertEqual(result["errors"], [])

    def test_valid_email_with_numbers(self):
        result = validate_email("user123@example456.com")
        self.assertTrue(result["valid"])
        self.assertEqual(result["errors"], [])

    def test_invalid_email_empty_string(self):
        with self.assertRaises(ValueError) as ctx:
            validate_email("")
        self.assertEqual(str(ctx.exception), "Email is required")

    def test_invalid_email_none(self):
        with self.assertRaises(ValueError) as ctx:
            validate_email(None)
        self.assertEqual(str(ctx.exception), "Email is required")

    def test_invalid_email_whitespace_only(self):
        with self.assertRaises(ValueError) as ctx:
            validate_email("   ")
        self.assertEqual(str(ctx.exception), "Email is required")

    def test_invalid_email_missing_at(self):
        result = validate_email("userexample.com")
        self.assertFalse(result["valid"])
        self.assertIn("Invalid email format", result["errors"])

    def test_invalid_email_missing_domain(self):
        result = validate_email("user@")
        self.assertFalse(result["valid"])
        self.assertIn("Invalid email format", result["errors"])

    def test_invalid_email_missing_username(self):
        result = validate_email("@example.com")
        self.assertFalse(result["valid"])
        self.assertIn("Invalid email format", result["errors"])

    def test_invalid_email_double_at(self):
        result = validate_email("user@@example.com")
        self.assertFalse(result["valid"])
        self.assertIn("Invalid email format", result["errors"])

    def test_invalid_email_no_tld(self):
        result = validate_email("user@example")
        self.assertFalse(result["valid"])
        self.assertIn("Invalid email format", result["errors"])

    def test_invalid_email_short_tld(self):
        result = validate_email("user@example.c")
        self.assertFalse(result["valid"])
        self.assertIn("Invalid email format", result["errors"])

    def test_invalid_email_spaces(self):
        result = validate_email("user @example.com")
        self.assertFalse(result["valid"])
        self.assertIn("Invalid email format", result["errors"])

    def test_invalid_email_too_long(self):
        long_email = "a" * 245 + "@example.com"
        result = validate_email(long_email)
        self.assertFalse(result["valid"])
        self.assertIn("Email must not exceed 254 characters", result["errors"])


class TestValidatePassword(unittest.TestCase):
    """Tests for validate_password function."""

    def test_valid_password(self):
        result = validate_password("Passw0rd!")
        self.assertTrue(result["valid"])
        self.assertEqual(result["errors"], [])

    def test_valid_password_complex(self):
        result = validate_password("MyStr0ng@Pass")
        self.assertTrue(result["valid"])
        self.assertEqual(result["errors"], [])

    def test_invalid_password_none(self):
        with self.assertRaises(ValueError) as ctx:
            validate_password(None)
        self.assertEqual(str(ctx.exception), "Password is required")

    def test_invalid_password_empty_string(self):
        with self.assertRaises(ValueError) as ctx:
            validate_password("")
        self.assertEqual(str(ctx.exception), "Password is required")

    def test_invalid_password_too_short(self):
        result = validate_password("Ab1!")
        self.assertFalse(result["valid"])
        self.assertIn(
            "Password must be at least 8 characters long", result["errors"]
        )

    def test_invalid_password_no_uppercase(self):
        result = validate_password("password1!")
        self.assertFalse(result["valid"])
        self.assertIn(
            "Password must contain at least one uppercase letter",
            result["errors"],
        )

    def test_invalid_password_no_lowercase(self):
        result = validate_password("PASSWORD1!")
        self.assertFalse(result["valid"])
        self.assertIn(
            "Password must contain at least one lowercase letter",
            result["errors"],
        )

    def test_invalid_password_no_digit(self):
        result = validate_password("Password!")
        self.assertFalse(result["valid"])
        self.assertIn(
            "Password must contain at least one digit", result["errors"]
        )

    def test_invalid_password_no_special_char(self):
        result = validate_password("Password1")
        self.assertFalse(result["valid"])
        self.assertIn(
            "Password must contain at least one special character",
            result["errors"],
        )

    def test_invalid_password_multiple_failures(self):
        result = validate_password("abc")
        self.assertFalse(result["valid"])
        self.assertTrue(len(result["errors"]) > 1)

    def test_valid_password_exactly_8_chars(self):
        result = validate_password("Abcde1!x")
        self.assertTrue(result["valid"])
        self.assertEqual(result["errors"], [])

    def test_valid_password_long(self):
        result = validate_password("A" * 50 + "a1!" + "b" * 50)
        self.assertTrue(result["valid"])
        self.assertEqual(result["errors"], [])

    def test_invalid_password_too_long(self):
        long_password = "Aa1!" + "x" * 125
        result = validate_password(long_password)
        self.assertFalse(result["valid"])
        self.assertIn(
            "Password must not exceed 128 characters", result["errors"]
        )


class TestValidateLoginForm(unittest.TestCase):
    """Tests for validate_login_form function."""

    def test_all_valid(self):
        result = validate_login_form("user@example.com", "Passw0rd!")
        self.assertTrue(result["valid"])
        self.assertEqual(result["errors"]["email"], [])
        self.assertEqual(result["errors"]["password"], [])

    def test_invalid_email_valid_password(self):
        result = validate_login_form("invalid", "Passw0rd!")
        self.assertFalse(result["valid"])
        self.assertTrue(len(result["errors"]["email"]) > 0)
        self.assertEqual(result["errors"]["password"], [])

    def test_valid_email_invalid_password(self):
        result = validate_login_form("user@example.com", "weak")
        self.assertFalse(result["valid"])
        self.assertEqual(result["errors"]["email"], [])
        self.assertTrue(len(result["errors"]["password"]) > 0)

    def test_valid_email_empty_password(self):
        with self.assertRaises(ValueError) as ctx:
            validate_login_form("user@example.com", "")
        self.assertEqual(str(ctx.exception), "Password is required")

    def test_both_invalid_empty(self):
        with self.assertRaises(ValueError) as ctx:
            validate_login_form("", "")
        self.assertEqual(str(ctx.exception), "Email is required")

    def test_none_inputs(self):
        with self.assertRaises(ValueError) as ctx:
            validate_login_form(None, None)
        self.assertEqual(str(ctx.exception), "Email is required")

    def test_whitespace_only_inputs(self):
        with self.assertRaises(ValueError) as ctx:
            validate_login_form("   ", "   ")
        self.assertEqual(str(ctx.exception), "Email is required")


if __name__ == "__main__":
    unittest.main()
