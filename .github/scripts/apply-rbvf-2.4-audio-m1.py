from pathlib import Path
import sys

root = Path(sys.argv[1])

def read(rel):
    return (root / rel).read_text(encoding='utf-8')

def write(rel, data):
    (root / rel).write_text(data, encoding='utf-8', newline='\n')

def replace(rel, old, new):
    data = read(rel)
    if old not in data:
        raise RuntimeError(f'{rel}: expected text not found: {old}')
    write(rel, data.replace(old, new, 1))

header_rel = 'app/widget/audiomonitor/audiomonitor.h'
impl_rel = 'app/widget/audiomonitor/audiomonitor.cpp'

replace(header_rel,
        '  QVector<bool> peaked_;',
        '  // RB VideoFire: absolute expiry time for per-channel clipping peak hold.\n  QVector<qint64> peak_hold_until_;')

impl = read(impl_rel)
if '#include <cmath>' not in impl:
    impl = impl.replace('#include <QApplication>\n', '#include <QApplication>\n#include <cmath>\n', 1)
impl = impl.replace('const int kDecibelMinimum = -198; // Must be divisible by kDecibelStep for infinity to appear',
                    'const int kDecibelMinimum = -60; // Professional editorial meter floor in dBFS')
impl = impl.replace('const int kMaximumSmoothness = 8;',
                    'const int kMaximumSmoothness = 8;\nconst qint64 kPeakHoldMs = 1500;')
impl = impl.replace('    peaked_.resize(params_.channel_count());\n    peaked_.fill(false);',
                    '    peak_hold_until_.resize(params_.channel_count());\n    peak_hold_until_.fill(0);')
impl = impl.replace('    // Validate value and whether it peaked\n    double vol = vals.at(i);\n    if (vol > 1.0) {\n      peaked_[i] = true;\n    }',
                    '    // RB VideoFire professional clipping state: hold a real peak for 1.5 seconds.\n    double vol = vals.at(i);\n    const qint64 now = QDateTime::currentMSecsSinceEpoch();\n    if (std::isfinite(vol) && vol >= 1.0) {\n      peak_hold_until_[i] = now + kPeakHoldMs;\n    }')
impl = impl.replace('    if (!peaked_.at(i)) {\n      p.drawRect(peaks_rect);\n    }',
                    '    if (!(now < peak_hold_until_.at(i))) {\n      p.drawRect(peaks_rect);\n    }')
impl = impl.replace('  peaked_.fill(false);', '  peak_hold_until_.fill(0);')
write(impl_rel, impl)

print('Applied RB VideoFire 2.4 M1 professional Audio Monitor: -60 dBFS scale, existing-engine feed, 1500 ms clipping peak hold')
