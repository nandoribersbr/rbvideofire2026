from pathlib import Path
import sys

root = Path(sys.argv[1])

# ---------------- Footage media state, metadata and real proxy playback path ----------------
h_path = root / 'app/node/project/footage/footage.h'
h = h_path.read_text(encoding='utf-8')

old = '''class Footage : public ViewerOutput\n{\n  Q_OBJECT\npublic:\n'''
new = '''class Footage : public ViewerOutput\n{\n  Q_OBJECT\npublic:\n  enum class RBMediaState {\n    kOriginal = 0,\n    kProxy = 1,\n    kOffline = 2\n  };\n\n'''
if old not in h:
    raise SystemExit('Footage class header anchor not found')
h = h.replace(old, new, 1)

old = '''  void set_filename(const QString& s);\n\n  /**\n   * @brief Retrieve the last modified time/date\n'''
new = '''  void set_filename(const QString& s);\n\n  void SetOriginalPath(const QString& s) { set_filename(s); }\n  QString original_path() const { return filename(); }\n\n  void SetProxyPath(const QString& s);\n  QString proxy_path() const { return GetStandardValue(kProxyPathInput).toString(); }\n\n  void SetMediaState(RBMediaState state) { SetStandardValue(kMediaStateInput, static_cast<int>(state)); }\n  RBMediaState media_state() const { return static_cast<RBMediaState>(GetStandardValue(kMediaStateInput).toInt()); }\n  QString ResolvePlaybackPath() const;\n  QString MediaStateLabel() const;\n\n  QString reel() const { return GetStandardValue(kReelInput).toString(); }\n  QString scene() const { return GetStandardValue(kSceneInput).toString(); }\n  QString take() const { return GetStandardValue(kTakeInput).toString(); }\n  QString camera() const { return GetStandardValue(kCameraInput).toString(); }\n  QString notes() const { return GetStandardValue(kNotesInput).toString(); }\n  QString label_color() const { return GetStandardValue(kLabelColorInput).toString(); }\n  bool favorite() const { return GetStandardValue(kFavoriteInput).toBool(); }\n\n  static const QString kProxyPathInput;\n  static const QString kMediaStateInput;\n  static const QString kReelInput;\n  static const QString kSceneInput;\n  static const QString kTakeInput;\n  static const QString kCameraInput;\n  static const QString kNotesInput;\n  static const QString kLabelColorInput;\n  static const QString kFavoriteInput;\n\n  /**\n   * @brief Retrieve the last modified time/date\n'''
if old not in h:
    raise SystemExit('Footage set_filename anchor not found')
h = h.replace(old, new, 1)

old = '''  void Reprobe();\n\n  VideoParams MergeVideoStream'''
new = '''  void Reprobe();\n\n  void ProbeProxy();\n\n  VideoParams MergeVideoStream'''
if old not in h:
    raise SystemExit('Footage Reprobe anchor not found')
h = h.replace(old, new, 1)

old = '''  QString decoder_;\n\n  bool valid_;\n'''
new = '''  QString decoder_;\n\n  QString proxy_decoder_;\n\n  bool valid_;\n'''
if old not in h:
    raise SystemExit('Footage decoder member anchor not found')
h = h.replace(old, new, 1)
h_path.write_text(h, encoding='utf-8')

cpp_path = root / 'app/node/project/footage/footage.cpp'
cpp = cpp_path.read_text(encoding='utf-8')

old = '''const QString Footage::kFilenameInput = QStringLiteral("file_in");\n'''
new = '''const QString Footage::kFilenameInput = QStringLiteral("file_in");\nconst QString Footage::kProxyPathInput = QStringLiteral("rb_proxy_path");\nconst QString Footage::kMediaStateInput = QStringLiteral("rb_media_state");\nconst QString Footage::kReelInput = QStringLiteral("rb_reel");\nconst QString Footage::kSceneInput = QStringLiteral("rb_scene");\nconst QString Footage::kTakeInput = QStringLiteral("rb_take");\nconst QString Footage::kCameraInput = QStringLiteral("rb_camera");\nconst QString Footage::kNotesInput = QStringLiteral("rb_notes");\nconst QString Footage::kLabelColorInput = QStringLiteral("rb_label_color");\nconst QString Footage::kFavoriteInput = QStringLiteral("rb_favorite");\n'''
if old not in cpp:
    raise SystemExit('Footage constant anchor not found')
