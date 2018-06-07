ArrayMatch
==========
Compare two array-like objects for equality, returning the ratio of elements that are exactly equal in both arrays. When comparing nested arrays, the inner-most subarrays are compared first so that the returned ratio reflects the number of subarrays that are equal across all elements. For example:

| array_a                           | array_b                           | result |
|-----------------------------------|-----------------------------------|--------|
| [x, x, x]                         | [y, y, y]                         | 0      |
| [x, x, x]                         | [x, y, y]                         | 0.33   |
| [[x, x, x], [x, x, x], [x, x, x]] | [[x, x, x], [x, x, x], [x, x, y]] | 0.66   |

Properties
----------
- **array_a**: Any array-like object or nested sequence.
- **array_b**: Any array-like object or nested sequence.
- **enrich**: Signal Enrichment
  - *exclude_existing*: If checked (true), the attributes of the incoming signal will be excluded from the outgoing signal. If unchecked (false), the attributes of the incoming signal will be included in the outgoing signal.
  - *enrich_field*: (hidden) The attribute on the signal to store the results from this block. If this is empty, the results will be merged onto the incoming signal. This is the default operation. Having this field allows a block to 'save' the results of an operation to a single field on an incoming signal and notify the enriched signal.
- **result_field**: Outgoing signal attribute in which to store the result.

Inputs
------
- **default**: Any list of signals.

Outputs
-------
- **default**: A list of signals of equal length to input.
  - `result_field` (float) The ratio of elements (or subarrays) that are an exact match between `array_a` and `array_b`.

Commands
--------
None

