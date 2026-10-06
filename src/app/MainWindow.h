#pragma once

#include <QMainWindow>

#include <memory>

class QTableWidget;

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
    static QString formatDuration(double seconds);

    std::unique_ptr<IMediaEngine> m_mediaEngine;
    QTableWidget* m_mediaTable{nullptr};
};

} // namespace rbvf
