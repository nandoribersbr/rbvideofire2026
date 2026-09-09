from pathlib import Path
import sys

root = Path(sys.argv[1])

# --- Multicam: preserve existing real switch/undo path and extend direct angle shortcuts to 25.
multicam_path = root / 'app/widget/multicam/multicamwidget.cpp'
multicam = multicam_path.read_text(encoding='utf-8')
old_multicam = '''  for (int i=0; i<9; i++) {\n    new QShortcut(QStringLiteral("Ctrl+%1").arg(QString::number(i+1)), this, this, [this, i]{Switch(i, false);});\n    new QShortcut(QString::number(i+1), this, this, [this, i]{Switch(i, true);});\n  }\n'''
new_multicam = '''  // RB_M3_MULTICAM_25: keep the existing first nine shortcuts and add real editorial\n  // switching for angles 10-25. Switch() already splits at the playhead, preserves linked\n  // clips and pushes the change through the native undo stack.\n  for (int i=0; i<9; i++) {\n    new QShortcut(QStringLiteral("Ctrl+%1").arg(QString::number(i+1)), this, this, [this, i]{Switch(i, false);});\n    new QShortcut(QString::number(i+1), this, this, [this, i]{Switch(i, true);});\n  }\n\n  const QStringList rb_m3_extra_multicam_shortcuts = {\n    QStringLiteral("Ctrl+Shift+1"), QStringLiteral("Ctrl+Shift+2"), QStringLiteral("Ctrl+Shift+3"),\n    QStringLiteral("Ctrl+Shift+4"), QStringLiteral("Ctrl+Shift+5"), QStringLiteral("Ctrl+Shift+6"),\n    QStringLiteral("Ctrl+Shift+7"), QStringLiteral("Ctrl+Shift+8"), QStringLiteral("Ctrl+Shift+9"),\n    QStringLiteral("Alt+1"), QStringLiteral("Alt+2"), QStringLiteral("Alt+3"), QStringLiteral("Alt+4"),\n    QStringLiteral("Alt+5"), QStringLiteral("Alt+6"), QStringLiteral("Alt+7")\n  };\n  for (int i=0; i<rb_m3_extra_multicam_shortcuts.size(); ++i) {\n    const int source = i + 9;\n    new QShortcut(rb_m3_extra_multicam_shortcuts.at(i), this, this, [this, source]{Switch(source, true);});\n  }\n'''
if old_multicam not in multicam:
    raise SystemExit('M3 multicam baseline not found; refusing unsafe patch')
multicam = multicam.replace(old_multicam, new_multicam, 1)
multicam_path.write_text(multicam, encoding='utf-8')

# --- Inspector presets: reuse NodeParamView's native copy/paste serializer and undo-aware paste.
param_h_path = root / 'app/panel/param/param.h'
param_h = param_h_path.read_text(encoding='utf-8')
old_h = '''  void SetContexts(const QVector<Node*> &contexts);\n\nsignals:\n'''
new_h = '''  void SetContexts(const QVector<Node*> &contexts);\n\n  void SaveInspectorPreset();\n\n  void ApplyInspectorPreset();\n\nsignals:\n'''
if old_h not in param_h:
    raise SystemExit('ParamPanel slot insertion point not found')
param_h = param_h.replace(old_h, new_h, 1)
param_h_path.write_text(param_h, encoding='utf-8')

param_cpp_path = root / 'app/panel/param/param.cpp'
param_cpp = param_cpp_path.read_text(encoding='utf-8')
old_include = '''#include "param.h"\n\n#include "window/mainwindow/mainwindow.h"\n'''
new_include = '''#include "param.h"\n\n#include <QApplication>\n#include <QClipboard>\n#include <QInputDialog>\n#include <QKeySequence>\n#include <QMessageBox>\n#include <QMimeData>\n#include <QSettings>\n#include <QShortcut>\n\n#include "window/mainwindow/mainwindow.h"\n'''
if old_include not in param_cpp:
    raise SystemExit('ParamPanel include block not found')
param_cpp = param_cpp.replace(old_include, new_include, 1)

