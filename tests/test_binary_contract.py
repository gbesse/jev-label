import unittest,math
from jev_label import evaluate,fit_threshold
class BinaryContract(unittest.TestCase):
 def test_string_false_is_not_positive(self):
  with self.assertRaises(ValueError):evaluate([{'probability':.9,'label':'false'}])
 def test_missing_label_not_false_negative(self):
  with self.assertRaises(ValueError):fit_threshold([{'probability':.9,'label':None}])
 def test_nonfinite_probability(self):
  with self.assertRaises(ValueError):evaluate([{'probability':math.nan,'label':True}])
 def test_empty_set_not_division_by_zero(self):
  with self.assertRaises(ValueError):evaluate([])
 def test_zero_one_compatibility(self):
  self.assertEqual(evaluate([{'probability':.9,'label':1},{'probability':.1,'label':0}])['accuracy'],1)
