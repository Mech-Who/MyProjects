#include "QTalkRoom.h"
#include <QtWidgets/QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    QTalkRoom w;
    w.show();
    return a.exec();
}
