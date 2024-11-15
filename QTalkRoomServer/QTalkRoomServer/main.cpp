#include "QTalkRoomServer.h"
#include <QtWidgets/QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    QTalkRoomServer w;
    w.show();
    return a.exec();
}
