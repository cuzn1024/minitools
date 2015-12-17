#ifndef DIALOG_H
#define DIALOG_H

#include <QtWidgets>

class QNetworkReply;
class QNetworkAccessManager;
class Dialog : public QDialog
{
    Q_OBJECT

public:
    Dialog(QWidget *parent = 0);
    ~Dialog();

private slots:
    void updateData();
    void replyFinished(QNetworkReply*);

protected:
    void mousePressEvent(QMouseEvent *event);
    void mouseMoveEvent(QMouseEvent *event);
    void mouseReleaseEvent(QMouseEvent *event);

private:
    QList<QList<QString>> allStockData;

    QNetworkAccessManager *manager;
    QPoint pos;
    bool drag;
};

#endif // DIALOG_H
