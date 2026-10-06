#include <QApplication>
#include "app/MainWindow.h"

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    QApplication::setApplicationName("RB Videofire");
    QApplication::setApplicationVersion("0.1.0");
    QApplication::setOrganizationName("RB8 Solucoes Digitais");

    rbvf::MainWindow window;
    window.show();

    return app.exec();
}
