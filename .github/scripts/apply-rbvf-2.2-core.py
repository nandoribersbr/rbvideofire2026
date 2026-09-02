from pathlib import Path
import sys

root = Path(sys.argv[1])

def read(rel):
    return (root / rel).read_text(encoding='utf-8')

def write(rel, data):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data, encoding='utf-8', newline='\n')

def replace(rel, old, new):
    data = read(rel)
    if old not in data:
        raise RuntimeError(f'{rel}: expected text not found: {old[:120]!r}')
    write(rel, data.replace(old, new))

# -----------------------------------------------------------------------------
# Professional editorial policy module. These types formalize behavior that was
# previously distributed across UI code so it can be regression-tested.
# -----------------------------------------------------------------------------
write('app/professional/professionalcore.h', r'''#ifndef RB_PROFESSIONALCORE_H
#define RB_PROFESSIONALCORE_H

#include <QString>

namespace olive {
namespace rb {

class TrimState
{
public:
  enum Side { kA, kB, kBoth };
  enum Mode { kRipple, kRoll };

  TrimState() : side_(kBoth), mode_(kRoll), frame_delta_(0) {}

  Side side() const { return side_; }
  Mode mode() const { return mode_; }
  int frame_delta() const { return frame_delta_; }

  void set_side(Side side) { side_ = side; }
  void set_mode(Mode mode) { mode_ = mode; }
  void nudge(int frames) { frame_delta_ += frames; }
  void reset_delta() { frame_delta_ = 0; }

  bool affects_a() const { return side_ == kA || side_ == kBoth; }
  bool affects_b() const { return side_ == kB || side_ == kBoth; }

private:
  Side side_;
  Mode mode_;
  int frame_delta_;
};

class PlaybackQuality
{
public:
  enum Level { kFull, kHalf, kQuarter, kEighth };

  static int Divider(Level level)
  {
    switch (level) {
    case kFull: return 1;
    case kHalf: return 2;
    case kQuarter: return 4;
    case kEighth: return 8;
    }
    return 1;
  }

  static QString Name(Level level)
  {
    switch (level) {
    case kFull: return QStringLiteral("Full");
    case kHalf: return QStringLiteral("1/2");
    case kQuarter: return QStringLiteral("1/4");
    case kEighth: return QStringLiteral("1/8");
    }
    return QStringLiteral("Full");
  }
};

class MediaProxyState
{
public:
  MediaProxyState() : enabled_(false) {}
  explicit MediaProxyState(const QString& original) : original_(original), enabled_(false) {}

  void set_original(const QString& path) { original_ = path; }
  void set_proxy(const QString& path) { proxy_ = path; }
  void set_enabled(bool enabled) { enabled_ = enabled; }

  const QString& original() const { return original_; }
  const QString& proxy() const { return proxy_; }
  bool enabled() const { return enabled_; }
  bool has_proxy() const { return !proxy_.isEmpty(); }
  QString active_path() const { return enabled_ && has_proxy() ? proxy_ : original_; }

private:
  QString original_;
  QString proxy_;
  bool enabled_;
};

class RecoveryPolicy
{
public:
  static constexpr int kDefaultIntervalMinutes = 1;
  static constexpr int kDefaultMaximumSnapshots = 50;

  static int ClampIntervalMinutes(int value)
  {
    return value < 1 ? 1 : value;
  }

  static int ClampMaximumSnapshots(int value)
  {
    if (value < 5) return 5;
    if (value > 200) return 200;
    return value;
  }
};

} // namespace rb
} // namespace olive

#endif // RB_PROFESSIONALCORE_H
''')

write('app/professional/CMakeLists.txt', '''set(OLIVE_SOURCES\n  ${OLIVE_SOURCES}\n  professional/professionalcore.h\n  PARENT_SCOPE\n)\n''')

app_cmake = read('app/CMakeLists.txt')
if 'add_subdirectory(professional)' not in app_cmake:
    app_cmake = app_cmake.replace('add_subdirectory(panel)\n', 'add_subdirectory(panel)\nadd_subdirectory(professional)\n')
write('app/CMakeLists.txt', app_cmake)

