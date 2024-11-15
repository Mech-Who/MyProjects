#pragma once

#include <QtCore/QPointer>
#include <QtWidgets/QMainWindow>
#include <QtNetwork/QTcpServer>

#include "ui_QTalkRoomServer.h"

class QTalkRoomServer : public QMainWindow
{
    Q_OBJECT

public:
    QTalkRoomServer(QWidget *parent = nullptr);
    ~QTalkRoomServer();
    bool startServer(QString ip, QString port);
    bool stopServer();

private slots:
    void on_connectButton_clicked();
    void on_disconnectButton_clicked();
    void doProcessNewConnection();

signals:
    void newConnection();

private:
    Ui::QTalkRoomServerClass ui;
    QTcpServer* server_ptr;
    int MAX_CONNECTION = 10;
};