cpp = cpp.replace(old, new, 1)

old = '''  PrependInput(kFilenameInput, NodeValue::kFile, InputFlags(kInputFlagNotConnectable | kInputFlagNotKeyframable));\n\n  Clear();\n'''
new = '''  PrependInput(kFilenameInput, NodeValue::kFile, InputFlags(kInputFlagNotConnectable | kInputFlagNotKeyframable));\n\n  const InputFlags rb_media_flags = InputFlags(kInputFlagNotConnectable | kInputFlagNotKeyframable | kInputFlagHidden);\n  AddInput(kProxyPathInput, NodeValue::kFile, rb_media_flags);\n  AddInput(kMediaStateInput, NodeValue::kInt, rb_media_flags);\n  AddInput(kReelInput, NodeValue::kText, rb_media_flags);\n  AddInput(kSceneInput, NodeValue::kText, rb_media_flags);\n  AddInput(kTakeInput, NodeValue::kText, rb_media_flags);\n  AddInput(kCameraInput, NodeValue::kText, rb_media_flags);\n  AddInput(kNotesInput, NodeValue::kText, rb_media_flags);\n  AddInput(kLabelColorInput, NodeValue::kText, rb_media_flags);\n  AddInput(kFavoriteInput, NodeValue::kBoolean, rb_media_flags);\n  SetStandardValue(kMediaStateInput, static_cast<int>(RBMediaState::kOriginal));\n  SetStandardValue(kFavoriteInput, false);\n\n  Clear();\n'''
if old not in cpp:
    raise SystemExit('Footage constructor input anchor not found')
cpp = cpp.replace(old, new, 1)

old = '''  SetInputName(kFilenameInput, tr("Filename"));\n}\n'''
new = '''  SetInputName(kFilenameInput, tr("Filename"));\n  SetInputName(kProxyPathInput, tr("Proxy Media"));\n  SetInputName(kMediaStateInput, tr("Media State"));\n  SetInputName(kReelInput, tr("Reel"));\n  SetInputName(kSceneInput, tr("Scene"));\n  SetInputName(kTakeInput, tr("Take"));\n  SetInputName(kCameraInput, tr("Camera"));\n  SetInputName(kNotesInput, tr("Notes"));\n  SetInputName(kLabelColorInput, tr("Label"));\n  SetInputName(kFavoriteInput, tr("Favorite"));\n}\n'''
if old not in cpp:
    raise SystemExit('Footage Retranslate anchor not found')
cpp = cpp.replace(old, new, 1)

old = '''  if (input == kFilenameInput) {\n    // Reset internal stream cache\n    Clear();\n\n    Reprobe();\n  } else {\n    super::InputValueChangedEvent(input, element);\n  }\n'''
new = '''  if (input == kFilenameInput) {\n    // Reset internal stream cache\n    Clear();\n\n    Reprobe();\n  } else if (input == kProxyPathInput) {\n    ProbeProxy();\n  } else if (input == kMediaStateInput\n             || input == kReelInput || input == kSceneInput || input == kTakeInput\n             || input == kCameraInput || input == kNotesInput || input == kLabelColorInput\n             || input == kFavoriteInput) {\n    // Persistent RB media metadata does not invalidate decoded frames by itself.\n  } else {\n    super::InputValueChangedEvent(input, element);\n  }\n'''
if old not in cpp:
    raise SystemExit('Footage InputValueChangedEvent anchor not found')
cpp = cpp.replace(old, new, 1)

old = '''void Footage::set_filename(const QString &s)\n{\n  SetStandardValue(kFilenameInput, s);\n}\n'''
new = '''void Footage::set_filename(const QString &s)\n{\n  SetStandardValue(kFilenameInput, s);\n}\n\nvoid Footage::SetProxyPath(const QString &s)\n{\n  SetStandardValue(kProxyPathInput, s);\n  ProbeProxy();\n}\n\nQString Footage::ResolvePlaybackPath() const\n{\n  const QString original = filename();\n  const QString proxy = proxy_path();\n  const RBMediaState requested = media_state();\n\n  if (requested == RBMediaState::kProxy && !proxy.isEmpty()\n      && QFileInfo::exists(proxy) && !proxy_decoder_.isEmpty()) {\n    return proxy;\n  }\n\n  if (requested != RBMediaState::kOffline && !original.isEmpty() && QFileInfo::exists(original)) {\n    return original;\n  }\n\n  return QString();\n}\n\nQString Footage::MediaStateLabel() const\n{\n  const QString resolved = ResolvePlaybackPath();\n  if (resolved.isEmpty()) {\n    return tr("Offline");\n  }\n  if (!proxy_path().isEmpty() && resolved == proxy_path()) {\n    return tr("Proxy");\n  }\n  return tr("Original");\n}\n'''
if old not in cpp:
    raise SystemExit('Footage set_filename implementation anchor not found')
