document.getElementById('negotiations_sent').onclick = function(){
    window.location.href = '/negotiations_sent';
};

document.getElementById('accepted_requests').onclick = function(){
    window.location.href  = '/requests_undertaken';
};

document.getElementById('profile').onclick = function(){
    window.location.href  = '/profile_influencer';
};

document.getElementById('pvt_requests').onclick = function(){
    window.location.href = '/pvt_requests';
};

document.getElementById('submit').onclick = function(){
    const campaign_field = document.getElementById('campaign_field').value.trim()

    const baseURL = 'http://127.0.0.1:5000/dashboard_influencer';
    const queryParams = {'campaign_field': campaign_field};
    
    const searchParams = new URLSearchParams(queryParams);
    const url = new URL(`${baseURL}?${searchParams.toString()}`);
    
    window.location.href = url;
};

document.onclick = function(event){
    const parent_containers = document.getElementsByClassName('campaign_details');

    for(var i = 0; i < parent_containers.length; i++){
        if(parent_containers[i].contains(event.target) && event.target.id == 'redirect'){
            const baseURL = 'http://127.0.0.1:5000/public_requests';
            const queryParams = {'campaign_id' : `${parent_containers[i].id}`};
            
            const searchParams = new URLSearchParams(queryParams);
            const url = new URL(`${baseURL}?${searchParams.toString()}`);
            
            window.location.href = url;
        }
    }
};

