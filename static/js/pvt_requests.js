document.getElementById('return').onclick = function(){
    const baseURL = 'http://127.0.0.1:5000/dashboard_influencer';
    const queryParams = {'message' : 'null'};
    
    const searchParams = new URLSearchParams(queryParams);
    const url = new URL(`${baseURL}?${searchParams.toString()}`);
    
    window.location.href = url;
};

const request_containers = document.getElementsByClassName('request_details');
for(let i = 0; i < request_containers.length; i++){
    var request_status = request_containers[i].querySelector('#status').textContent;
    if(request_status == 'Pending'){
       continue;
    }
    else{
        request_containers[i].querySelector('#accept').disabled = true;
        request_containers[i].querySelector('#accept').style.backgroundImage = 'url("/static/images/acceptance_denied.png")';
        request_containers[i].querySelector('#accept').style.backgroundSize = '1.7vw'; 

        request_containers[i].querySelector('#reject').disabled = true;
        request_containers[i].querySelector('#reject').style.backgroundImage = 'url("/static/images/rejection_denied.png")';
        request_containers[i].querySelector('#reject').style.backgroundSize = '1.7vw';
        
        request_containers[i].querySelector('#negotiate').disabled = true;
        request_containers[i].querySelector('#negotiate').style.backgroundImage = 'url("/static/images/negotiation_denied.png")';
        request_containers[i].querySelector('#negotiate').style.backgroundSize = '1.7vw';
    }
};

document.onclick = function(event){
    const parent_containers = document.getElementsByClassName('request_details');

    for(var i = 0; i < parent_containers.length; i++){
        if(parent_containers[i].contains(event.target) && event.target.id == 'accept'){
            const request_id = parent_containers[i].id

            const baseURL = 'http://127.0.0.1:5000/accept';
            const queryParams = {'request_id' : `${request_id}`,'type' : 'private'};
            
            const searchParams = new URLSearchParams(queryParams);
            const url = new URL(`${baseURL}?${searchParams.toString()}`);
            
            window.location.href = url;
        }
        else if(parent_containers[i].contains(event.target) && event.target.id == 'reject'){
            const request_id = parent_containers[i].id

            const baseURL = 'http://127.0.0.1:5000/reject';
            const queryParams = {'request_id' : `${request_id}`,'type' : 'private'};
            
            const searchParams = new URLSearchParams(queryParams);
            const url = new URL(`${baseURL}?${searchParams.toString()}`);
            
            window.location.href = url;
        }
        else if(parent_containers[i].contains(event.target) && event.target.id == 'negotiate'){
            const request_id = parent_containers[i].id
            const sponsor_id = parent_containers[i].querySelector('#sponsor_id').textContent
            const campaign_id = parent_containers[i].querySelector('#campaign_id').textContent

            const baseURL = 'http://127.0.0.1:5000/negotiate';
            const queryParams = {'request_id' : `${request_id}`,'campaign_id' : `${campaign_id}`,'sponsor_id' : `${sponsor_id}`};
            
            const searchParams = new URLSearchParams(queryParams);
            const url = new URL(`${baseURL}?${searchParams.toString()}`);
            
            window.location.href = url;
        }
    }
};


