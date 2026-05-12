document.getElementById('negotiation_requests').onclick = function(){
    window.location.href = '/negotiation_requests';
};

document.getElementById('add_campaign').onclick = function(){
    window.location.href = '/add_campaign';
};

document.getElementById('profile').onclick = function(){
    window.location.href = '/profile_sponsor';
};

document.onclick = function(event){
    const parent_containers = document.getElementsByClassName('campaign_details');

    for(var i = 0; i < parent_containers.length; i++){
        if(parent_containers[i].contains(event.target) && event.target.id == 'redirect'){
            const baseURL = 'http://127.0.0.1:5000/campaign_requests';
            const queryParams = {'campaign_id' : `${parent_containers[i].id}`};
            
            const searchParams = new URLSearchParams(queryParams);
            const url = new URL(`${baseURL}?${searchParams.toString()}`);
            
            window.location.href = url;
        }
        else if(parent_containers[i].contains(event.target) && event.target.id == 'delete'){
            const baseURL = 'http://127.0.0.1:5000/delete_campaign';
            const queryParams = {'campaign_id' : `${parent_containers[i].id}`};
            
            const searchParams = new URLSearchParams(queryParams);
            const url = new URL(`${baseURL}?${searchParams.toString()}`);
            
            window.location.href = url;
        }
        else if(parent_containers[i].contains(event.target) && event.target.id == 'edit'){
            const baseURL = 'http://127.0.0.1:5000/edit_campaign';
            const queryParams = {'campaign_id' : `${parent_containers[i].id}`};
            
            const searchParams = new URLSearchParams(queryParams);
            const url = new URL(`${baseURL}?${searchParams.toString()}`);
            
            window.location.href = url;
        }
    }
}

fetch('/campaign_status')
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    for(let i = 0; i < data.length; i++){
        var campaign_div = document.getElementById(data[i]);
        var delete_button = campaign_div.querySelector('#delete');
        delete_button.disabled = true;
        delete_button.style.backgroundImage = 'url("/static/images/delete_overlay.png")';
        delete_button.style.backgroundSize = '2vw'; 
    }
  })