cpp = cpp.replace(old, new, 1)

old = '''  // Pop filename from table\n  QString file = value[kFilenameInput].toString();\n\n  // If the file exists and the reference is valid, push a footage job to the renderer\n  if (QFileInfo::exists(file)) {\n'''
new = '''  // Resolve the same Footage item to Original or Proxy. No second media pipeline is created.\n  QString file = ResolvePlaybackPath();\n  const QString decoder_to_use = (!proxy_path().isEmpty() && file == proxy_path() && !proxy_decoder_.isEmpty())\n      ? proxy_decoder_ : decoder_;\n\n  // If the resolved file exists and the reference is valid, push a footage job to the renderer\n  if (!file.isEmpty() && QFileInfo::exists(file)) {\n'''
if old not in cpp:
    raise SystemExit('Footage Value file anchor not found')
cpp = cpp.replace(old, new, 1)

old = '''      FootageJob job(globals.time(), decoder_, filename(), ref.type(), GetLength(), globals.loop_mode());\n'''
new = '''      FootageJob job(globals.time(), decoder_to_use, file, ref.type(), GetLength(), globals.loop_mode());\n'''
if old not in cpp:
    raise SystemExit('FootageJob anchor not found')
cpp = cpp.replace(old, new, 1)

old = '''    if (valid_ && GetTotalStreamCount()) {\n'''
new = '''    if ((valid_ || !proxy_decoder_.isEmpty()) && GetTotalStreamCount()) {\n'''
if old not in cpp:
    raise SystemExit('Footage icon validity anchor not found')
cpp = cpp.replace(old, new, 1)

old = '''    if (valid_) {\n      QString tip = tr("Filename: %1").arg(filename());\n'''
new = '''    if (valid_ || !proxy_decoder_.isEmpty()) {\n      QString tip = tr("Filename: %1").arg(filename());\n      tip.append(tr("\\nMedia: %1").arg(MediaStateLabel()));\n      if (!proxy_path().isEmpty()) {\n        tip.append(tr("\\nProxy: %1").arg(proxy_path()));\n      }\n      if (!reel().isEmpty()) tip.append(tr("\\nReel: %1").arg(reel()));\n      if (!scene().isEmpty()) tip.append(tr("\\nScene: %1").arg(scene()));\n      if (!take().isEmpty()) tip.append(tr("\\nTake: %1").arg(take()));\n      if (!camera().isEmpty()) tip.append(tr("\\nCamera: %1").arg(camera()));\n'''
if old not in cpp:
    raise SystemExit('Footage tooltip anchor not found')
cpp = cpp.replace(old, new, 1)

# Insert ProbeProxy before Reprobe.
anchor = '''void Footage::Reprobe()\n{\n'''
probe_proxy = '''void Footage::ProbeProxy()\n{\n  proxy_decoder_.clear();\n  const QString proxy = proxy_path();\n  if (proxy.isEmpty() || !QFileInfo::exists(proxy)) {\n    return;\n  }\n\n  const QVector<DecoderPtr> decoder_list = Decoder::ReceiveListOfAllDecoders();\n  for (const DecoderPtr &decoder : decoder_list) {\n    FootageDescription info = decoder->Probe(proxy, nullptr);\n    if (!info.IsValid()) {\n      continue;\n    }\n\n    const int proxy_stream_count = info.GetVideoStreams().size()\n        + info.GetAudioStreams().size() + info.GetSubtitleStreams().size();\n    if (GetTotalStreamCount() == 0 || proxy_stream_count == GetTotalStreamCount()) {\n      proxy_decoder_ = info.decoder();\n    }\n    break;\n  }\n}\n\nvoid Footage::Reprobe()\n{\n'''
if anchor not in cpp:
    raise SystemExit('Footage Reprobe function anchor not found')
