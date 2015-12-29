<?php

require_once("defines.php");

function openDatabase() {
    global $host, $username, $password, $database;
    $con = mysql_connect($host, $username, $password);
    do {
        if (!$con)
            break;

        if (!mysql_select_db($database, $con))
            break;

        return $con;
    } while (false);

    die("Fail to open database:" . mysql_error());
}

function readStocksOfUser($username, $password) {
    $con = openDatabase();

    do {
        $result = null;
        $result = mysql_query("select * from user where user.name='$username'");

        if (!mysql_fetch_row($result))
        {
            mysql_close($con);
            return -1;
        }

        $result = mysql_query("select * from stock, user where stock.user_id=user.id and user.name='$username' order by stock.id");

        $ret = Array();

        do {
            $temp = mysql_fetch_row($result);
            if (!$temp)
                break;

            $tmp['id'] = $temp[0];
            $tmp['code'] = $temp[1];
            $tmp['price'] = $temp[2];
            $tmp['count'] = $temp[3];
            $tmp['user'] = $temp[4];
            $tmp['current'] = $temp[2];

            array_push($ret, $tmp);
        }
        while (true);

        mysql_close($con);
        return $ret;
    } while (false);

    die("cannot find such user info:" . mysql_error());
}

function deleteStock($username, $stockId)
{
    $con = openDatabase();

    mysql_query("delete from stock where user_id=(select id from user where name='$username')  and id=$stockId");
}

function addStock($username, $code, $price, $count)
{
    $con = openDatabase();

    mysql_query("INSERT INTO stock(`code`, `price`, `count`, `user_id`) VALUES ('$code', '$price', '$count', (select id from user where user.name='$username'))");
}

?>