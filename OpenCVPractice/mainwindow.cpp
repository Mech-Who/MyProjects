#include "mainwindow.h"
#include "./ui_mainwindow.h"

#include <opencv2/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    cv::Mat img = cv::imread("C:\\Users\\HP\\Pictures\\Camera Roll\\pretty_sis.png");
    cv::imshow("pretty_sis", img);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_introduceBtn_clicked()
{
    ui->stackedWidget->setCurrentWidget(ui->pageIntroduce);
}


void MainWindow::on_imgProcessBtn_clicked()
{
    ui->stackedWidget->setCurrentWidget(ui->pageProcess);
}

