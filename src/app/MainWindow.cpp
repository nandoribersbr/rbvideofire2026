#include "MainWindow.h"

#include "media/FfmpegMediaEngine.h"
#include "media/IMediaEngine.h"

#include <QAbstractItemView>
#include <QAction>
#include <QDockWidget>
#include <QFileDialog>
#include <QFileInfo>
#include <QHBoxLayout>
#include <QHeaderView>
#include <QImage>
#include <QKeySequence>
#include <QLabel>
#include <QMenu>
#include <QMenuBar>
#include <QMessageBox>
#include <QPixmap>
#include <QPushButton>
#include <QSlider>
#include <QStatusBar>
#include <QTableWidget>
#include <QTableWidgetItem>
#include <QTextEdit>
#include <QTimer>
#include <QVBoxLayout>
#include <QWidget>

#include <algorithm>
#include <cmath>
#include <exception>
#include <filesystem>
#include <stdexcept>

namespace rbvf {

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent),
      m_mediaEngine(std::make_unique<FfmpegMediaEngine>())
{
    setWindowTitle("RB Videofire 0.1");
    resize(1440, 900);

    buildMenus();
    buildUi();

    statusBar()->showMessage("Pronto");
}

void MainWindow::buildMenus()
{
    auto *fileMenu = menuBar()->addMenu("Arquivo");
    fileMenu->addAction("Novo projeto");
    fileMenu->addAction("Abrir projeto");
    fileMenu->addAction("Salvar projeto");
    fileMenu->addSeparator();

    auto *importAction = fileMenu->addAction("Importar mídia...");
    importAction->setShortcut(QKeySequence("Ctrl+I"));
    connect(importAction, &QAction::triggered, this, &MainWindow::importMedia);

    fileMenu->addSeparator();

    auto *exitAction = fileMenu->addAction("Sair");
    connect(exitAction, &QAction::triggered, this, &QWidget::close);

    menuBar()->addMenu("Editar");
    menuBar()->addMenu("Exibir");
    menuBar()->addMenu("Exportar");
    menuBar()->addMenu("Ajuda");
}

void MainWindow::buildUi()
{
    auto *center = new QWidget(this);
    auto *layout = new QVBoxLayout(center);

    m_preview = new QLabel("PREVIEW", center);
    m_preview->setAlignment(Qt::AlignCenter);
    m_preview->setMinimumHeight(360);
    m_preview->setStyleSheet("background:#101214;color:#d8d8d8;font-size:22px;");

    auto *transport = new QWidget(center);
    auto *transportLayout = new QHBoxLayout(transport);
    transportLayout->setContentsMargins(0, 0, 0, 0);

    m_playButton = new QPushButton("Play", transport);
    auto *stopButton = new QPushButton("Stop", transport);
    m_seekSlider = new QSlider(Qt::Horizontal, transport);
    m_seekSlider->setRange(0, 1000);
    m_seekSlider->setEnabled(false);
    m_timeLabel = new QLabel("00:00:00.000 / 00:00:00.000", transport);

    transportLayout->addWidget(m_playButton);
    transportLayout->addWidget(stopButton);
    transportLayout->addWidget(m_seekSlider, 1);
    transportLayout->addWidget(m_timeLabel);

    connect(m_playButton, &QPushButton::clicked, this, &MainWindow::togglePlayback);
    connect(stopButton, &QPushButton::clicked, this, &MainWindow::stopPlayback);
    connect(m_seekSlider, &QSlider::sliderMoved, this, [this](int value) {
        if (m_currentDuration <= 0.0) {
            return;
        }

        m_currentPosition = m_currentDuration * (static_cast<double>(value) / 1000.0);
        renderPreview(m_currentPosition);
    });

    m_playTimer = new QTimer(this);
    m_playTimer->setInterval(40);
    connect(m_playTimer, &QTimer::timeout, this, &MainWindow::onPlaybackTick);

    auto *timeline = new QTextEdit(center);
    timeline->setReadOnly(true);
    timeline->setMinimumHeight(280);
    timeline->setPlainText(
        "TIMELINE\n\n"
        "V2  --------------------------------------------------------\n"
        "V1  --------------------------------------------------------\n"
        "A1  --------------------------------------------------------"
    );

    layout->addWidget(m_preview, 3);
    layout->addWidget(transport);
    layout->addWidget(timeline, 2);
    setCentralWidget(center);

    auto *mediaDock = new QDockWidget("Mídia", this);

    m_mediaTable = new QTableWidget(mediaDock);
    m_mediaTable->setColumnCount(6);
    m_mediaTable->setHorizontalHeaderLabels({
        "Arquivo",
        "Duração",
        "Resolução",
        "FPS",
        "Codec de vídeo",
        "Codec de áudio"
    });
    m_mediaTable->setSelectionBehavior(QAbstractItemView::SelectRows);
    m_mediaTable->setSelectionMode(QAbstractItemView::SingleSelection);
    m_mediaTable->setEditTriggers(QAbstractItemView::NoEditTriggers);
    m_mediaTable->setAlternatingRowColors(true);
    m_mediaTable->verticalHeader()->setVisible(false);
    m_mediaTable->horizontalHeader()->setStretchLastSection(true);
    m_mediaTable->horizontalHeader()->setSectionResizeMode(0, QHeaderView::Stretch);
    for (int column = 1; column < 6; ++column) {
        m_mediaTable->horizontalHeader()->setSectionResizeMode(column, QHeaderView::ResizeToContents);
    }

    connect(m_mediaTable, &QTableWidget::cellDoubleClicked,
            this, &MainWindow::loadSelectedMedia);

    mediaDock->setWidget(m_mediaTable);
    mediaDock->setMinimumWidth(650);
    addDockWidget(Qt::LeftDockWidgetArea, mediaDock);

    auto *inspectorDock = new QDockWidget("Propriedades", this);
    inspectorDock->setWidget(new QLabel("Inspector do clipe", inspectorDock));
    addDockWidget(Qt::RightDockWidgetArea, inspectorDock);
}

