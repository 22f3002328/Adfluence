document.getElementById('return').onclick = function(){
    const baseURL = 'http://127.0.0.1:5000/dashboard_sponsor';
    const queryParams = {'message' : 'null'};
    
    const searchParams = new URLSearchParams(queryParams);
    const url = new URL(`${baseURL}?${searchParams.toString()}`);
    
    window.location.href = url;
};

document.onclick = function(event){
    const parent_containers = document.getElementsByClassName('negotiation_details');

    for(var i = 0; i < parent_containers.length; i++){
        if(parent_containers[i].contains(event.target) && event.target.id == 'accept'){
            const negotiation_id = parent_containers[i].id

            const baseURL = 'http://127.0.0.1:5000/negotiation_accept';
            const queryParams = {'negotiation_id' : `${negotiation_id}`};
        
            const searchParams = new URLSearchParams(queryParams);
            const url = new URL(`${baseURL}?${searchParams.toString()}`);
        
            window.location.href = url;
        }
        else if(parent_containers[i].contains(event.target) && event.target.id == 'reject'){
            const negotiation_id = parent_containers[i].id

            const baseURL = 'http://127.0.0.1:5000/negotiation_reject';
            const queryParams = {'negotiation_id' : `${negotiation_id}`};
        
            const searchParams = new URLSearchParams(queryParams);
            const url = new URL(`${baseURL}?${searchParams.toString()}`);
        
            window.location.href = url;
        }
    }
};