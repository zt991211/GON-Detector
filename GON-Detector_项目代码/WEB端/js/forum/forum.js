jQuery(document).ready(function ($) {
        var username = getQueryVariable("username");
        var fwelcome = "你好，" + username + "!";
        document.getElementById("welcome").innerHTML = fwelcome;
        document.getElementById("username").value = username;

        var proup = $('.branch-proup');
        // 点击弹窗内容以外的地方关闭弹窗
        proup.on('click', function (e) {
                if ($(e.target).closest('#uparticle').length <= 0) {
                        proup.hide();
                        $("#uparticle").hide();
                }
        });

        //按最近的文章开始进行加载
        $.ajax({
                url: "php/load_article.php",
                type: "POST",
                dataType: 'json',
                success: function (data) {
                        if (data != null) passageload(data);

                        //加载文章封面
                        $.ajax({
                                url: "php/load_article_picture.php",
                                type: "POST",
                                dataType: 'json',
                                success: function (data) {
                                        //console.log(data);
                                        if (data != null) article_picture_load(data);
                                },
                                error: function (err) {
                                        window.alert("服务器未响应");
                                        console.log(err);
                                }
                        });
                },
                error: function (err) {
                        window.alert("服务器未响应");
                        console.log(err);
                }
        });




        //文章搜索
        $('#search_article').bind('keydown', function (event) {
                if (event.keyCode == "13") {
                        var article_name = document.getElementById("search_article").value;
                        //console.log(article_name);
                        //用户名，文章id
                        var username = getQueryVariable("username");
                        var x = document.getElementsByClassName("post-title");
                        for (var i = 0; i < x.length; i++) {
                                //console.log("length:" + x.length);
                                //console.log("x[i].innerHTML:" + x[i].innerHTML);
                                //console.log("article_name:" + article_name);
                                //console.log(x[i].innerHTML == article_name);
                                if (x[i].innerHTML == article_name) {
                                        var id = x[i].parentNode.parentNode.id;
                                        var writer=x[i].parentNode.getElementsByClassName("post-autor")[0].innerHTML;
                                        var wwriter=writer.substr(4);
                                        console.log(wwriter);
                                        var num = id.substr(8);
                                        newurl = "article.html?" + "username=" + username + "&num=" + num+"&writer="+wwriter;
                                        window.location.href = newurl;
                                        return;
                                }
                        }
                        window.alert("不存在该文章");
                }
        });

        //热门文章，统计所有文章的评论数，然后按照评论数+上传时间来进行排序
        $.ajax({
                url: "php/hot_article.php",
                type: "POST",
                dataType: 'json',
                success: function (data) {
                        //console.log(data);
                        load_hot_article(data);
                },
                error: function (err) {
                        window.alert("服务器未响应");
                        console.log(err);
                }
        });


});

function load_hot_article(parm) {
        var node = document.getElementsByClassName("post-disc");
        var n_node = document.getElementsByClassName("thumb");
        var m_node = document.getElementsByClassName("widget-post");
        var target_herf = "article.html";
        var username = getQueryVariable("username");
        for (var i = 0; i < 3; i++) {
                node[i].getElementsByClassName("title")[0].innerHTML = parm[i]["title"];
                node[i].getElementsByClassName("fp-meta")[0].innerHTML = parm[i]["uptime"];
                node[i].getElementsByClassName("fp-meta")[1].innerHTML = "上传者：" + parm[i]["writer"];
                n_node[i].getElementsByClassName("hot_article_pic")[0].setAttribute("src", parm[i]["path"]);
                // var url = params + "?" + "username=" + username + "&num=" + num;
                var url = target_herf + "?" + "username=" + username + "&num=" + parm[i]["num"]+"&writer="+parm[i]["writer"];
                m_node[i].setAttribute("href", url);
        }
}

function article_picture_load(data) {
        for (var i = 1; i <= data.length; i++) {
                var iid = "passage-" + i;
                document.getElementById(iid).getElementsByClassName("fmpciture")[0].setAttribute("src", data[i - 1]);
        }
}

