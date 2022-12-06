
var socket;

$(document).ready(function(){
    ///set up and connect to socket
    console.log('http://' + document.domain + ':' + location.port + '/chat');
    socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
    socket.io.opts.transports = ['websocket'];
    
    socket.on('connect', function() {
        socket.emit('join', {});
    });
    socket.on('status', function(data) {
    });
    socket.on('ex', function(data) {
        console.log("server returned: " + JSON.stringify(data));
        switch(data.fn)
        {
            case 'mkB':
                makeButton(data.id, data.msg, data.msg);
                break;


            case 'cht':
                $('#'+data.id).tabs('option', 'active',data.msg);
                break;

            case 'scb':
                if (data.usr != username){
                    settextscroll(data.id, data.msg);
                }
                
                break;
                
            case 'rem_butt_del':
                if ($('#' + data.parent).find('#' + data.id).length) {
                    // found! -> remove in only in that div
                    $('#' + data.parent).find('#' + data.id).remove();
                }
                break;

            
            case 'rem_butt_del_sbox':
                var box = document.getElementById(data.parent).shadowRoot.getElementById("box");
                 $(box).find('#' + data.id).remove();
                break;

            case 'tgl':
                $('#'+ data.id).val(data.val)
                ue4("tgl", data);
                break;

            case 'but':
                //$('#'+ data.id).val(data.val)
                ue4("but", data);
                break;

            case 'chk':
                $('#'+ data.id).prop('checked', (data.val));
                ue4("chk", data);
                break;

            case 'cnl':
                ue4("cnl", data);
                break;

            case 'nlc':
                ue4("nlc", data);
                break;

            case 'prot':
                ue4("prot", data);
                //console.log(data);
                break;

            case 'sel':
                // SPECIAL CASE: Refresh Page When loading new project
                if (data.id == "projects"){
                    var url = window.location.href.split('?')[0] + "?usr="  + username + "&project=" + data.opt;
                    console.log(url);
                    window.location.href = url;

                }

                $('#'+ data.id).val(data.opt);
                $('#'+ data.id).selectmenu("refresh");
                ///ue4("sel", data);
                //$("#dropdown", $(data.id).shadowRoot).selectmenu("value", 1);
                //$("#dropdown", $(data.id).shadowRoot).selectmenu("change");
           
                ///var select = document.getElementById(data.id).shadowRoot.getElementById("dropdown-button");
                //$(select).selectmenu("value", data.opt);
                //$(select).selectmenu("change"); 
                //select.value = data.opt;
                // cold also add options.... select.append(new Option("reeeee"));
                break; 

            case 'sli':
                if (data.usr != username){
                    //var slider = document.getElementById(data.id).shadowRoot.getElementById("slider");
                   // slider.value= data.val;
                   $('#'+ data.id).slider('value', data.val);
                }
                //ue4("slider", data);
                break; 
            case 'tex':
                    var text = document.getElementById(data.id).shadowRoot.getElementById("text");
                    text.value= data.val;
                break;
            
            case 'sres':
                console.log(data.val.length);

                document.getElementById("sres").shadowRoot.getElementById("box").innerHTML = ''
                for (let i = 0; i < data.val.length; i++) {
                    var p = document.createElement("mc-sresult");
                    p.setAttribute("id", data.val[i].id);
                    //console.log(data.val[i].id);
                    p.setAttribute("name", data.val[i].name);
                    p.setAttribute("style", "width=150px");
                    p.setAttribute("color" , '#' + Math.floor(Math.random()*16777215).toString(16));
                    document.getElementById("sres").shadowRoot.getElementById("box").appendChild(p);
                }
                break;
                

            case 'sres_butt_clicked':
                    console.log(data.id);
                    //ue4("selectnode", data)
                    break;


        }
        
        
    });

});



function settextscroll(id, val) {
    var box = document.getElementById(id).shadowRoot.getElementById("box");
    $(box).scrollTop(val[0]);
    $(box).scrollLeft(val[1]);
}
