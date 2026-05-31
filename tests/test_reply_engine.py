import unittest

from auto_reply_bot.reply_engine import ReplyRule, choose_reply, is_opt_out, normalize_message


class ReplyEngineTests(unittest.TestCase):
    def test_normalize_message_removes_extra_spacing(self):
        self.assertEqual(normalize_message("  hey   there  "), "hey there")

    def test_rule_match_is_case_insensitive(self):
        rules = [ReplyRule(name="hello", pattern=r"\bhello\b", reply="Hi there")]
        self.assertEqual(choose_reply("HELLO", rules), "Hi there")

    def test_default_reply_when_no_rule_matches(self):
        self.assertEqual(choose_reply("random text", [], "Fallback"), "Fallback")

    def test_empty_message_gets_helpful_reply(self):
        self.assertIn("empty", choose_reply("   ", []).lower())

    def test_opt_out_words_are_detected(self):
        self.assertTrue(is_opt_out("STOP"))
        self.assertTrue(choose_reply("stop", []).startswith("You have been unsubscribed"))


if __name__ == "__main__":
    unittest.main()

