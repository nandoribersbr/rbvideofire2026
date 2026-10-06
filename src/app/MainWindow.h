#pragma once

#include <QMainWindow>

namespace rbvf {

class MainWindow final : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);

private:
    void buildUi();
    void buildMenus();
};

} // namespace rbvf
