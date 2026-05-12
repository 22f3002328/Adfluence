document.getElementById('logout').onclick = function(){
    window.location.href = '/logout';
};

document.getElementById('stats').onclick = function(){
    window.location.href = '/statistics';
};

document.onclick = function(event){
    let sponsors = document.getElementsByClassName('sponsor_details');
    let influencers = document.getElementsByClassName('influencer_details');
    let campaigns = document.getElementsByClassName('campaign_details');
    let requests = document.getElementsByClassName('request_details');
    let negotiations = document.getElementsByClassName('negotiation_details');
    for(let i = 0;i < sponsors.length;i++){
        if(sponsors[i].contains(event.target) && event.target.id == 'flag'){
            const baseURL = 'http://127.0.0.1:5000/flag';
            const queryParams = {'sponsor_id' : `${sponsors[i].id}`};
            
            const searchParams = new URLSearchParams(queryParams);
            const url = new URL(`${baseURL}?${searchParams.toString()}`);
            
            window.location.href = url;
        }
    }
    for(let i = 0;i < influencers.length;i++){
        if(influencers[i].contains(event.target) && event.target.id == 'flag'){
            const baseURL = 'http://127.0.0.1:5000/flag';
            const queryParams = {'influencer_id' : `${influencers[i].id}`};
            
            const searchParams = new URLSearchParams(queryParams);
            const url = new URL(`${baseURL}?${searchParams.toString()}`);
            
            window.location.href = url;
        }
    }
    for(let i = 0;i < campaigns.length;i++){
        if(campaigns[i].contains(event.target) && event.target.id == 'flag'){
            const baseURL = 'http://127.0.0.1:5000/flag';
            const queryParams = {'campaign_id' : `${campaigns[i].id}`};
            
            const searchParams = new URLSearchParams(queryParams);
            const url = new URL(`${baseURL}?${searchParams.toString()}`);
            
            window.location.href = url;
        }
    }
    for(let i = 0;i < requests.length;i++){
        if(requests[i].contains(event.target) && event.target.id == 'flag'){
            const baseURL = 'http://127.0.0.1:5000/flag';
            const queryParams = {'request_id' : `${requests[i].id}`};
            
            const searchParams = new URLSearchParams(queryParams);
            const url = new URL(`${baseURL}?${searchParams.toString()}`);
            
            window.location.href = url;
        }
    }
    for(let i = 0;i < negotiations.length;i++){
        if(negotiations[i].contains(event.target) && event.target.id == 'flag'){
            const baseURL = 'http://127.0.0.1:5000/flag';
            const queryParams = {'negotiation_id' : `${negotiations[i].id}`};
            
            const searchParams = new URLSearchParams(queryParams);
            const url = new URL(`${baseURL}?${searchParams.toString()}`);
            
            window.location.href = url;
        }
    }
};

let sponsors = document.getElementsByClassName('sponsor_details');
let influencers = document.getElementsByClassName('influencer_details');
let campaigns = document.getElementsByClassName('campaign_details');
let requests = document.getElementsByClassName('request_details');
let negotiations = document.getElementsByClassName('negotiation_details');

for (let i = 0;i < sponsors.length;i++){
    let flag_status = sponsors[i].querySelector('#flag_status').textContent
    if(flag_status == 'True'){
        (sponsors[i]).querySelector('#flag').disabled = true;
        (sponsors[i]).querySelector('#flag').style.backgroundImage = 'url("/static/images/flagged.png")';
        (sponsors[i]).querySelector('#flag').style.backgroundSize = '1.75vw';
    }
};

for (let i = 0;i < influencers.length;i++){
    let flag_status = influencers[i].querySelector('#flag_status').textContent
    if(flag_status == 'True'){
        (influencers[i]).querySelector('#flag').disabled = true;
        (influencers[i]).querySelector('#flag').style.backgroundImage = 'url("/static/images/flagged.png")';
        (influencers[i]).querySelector('#flag').style.backgroundSize = '1.75vw';
    }
};

for (let i = 0;i < campaigns.length;i++){
    let flag_status = campaigns[i].querySelector('#flag_status').textContent
    if(flag_status == 'True'){
        (campaigns[i]).querySelector('#flag').disabled = true;
        (campaigns[i]).querySelector('#flag').style.backgroundImage = 'url("/static/images/flagged.png")';
        (campaigns[i]).querySelector('#flag').style.backgroundSize = '1.75vw';
    }
}

for (let i = 0;i < requests.length;i++){
    let flag_status = requests[i].querySelector('#flag_status').textContent
    if(flag_status == 'True'){
       (requests[i]).querySelector('#flag').disabled = true;
       (requests[i]).querySelector('#flag').style.backgroundImage = 'url("/static/images/flagged.png")';
       (requests[i]).querySelector('#flag').style.backgroundSize = '1.75vw';
    }
}

for (let i = 0;i < negotiations.length;i++){
    let flag_status = negotiations[i].querySelector('#flag_status').textContent
    if(flag_status == 'True'){
       (negotiations[i]).querySelector('#flag').disabled = true;
       (negotiations[i]).querySelector('#flag').style.backgroundImage = 'url("/static/images/flagged.png")';
       (negotiations[i]).querySelector('#flag').style.backgroundSize = '1.75vw';
    }
}
