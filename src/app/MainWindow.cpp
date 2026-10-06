#include "MainWindow.h"

#include "media/FfmpegMediaEngine.h"
#include "media/IMediaEngine.h"

#include <QAbstractItemView>
#include <QAction>
#include <QDockWidget>
#include <QFileDialog>
#include <QFileInfo>
#include <QHeaderView>
#include <QKeySequence>
#include <QLabel>
#include <QMenu>
#include <QMenuBar>
#include <QMessageBox>
#include <QStatusBar>
#include <QTableWidget>
#include <QTableWidgetItem>
#include <QTextEdit>
#include <QVBoxLayout>
#include <QWidget>

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

    auto *preview = new QLabel("PREVIEW", center);
    preview->setAlignment(Qt::AlignCenter);
    preview->setMinimumHeight(360);
    preview->setStyleSheet("background:#101214;color:#d8d8d8;font-size:22px;");

    auto *timeline = new QTextEdit(center);
    timeline->setReadOnly(true);
    timeline->setMinimumHeight(280);
    timeline->setPlainText(
        "TIMELINE\n\n"
        "V2  --------------------------------------------------------\n"
        "V1  --------------------------------------------------------\n"
        "A1  --------------------------------------------------------"
    );

    layout->addWidget(preview, 3);
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
    const std::filesystem::path nativePath =
        std::filesystem::path(filePath.toStdWString());

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

    m_mediaTable->setItem(row, 0, new QTableWidgetItem(QFileInfo(filePath).fileName()));
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
