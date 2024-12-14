import unittest

import thalesians.adiutor.strings as our_strings

class Test(unittest.TestCase):
    def test_sanitize_str(self):
        self.assertEqual(
                our_strings.sanitize_str("Hello, Hélyette?! This  is a__raw_str"),
                "hello_helyette_this_is_a_raw_str")
        
    def test_make_unique_str(self):
        self.assertEqual(our_strings.make_unique_str("foo", ["bar"]), "foo")
        self.assertEqual(
                our_strings.make_unique_str("foo", ["foo", "foo_1", "foo_3"]),
                "foo_2")

if __name__ == "__main__":
    unittest.main()
    