function passageload(parm) {
        var sourceNode = document.getElementById("passage-0"); // 获得被克隆的节点对象
        var j = 0;
        var username = getQueryVariable("username");
        for (var i = parm.length; i >= 1; i--) {
                var clonedNode = sourceNode.cloneNode(true); // 克隆节点 
                clonedNode.setAttribute("id", "passage-" + i); // 修改一下id 值，避免id 重复 

                clonedNode.style.display = "";
                var iid = "passage-" + i;

                sourceNode.parentNode.appendChild(clonedNode); // 在父节点插入克隆的节点 

                document.getElementById(iid).getElementsByClassName("post-title")[0].innerHTML = parm[j].title;
                document.getElementById(iid).getElementsByClassName("post-autor")[0].innerHTML = "上传者：" + parm[j].writer;
                document.getElementById(iid).getElementsByClassName("post-comment-count")[0].innerHTML = "上传时间：" + parm[j].uptime;
                document.getElementById(iid).getElementsByClassName("fmintro")[0].innerHTML = parm[j].intro;
                var url="article.html" + "?" + "username=" + username + "&num=" + iid.substr(8)+"&writer="+parm[j].writer;
                document.getElementById(iid).getElementsByClassName("fp-more")[0].setAttribute("href",url);
                //document.getElementById(iid).getElementsByClassName("fmpciture")[0].setAttribute("src",parm[j].picture);
                j++;

                //document.getElementById(iid).getElementsByClassName("fmpciture")[0].setAttribute("src",parm[i-1].picture);
        }
}


function getQueryVariable(variable) {
        var query = window.location.search.substring(1);
        var vars = query.split("&");
        for (var i = 0; i < vars.length; i++) {
                var pair = vars[i].split("=");
                if (pair[0] == variable) { return pair[1]; }
        }
        return (false);
}

function func_cancel() {
        document.getElementById("bj_title").value = "";
        document.getElementById("bj_passage").value = "";
        document.getElementById("bj_intro").value = "";
        document.getElementById("bj_picture").value = "";
        document.getElementById("uparticle").style.display = "none";

        document.getElementsByClassName("branch-proup")[0].style.display = "none";

        var mydate = new Date;
        var a = mydate.toLocaleString();
}

function func_save() {
        var options = {
                type: 'POST',
                url: 'php/upload_article.php',
                success: function (data) {
                        if (data.message == 'success') {
                                window.alert("上传成功");
                                window.location.reload();
                        }
                },
                dataType: 'json',
                error: function (xhr, status, err) {
                        alert("操作失败");
                        console.log(xhr);
                },
                resetForm: false,
                clearForm: false
        };

        //防止表单自动提交
        $("#upload_article").submit(function () {
                $(this).ajaxSubmit(options);
                return false;
        });

        $("#upload_article").ajaxSubmit(options);
}

function adddiv() {
        var sourcenode = document.getElementById("passage-0");
        var clonedNode = sourcenode.cloneNode(true);
        var num = getclassnum("all-passage", "post");
        clonedNode.setAttribute("id", "div-" + num);
        document.getElementById("all-passage").appendChild(clonedNode);
}

function getclassnum(parm1, parm2) {
        var newobj = document.getElementById(parm1).childNodes;
        var num = 0;
        for (var i = 0; i < newobj.length; i++) {
                if (newobj[i].className == parm2)
                        num++;
        }
        return num;
}


function function1(params, tthis) {
        var id = tthis.parentNode.parentNode.parentNode.id;
        var num = id.substr(8);
        var username = getQueryVariable("username");
        var url = params + "?" + "username=" + username + "&num=" + num+"&writer"+"";
        //console.log(url);
        window.location.href = url;
}

function checkFileExt(filename) {
        var flag = ture; //状态
        var arr = "md";
        //取出上传文件的扩展名
        var index = filename.lastIndexOf(".");
        var ext = filename.substr(index + 1);

        if (ext != arr) flag = false;

        return flag;
}