# -----------------------------------------------------------------------------
# Tests: professional trim state, playback quality, proxy switching and recovery
# policy. These are deliberately small contracts around production behavior.
# -----------------------------------------------------------------------------
write('tests/general/rb-professional-core-tests.cpp', r'''#include "professional/professionalcore.h"
#include "testutil.h"

namespace olive {

OLIVE_ADD_TEST(RBProfessionalTrimState)
{
  rb::TrimState state;
  OLIVE_ASSERT(state.side() == rb::TrimState::kBoth);
  OLIVE_ASSERT(state.affects_a());
  OLIVE_ASSERT(state.affects_b());
  OLIVE_ASSERT(state.mode() == rb::TrimState::kRoll);

  state.set_side(rb::TrimState::kA);
  state.set_mode(rb::TrimState::kRipple);
  state.nudge(-3);
  OLIVE_ASSERT(state.affects_a());
  OLIVE_ASSERT(!state.affects_b());
  OLIVE_ASSERT(state.frame_delta() == -3);
  state.reset_delta();
  OLIVE_ASSERT(state.frame_delta() == 0);

  OLIVE_TEST_END;
}

OLIVE_ADD_TEST(RBPlaybackQuality)
{
  OLIVE_ASSERT(rb::PlaybackQuality::Divider(rb::PlaybackQuality::kFull) == 1);
  OLIVE_ASSERT(rb::PlaybackQuality::Divider(rb::PlaybackQuality::kHalf) == 2);
  OLIVE_ASSERT(rb::PlaybackQuality::Divider(rb::PlaybackQuality::kQuarter) == 4);
  OLIVE_ASSERT(rb::PlaybackQuality::Divider(rb::PlaybackQuality::kEighth) == 8);
  OLIVE_ASSERT(rb::PlaybackQuality::Name(rb::PlaybackQuality::kEighth) == QStringLiteral("1/8"));
  OLIVE_TEST_END;
}

OLIVE_ADD_TEST(RBMediaProxyState)
{
  rb::MediaProxyState media(QStringLiteral("camera-original.mov"));
  OLIVE_ASSERT(media.active_path() == QStringLiteral("camera-original.mov"));
  media.set_proxy(QStringLiteral("proxy.mov"));
  OLIVE_ASSERT(media.active_path() == QStringLiteral("camera-original.mov"));
  media.set_enabled(true);
  OLIVE_ASSERT(media.active_path() == QStringLiteral("proxy.mov"));
  media.set_enabled(false);
  OLIVE_ASSERT(media.active_path() == QStringLiteral("camera-original.mov"));
  OLIVE_TEST_END;
}

OLIVE_ADD_TEST(RBRecoveryPolicy)
{
  OLIVE_ASSERT(rb::RecoveryPolicy::kDefaultIntervalMinutes == 1);
  OLIVE_ASSERT(rb::RecoveryPolicy::kDefaultMaximumSnapshots == 50);
  OLIVE_ASSERT(rb::RecoveryPolicy::ClampIntervalMinutes(0) == 1);
  OLIVE_ASSERT(rb::RecoveryPolicy::ClampMaximumSnapshots(2) == 5);
  OLIVE_ASSERT(rb::RecoveryPolicy::ClampMaximumSnapshots(1000) == 200);
  OLIVE_TEST_END;
}

}
''')

general_cmake = read('tests/general/CMakeLists.txt')
line = 'olive_add_test(General rb-professional-core-tests rb-professional-core-tests.cpp)\n'
if line not in general_cmake:
    general_cmake += '\n' + line
write('tests/general/CMakeLists.txt', general_cmake)

# -----------------------------------------------------------------------------
# Recovery defaults and user-facing recovery language.
# -----------------------------------------------------------------------------
config = read('app/config/config.cpp')
config = config.replace('SetEntryInternal(QStringLiteral("AutorecoveryMaximum"), NodeValue::kInt, 20);',
                        'SetEntryInternal(QStringLiteral("AutorecoveryMaximum"), NodeValue::kInt, rb::RecoveryPolicy::kDefaultMaximumSnapshots);')
if '#include "professional/professionalcore.h"' not in config:
    config = config.replace('#include "config.h"', '#include "config.h"\n#include "professional/professionalcore.h"')
