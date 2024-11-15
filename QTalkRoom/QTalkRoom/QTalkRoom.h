#pragma once

#include <QtWidgets/QMainWindow>
#include "ui_QTalkRoom.h"

class QTalkRoom : public QMainWindow
{
    Q_OBJECT

public:
    QTalkRoom(QWidget *parent = nullptr);
    ~QTalkRoom();

private:
    Ui::QTalkRoomClass ui;
};