void MainWindow::importMedia()
{
    const QStringList files = QFileDialog::getOpenFileNames(
        this,
        "Importar vídeo",
        QString(),
        "Arquivos de vídeo (*.mp4 *.mov *.mkv *.avi *.m4v *.webm *.mts *.m2ts *.mpeg *.mpg);;Todos os arquivos (*.*)"
    );

    if (files.isEmpty()) {
        return;
    }

    int imported = 0;
    QStringList failures;

    statusBar()->showMessage("Analisando mídia com FFmpeg...");

    for (const QString& filePath : files) {
        try {
            addMediaRow(filePath);
            ++imported;
        } catch (const std::exception& error) {
            failures << QString("%1: %2")
                            .arg(QFileInfo(filePath).fileName(),
                                 QString::fromUtf8(error.what()));
        }
    }

    if (!failures.isEmpty()) {
        QMessageBox::warning(
            this,
            "Alguns arquivos não foram importados",
            failures.join("\n")
        );
    }

    statusBar()->showMessage(
        QString("%1 arquivo(s) importado(s)").arg(imported),
        5000
    );
}

void MainWindow::addMediaRow(const QString& filePath)
{
    const std::filesystem::path nativePath(filePath.toStdWString());
    const MediaInfo info = m_mediaEngine->probe(nativePath);

    if (!info.hasVideo) {
        throw std::runtime_error("O arquivo não contém uma faixa de vídeo compatível.");
    }

    const int row = m_mediaTable->rowCount();
    m_mediaTable->insertRow(row);

    const QString resolution =
        info.width > 0 && info.height > 0
            ? QString("%1x%2").arg(info.width).arg(info.height)
            : QStringLiteral("—");

    const QString fps =
        info.frameRate > 0.0
            ? QString::number(info.frameRate, 'f', 3)
            : QStringLiteral("—");

    auto *nameItem = new QTableWidgetItem(QFileInfo(filePath).fileName());
    nameItem->setData(Qt::UserRole, filePath);
    nameItem->setData(Qt::UserRole + 1, info.durationSeconds);

    m_mediaTable->setItem(row, 0, nameItem);
    m_mediaTable->setItem(row, 1, new QTableWidgetItem(formatDuration(info.durationSeconds)));
    m_mediaTable->setItem(row, 2, new QTableWidgetItem(resolution));
    m_mediaTable->setItem(row, 3, new QTableWidgetItem(fps));
    m_mediaTable->setItem(row, 4, new QTableWidgetItem(
        info.videoCodec.empty() ? "—" : QString::fromStdString(info.videoCodec)
    ));
    m_mediaTable->setItem(row, 5, new QTableWidgetItem(
        info.audioCodec.empty() ? "Sem áudio" : QString::fromStdString(info.audioCodec)
    ));

    for (int column = 0; column < m_mediaTable->columnCount(); ++column) {
        if (auto *item = m_mediaTable->item(row, column)) {
            item->setToolTip(filePath);
        }
    }
}

