<?php

    require_once('360_safe3.php');
    require_once("database.php");

    if (empty($_POST) || empty($_POST['username']))
    {
        header("Location: http://money.cuzn1024.com/login.php");
        exit;
    }

    $stocks = readStocksOfUser($_POST['username'], $_POST['password']);

    if ($stocks == -1)
    {
        header("Location: http://money.cuzn1024.com/login.php");
        exit;
    }
?>

<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>Re&#58;</title>
        <script type='text/javascript'>
            var sz = 0, cyb = 0;
            var current = new Array(<?php echo count($stocks); ?>);
            for (var i = 0; i < current.length; i++)
            {
                current[i] = 0;
            }
            var script = null;
            function loadScript(url, callback){
                if (script != null)
                {
                    document.getElementsByTagName("head")[0].removeChild(script);
                }
                script = document.createElement ("script")
                script.type = "text/javascript";
                if (script.readyState){ //IE
                    script.onreadystatechange = function(){
                        if (script.readyState == "loaded" || script.readyState == "complete"){
                            script.onreadystatechange = null;
                            callback();
                        }
                    };
                } else { //Others
                    script.onload = function(){
                        callback();
                    };
                }
                script.src = url;
                document.getElementsByTagName("head")[0].appendChild(script);
            }

            function updateStocks()
            {                
                <?php
                    $url = "http://hq.sinajs.cn/list=sh000001,sz399006,";
                    for ($index = 0; $index < count($stocks); $index++)
                    {
                        $url = $url . $stocks[$index]["code"] . ",";
                    }
                ?>
                loadScript(<?php echo "'$url'"; ?>, function(){
                    var words;
                    var tr;
                    var title;

                    words = hq_str_sh000001.split(',');
                    tr = document.getElementsByTagName('tr')[0];
                    tr.childNodes[0].textContent = (parseFloat(words[3]) == sz ? "" : (parseFloat(words[3]) > sz ? "↑ " : "↓")) + Math.round((parseFloat(words[3]) - parseFloat(words[2])) / parseFloat(words[2]) * 10000) / 100.0;
                    tr.childNodes[1].textContent = Math.round((parseFloat(words[4]) - parseFloat(words[2])) / parseFloat(words[2]) * 10000) / 100.0;
                    sz = parseFloat(words[3]);
                    title = "Re:"
                    title += tr.childNodes[0].textContent;
                    title += " ";

                    words = hq_str_sz399006.split(',');
                    tr = document.getElementsByTagName('tr')[0];
                    tr.childNodes[2].textContent = (parseFloat(words[3]) == cyb ? "" : (parseFloat(words[3]) > cyb ? "↑ " : "↓")) + Math.round((parseFloat(words[3]) - parseFloat(words[2])) / parseFloat(words[2]) * 10000) / 100.0;
                    tr.childNodes[3].textContent = Math.round((parseFloat(words[4]) - parseFloat(words[2])) / parseFloat(words[2]) * 10000) / 100.0;
                    cyb = parseFloat(words[3]);
                    title += tr.childNodes[2].textContent;
                    document.title = title;

                <?php
                    for ($index = 0; $index < count($stocks); $index++)
                    {
                        echo "words = hq_str_" . $stocks[$index]["code"] . ".split(',');";
                        echo "tr = document.getElementsByTagName('tr')[" . ($index + 1) . "];";
                        echo "tr.childNodes[0].textContent = words[0].charAt(0);";
                        echo "tr.childNodes[1].textContent = (parseFloat(words[3]) == current[$index] ? '' : (parseFloat(words[3]) > current[$index] ? '↑ ' : '↓')) + Math.round((parseFloat(words[3]) - parseFloat(words[2])) / parseFloat(words[2]) * 10000) / 100.0;";
                        echo "tr.childNodes[2].textContent = Math.round((parseFloat(words[3]) - (" . $stocks[$index]["price"] . ")) / (" . $stocks[$index]["price"] . ") * 10000) / 100.0;";
                        echo "tr.childNodes[3].textContent = Math.round((parseFloat(words[3]) - (" . $stocks[$index]["price"] . ")) * " . $stocks[$index]["count"] .");";
                        // echo "tr.childNodes[3].textContent = Math.round((parseFloat(words[4]) - parseFloat(words[2])) / parseFloat(words[2]) * 10000) / 100.0;";
                        echo "current[$index] = parseFloat(words[3]);";
                    }
                ?>

                    if (document.getElementsByTagName('div')[0].style.visibility == 'visible')
                    {
                        setTimeout('updateStocks()', 2000);
                    }
                });
            }
<?php
    if (count($stocks) != 0)
    {
        echo "setTimeout('updateStocks()', 2000);";
    }
?>

        </script>
    </head>
    <body ondblclick="document.getElementsByTagName('div')[0].style.visibility ='visible';setTimeout('updateStocks()', 2000);">
        <div style="visibility:visible">
            <table border="1">
                <tr><td width="50"></td><td width="50"></td><td width="50"></td><td width="50"></td></tr>
                <?php
                    for ($index = 0; $index < count($stocks); $index++)
                    {
                        echo "<tr>";
                        echo "<td width='50'></td>";
                        echo "<td width='50'></td>";
                        echo "<td width='50'></td>";
                        echo "<td width='50'></td>";
                        echo "<td><form action='./deletestock.php' method='post' onsubmit='return confirm(\"Confirm to remove!\");'><button name='id' value='" . $stocks[$index]["id"] . "'>remove</button><input type='hidden' name='user' value='" . $_POST['username'] . "'/></form></td>";
                        echo "</tr>";
                    }
                ?>
            </table>
            <br />
            <table>
                <tr>
                    <form action='./addstock.php' method='post'>
                        <td><input size="8" type="text" placeholder="code" name="code"></input></td>
                        <td><input size="8" type="text" placeholder="price" name="price"></input></td>
                        <td><input size="8" type="text" placeholder="count" name="count"></input></td>
                        <td><button name='user' value=<?php echo "'" . $_POST['username'] . "'"; ?>>add</button></td>
                    </form>
                </tr>
                <tr>
                    <td><button id="hidden" onclick="document.getElementsByTagName('div')[0].style.visibility='hidden';">Hidden</button></td>
                </tr>
            </table>
        </div>
    </body>
</html>	