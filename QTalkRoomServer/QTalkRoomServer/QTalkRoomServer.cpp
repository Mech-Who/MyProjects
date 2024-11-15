/* 
* qt网络编程参考：https://doc.qt.io/qt-6/qtnetwork-programming.html
* 实现参考：
* https://blog.csdn.net/Dirty_artist/article/details/142535886
* https://blog.csdn.net/sumfortp/article/details/140359496
*/
#include <iostream>
#include "QTalkRoomServer.h"

QTalkRoomServer::QTalkRoomServer(QWidget *parent)
    : QMainWindow(parent)
{
    ui.setupUi(this);
    this->server_ptr = new QTcpServer(this);
    qDebug() << "Server start!";
}

QTalkRoomServer::~QTalkRoomServer()
{
    qDebug() << "Server stop!";
    delete this->server_ptr;
}

bool QTalkRoomServer::startServer(QString ip, QString port)
{
    // 创建服务器
    bool ret = this->server_ptr->listen(QHostAddress(ip), port.toUInt());
    //根据服务器状态返回
    if (!ret) {
        qDebug() << "Server" + ip + ":" + port + " start failed!";
        return false;
    }
    qDebug() << "Server" + ip + ":" + port + " start!";
    this->server_ptr->setMaxPendingConnections(this->MAX_CONNECTION);
    connect(this->server_ptr, SIGNAL(newConnection()), this, SLOT(doProcessNewConnection()));
    connect(this->server_ptr, SIGNAL(acceptError(QAbstractSocket::SocketError)),
        this, SLOT(doProcessAcceptError(QAbstractSocket::SocketError)));
    return true;
}

bool QTalkRoomServer::stopServer()
{
    // 停止服务期
    this->server_ptr->destroyed();
    // 根据服务器状态返回
    if (nullptr == this->server_ptr) {
        return true;
    }
    else {
        return false;
    }
    return true;
}

void QTalkRoomServer::on_connectButton_clicked() {
    // 获取ip和port信息
    QString ip = this->ui.ipLineEdit->text();
    QString port = this->ui.portLineEdit->text();
    // 锁定ip和port输入框
    this->ui.ipLineEdit->setDisabled(true);
    this->ui.portLineEdit->setDisabled(true);
    // 连接服务器
    // TODO
    bool res = this->startServer(ip, port);
    // 生成日志信息并打印
    QString message = "";
    if (res) {
        message = ip + " " + port + " connect succeed!";
        this->ui.conenctButton->setDisabled(true);
    }
    else
        message = ip + " " + port + " connect failed!";
    qDebug() << message;
    // 输出信息到UI终端
    this->ui.messageTextEdit->append(message);
}

void QTalkRoomServer::on_disconnectButton_clicked() {
    // 获取ip和port信息
    QString ip = this->ui.ipLineEdit->text();
    QString port = this->ui.portLineEdit->text();
    // 解锁ip和port输入框
    this->ui.ipLineEdit->setEnabled(true);
    this->ui.portLineEdit->setEnabled(true);
    // 断联服务器
    // TODO

    // 生成日志信息并打印
    QString message = ip + " " + port + " disconnected!";
    qDebug() << message;
    // 输出信息到UI终端
    this->ui.messageTextEdit->append(message);
}