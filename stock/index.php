<?php

    require_once('360_safe3.php');
    require_once("database.php");

    if (empty($_POST) || empty($_POST['username']))
    {
        header("Location: http://localhost/stock/login.php");
        exit;
    }

    $stocks = readStocksOfUser($_POST['username'], $_POST['password']);

    if ($stocks == -1)
    {
        header("Location: http://localhost/stock/login.php");
        exit;
    }
?>

<html>
    <head>
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

                    words = hq_str_sh000001.split(',');
                    tr = document.getElementsByTagName('tr')[0];
                    tr.childNodes[0].textContent = (parseFloat(words[3]) == sz ? "" : (parseFloat(words[3]) > sz ? "↑" : "↓")) + Math.round((parseFloat(words[3]) - parseFloat(words[2])) / parseFloat(words[2]) * 10000) / 100.0;
                    tr.childNodes[1].textContent = Math.round((parseFloat(words[4]) - parseFloat(words[2])) / parseFloat(words[2]) * 10000) / 100.0;
                    sz = parseFloat(words[3]);

                    words = hq_str_sz399006.split(',');
                    tr = document.getElementsByTagName('tr')[0];
                    tr.childNodes[2].textContent = (parseFloat(words[3]) == sz ? "" : (parseFloat(words[3]) > sz ? "↑" : "↓")) + Math.round((parseFloat(words[3]) - parseFloat(words[2])) / parseFloat(words[2]) * 10000) / 100.0;
                    tr.childNodes[3].textContent = Math.round((parseFloat(words[4]) - parseFloat(words[2])) / parseFloat(words[2]) * 10000) / 100.0;
                    cyb = parseFloat(words[3]);

                <?php
                    for ($index = 0; $index < count($stocks); $index++)
                    {
                        echo "words = hq_str_" . $stocks[$index]["code"] . ".split(',');";
                        echo "tr = document.getElementsByTagName('tr')[" . ($index + 1) . "];";
                        echo "tr.childNodes[0].textContent = words[0].charAt(0);";
                        echo "tr.childNodes[1].textContent = (parseFloat(words[3]) == current[$index] ? '' : (parseFloat(words[3]) > current[$index] ? '↑' : '↓')) + Math.round((parseFloat(words[3]) - parseFloat(words[2])) / parseFloat(words[2]) * 10000) / 100.0;";
                        echo "tr.childNodes[2].textContent = Math.round((parseFloat(words[3]) - " . $stocks[$index]["price"] . ") / " . $stocks[$index]["price"] . " * 10000) / 100.0;";
                        echo "tr.childNodes[3].textContent = Math.round((parseFloat(words[3]) - " . $stocks[$index]["price"] . ") * " . $stocks[$index]["count"] .");";
                        // echo "tr.childNodes[3].textContent = Math.round((parseFloat(words[4]) - parseFloat(words[2])) / parseFloat(words[2]) * 10000) / 100.0;";
                        echo "current[$index] = parseFloat(words[3]);";
                    }
                ?>

                    if (document.getElementsByTagName('table')[0].style.visibility == 'visible')
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
    <body ondblclick="document.getElementById('edit').style.visibility = document.getElementById('hidden').style.visibility = document.getElementsByTagName('table')[0].style.visibility='visible';setTimeout('updateStocks()', 2000);">
        <table border="1" style="visibility:visible">
            <tr><td width="50"></td><td width="50"></td><td width="50"></td><td width="50"></td></tr>
            <?php
                for ($index = 0; $index < count($stocks); $index++)
                {
                    echo "<tr>";
                    echo "<td width='50'></td>";
                    echo "<td width='50'></td>";
                    echo "<td width='50'></td>";
                    echo "<td width='50'></td>";
                    echo "<td style='display:none'><button id='remove$index'>remove</button></td>";
                    echo "</tr>";
                }
            ?>
        </table>
        <br />
        <button id="edit">Edit</button>
        <button id="hidden" onclick="document.getElementById('edit').style.visibility = document.getElementById('hidden').style.visibility = document.getElementsByTagName('table')[0].style.visibility='hidden';">Hidden</button>
    </body>
</html>