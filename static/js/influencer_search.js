document.getElementById('submit').onclick = function(){
    const niche = document.getElementById('niche').value
    const followers = document.getElementById('followers').value
    const campaign_id = document.getElementById('campaign_id').textContent.slice(1,8)

    const baseURL = 'http://127.0.0.1:5000/influencer_search';
    const queryParams = {'niche': niche,'followers' : followers,'campaign_id' : campaign_id};
    
    const searchParams = new URLSearchParams(queryParams);
    const url = new URL(`${baseURL}?${searchParams.toString()}`);
    
    window.location.href = url;
}

document.getElementById("return").onclick = function(){
    const campaign_id = document.getElementById('campaign_id').textContent.slice(1,8)
    
    const baseURL = 'http://127.0.0.1:5000/campaign_requests';
    const queryParams = {'campaign_id' : campaign_id};
    
    const searchParams = new URLSearchParams(queryParams);
    const url = new URL(`${baseURL}?${searchParams.toString()}`);
    
    window.location.href = url;
}

document.onclick = function(event){
    const parent_containers = document.getElementsByClassName('influencer_details');

    for(var i = 0; i < parent_containers.length; i++){
        if(parent_containers[i].contains(event.target) && event.target.id == 'redirect'){
            const campaign_id = document.getElementById('campaign_id').textContent.slice(1,8)
            const influencer_id = parent_containers[i].id
            
            const baseURL = 'http://127.0.0.1:5000/add_request';
            const queryParams = {'campaign_id' : campaign_id ,'influencer_id' : influencer_id};
            
            const searchParams = new URLSearchParams(queryParams);
            const url = new URL(`${baseURL}?${searchParams.toString()}`);
            
            window.location.href = url;
        }
    }
}