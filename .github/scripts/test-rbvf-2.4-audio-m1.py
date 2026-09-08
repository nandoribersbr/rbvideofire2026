from pathlib import Path
import sys

root = Path(sys.argv[1])
header = (root / 'app/widget/audiomonitor/audiomonitor.h').read_text(encoding='utf-8')
impl = (root / 'app/widget/audiomonitor/audiomonitor.cpp').read_text(encoding='utf-8')
viewer = (root / 'app/widget/viewer/viewer.cpp').read_text(encoding='utf-8')

required_header = [
    'QVector<qint64> peak_hold_until_',
    'PushSampleBufferOnAll',
    'StartWaveformOnAll',
]
for needle in required_header:
    assert needle in header, f'M1 audio monitor contract missing in header: {needle}'

required_impl = [
    'kDecibelMinimum = -60',
    'kPeakHoldMs = 1500',
    'peak_hold_until_.resize',
    'peak_hold_until_.fill(0)',
    'QDateTime::currentMSecsSinceEpoch()',
    'std::isfinite(vol)',
    'vol >= 1.0',
    'now < peak_hold_until_.at(i)',
]
for needle in required_impl:
    assert needle in impl, f'M1 audio monitor contract missing in implementation: {needle}'

# The monitor must consume the existing playback/scrub pipeline rather than start a second decoder.
for needle in ('AudioMonitor::PushSampleBufferOnAll(samples)', 'AudioMonitor::StartWaveformOnAll'):
    assert needle in viewer, f'M1 existing-engine integration missing: {needle}'

assert 'new AudioManager' not in impl, 'M1 must not create a second audio output/decoder pipeline'
assert 'AudioManager::instance()->PushToOutput' not in impl, 'M1 meter must observe existing audio, not own playback output'

print('M1 real Audio Monitor source/integration contract PASS')
