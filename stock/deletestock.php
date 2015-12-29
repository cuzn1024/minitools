<?php
    require_once('360_safe3.php');
    require_once("database.php");

    if (!$_POST || !isset($_POST['id']) || !isset($_POST['user']))
    {
        echo "<script type='text/javascript'>history.go(-1);</script>";
        return;
    }

    deleteStock($_POST['user'], $_POST['id']);

    echo "<script type='text/javascript'>history.go(-1);</script>";
?>