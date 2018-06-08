import numpy as np
from nio.block.base import Block, Signal
from nio.block.mixins.enrich.enrich_signals import EnrichSignals
from nio.properties import Property, PropertyHolder, VersionProperty


class ArrayMatch(EnrichSignals, Block):

    array_a = Property(title='Array A', default='{{ $labels }}')
    array_b = Property(title='Array B', default='{{ $prediction }}')
    result_field = Property(title='Comparison Result Field', default='match')
    version = VersionProperty('0.1.0')

    def process_signals(self, signals):
        outgoing_signals = []
        for signal in signals:
            lst = []
            # cast to array to accept array-like objects for input
            A = np.array(self.array_a(signal))
            B = np.array(self.array_b(signal))
            diff = A - B
            if len(diff.shape) > 1:
                # matching subarrays sum to 0
                sub_diff = np.sum(np.abs(diff), axis=-1)
                C = np.mean(sub_diff == 0)
            else:
                # percent of elements that are equal
                C = np.mean(diff == 0)
            new_dict = {self.result_field(signal): C}
            new_signal = self.get_output_signal(new_dict, signal)
            outgoing_signals.append(new_signal)
        self.notify_signals(outgoing_signals)