void MainWindow::loadSelectedMedia(int row, int)
{
    auto *item = m_mediaTable->item(row, 0);
    if (!item) {
        return;
    }

    m_currentMediaPath = item->data(Qt::UserRole).toString();
    m_currentDuration = item->data(Qt::UserRole + 1).toDouble();
    m_currentPosition = 0.0;
    m_playing = false;
    m_playTimer->stop();
    m_playButton->setText("Play");
    m_seekSlider->setEnabled(true);
    m_seekSlider->setValue(0);

    renderPreview(0.0);
}

void MainWindow::renderPreview(double seconds)
{
    if (m_currentMediaPath.isEmpty()) {
        return;
    }

    try {
        const std::filesystem::path nativePath(m_currentMediaPath.toStdWString());
        const VideoFrame frame = m_mediaEngine->decodeFrameAt(nativePath, seconds);

        QImage image(
            frame.rgb24.data(),
            frame.width,
            frame.height,
            frame.stride,
            QImage::Format_RGB888
        );

        const QPixmap pixmap = QPixmap::fromImage(image.copy());

        m_preview->setPixmap(
            pixmap.scaled(
                m_preview->size(),
                Qt::KeepAspectRatio,
                Qt::SmoothTransformation
            )
        );

        if (m_currentDuration > 0.0) {
            const int sliderValue = static_cast<int>(
                std::clamp(m_currentPosition / m_currentDuration, 0.0, 1.0) * 1000.0
            );
            if (!m_seekSlider->isSliderDown()) {
                m_seekSlider->setValue(sliderValue);
            }
        }

        m_timeLabel->setText(
            QString("%1 / %2")
                .arg(formatDuration(m_currentPosition),
                     formatDuration(m_currentDuration))
        );
    } catch (const std::exception& error) {
        statusBar()->showMessage(
            QString("Erro no preview: %1").arg(QString::fromUtf8(error.what())),
            5000
        );
    }
}

void MainWindow::togglePlayback()
{
    if (m_currentMediaPath.isEmpty()) {
        return;
    }

    m_playing = !m_playing;

    if (m_playing) {
        if (m_currentPosition >= m_currentDuration && m_currentDuration > 0.0) {
            m_currentPosition = 0.0;
        }

        m_playButton->setText("Pause");
        m_playTimer->start();
    } else {
        m_playButton->setText("Play");
        m_playTimer->stop();
    }
}

void MainWindow::stopPlayback()
{
    m_playing = false;
    m_playTimer->stop();
    m_playButton->setText("Play");
    m_currentPosition = 0.0;

    if (!m_currentMediaPath.isEmpty()) {
        renderPreview(0.0);
    }
}

void MainWindow::onPlaybackTick()
{
    if (!m_playing || m_currentMediaPath.isEmpty()) {
        return;
    }

    m_currentPosition += static_cast<double>(m_playTimer->interval()) / 1000.0;

    if (m_currentDuration > 0.0 && m_currentPosition >= m_currentDuration) {
        m_currentPosition = m_currentDuration;
        renderPreview(m_currentPosition);
        m_playing = false;
        m_playTimer->stop();
        m_playButton->setText("Play");
        return;
    }

    renderPreview(m_currentPosition);
}

QString MainWindow::formatDuration(double seconds)
{
    if (!std::isfinite(seconds) || seconds < 0.0) {
        return QStringLiteral("—");
    }

    const qint64 totalMilliseconds =
        static_cast<qint64>(std::llround(seconds * 1000.0));

    const qint64 hours = totalMilliseconds / 3'600'000;
    const qint64 minutes = (totalMilliseconds / 60'000) % 60;
    const qint64 secs = (totalMilliseconds / 1000) % 60;
    const qint64 millis = totalMilliseconds % 1000;

    return QString("%1:%2:%3.%4")
        .arg(hours, 2, 10, QLatin1Char('0'))
        .arg(minutes, 2, 10, QLatin1Char('0'))
        .arg(secs, 2, 10, QLatin1Char('0'))
        .arg(millis, 3, 10, QLatin1Char('0'));
}

} // namespace rbvf
