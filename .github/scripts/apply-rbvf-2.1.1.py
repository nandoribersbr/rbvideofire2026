from pathlib import Path
import sys

root = Path(sys.argv[1])


def read(rel):
    return (root / rel).read_text(encoding="utf-8")


def write(rel, data):
    (root / rel).write_text(data, encoding="utf-8", newline="\n")


def replace(rel, old, new):
    data = read(rel)
    if old not in data:
        raise RuntimeError(f"{rel}: expected text not found: {old[:100]!r}")
    write(rel, data.replace(old, new))


# 2.1.1 version identity
replace("CMakeLists.txt",
        "project(rb-videofire VERSION 2.1.0 LANGUAGES CXX)",
        "project(rb-videofire VERSION 2.1.1 LANGUAGES CXX)")
replace("packaging/rb-videofire/RBVideoFire.nsi",
        '!define VERSION "2.1.0 Alpha Editorial"',
        '!define VERSION "2.1.1 Alpha Editorial"')
replace("packaging/rb-videofire/RBVideoFire.nsi",
        "RB VideoFire Setup 2.1.0 Alpha Editorial.exe",
        "RB VideoFire Setup 2.1.1 Alpha Editorial.exe")

version = read("app/packaging/windows/version.h")
version = version.replace("2,1,0,0", "2,1,1,0")
version = version.replace('"2.1.0.0\\0"', '"2.1.1.0\\0"')
version = version.replace('"2.1.0 Alpha Editorial\\0"', '"2.1.1 Alpha Editorial\\0"')
write("app/packaging/windows/version.h", version)

# Brazilian Portuguese is the explicit RB VideoFire default.
replace("app/config/config.cpp",
        'SetEntryInternal(QStringLiteral("Language"), NodeValue::kText, QString());',
        'SetEntryInternal(QStringLiteral("Language"), NodeValue::kText, QStringLiteral("pt_BR"));')

core = read("app/core.cpp")
old = '''  if (use_locale.isEmpty()) {
    // No configured locale, auto-detect the system's locale
    use_locale = QLocale::system().name();
  }'''
new = '''  if (use_locale.isEmpty()) {
    // RB VideoFire defaults to Brazilian Portuguese, including upgrades from auto/system language.
    use_locale = QStringLiteral("pt_BR");
  }'''
if old not in core:
    raise RuntimeError("Core locale fallback block not found")
write("app/core.cpp", core.replace(old, new))

# Only expose the seven languages supported by RB VideoFire, in deterministic order.
prefs = read("app/dialog/preferences/tabs/preferencesgeneraltab.cpp")
old = '''    // Add default language (en-US)
    QDir language_dir(QStringLiteral(":/ts"));
    QStringList languages = language_dir.entryList();
    foreach (const QString& l, languages) {
      AddLanguage(l);
    }

    QString current_language = OLIVE_CONFIG("Language").toString();
    if (current_language.isEmpty()) {
      // No configured language, use system language
      current_language = QLocale::system().name();

      // If we don't have a language for this, default to en_US
      if (!languages.contains(current_language)) {
        current_language = QStringLiteral("en_US");
      }
    }
    language_combobox_->setCurrentIndex(languages.indexOf(current_language));'''
new = '''    const QStringList languages = {
      QStringLiteral("pt_BR"),
      QStringLiteral("en_US"),
      QStringLiteral("es_ES"),
      QStringLiteral("it_IT"),
      QStringLiteral("fr_FR"),
      QStringLiteral("zh_CN"),
      QStringLiteral("ja_JP")
    };
    for (const QString& language : languages) {
      AddLanguage(language);
    }

    QString current_language = OLIVE_CONFIG("Language").toString();
    if (!languages.contains(current_language)) {
      current_language = QStringLiteral("pt_BR");
    }
    language_combobox_->setCurrentIndex(languages.indexOf(current_language));'''
if old not in prefs:
    raise RuntimeError("Preferences language selector block not found")
prefs = prefs.replace(old, new)

old_accept = '''  QString set_language = language_combobox_->currentData().toString();
  if (QLocale::system().name() == set_language) {
    // Language is set to the system, assume this is effectively "auto"
    set_language = QString();
  }

  // If the language has changed, set it now
  if (OLIVE_CONFIG("Language").toString() != set_language) {
    OLIVE_CONFIG("Language") = set_language;
    Core::instance()->SetLanguage(set_language.isEmpty() ? QLocale::system().name() : set_language);
  }'''
new_accept = '''  const QString set_language = language_combobox_->currentData().toString();

  // Store an explicit locale so the user's selection survives restarts.
  if (OLIVE_CONFIG("Language").toString() != set_language) {
    OLIVE_CONFIG("Language") = set_language;
    Core::instance()->SetLanguage(set_language);
  }'''
if old_accept not in prefs:
    raise RuntimeError("Preferences language persistence block not found")
write("app/dialog/preferences/tabs/preferencesgeneraltab.cpp", prefs.replace(old_accept, new_accept))

# The About/Welcome dialog must visibly show the RB logo and must never silently render blank.
about = read("app/dialog/about/about.cpp")
if "#include <QPixmap>" not in about:
    about = about.replace("#include <QLabel>", "#include <QLabel>\n#include <QPixmap>")
old = '''  QLabel* icon = new QLabel(QStringLiteral("<html><img width='256' height='256' src=':/graphics/rb-videofire.png'></html>"));
  icon->setAlignment(Qt::AlignCenter);
  horiz_layout->addWidget(icon);'''
new = '''  QLabel* icon = new QLabel();
  const QPixmap rb_icon(QStringLiteral(":/graphics/rb-videofire.png"));
  if (!rb_icon.isNull()) {
    icon->setPixmap(rb_icon.scaled(160, 160, Qt::KeepAspectRatio, Qt::SmoothTransformation));
  } else {
    icon->setText(QStringLiteral("RB\\nVideoFire"));
    icon->setStyleSheet(QStringLiteral("font-size: 24px; font-weight: 700;"));
  }
  icon->setFixedSize(180, 180);
  icon->setAlignment(Qt::AlignCenter);
  horiz_layout->addWidget(icon);'''
if old not in about:
    raise RuntimeError("Welcome/About icon block not found")
about = about.replace(old, new)
about = about.replace("RB VideoFire 2.1 Alpha Editorial • RB8 Digital",
                      "RB VideoFire 2.1.1 Alpha Editorial • RB8 Digital")
write("app/dialog/about/about.cpp", about)

# Force the runtime window/taskbar icon from the embedded Qt resource. Windows can otherwise
# display a corrupted/default icon even when the PE resource contains an .ico.
main = read("app/main.cpp")
if "#include <QIcon>" not in main:
    marker = "#include <QGuiApplication>"
    if marker in main:
        main = main.replace(marker, marker + "\n#include <QIcon>")
    else:
        main = "#include <QIcon>\n" + main
app_name = '  QCoreApplication::setApplicationName("RB VideoFire");'
icon_line = '  QApplication::setWindowIcon(QIcon(QStringLiteral(":/graphics/rb-videofire.png")));'
if icon_line not in main:
    if app_name not in main:
        raise RuntimeError("RB VideoFire application name marker not found")
    main = main.replace(app_name, app_name + "\n" + icon_line)
write("app/main.cpp", main)

print("Applied RB VideoFire 2.1.1 language and runtime icon patch")
