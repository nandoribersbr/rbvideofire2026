#include "MainWindow.h"

#include <QAction>
#include <QDockWidget>
#include <QLabel>
#include <QMenu>
#include <QMenuBar>
#include <QStatusBar>
#include <QTextEdit>
#include <QVBoxLayout>
#include <QWidget>

namespace rbvf {

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
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
    fileMenu->addAction("Importar mídia");
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
    mediaDock->setWidget(new QLabel("Biblioteca de mídia", mediaDock));
    addDockWidget(Qt::LeftDockWidgetArea, mediaDock);

    auto *inspectorDock = new QDockWidget("Propriedades", this);
    inspectorDock->setWidget(new QLabel("Inspector do clipe", inspectorDock));
    addDockWidget(Qt::RightDockWidgetArea, inspectorDock);
}

} // namespace rbvf