old_ctor = '''  SetTimeBasedWidget(view);\n\n  Retranslate();\n}\n'''
new_ctor = '''  SetTimeBasedWidget(view);\n\n  auto *save_preset_shortcut = new QShortcut(QKeySequence(QStringLiteral("Ctrl+Shift+Alt+S")), this);\n  connect(save_preset_shortcut, &QShortcut::activated, this, &ParamPanel::SaveInspectorPreset);\n  auto *apply_preset_shortcut = new QShortcut(QKeySequence(QStringLiteral("Ctrl+Shift+Alt+P")), this);\n  connect(apply_preset_shortcut, &QShortcut::activated, this, &ParamPanel::ApplyInspectorPreset);\n  setToolTip(tr("Inspector presets: Ctrl+Shift+Alt+S to save, Ctrl+Shift+Alt+P to apply"));\n\n  Retranslate();\n}\n'''
if old_ctor not in param_cpp:
    raise SystemExit('ParamPanel constructor insertion point not found')
param_cpp = param_cpp.replace(old_ctor, new_ctor, 1)

old_retranslate = '''void ParamPanel::Retranslate()\n{\n  SetTitle(tr("Parameter Editor"));\n}\n'''
new_functions = r'''void ParamPanel::SaveInspectorPreset()
{
  if (!GetParamView()->CopySelected(false)) {
    QMessageBox::information(this, tr("Inspector Preset"), tr("Select one or more Inspector nodes before saving a preset."));
    return;
  }

  bool ok = false;
  QString name = QInputDialog::getText(this, tr("Save Inspector Preset"), tr("Preset name:"), QLineEdit::Normal, QString(), &ok).trimmed();
  if (!ok || name.isEmpty()) {
    return;
  }
  name.replace('/', '_');
  name.replace('\\', '_');

  const QMimeData *mime = QApplication::clipboard()->mimeData();
  const QStringList formats = mime->formats();
  if (formats.isEmpty()) {
    QMessageBox::warning(this, tr("Inspector Preset"), tr("The selected Inspector data could not be serialized."));
    return;
  }

  QSettings settings;
  settings.beginGroup(QStringLiteral("RBVideoFire/InspectorPresets"));
  settings.beginGroup(name);
  settings.remove(QString());
  settings.setValue(QStringLiteral("count"), formats.size());
  for (int i = 0; i < formats.size(); ++i) {
    settings.setValue(QStringLiteral("format_%1").arg(i), formats.at(i));
    settings.setValue(QStringLiteral("data_%1").arg(i), mime->data(formats.at(i)));
  }
  settings.endGroup();
  settings.endGroup();
  settings.sync();
}

void ParamPanel::ApplyInspectorPreset()
{
  QSettings settings;
  settings.beginGroup(QStringLiteral("RBVideoFire/InspectorPresets"));
  const QStringList names = settings.childGroups();
  if (names.isEmpty()) {
    settings.endGroup();
    QMessageBox::information(this, tr("Inspector Preset"), tr("No Inspector presets have been saved yet."));
    return;
  }

  bool ok = false;
  const QString name = QInputDialog::getItem(this, tr("Apply Inspector Preset"), tr("Preset:"), names, 0, false, &ok);
  if (!ok || name.isEmpty()) {
    settings.endGroup();
    return;
  }

  settings.beginGroup(name);
  const int count = settings.value(QStringLiteral("count"), 0).toInt();
  auto *mime = new QMimeData();
  for (int i = 0; i < count; ++i) {
    const QString format = settings.value(QStringLiteral("format_%1").arg(i)).toString();
    const QByteArray data = settings.value(QStringLiteral("data_%1").arg(i)).toByteArray();
    if (!format.isEmpty() && !data.isEmpty()) {
      mime->setData(format, data);
    }
  }
  settings.endGroup();
  settings.endGroup();

  QApplication::clipboard()->setMimeData(mime);
  if (!GetParamView()->Paste()) {
    QMessageBox::warning(this, tr("Inspector Preset"), tr("This preset is not compatible with the current Inspector context."));
  }
}

void ParamPanel::Retranslate()
{
  SetTitle(tr("Inspector"));
}
'''
if old_retranslate not in param_cpp:
    raise SystemExit('ParamPanel Retranslate baseline not found')
param_cpp = param_cpp.replace(old_retranslate, new_functions, 1)
param_cpp_path.write_text(param_cpp, encoding='utf-8')

print('Applied RB VideoFire M3 editorial precision: 25-angle multicam + persistent Inspector presets')
