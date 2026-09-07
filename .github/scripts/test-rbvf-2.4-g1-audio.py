from pathlib import Path
import math
import re
import sys

root = Path(sys.argv[1])
header = (root / 'app/professional/professionalcore.h').read_text(encoding='utf-8')

# G1-001..G1-013: executable source contract for the audio meter policy.
# This gate intentionally requires edge-case handling not present in the M1 baseline,
# so the first CI execution must be RED before production code is changed.
required = {
    'G1-001': '20.0 * std::log10',
    'G1-007': '-60.0',
    'G1-008': 'std::isfinite',
    'G1-010': 'linear >= 1.0',
    'G1-012': 'peak_hold_ms',
}
for case_id, needle in required.items():
    assert needle in header, f'{case_id} FAIL: missing {needle}'

# Reference values used by G1-001..G1-006.
def expected_dbfs(linear: float) -> float:
    if not math.isfinite(linear) or linear <= 0.0:
        return -60.0
    return max(-60.0, min(0.0, 20.0 * math.log10(linear)))

cases = [
    ('G1-001', 1.0, 0.0, 0.05),
    ('G1-002', 0.5, -6.020599913, 0.10),
    ('G1-003', 0.25, -12.041199826, 0.10),
    ('G1-004', 0.1, -20.0, 0.10),
    ('G1-005', 0.01, -40.0, 0.15),
    ('G1-006', 0.001, -60.0, 0.20),
    ('G1-007', 0.0, -60.0, 0.0),
    ('G1-008', -1.0, -60.0, 0.0),
]
for case_id, linear, expected, tolerance in cases:
    actual = expected_dbfs(linear)
    assert abs(actual - expected) <= tolerance + 1e-12, f'{case_id} reference fixture invalid'

assert expected_dbfs(float('nan')) == -60.0, 'G1-008 reference NaN policy invalid'
assert expected_dbfs(float('inf')) == -60.0, 'G1-008 reference infinity policy invalid'

# Clipping boundary G1-009..G1-011.
def clipping(x: float) -> bool:
    return math.isfinite(x) and x >= 1.0
assert not clipping(0.999), 'G1-009 reference invalid'
assert clipping(1.0), 'G1-010 reference invalid'
assert clipping(1.1), 'G1-011 reference invalid'

# Peak hold policy G1-012..G1-013 must expose a non-negative configured hold.
assert re.search(r'peak_hold_ms_\s*\(', header), 'G1-012 FAIL: peak hold storage missing'
assert 'peak_hold_ms < 0 ? 0 : peak_hold_ms' in header, 'G1-013 FAIL: negative peak hold must clamp to zero'

print('G1-001..G1-013 audio policy contract PASS')
