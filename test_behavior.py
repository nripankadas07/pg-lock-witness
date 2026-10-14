import unittest
from pg_lock_witness import analyze

def fixture(*pairs):return {'sessions':[{'pid':p,'blocking_pids':b} for p,b in pairs]}
class Behavior(unittest.TestCase):
    def test_cycle_edges(self):
        r=analyze(fixture((1,[2]),(2,[1])));self.assertEqual(r['cycles'][0]['cycle'],[1,2,1]);self.assertEqual(r['cycles'][0]['edges'],[{'waiter':1,'blocker':2},{'waiter':2,'blocker':1}])
    def test_acyclic_root(self):self.assertEqual(analyze(fixture((1,[2]),(2,[])))['terminal_observed_blockers'],[2])
    def test_upstream(self):self.assertEqual(analyze(fixture((1,[2]),(2,[1]),(3,[1])))['blocked_by_cycle'],[3])
    def test_prepared_indirect(self):self.assertEqual(analyze(fixture((1,[2]),(2,[0])))['prepared_transaction_waiters'],[1,2])
    def test_unobserved(self):self.assertEqual(analyze(fixture((1,[9])))['unobserved_blockers'],[9])
    def test_disjoint(self):self.assertEqual(len(analyze(fixture((1,[2]),(2,[1]),(3,[4]),(4,[3])))['cycles']),2)
    def test_duplicates_collapsed(self):self.assertEqual(analyze(fixture((1,[2,2]),(2,[])))['edges'],1)
    def test_parallel_self_is_snapshot_only(self):self.assertTrue(analyze(fixture((1,[1])))['snapshot_cycle_only'])
    def test_duplicate_session(self):
        with self.assertRaises(ValueError):analyze(fixture((1,[]),(1,[])))
    def test_bool_pid(self):
        with self.assertRaises(ValueError):analyze(fixture((True,[])))
    def test_negative_blocker(self):
        with self.assertRaises(ValueError):analyze(fixture((1,[-2])))
    def test_bounded(self):
        with self.assertRaises(ValueError):analyze(fixture(*[(i+1,[]) for i in range(257)]))

if __name__=="__main__":unittest.main()
