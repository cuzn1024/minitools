<?php
    require_once('360_safe3.php');
    require_once("database.php");

    if (!$_POST || !isset($_POST['price']) || !isset($_POST['count']) || !isset($_POST['code']) || !isset($_POST['user']))
    {
        echo "<script type='text/javascript'>history.go(-1);</script>";
        return;
    }

    if (strlen(file_get_contents("http://hq.sinajs.cn/list=" . $_POST["code"])) >= 20)
    {
        addStock($_POST['user'], $_POST['code'], $_POST['price'], $_POST['count']);
    }

    echo "<script type='text/javascript'>history.go(-1);</script>";
?>