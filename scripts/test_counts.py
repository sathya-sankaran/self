"""Tests for scripts/counts.py. Run: python3 -m unittest scripts/test_counts.py"""

import unittest

from counts import sync

PAGE = """<b data-count="tools">5</b> free tools: <span data-list="tools">old list</span>.
<h2><span data-count="tools" data-as="word">Five</span> things</h2>
<b data-count="stories">1</b> stories: <span data-list="stories">x</span>.
<section id="tools">
  <article class="card span-4" data-teaser="an atlas">a</article>
  <article class="card span-4" data-teaser="live air">b</article>
  <article class="card span-4" data-teaser="a raga identifier">c</article>
</section>
<section id="work"><article class="card span-6" data-teaser="not a tool">w</article></section>
<a class="story" data-teaser="soil" href="x">s</a>
<a class="story" data-teaser="forests" href="y">t</a>
"""


class Sync(unittest.TestCase):
    def test_counts_and_lists_follow_the_cards(self):
        out = sync(PAGE)
        self.assertIn('<b data-count="tools">3</b>', out)
        self.assertIn('<span data-count="tools" data-as="word">Three</span>', out)
        self.assertIn('<span data-list="tools">an atlas, live air, and a raga identifier</span>', out)
        self.assertIn('<b data-count="stories">2</b>', out)
        self.assertIn('<span data-list="stories">soil and forests</span>', out)

    def test_only_cards_in_the_tools_section_count_as_tools(self):
        self.assertNotIn("not a tool", sync(PAGE).split("</h2>")[0])

    def test_a_second_run_changes_nothing(self):
        once = sync(PAGE)
        self.assertEqual(sync(once), once)

    def test_a_card_without_a_teaser_is_an_error(self):
        with self.assertRaises(ValueError):
            sync(PAGE.replace(' data-teaser="live air"', ""))


if __name__ == "__main__":
    unittest.main()
