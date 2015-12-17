#include "dialog.h"

#include <QtNetwork>

Dialog::Dialog(QWidget *parent)
    : QDialog(parent), pos(0, 0), drag(false)
{
    setWindowFlags(Qt::WindowStaysOnTopHint | Qt::FramelessWindowHint);

    QVBoxLayout *vLayout = new QVBoxLayout();
    setLayout(vLayout);

    QSettings settings(QApplication::applicationDirPath() + "/stock.ini", QSettings::IniFormat);
    int count = settings.value("count").toInt();

    for (int i = 0; i < count; i++)
    {
        QList<QString> stockData;
        QString code = settings.value(QString("stock%1/code").arg(i+1)).toString();
        QString price = settings.value(QString("stock%1/price").arg(i+1)).toString();
        QString count = settings.value(QString("stock%1/count").arg(i+1)).toString();
        QString ratio = settings.value(QString("stock%1/ratio").arg(i+1)).toString();

        stockData.push_back(code);
        stockData.push_back(price);
        stockData.push_back(count);
        stockData.push_back(price);
        stockData.push_back(ratio);

        allStockData.push_back(stockData);
    }

    for (int i = 0; i < allStockData.count(); i++)
    {
        QHBoxLayout *hLayout = new QHBoxLayout();
        vLayout->addLayout(hLayout);
        const QList<QString> &data = allStockData.at(i);
        QLabel *name = new QLabel;
        name->setObjectName(QString("name_%1").arg(data.at(0)));
        name->setFixedSize(30, 20);
        hLayout->addWidget(name);
        QLabel *ratio = new QLabel;
        ratio->setObjectName(QString("ratio_%1").arg(data.at(0)));
        ratio->setFixedSize(50, 20);
        hLayout->addWidget(ratio);
        ratio = new QLabel;
        ratio->setObjectName(QString("todayratio_%1").arg(data.at(0)));
        ratio->setPalette(Qt::red);
        ratio->setFixedSize(50, 20);
        hLayout->addWidget(ratio);
        ratio = new QLabel;
        ratio->setObjectName(QString("highestratio_%1").arg(data.at(0)));
        ratio->setFixedSize(50, 20);
        hLayout->addWidget(ratio);
        QLabel *money = new QLabel;
        money->setObjectName(QString("money_%1").arg(data.at(0)));
        money->setFixedSize(60, 20);
        hLayout->addWidget(money);
    }

    manager = new QNetworkAccessManager(this);

    connect(manager, SIGNAL(finished(QNetworkReply*)),
            this, SLOT(replyFinished(QNetworkReply*)));

    QTimer *timer = new QTimer(this);
    connect(timer, SIGNAL(timeout()), this, SLOT(updateData()));
    timer->start(3000);
}

Dialog::~Dialog()
{

}

void Dialog::updateData()
{
    QString query = "http://hq.sinajs.cn/list=";
    for (int i = 0; i < allStockData.count(); i++)
    {
        query += allStockData.at(i).at(0);
        query += ",";
    }
    manager->get(QNetworkRequest(QUrl(query)));
}

void Dialog::replyFinished(QNetworkReply *networkReply)
{
    networkReply->waitForReadyRead(-1);

    QTextStream ts(networkReply);
    QString reply = ts.readAll();

    if (reply.isEmpty()) return;

    QStringList replyList = reply.split(";\n", QString::SkipEmptyParts);
    foreach (reply, replyList)
    {
        QString code = reply.mid(11, 8);

        int index = -1;
        for (int i = 0; i < allStockData.size(); i++)
        {
            index = i;
            if (allStockData.at(i).at(0) == code) break;
        }

        reply = reply.split("\"").at(1);
        QStringList data = reply.split(",");
        QString name = data.at(0);
        float current = data.at(3).toFloat();

        QLabel *label = findChild<QLabel*>(QString("name_%1").arg(code));
        label->setText(name.left(1));

        label = findChild<QLabel*>(QString("ratio_%1").arg(code));
        QString prefix = current == allStockData.at(index).at(3).toFloat() ? "" : (current > allStockData.at(index).at(3).toFloat() ? "↑" : "↓");
        label->setText(prefix + QString("%1%").arg(
                           int((current - allStockData.at(index).at(1).toFloat()) / allStockData.at(index).at(1).toFloat() * 10000) / 100.0
                           ));

        label = findChild<QLabel*>(QString("todayratio_%1").arg(code));
        float todayRatio = int((current - data.at(2).toFloat()) / data.at(2).toFloat() * 10000) / 100.0;
        label->setText(prefix + QString("%1%").arg(
                           int((current - data.at(2).toFloat()) / data.at(2).toFloat() * 10000) / 100.0
                           ));

        label->setAutoFillBackground(!allStockData.at(index).at(4).isEmpty() && (todayRatio > 0 && allStockData.at(index).at(4).toFloat() < todayRatio || todayRatio < 0 && allStockData.at(index).at(4).toFloat() > todayRatio));

        label = findChild<QLabel*>(QString("highestratio_%1").arg(code));
        label->setText(QString("%1%").arg(
                           int((data.at(4).toFloat() - allStockData.at(index).at(1).toFloat()) / allStockData.at(index).at(1).toFloat() * 10000) / 100.0
                           ));

        label = findChild<QLabel*>(QString("money_%1").arg(code));
        label->setText(QString::number(allStockData.at(index).at(2).toInt() * (current - allStockData.at(index).at(1).toFloat())));

        allStockData[index][3] = QString::number(current);
    }

    networkReply->deleteLater();
}

void Dialog::mousePressEvent(QMouseEvent *event)
{
    if (event->button() != Qt::LeftButton)
        return;

    drag = true;
    pos = event->globalPos() - frameGeometry().topLeft();
    event->accept();
}

void Dialog::mouseMoveEvent(QMouseEvent *event)
{
    if (!drag)
        return;

    if (event->globalPos().y() == 0)
        this->move(event->globalPos().x() - pos.x(), 0);
    else
        this->move(event->globalPos() - pos);

    event->accept();
}

void Dialog::mouseReleaseEvent(QMouseEvent *event)
{
    drag = false;
    event->accept();
}
