<html>
    <head>
        <title>走势图</title>
        <meta charset="UTF-8">
        <style type="text/css">
            body {
                margin: auto;
                width: 1070px;
            }

            * {
                margin: 0;
                padding: 0;
            }

            .container {
                min-height: 1824px;
                position: relative;
            }

            #container-center {
                background-image: url("http://cdn.elmerzhang.com/sporttery/trends/bg_center.jpg");
                background-position-y: 300px;
            }

            #container-header {
                background-image: url("http://cdn.elmerzhang.com/sporttery/trends/bg_head.jpg");
                background-position: top;
                background-repeat: no-repeat;
            }

            #container-footer {
                background-image: url("http://cdn.elmerzhang.com/sporttery/trends/bg_footer.jpg");
                background-position: bottom;
                background-repeat: no-repeat;
            }

            #title {
                width: 100%;
                text-align: center;
                padding-top: 60px;
                color: #2d5186;
                font-size: 50px;
                font-weight: 500;
            }

            #table-container {
                min-height: 1000px;
                width: 100%;
                /* padding: 0 50px; */
            }

            #table-container table {
                width: 970px;
                margin: 0 auto;
                background: #FFF;
                border-top: 1px solid #000;
                border-left: 1px solid #000;
                border-right: 2px solid #000;
                border-bottom: 2px solid #000;
                font-size: 20px;
                text-align: center;
                border-spacing: unset;
            }

            #table-container table th,td {
                border-top: 1px solid #000;
                border-left: 1px solid #000;
            }

            #table-container table .date {
                background: #93c5ff;
                width: 100px;
            }

            #table-container table .weekday {
                background: #93c5ff;
                width: 35px;
            }

            #table-container table .match {
                background: #ccff95;
                width: 260px;
            }

            #table-container table .match .score {
                color: #ff0000;
            }

            #table-container table .spf {
                background: #fbff00;
                width: 60px;
            }

            #table-container table .spf.active-win {
                background: #ff0000;
                color: #ffffff;
            }

            #table-container table .spf.active-level {
                background: #83bf40;
                color: #ffffff;
            }

            #table-container table .spf.active-lose {
                background: #407abf;
                color: #ffffff;
            }

            #table-container table .odds {
                background: #ffd797;
                width: 50px;
            }

            #table-container table .total {
                background: #ff96a1;
                width: 50px;
            }

            #table-container table .half {
                background: #fff896;
                width: 80px;
            }

            #table-container table .active-low {
                background: #ff0000;
                color: #ffffff;
            }

            #table-container table .active-middle {
                background: #83bf40;
                color: #ffffff;
            }

            #table-container table .active-high {
                background: #407abf;
                color: #ffffff;
            }

            #info-container {
                padding: 10px 50px 50px 50px;
            }

            #qrcode {
                width: 230px;
                float: left;
            }

            #qrcode img {
                width: 230px;
            }

            #qrcode-title {
                width: 100%;
                color: #ff0000;
                font-size: 30px;
                text-align: center;
            }

            #miss-table {
                float: left;
            }

            #miss-table table {
                margin: 0px 50px;
                width: 640px;
                background: #fffc16;
                border-spacing: unset;
                border: solid 1px #000;
                text-align: center;
                font-size: 20px;
            }

            #miss-table table td {
                padding: 10px;
                border: solid 1px #000;
            }

            #miss-table table .comment {
                font-weight: 200;
            }

        </style>
    </head>
    <body>
        <div id="container-center" class="container">
            <div id="container-header" class="container">
                <div id="container-footer" class="container">
                    <h1 id="title">
                        近30天单关走势图
                    </h1>
                    <div id="table-container">
                        //CONTENT_TABLE//
                    </div>
                    <div id="info-container">
                        <div id="qrcode">
                            <div id="qrcode-title">联系店主</div>
                            <img src="http://cdn.elmerzhang.com/sporttery/trends/upload_qrcode.png">
                        </div>
                        <div id="miss-table">
                            //MISS_TABLE//
                        </div>
                        <div id="text">

                        </div>
                        <div style="clear: both;"></div>
                    </div>
                </div>
            </div>
        </div>
    </body>
</html>