cpp = cpp.replace(anchor, probe_proxy, 1)
cpp_path.write_text(cpp, encoding='utf-8')

# ---------------- Project Bin metadata columns ----------------
model_h_path = root / 'app/widget/projectexplorer/projectviewmodel.h'
model_h = model_h_path.read_text(encoding='utf-8')
old = '''    /// Media rate (frame rate for video, sample rate for audio)\n    kRate,\n\n    /// Last modified time (for footage/files)\n'''
new = '''    /// Media rate (frame rate for video, sample rate for audio)\n    kRate,\n\n    /// RB Media Intelligence columns\n    kMediaState,\n    kReel,\n    kScene,\n    kTake,\n    kCamera,\n    kLabelColor,\n    kFavorite,\n\n    /// Last modified time (for footage/files)\n'''
if old not in model_h:
    raise SystemExit('ProjectViewModel enum anchor not found')
model_h = model_h.replace(old, new, 1)
model_h_path.write_text(model_h, encoding='utf-8')

model_cpp_path = root / 'app/widget/projectexplorer/projectviewmodel.cpp'
model_cpp = model_cpp_path.read_text(encoding='utf-8')
old = '''#include "node/nodeundo.h"\n'''
new = '''#include "node/nodeundo.h"\n#include "node/project/footage/footage.h"\n'''
if old not in model_cpp:
    raise SystemExit('ProjectViewModel include anchor not found')
model_cpp = model_cpp.replace(old, new, 1)

old = '''    case kRate:\n      return internal_item->data(Node::FREQUENCY_RATE);\n    case kLastModified:\n'''
new = '''    case kRate:\n      return internal_item->data(Node::FREQUENCY_RATE);\n    case kMediaState:\n      if (auto *f = dynamic_cast<Footage*>(internal_item)) return f->MediaStateLabel();\n      break;\n    case kReel:\n      if (auto *f = dynamic_cast<Footage*>(internal_item)) return f->reel();\n      break;\n    case kScene:\n      if (auto *f = dynamic_cast<Footage*>(internal_item)) return f->scene();\n      break;\n    case kTake:\n      if (auto *f = dynamic_cast<Footage*>(internal_item)) return f->take();\n      break;\n    case kCamera:\n      if (auto *f = dynamic_cast<Footage*>(internal_item)) return f->camera();\n      break;\n    case kLabelColor:\n      if (auto *f = dynamic_cast<Footage*>(internal_item)) return f->label_color();\n      break;\n    case kFavorite:\n      if (auto *f = dynamic_cast<Footage*>(internal_item)) return f->favorite() ? QStringLiteral("★") : QString();\n      break;\n    case kLastModified:\n'''
if old not in model_cpp:
    raise SystemExit('ProjectViewModel data switch anchor not found')
model_cpp = model_cpp.replace(old, new, 1)

old = '''  case Qt::EditRole:\n    if (column_type == kName) {\n      return internal_item->GetLabel();\n    }\n    break;\n'''
new = '''  case Qt::EditRole:\n    if (column_type == kName) {\n      return internal_item->GetLabel();\n    }\n    if (auto *f = dynamic_cast<Footage*>(internal_item)) {\n      switch (column_type) {\n      case kReel: return f->reel();\n      case kScene: return f->scene();\n      case kTake: return f->take();\n      case kCamera: return f->camera();\n      case kLabelColor: return f->label_color();\n      case kFavorite: return f->favorite();\n      default: break;\n      }\n    }\n    break;\n'''
if old not in model_cpp:
    raise SystemExit('ProjectViewModel EditRole anchor not found')
model_cpp = model_cpp.replace(old, new, 1)

old = '''    case kRate:\n      return tr("Rate");\n    case kLastModified:\n'''
new = '''    case kRate:\n      return tr("Rate");\n    case kMediaState:\n      return tr("Media");\n    case kReel:\n      return tr("Reel");\n    case kScene:\n      return tr("Scene");\n    case kTake:\n      return tr("Take");\n    case kCamera:\n      return tr("Camera");\n    case kLabelColor:\n      return tr("Label");\n    case kFavorite:\n      return tr("Favorite");\n    case kLastModified:\n'''
if old not in model_cpp:
    raise SystemExit('ProjectViewModel headerData anchor not found')
model_cpp = model_cpp.replace(old, new, 1)

