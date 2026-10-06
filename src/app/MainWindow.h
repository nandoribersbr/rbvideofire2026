#pragma once

#include <QMainWindow>

#include <memory>

class QLabel;
class QPushButton;
class QSlider;
class QTableWidget;
class QTimer;

namespace rbvf {

class IMediaEngine;

class MainWindow final : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);

private:
    void buildUi();
    void buildMenus();
    void importMedia();
    void addMediaRow(const QString& filePath);
    void loadSelectedMedia(int row, int column);
    void renderPreview(double seconds);
    void togglePlayback();
    void stopPlayback();
    void onPlaybackTick();
    static QString formatDuration(double seconds);

    std::unique_ptr<IMediaEngine> m_mediaEngine;
    QTableWidget* m_mediaTable{nullptr};
    QLabel* m_preview{nullptr};
    QLabel* m_timeLabel{nullptr};
    QPushButton* m_playButton{nullptr};
    QSlider* m_seekSlider{nullptr};
    QTimer* m_playTimer{nullptr};

    QString m_currentMediaPath;
    double m_currentDuration{0.0};
    double m_currentPosition{0.0};
    bool m_playing{false};
};

} // namespace rbvf
