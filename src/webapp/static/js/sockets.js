//~ generic
    socket = io.connect(location.protocol+'//' + document.domain + ':' + location.port+'/sio_users');
	
    socket.on('connect', function() {
        connection_done();
        console.log('Listening users namespace');
    });

    socket.on('connect_error', function(data) {
      connection_lost();
    });

    socket.on('result', function (data) {
        var data = JSON.parse(data);
        new PNotify({
                title: data.title,
                text: data.text,
                hide: true,
                delay: 4000,
                icon: 'fa fa-'+data.icon,
                opacity: 1,
                type: data.type
        });
    });

    socket.on('add_form_result', function (data) {
        var data = JSON.parse(data);
        if(data.result){
            $("#modalAdd")[0].reset();
            $("#modalAddDesktop").modal('hide');
        }
        new PNotify({
                title: data.title,
                text: data.text,
                hide: true,
                delay: 4000,
                icon: 'fa fa-'+data.icon,
                opacity: 1,
                type: data.type
        });
    });

    socket.on('edit_form_result', function (data) {
        var data = JSON.parse(data);
        if(data.result){
            $("#modalEdit")[0].reset();
            $("#modalEditDesktop").modal('hide');
            setHardwareDomainDefaults_viewer('#hardware-'+data.id,data.id);
        }
        new PNotify({
                title: data.title,
                text: data.text,
                hide: true,
                delay: 4000,
                icon: 'fa fa-'+data.icon,
                opacity: 1,
                type: data.type
        });
    });

//~ quota

    socket.on('user_quota', function(data) {
        var data = JSON.parse(data);
        drawUserQuota(data);
    });

//~ viewer
    socket.on('domain_viewer', function (data) {
        var data = JSON.parse(data);
       
        if(data['kind']=='url'){
            viewer=data['viewer']
            window.open(viewer.replace('<domain>',document.domain));            
            
        }        
         if(data['kind']=='file'){
            var viewerFile = new Blob([data['content']], {type: data['mime']});
            var a = document.createElement('a');
                a.download = 'console.'+data['ext'];
                a.href = window.URL.createObjectURL(viewerFile);
            var ev = document.createEvent("MouseEvents");
                ev.initMouseEvent("click", true, false, self, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
                a.dispatchEvent(ev);              
                    }
    });
    
//~ desktops
    socket.on('desktop_data', function(data){
        var data = JSON.parse(data);
        if(data.status =='Started' && tbl_desktops.row('#'+data.id).data().status != 'Started'){
            if('preferred' in data['options']['viewers'] && data['options']['viewers']['preferred']){
                socket.emit('domain_viewer',{'pk':data.id,'kind':data['options']['viewers']['preferred'],'os':getOS()});
            }else{
                 setViewerButtons(data.id,socket);
                    $('#modalOpenViewer').modal({
                        backdrop: 'static',
                        keyboard: false
                    }).modal('show');
        }

        }
        
        //~ if(claimed==false){

        //~ }
            
        dtUpdateInsert(tbl_desktops,data,false);
        setDesktopDetailButtonsStatus(data.id, data.status);
    });
    
    socket.on('desktop_delete', function(data){
        var data = JSON.parse(data);
        var row = tbl_desktops.row('#'+data.id).remove().draw();
        new PNotify({
                title: "Desktop deleted",
                text: "Desktop "+data.name+" has been deleted",
                hide: true,
                delay: 4000,
                icon: 'fa fa-success',
                opacity: 1,
                type: 'success'
        });
    });
    

    
    
// templates
    socket.on('template_data', function(data){
        //~ console.log('update')
        var data = JSON.parse(data);
        dtUpdateInsert(tbl_templates,data,false);
        //~ setDesktopDetailButtonsStatus(data.id, data.status);

        
        //~ var data = JSON.parse(data);
        //~ var row = table.row('#'+data.id); 
        //~ table.row(row).data(data);
        //~ setDesktopDetailButtonsStatus(data.id, data.status);
    });

    socket.on('template_add', function(data){
        //~ console.log('add')
        var data = JSON.parse(data);
        if($("#" + data.id).length == 0) {
          //it doesn't exist
          tbl_templates.row.add(data).draw();
        }else{
          //if already exists do an update (ie. connection lost and reconnect)
          var row = tbl_templates.row('#'+data.id); 
          tbl_templates.row(row).data(data);            
        }
    });
    
    socket.on('template_delete', function(data){
        //~ console.log('delete')
        var data = JSON.parse(data);
        var row = tbl_templates.row('#'+data.id).remove().draw();
        new PNotify({
                title: "Desktop deleted",
                text: "Desktop "+data.name+" has been deleted",
                hide: true,
                delay: 4000,
                icon: 'fa fa-success',
                opacity: 1,
                type: 'info'
        });
    });
    
// media

    socket.on('media_data', function(data){
        //~ console.log('add or update')
        var data = JSON.parse(data);
            //~ $('#pbid_'+data.id).data('transitiongoal',data.percentage);
            //~ $('#pbid_').css('width', data.percentage+'%').attr('aria-valuenow', data.percentage).text(data.percentage); 
            //~ $('#psmid_'+data.id).text(data.percentage);
        dtUpdateInsert(tbl_media,data,false);
        //~ $('.progress .progress-bar').progressbar();
    });

    
    socket.on('media_delete', function(data){
        //~ console.log('delete')
        var data = JSON.parse(data);
        var row = tbl_media.row('#'+data.id).remove().draw();
        new PNotify({
                title: "Media deleted",
                text: "Media "+data.name+" has been deleted",
                hide: true,
                delay: 4000,
                icon: 'fa fa-success',
                opacity: 1,
                type: 'success'
        });
    });   