old = '''  // The name is editable\n  if (index.isValid() && index.column() == kName && role == Qt::EditRole) {\n'''
new = '''  if (index.isValid() && role == Qt::EditRole && index.column() != kName) {\n    if (auto *footage = dynamic_cast<Footage*>(GetItemObjectFromIndex(index))) {\n      QString input_id;\n      switch (static_cast<ColumnType>(index.column())) {\n      case kReel: input_id = Footage::kReelInput; break;\n      case kScene: input_id = Footage::kSceneInput; break;\n      case kTake: input_id = Footage::kTakeInput; break;\n      case kCamera: input_id = Footage::kCameraInput; break;\n      case kLabelColor: input_id = Footage::kLabelColorInput; break;\n      case kFavorite: input_id = Footage::kFavoriteInput; break;\n      default: break;\n      }\n      if (!input_id.isEmpty()) {\n        auto *cmd = new NodeParamSetStandardValueCommand(NodeKeyframeTrackReference(NodeInput(footage, input_id)), value);\n        Core::instance()->undo_stack()->push(cmd, tr("Edit Media Metadata"));\n        emit dataChanged(index, index);\n        return true;\n      }\n    }\n  }\n\n  // The name is editable\n  if (index.isValid() && index.column() == kName && role == Qt::EditRole) {\n'''
if old not in model_cpp:
    raise SystemExit('ProjectViewModel setData anchor not found')
model_cpp = model_cpp.replace(old, new, 1)

old = '''  // If the column is the kName column, that means it's editable\n  if (index.column() == kName) {\n    f |= Qt::ItemIsEditable;\n  }\n'''
new = '''  // Name and RB media metadata are editable for Footage items.\n  if (index.column() == kName) {\n    f |= Qt::ItemIsEditable;\n  } else if (dynamic_cast<Footage*>(GetItemObjectFromIndex(index))) {\n    switch (static_cast<ColumnType>(index.column())) {\n    case kReel: case kScene: case kTake: case kCamera: case kLabelColor: case kFavorite:\n      f |= Qt::ItemIsEditable;\n      break;\n    default:\n      break;\n    }\n  }\n'''
if old not in model_cpp:
    raise SystemExit('ProjectViewModel flags anchor not found')
model_cpp = model_cpp.replace(old, new, 1)
model_cpp_path.write_text(model_cpp, encoding='utf-8')

# ---------------- Project Explorer proxy assignment / toggles and metadata search ----------------
explorer_h_path = root / 'app/widget/projectexplorer/projectexplorer.h'
explorer_h = explorer_h_path.read_text(encoding='utf-8')
old = '''  void ReplaceSelectedFootage();\n\n  void OpenContextMenuItemInNewTab();\n'''
new = '''  void ReplaceSelectedFootage();\n\n  void AssignSelectedProxyMedia();\n\n  void UseSelectedOriginalMedia();\n\n  void UseSelectedProxyMedia();\n\n  void OpenContextMenuItemInNewTab();\n'''
if old not in explorer_h:
    raise SystemExit('ProjectExplorer slots anchor not found')
explorer_h = explorer_h.replace(old, new, 1)
explorer_h_path.write_text(explorer_h, encoding='utf-8')

explorer_cpp_path = root / 'app/widget/projectexplorer/projectexplorer.cpp'
explorer_cpp = explorer_cpp_path.read_text(encoding='utf-8')
old = '''  sort_model_.setFilterCaseSensitivity(Qt::CaseInsensitive);\n  sort_model_.setSortRole(ProjectViewModel::kInnerTextRole);\n'''
new = '''  sort_model_.setFilterCaseSensitivity(Qt::CaseInsensitive);\n  sort_model_.setFilterKeyColumn(-1); // search across name + RB media metadata columns\n  sort_model_.setSortRole(ProjectViewModel::kInnerTextRole);\n'''
if old not in explorer_cpp:
    raise SystemExit('ProjectExplorer filter anchor not found')
explorer_cpp = explorer_cpp.replace(old, new, 1)

