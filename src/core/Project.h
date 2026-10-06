#pragma once

#include <QString>
#include "Timeline.h"

namespace rbvf {

class Project
{
public:
    QString name{"Projeto sem título"};
    int width{1920};
    int height{1080};
    double fps{30.0};
    Timeline timeline;
};

} // namespace rbvf
