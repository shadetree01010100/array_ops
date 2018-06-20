from nio.block.terminals import DEFAULT_TERMINAL
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from ..array_match_block import ArrayMatch


class TestMatrixCompare(NIOBlockTestCase):

    def test_array_comparison(self):
        """Flat arrays are compared for equality"""
        blk = ArrayMatch()
        self.configure_block(blk, {})
        blk.start()
        test_signal = {
            'prediction': [0, 0, 0, 0],
            'labels': [0, 1, 2, 3],
        }
        blk.process_signals([Signal(test_signal)])
        blk.stop()
        self.assert_num_signals_notified(1)
        last_signal = self.last_notified[DEFAULT_TERMINAL][0].to_dict()
        # convert result array to list to do dict comparison
        last_signal['match'] = last_signal['match'].tolist()
        # one of four elements is equal
        target_signal = {'match': 1 /4}
        self.assertDictEqual(last_signal, target_signal)

    def test_nested_array_comparison(self):
        """Nested arrays with shape (4, 2) are compared for equality 
        of subarrays"""
        blk = ArrayMatch()
        self.configure_block(blk, {
            'array_a': '{{ $foo }}',
            'array_b': '{{ $bar }}',
            'result_field': 'baz',
            'enrich': {'exclude_existing': False},
        })
        blk.start()
        test_signal = {
            'foo': [
                [0, 0],
                [0, 0],
                [0, 0],
                [0, 0],
                [0, 0],
            ],
            'bar': [
                [-1, 1],
                [3.14, 0],
                [0, 0],
                [0, 0],
                [0, 0],
            ],
        }
        blk.process_signals([Signal(test_signal)])
        blk.stop()
        self.assert_num_signals_notified(1)
        last_signal = self.last_notified[DEFAULT_TERMINAL][0].to_dict()
        # convert result array to list to do dict comparison
        last_signal['baz'] = last_signal['baz'].tolist()
        target_signal = test_signal
        # three of five subarrays are equal across all elements
        target_signal['baz'] = 3 / 5
        self.assertDictEqual(last_signal, target_signal)

    def test_higher_dimensions(self):
        """Nested arrays with shape (1, 4, 4, 3) such as a 3 channel image, 
        inner-most sub-array is to be compared"""
        blk = ArrayMatch()
        self.configure_block(blk, {
            'array_a': '{{ $foo }}',
            'array_b': '{{ $bar }}',
        })
        blk.start()
        test_signal = {
            'foo': [
                [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                ],
                [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                ],
                [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                ],
                [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                ],
            ],
            'bar': [
                [
                    [1, -1, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                ],
                [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                ],
                [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                ],
                [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                ],
            ],
        }
        blk.process_signals([Signal(test_signal)])
        blk.stop()
        self.assert_num_signals_notified(1)
        last_signal = self.last_notified[DEFAULT_TERMINAL][0].to_dict()
        # convert result array to list for assertDictEqual
        last_signal['match'] = last_signal['match'].tolist()
        # one of 4*4=16 pixels does not match all 3 values
        target_signal = {'match': 15 /16}
        self.assertDictEqual(last_signal, target_signal)
