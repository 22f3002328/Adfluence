document.getElementById('add_request').onclick = function(){
    const campaign_id = document.getElementById('campaign_id').textContent
    const baseURL = 'http://127.0.0.1:5000/add_request';
    
    const queryParams = {'campaign_id' : campaign_id};
    const searchParams = new URLSearchParams(queryParams);
        
    const url = new URL(`${baseURL}?${searchParams.toString()}`);
    window.location.href = url;
    
};

document.onclick = function(event){
    const parent_containers = document.getElementsByClassName('request_details');

    for(var i = 0; i < parent_containers.length; i++){
        if(parent_containers[i].contains(event.target) && event.target.id == 'edit'){
            const request_id = parent_containers[i].id

            const baseURL = 'http://127.0.0.1:5000/edit_request';
            const queryParams = {'request_id' : `${request_id}`};
            
            const searchParams = new URLSearchParams(queryParams);
            const url = new URL(`${baseURL}?${searchParams.toString()}`);
            
            window.location.href = url;
        }
        else if(parent_containers[i].contains(event.target) && event.target.id == 'delete'){
            const request_id = parent_containers[i].id

            const baseURL = 'http://127.0.0.1:5000/delete_request';
            const queryParams = {'request_id' : `${request_id}`};
            
            const searchParams = new URLSearchParams(queryParams);
            const url = new URL(`${baseURL}?${searchParams.toString()}`);
            
            window.location.href = url;
        }
    }
};
   
document.getElementById('return').onclick = function(){
    const baseURL = 'http://127.0.0.1:5000/dashboard_sponsor';
    const queryParams = {'message' : 'null'};
    
    const searchParams = new URLSearchParams(queryParams);
    const url = new URL(`${baseURL}?${searchParams.toString()}`);
    
    window.location.href = url;

};

const request_containers = document.getElementsByClassName('request_details');
for(let i = 0; i < request_containers.length; i++){
    var request_status = request_containers[i].querySelector('#status').textContent;
    if(request_status == 'Accepted'){
        request_containers[i].querySelector('#edit').disabled = true;
        request_containers[i].querySelector('#edit').style.backgroundImage = 'url("/static/images/edit_overlay.png")';
        request_containers[i].querySelector('#edit').style.backgroundSize = '2vw';
        
        request_containers[i].querySelector('#delete').disabled = true;
        request_containers[i].querySelector('#delete').style.backgroundImage = 'url("/static/images/delete_overlay.png")';
        request_containers[i].querySelector('#delete').style.backgroundSize = '2vw';   
    }
    else if(request_status == 'Rejected'){
        request_containers[i].querySelector('#edit').disabled = true;
        request_containers[i].querySelector('#edit').style.backgroundImage = 'url("/static/images/edit_overlay.png")';
        request_containers[i].querySelector('#edit').style.backgroundSize = '2vw'; 
    }
};

