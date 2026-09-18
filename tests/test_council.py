"""Behavioural fixtures for scripts/council.py — no model calls. Each test names the invariant it protects."""
import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
from council import member_status, parse_review, aggregate, split_members, trigger

ANSWER = "\n\n".join(f"{h}\nA substantive sentence about this section of the answer." for h in
                     ["## Core judgment", "## Top risks", "## Recommended change", "## Confidence", "## Weakest assumption"])
M = ["Pragmatist", "Skeptic", "Devil's Advocate"]

def block(member, c=4, i=4, p=4, r=4, abstain="false"):
    return f"```rubric\nmember: {member}\ncorrectness: {c}\ninsight: {i}\npractical: {p}\nrisk: {r}\nabstain: {abstain}\n```\n"
def review(scores):  # scores: {member: (c, i, p, r)}
    return "prose first\n" + "".join(block(m, *s) for m, s in scores.items())

class Members(unittest.TestCase):
    def test_answer_with_five_sections_is_valid(self): self.assertEqual(member_status(ANSWER), "answered")
    def test_abstention_alone_is_valid_and_needs_no_sections(self):
        self.assertEqual(member_status("OUT OF DOMAIN — defer to others on this question."), "abstained")
    def test_empty_output_is_a_failure_not_an_abstention(self): self.assertEqual(member_status("  ")[0], "invalid")
    def test_headers_with_nothing_under_them_are_rejected(self):
        self.assertEqual(member_status("\n".join(["## Core judgment", "## Top risks", "- ", "## Recommended change", "## Confidence", "## Weakest assumption"]))[0], "invalid")
    def test_missing_section_is_rejected(self): self.assertEqual(member_status(ANSWER.replace("## Confidence", "## Sureness"))[0], "invalid")

class Reviews(unittest.TestCase):
    def test_valid_review_parses(self):
        r = parse_review(review({m: (5, 4, 3, 2) for m in M}), M); self.assertEqual(r["Skeptic"], {"correctness": 5, "insight": 4, "practical": 3, "risk": 2})
    def test_out_of_range_and_non_integer_scores_are_rejected_not_truncated(self):
        for bad in ["0", "6", "10", "5.5", "true", "4 out of 5", "-1", ""]:
            with self.assertRaises(ValueError, msg=bad): parse_review(review({m: (4, 4, 4, 4) for m in M}).replace("correctness: 4", f"correctness: {bad}", 1), M)
    def test_missing_unknown_and_duplicate_members_are_rejected(self):
        with self.assertRaises(ValueError): parse_review(review({m: (4, 4, 4, 4) for m in M[:2]}), M)
        with self.assertRaises(ValueError): parse_review(review({**{m: (4, 4, 4, 4) for m in M}, "Stranger": (5, 5, 5, 5)}), M)
        with self.assertRaises(ValueError): parse_review(review({m: (4, 4, 4, 4) for m in M}) + block("Skeptic"), M)
    def test_abstainer_is_NA_and_left_out_of_averages_not_scored_zero(self):
        txt = review({"Pragmatist": (5, 5, 5, 5), "Skeptic": (3, 3, 3, 3)}) + block("Devil's Advocate", "N/A", "N/A", "N/A", "N/A", "true")
        agg = aggregate({"r1": parse_review(txt, M)}, M); self.assertIsNone(agg["Devil's Advocate"]); self.assertEqual(agg["Pragmatist"]["overall"], 5)
    def test_abstainer_with_numeric_scores_is_malformed(self):
        with self.assertRaises(ValueError): parse_review(review({m: (4, 4, 4, 4) for m in M[:2]}) + block("Devil's Advocate", abstain="true"), M)

class Trigger(unittest.TestCase):
    def revs(self, *rows): return {f"r{k}": parse_review(review(dict(zip(M, row))), M) for k, row in enumerate(rows)}
    def test_all_abstain_gives_no_averages(self):
        txt = "".join(block(m, "N/A", "N/A", "N/A", "N/A", "true") for m in M); agg, fired = trigger({"r1": parse_review(txt, M)}, M)
        self.assertTrue(all(v is None for v in agg.values())); self.assertEqual(fired, [])
    def test_clause_1_variance(self):
        _, fired = trigger(self.revs(((5,5,5,5),(4,4,4,4),(1,4,4,4)), ((5,5,5,5),(4,4,4,4),(5,4,4,4)), ((5,5,5,5),(4,4,4,4),(1,4,4,4))), M)
        self.assertTrue(any(f.startswith("clause 1") and "Devil's Advocate" in f for f in fired))
    def test_clause_2_real_split_fires(self):
        r = self.revs(((5,4,4,4),(4,4,4,4),(3,4,4,4)), ((3,4,4,4),(4,4,4,4),(5,4,4,4)))
        self.assertTrue(any(m == "Pragmatist" and a == "correctness" for m, a, *_ in split_members(r, M)))
    def test_clause_2_one_point_gap_among_ties_is_noise(self):
        r = self.revs(((5,4,4,4),(5,4,4,4),(5,4,4,4)), ((4,4,4,4),(5,4,4,4),(5,4,4,4)))  # flat tie in r0, a 5-vs-4 in r1
        self.assertEqual(split_members(r, M), [])
    def test_clause_3_equal_scores_with_a_split_on_the_conclusion_still_fires(self):
        _, fired = trigger(self.revs(((4,4,4,4),) * 3, ((4,4,4,4),) * 3), M, positions={"migrate": 2, "wait": 2, "neither": 1})
        self.assertTrue(any(f.startswith("clause 3") for f in fired))
    def test_clause_3_majority_does_not_fire(self):
        _, fired = trigger(self.revs(((4,4,4,4),) * 3), M, positions={"migrate": 3, "wait": 2}); self.assertEqual(fired, [])

if __name__ == "__main__": unittest.main()