write('app/config/config.cpp', config)

core = read('app/core.cpp')
core = core.replace('The following projects had unsaved changes when Olive forcefully quit. Would you like to load them?',
                    'RB VideoFire found recoverable project snapshots from the previous session. Would you like to load them?')
core = core.replace('Olive may not have permission to this directory.',
                    'RB VideoFire may not have permission to this directory.')
write('app/core.cpp', core)

# -----------------------------------------------------------------------------
# Professional timeline/cache surface: expose cache actions and use editorial
# terminology familiar to Avid/Resolve users while retaining the same commands.
# -----------------------------------------------------------------------------
menu = read('app/window/mainwindow/mainmenu.cpp')
menu = menu.replace('  // TEMP: Hide sequence cache items for now. Want to see if clip caching will supersede it.\n  sequence_cache_item_->setVisible(false);\n  sequence_cache_in_to_out_item_->setVisible(false);\n', '')
menu = menu.replace('sequence_cache_item_->setText(tr("Cache Entire Sequence"));',
                    'sequence_cache_item_->setText(tr("Render Cache Entire Sequence"));')
menu = menu.replace('sequence_cache_in_to_out_item_->setText(tr("Cache Sequence In/Out"));',
                    'sequence_cache_in_to_out_item_->setText(tr("Render Cache In/Out"));')
menu = menu.replace('sequence_disk_cache_clear_item_->setText(tr("Clear Disk Cache"));',
                    'sequence_disk_cache_clear_item_->setText(tr("Clear Render Cache"));')
menu = menu.replace('tools_ripple_item_->setText(tr("Ripple Tool"));',
                    'tools_ripple_item_->setText(tr("Ripple Trim Tool"));')
menu = menu.replace('tools_rolling_item_->setText(tr("Rolling Tool"));',
                    'tools_rolling_item_->setText(tr("Roll Trim Tool"));')
menu = menu.replace('tools_slip_item_->setText(tr("Slip Tool"));',
                    'tools_slip_item_->setText(tr("Slip Edit Tool"));')
menu = menu.replace('tools_slide_item_->setText(tr("Slide Tool"));',
                    'tools_slide_item_->setText(tr("Slide Edit Tool"));')
write('app/window/mainwindow/mainmenu.cpp', menu)

# Professional playback menu: keep the editor-facing choices predictable.
viewer = read('app/widget/viewer/viewer.cpp')
old = '''      for (int d : VideoParams::kSupportedDividers) {
        playback_res_menu->AddActionWithData(VideoParams::GetNameForDivider(d), d, GetConnectedNode()->GetVideoParams().divider());
      }'''
new = '''      const QVector<int> professional_dividers = {1, 2, 4, 8};
      for (int d : professional_dividers) {
        playback_res_menu->AddActionWithData(VideoParams::GetNameForDivider(d), d, GetConnectedNode()->GetVideoParams().divider());
      }'''
if old not in viewer:
    raise RuntimeError('viewer playback resolution block not found')
write('app/widget/viewer/viewer.cpp', viewer.replace(old, new))

# Proxy/cache terminology in project explorer. Existing PreCacheTask already runs
# in TaskManager background infrastructure; 2.2 exposes it as an editorial proxy
# cache operation without changing original media paths.
explorer = read('app/widget/projectexplorer/projectexplorer.cpp')
explorer = explorer.replace('Menu* proxy_menu = new Menu(tr("Pre-Cache"), &menu);',
                            'Menu* proxy_menu = new Menu(tr("Create Proxy Cache"), &menu);')
explorer = explorer.replace('tr("For \\"%1\\"").arg(i->GetLabel())',
                            'tr("Proxy Cache for \\"%1\\"").arg(i->GetLabel())')
write('app/widget/projectexplorer/projectexplorer.cpp', explorer)

precache = read('app/task/precache/precachetask.cpp')
precache = precache.replace('SetTitle(tr("Pre-caching %1:%2")',
                            'SetTitle(tr("Creating proxy cache %1:%2")')
write('app/task/precache/precachetask.cpp', precache)

print('Applied RB VideoFire 2.2 professional editorial core services')