old = '''        QAction *replace_action = menu.addAction(tr("Replace Footage"));\n        connect(replace_action, &QAction::triggered, this, &ProjectExplorer::ReplaceSelectedFootage);\n\n      }\n'''
new = '''        QAction *replace_action = menu.addAction(tr("Replace Footage"));\n        connect(replace_action, &QAction::triggered, this, &ProjectExplorer::ReplaceSelectedFootage);\n\n        auto *footage = static_cast<Footage*>(context_menu_item);\n        QAction *assign_proxy_action = menu.addAction(tr("Assign Proxy Media..."));\n        connect(assign_proxy_action, &QAction::triggered, this, &ProjectExplorer::AssignSelectedProxyMedia);\n\n        QAction *use_original_action = menu.addAction(tr("Use Original Media"));\n        use_original_action->setCheckable(true);\n        use_original_action->setChecked(footage->media_state() == Footage::RBMediaState::kOriginal);\n        connect(use_original_action, &QAction::triggered, this, &ProjectExplorer::UseSelectedOriginalMedia);\n\n        QAction *use_proxy_action = menu.addAction(tr("Use Proxy Media"));\n        use_proxy_action->setCheckable(true);\n        use_proxy_action->setEnabled(!footage->proxy_path().isEmpty());\n        use_proxy_action->setChecked(footage->media_state() == Footage::RBMediaState::kProxy);\n        connect(use_proxy_action, &QAction::triggered, this, &ProjectExplorer::UseSelectedProxyMedia);\n\n      }\n'''
if old not in explorer_cpp:
    raise SystemExit('ProjectExplorer footage context menu anchor not found')
explorer_cpp = explorer_cpp.replace(old, new, 1)

# Insert methods immediately before OpenContextMenuItemInNewTab.
anchor = '''void ProjectExplorer::OpenContextMenuItemInNewTab()\n'''
methods = '''void ProjectExplorer::AssignSelectedProxyMedia()\n{\n  if (context_menu_items_.size() != 1) return;\n  auto *footage = dynamic_cast<Footage*>(context_menu_items_.first());\n  if (!footage) return;\n\n  const QString file = QFileDialog::getOpenFileName(this, tr("Assign Proxy Media"));\n  if (file.isEmpty()) return;\n\n  auto *command = new MultiUndoCommand();\n  command->add_child(new NodeParamSetStandardValueCommand(NodeKeyframeTrackReference(NodeInput(footage, Footage::kProxyPathInput)), file));\n  command->add_child(new NodeParamSetStandardValueCommand(NodeKeyframeTrackReference(NodeInput(footage, Footage::kMediaStateInput)), static_cast<int>(Footage::RBMediaState::kProxy)));\n  Core::instance()->undo_stack()->push(command, tr("Assign Proxy Media"));\n}\n\nvoid ProjectExplorer::UseSelectedOriginalMedia()\n{\n  if (context_menu_items_.size() != 1) return;\n  auto *footage = dynamic_cast<Footage*>(context_menu_items_.first());\n  if (!footage) return;\n  Core::instance()->undo_stack()->push(\n      new NodeParamSetStandardValueCommand(NodeKeyframeTrackReference(NodeInput(footage, Footage::kMediaStateInput)), static_cast<int>(Footage::RBMediaState::kOriginal)),\n      tr("Use Original Media"));\n}\n\nvoid ProjectExplorer::UseSelectedProxyMedia()\n{\n  if (context_menu_items_.size() != 1) return;\n  auto *footage = dynamic_cast<Footage*>(context_menu_items_.first());\n  if (!footage) return;\n  if (footage->proxy_path().isEmpty() || !QFileInfo::exists(footage->proxy_path())) {\n    QMessageBox::warning(this, tr("Proxy Media"), tr("The assigned proxy file is unavailable. Assign or relink a proxy first."));\n    return;\n  }\n  Core::instance()->undo_stack()->push(\n      new NodeParamSetStandardValueCommand(NodeKeyframeTrackReference(NodeInput(footage, Footage::kMediaStateInput)), static_cast<int>(Footage::RBMediaState::kProxy)),\n      tr("Use Proxy Media"));\n}\n\nvoid ProjectExplorer::OpenContextMenuItemInNewTab()\n'''
if anchor not in explorer_cpp:
    raise SystemExit('ProjectExplorer method insertion anchor not found')
explorer_cpp = explorer_cpp.replace(anchor, methods, 1)
explorer_cpp_path.write_text(explorer_cpp, encoding='utf-8')

print('Applied RB VideoFire M4 Media Intelligence core: persistent metadata, Original/Proxy/Offline and real proxy playback resolution')
